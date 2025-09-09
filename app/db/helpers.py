from typing import Any, Type, TypeVar

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import DeclarativeBase

from app.utils.error_handler import create_error_response

T = TypeVar("T", bound=DeclarativeBase)


async def get_one_or_error(
    db: AsyncSession, model_class: Type[T], condition: Any, resource_name: str = "Resource"
) -> T:
    """
    Get one record by condition or raise 404 error if not found
    """
    query = select(model_class).where(condition)
    result = await db.execute(query)
    record = result.scalar_one_or_none()

    if record is None:
        raise create_error_response(
            status_code=404,
            error_type="Not Found",
            message=f"{resource_name} not found",
            error_code=f"{resource_name.upper()}_NOT_FOUND",
        )

    return record
