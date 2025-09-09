import uuid
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.db import get_db
from app.schemas import AnalysisRequest, AnalysisResponse
from app.services import AnalysisService
from app.utils.error_handler import handle_api_errors

router = APIRouter()


@router.post("/", response_model=List[AnalysisResponse])
@handle_api_errors
async def analyze_texts(request: AnalysisRequest, db: AsyncSession = Depends(get_db)):
    """
    Analyze multiple texts and extract structured information
    Returns list of successfully created analyzed texts.
    """
    analysis_service = AnalysisService()
    results = await analysis_service.analyze_texts(request.texts, db)
    return results


@router.get("/", response_model=List[AnalysisResponse])
@handle_api_errors
async def get_all_analyses(db: AsyncSession = Depends(get_db)):
    """
    Get all analyses
    """
    analysis_service = AnalysisService()
    results = await analysis_service.get_all_analyses(db)
    return results


@router.get("/{analysis_id}", response_model=AnalysisResponse)
@handle_api_errors
async def get_analysis(analysis_id: uuid.UUID, db: AsyncSession = Depends(get_db)):
    """
    Get a specific analysis by ID
    """
    analysis_service = AnalysisService()
    return await analysis_service.get_analysis_by_id(analysis_id, db)
