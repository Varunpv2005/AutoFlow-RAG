# log_utils.py - Logging utility for operational events and gotchas
import os
import json
from datetime import datetime
from typing import Any, Dict
from app.request_context import get_request_id


def build_log_entry(event: str, **fields: Any) -> str:
    """Create a structured log entry with request context and latency details."""
    payload = {"event": event, "timestamp": datetime.now().isoformat()}
    if "request_id" not in fields:
        fields["request_id"] = get_request_id()
    payload.update(fields)
    parts = [f"event={payload['event']}", f"timestamp={payload['timestamp']}"]
    for key, value in payload.items():
        if key not in {"event", "timestamp"}:
            parts.append(f"{key}={value}")
    return " ".join(parts)


def emit_observability_event(event: str, **fields: Any) -> Dict[str, Any]:
    """Emit a structured observability payload and return it for callers to log or inspect."""
    payload = {"event": event, "timestamp": datetime.now().isoformat()}
    if "request_id" not in fields:
        fields["request_id"] = get_request_id()
    payload.update(fields)
    return payload


def safe_log_gotcha(event_name: str, **fields: Any):
    """
    Log a gotcha, error, or operational event to gotchas.md in the project root.
    Appends timestamped entries for traceability and compliance.
    """
    payload = emit_observability_event(event_name, **fields)
    gotchas_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../gotchas.md'))
    entry = build_log_entry(payload["event"], **{k: v for k, v in payload.items() if k not in {"event", "timestamp"}})
    entry = f"[{payload['timestamp']}] {entry}\n"
    try:
        with open(gotchas_path, 'a') as f:
            f.write(entry)
    except Exception as e:
        print(f"[safe_log_gotcha ERROR] Could not write to gotchas.md: {e}")
    return payload
