import functools
from typing import Any, Callable

from fastapi import HTTPException

from app.core.logger import get_logger

logger = get_logger("error_handler")


def create_error_response(
    status_code: int, error_type: str, message: str, error_code: str = None
) -> HTTPException:
    """
    Create a standardized error response
    """
    if error_code is None:
        error_code = f"HTTP_{status_code}"

    detail = {"error": error_type, "detail": message, "error_code": error_code}

    return HTTPException(status_code=status_code, detail=detail)


def handle_api_errors(func: Callable) -> Callable:
    """
    Decorator to handle API errors with standardized response format
    """

    @functools.wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except HTTPException:
            raise
        except ValueError as e:
            logger.error(f"Validation error in {func.__name__}: {str(e)}")
            raise create_error_response(
                status_code=400,
                error_type="Validation Error",
                message=f"Invalid input: {str(e)}",
                error_code="VALIDATION_ERROR",
            )
        except Exception as e:
            logger.error(f"Server error in {func.__name__}: {str(e)}")
            raise create_error_response(
                status_code=500,
                error_type="Internal Server Error",
                message="An internal server error occurred",
                error_code="INTERNAL_ERROR",
            )

    return wrapper


def safe_execute(func: Callable, *args, **kwargs) -> Any:
    """
    Safely execute a function and return None if it fails
    """
    try:
        return func(*args, **kwargs)
    except Exception as e:
        logger.error(f"Error in {func.__name__}: {str(e)}")
        return None
