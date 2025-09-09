from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas import AnalysisResponse
from app.services import AnalysisService
from app.utils.error_handler import handle_api_errors

router = APIRouter()


@router.get("/", response_model=list[AnalysisResponse])
@handle_api_errors
async def search_analyses(
    topic: Optional[str] = Query(None, description="Search by topic"),
    keyword: Optional[str] = Query(None, description="Search by keyword"),
    sentiment: Optional[str] = Query(
        None, description="Search by sentiment (positive, neutral, negative)"
    ),
    db: AsyncSession = Depends(get_db),
):
    """
    Search analyses by topic, keyword, or sentiment
    """
    analysis_service = AnalysisService()
    results = await analysis_service.search_analyses(
        db=db, topic=topic, keyword=keyword, sentiment=sentiment
    )
    return results
