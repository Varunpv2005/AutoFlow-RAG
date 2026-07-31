import json
import re
from typing import Any, Dict, Optional

from app.services.gemini_service import gemini_service


def build_document_intelligence_payload(text: str) -> Dict[str, Any]:
    prompt = (
        "You are an AI Document Intelligence analyzer.\n"
        f"Analyze the following text and generate:\n"
        "1. A concise summary of the document.\n"
        "2. 5 key keywords or tags.\n"
        "3. 3 suggested questions a user might ask about this document.\n\n"
        f"Document text:\n{text}\n\n"
        "CRITICAL: Output ONLY a valid JSON object. Do not include any markdown styling like ```json or backticks. Just raw JSON.\n"
        "The JSON object must have exactly these keys:\n"
        "- \"summary\": string\n"
        "- \"keywords\": list of strings\n"
        "- \"suggested_questions\": list of strings\n"
    )
    raw_intel = gemini_service.invoke(prompt)
    cleaned_intel = re.sub(r"^```(?:json)?\s*|\s*```$", "", raw_intel.strip(), flags=re.IGNORECASE)
    return json.loads(cleaned_intel)


def enrich_file_metadata(text: Optional[str]) -> Dict[str, Any]:
    if not text:
        return {"summary": "", "keywords": [], "suggested_questions": []}
    return build_document_intelligence_payload(text)
