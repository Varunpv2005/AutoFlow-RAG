from types import SimpleNamespace

from fastapi.testclient import TestClient

from app.main import app
from app.services.gemini_service import GeminiService, GeminiServiceUnavailableError
from app.db.session import get_db
from app.auth import get_current_user


def test_generate_retries_and_falls_back(monkeypatch):
    service = GeminiService(api_key="test-key", model_name="gemini-2.5-flash")
    service.fallback_models = ["gemini-2.5-flash-lite"]
    calls = []

    def fake_generate_content(model, contents):
        calls.append(model)
        if model == "gemini-2.5-flash":
            raise Exception("503 UNAVAILABLE")
        return SimpleNamespace(text="fallback answer")

    service.client = SimpleNamespace(models=SimpleNamespace(generate_content=fake_generate_content))
    monkeypatch.setattr("app.services.gemini_service.time.sleep", lambda *_args, **_kwargs: None)

    assert service.generate("prompt") == "fallback answer"
    assert calls == [
        "gemini-2.5-flash",
        "gemini-2.5-flash",
        "gemini-2.5-flash",
        "gemini-2.5-flash",
        "gemini-2.5-flash-lite",
    ]


def test_chat_endpoint_returns_graceful_503_on_llm_outage(monkeypatch):
    def fake_chat_service(*args, **kwargs):
        raise GeminiServiceUnavailableError("Gemini service is temporarily unavailable")

    monkeypatch.setattr("app.main.chat_service", fake_chat_service)

    def override_get_db():
        yield None

    def override_get_current_user():
        return SimpleNamespace(id=1)

    app.dependency_overrides[get_db] = override_get_db
    app.dependency_overrides[get_current_user] = override_get_current_user

    client = TestClient(app)
    response = client.post("/api/chat?question=hello")

    assert response.status_code == 503
    assert response.json() == {
        "success": False,
        "error": "Gemini service is temporarily unavailable. Please try again in a few moments.",
    }

    app.dependency_overrides.clear()
