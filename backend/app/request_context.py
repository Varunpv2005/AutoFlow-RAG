import contextvars
import uuid
from typing import Optional

request_id_var: contextvars.ContextVar[Optional[str]] = contextvars.ContextVar("request_id", default=None)


def get_request_id() -> Optional[str]:
    return request_id_var.get()


def set_request_id(request_id: Optional[str] = None) -> str:
    value = request_id or str(uuid.uuid4())
    request_id_var.set(value)
    return value


def clear_request_id() -> None:
    request_id_var.set(None)
