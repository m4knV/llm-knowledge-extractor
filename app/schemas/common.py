from typing import Any, Dict, Optional

from pydantic import BaseModel


class ErrorResponse(BaseModel):
    error: str
    detail: Optional[str] = None
    error_code: Optional[str] = None
    timestamp: Optional[str] = None


class ValidationErrorResponse(BaseModel):
    error: str = "Validation Error"
    detail: str
    field: Optional[str] = None
    error_code: str = "VALIDATION_ERROR"


class LLMErrorResponse(BaseModel):
    error: str = "LLM Service Error"
    detail: str
    error_code: str = "LLM_SERVICE_ERROR"
