from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from sqlalchemy.exc import SQLAlchemyError
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR, HTTP_404_NOT_FOUND, HTTP_422_UNPROCESSABLE_ENTITY
import logging
from app.log_utils import safe_log_gotcha

# Centralized error handlers for FastAPI

def http_exception_handler(request: Request, exc: HTTPException):
    request_id = getattr(request.state, "request_id", None)
    safe_log_gotcha("http_exception", request_id=request_id, status_code=exc.status_code, message=str(exc.detail), path=request.url.path)
    return JSONResponse(
        status_code=exc.status_code,
        content={"detail": exc.detail}
    )

def sqlalchemy_exception_handler(request: Request, exc: SQLAlchemyError):
    request_id = getattr(request.state, "request_id", None)
    safe_log_gotcha("sqlalchemy_error", request_id=request_id, error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "A database error occurred."}
    )

def generic_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", None)
    safe_log_gotcha("generic_exception", request_id=request_id, error=str(exc), path=request.url.path)
    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={"detail": "An internal server error occurred."}
    )
