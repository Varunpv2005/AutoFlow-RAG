import logging
import os
import time
from typing import Tuple, Optional, List
from google import genai
from google.genai import errors as genai_errors
from app.config import settings

logger = logging.getLogger(__name__)


class GeminiServiceUnavailableError(RuntimeError):
    """Raised when Gemini is temporarily unavailable after retries and fallbacks."""


class GeminiService:
    """
    Reusable Gemini LLM service wrapper.
    Encapsulates Google GenAI SDK calls and handles temporary provider outages.
    """

    def __init__(self, api_key: Optional[str] = None, model_name: Optional[str] = None):
        self.api_key = api_key or settings.GEMINI_API_KEY
        self.model_name = model_name or settings.GEMINI_MODEL
        self.fallback_models = self._get_fallback_models()

        if not self.api_key:
            logger.warning("GEMINI_API_KEY is not configured in settings or environment.")

        self.client = genai.Client(api_key=self.api_key)
        logger.info(
            "Initialized GeminiService for LLM text generation (model=%s, fallback_models=%s)",
            self.model_name,
            self.fallback_models,
        )

    def _get_fallback_models(self) -> List[str]:
        raw_value = os.getenv("GEMINI_FALLBACK_MODELS", "gemini-2.5-flash-lite,gemini-2.0-flash")
        models = []
        for candidate in raw_value.split(","):
            model = candidate.strip()
            if model:
                models.append(model)
        return models

    def _is_temporary_unavailable_error(self, error: Exception) -> bool:
        error_text = str(error).upper()
        return isinstance(error, genai_errors.ServerError) or "503" in error_text or "UNAVAILABLE" in error_text

    def _build_model_candidates(self) -> List[str]:
        candidates = [self.model_name]
        for model in self.fallback_models:
            if model and model not in candidates:
                candidates.append(model)
        return candidates

    def _request_with_retries(self, prompt: str, model_name: str, retries: int = 3) -> str:
        delays = (2, 4, 8)
        for attempt in range(retries + 1):
            started_at = time.perf_counter()
            try:
                response = self.client.models.generate_content(model=model_name, contents=prompt)
                latency_ms = round((time.perf_counter() - started_at) * 1000, 2)
                logger.info(
                    "Gemini request succeeded | model=%s | retry_count=%s | latency_ms=%.2f",
                    model_name,
                    attempt,
                    latency_ms,
                )
                return response.text or ""
            except Exception as error:
                latency_ms = round((time.perf_counter() - started_at) * 1000, 2)
                if self._is_temporary_unavailable_error(error) and attempt < retries:
                    delay = delays[attempt]
                    logger.warning(
                        "Gemini request hit temporary outage | model=%s | retry_count=%s/%s | fallback_model=%s | latency_ms=%.2f | error=%s",
                        model_name,
                        attempt,
                        retries,
                        self.fallback_models[0] if self.fallback_models else "none",
                        latency_ms,
                        error,
                    )
                    time.sleep(delay)
                    continue
                raise

    def generate(self, prompt: str) -> str:
        """
        Synchronous text generation with retry and fallback for temporary Gemini outages.
        """
        model_candidates = self._build_model_candidates()
        last_error: Optional[Exception] = None

        for index, model_name in enumerate(model_candidates):
            is_fallback = index > 0
            try:
                return self._request_with_retries(prompt, model_name)
            except Exception as error:
                last_error = error
                if self._is_temporary_unavailable_error(error):
                    logger.warning(
                        "Gemini model failed | model=%s | fallback_model=%s | error=%s",
                        model_name,
                        model_candidates[index + 1] if index + 1 < len(model_candidates) else "none",
                        error,
                    )
                    if is_fallback or index == len(model_candidates) - 1:
                        break
                    continue
                raise

        if last_error is not None:
            logger.error(
                "Gemini service unavailable after retries and fallbacks | primary_model=%s | fallback_models=%s | last_error=%s",
                self.model_name,
                self.fallback_models,
                last_error,
            )
            raise GeminiServiceUnavailableError(
                "Gemini service is temporarily unavailable. Please try again in a few moments."
            )

        raise GeminiServiceUnavailableError(
            "Gemini service is temporarily unavailable. Please try again in a few moments."
        )

    async def agenerate(self, prompt: str) -> str:
        """
        Asynchronous text generation using the same retry and fallback logic.
        """
        try:
            return self.generate(prompt)
        except Exception as error:
            logger.error("Gemini async generate error: %s", error)
            raise

    def invoke(self, prompt: str) -> str:
        """
        Duck-typed method matching LangChain interface.
        """
        return self.generate(prompt)

    async def ainvoke(self, prompt: str) -> str:
        """
        Duck-typed async method matching LangChain interface.
        """
        return await self.agenerate(prompt)

    def health_check(self) -> Tuple[bool, str, str]:
        """
        Verifies connectivity to Google Gemini API (checks API Key configuration without calling generate_content).
        Returns (is_ok, status_message, model_name).
        """
        if self.api_key and len(self.api_key) > 5:
            return True, "Connected", self.model_name
        return False, "Not Connected", self.model_name


# Global singleton instance for application use
gemini_service = GeminiService()
