import asyncio
import uuid
from typing import List, Union

from sqlalchemy import String, and_, cast, select
from sqlalchemy.dialects.postgresql import JSON, array
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.exceptions import AnalysisError, EmptyInputError, LLMServiceError
from app.core.logger import get_logger
from app.db.database import AsyncSessionLocal
from app.db.helpers import get_one_or_error
from app.db.models import Analysis
from app.schemas.analysis import AnalysisResponse
from app.services.llm_service import LLMService
from app.utils.keyword_extractor import KeywordExtractor

logger = get_logger("analysis_service")


class AnalysisService:
    """
    Service for analyzing text and returning structured analysis.
    """

    def __init__(self):
        self.llm_service = LLMService()
        self.keyword_extractor = KeywordExtractor()

    async def analyze_text(self, text: str, db: AsyncSession) -> AnalysisResponse:
        """
        Analyze text and return structured analysis.
        """
        try:
            # Get LLM analysis
            llm_result = await self.llm_service.analyze_text(text)
        except LLMServiceError as e:
            raise AnalysisError(f"LLM service failed: {str(e)}")
        except EmptyInputError as e:
            raise AnalysisError(f"Invalid input: {str(e)}")
        except Exception as e:
            raise AnalysisError(f"Analysis failed: {str(e)}")

        try:
            # Extract keywords using our custom extractor
            keywords = self.keyword_extractor.extract_keywords(text)
        except Exception as e:
            raise AnalysisError(f"Keyword extraction failed: {str(e)}")

        try:
            # Create DB record
            analysis = Analysis(
                original_text=text,
                summary=llm_result.get("summary"),
                title=llm_result.get("title"),
                topics=llm_result.get("topics"),
                sentiment=llm_result.get("sentiment"),
                keywords=keywords,
                confidence_score=llm_result.get("confidence_score", 0.0),
            )

            db.add(analysis)
            await db.commit()
            await db.refresh(analysis)

            return analysis
        except Exception as e:
            await db.rollback()
            raise AnalysisError(f"Failed to save analysis: {str(e)}")

    async def analyze_texts(self, texts: List[str], db: AsyncSession) -> List[AnalysisResponse]:
        """
        Analyze multiple texts and return list of successfully created database records
        Process texts sequentially
        """
        analyses = []

        for text in texts:
            try:
                analysis = await self.analyze_text(text, db)
                analyses.append(analysis)
            except Exception as e:
                # Log the error and continue with other analyses
                logger.warning(f"Analysis failed for text: {str(e)}")

        return analyses

    async def search_analyses(
        self,
        db: AsyncSession,
        topic: str = None,
        keyword: str = None,
        sentiment: str = None,
    ) -> List[AnalysisResponse]:
        """
        Search analyses by various criteria.
        """
        query = select(Analysis)

        # Build search conditions
        conditions = []

        if topic:
            conditions.append(Analysis.topics.op("?")(topic))

        if keyword:
            conditions.append(Analysis.keywords.op("?")(keyword))

        if sentiment:
            conditions.append(Analysis.sentiment == sentiment)

        if conditions:
            query = query.where(and_(*conditions))

        query = query.order_by(Analysis.created_at.desc())

        result = await db.execute(query)
        analyses = result.scalars().all()

        return analyses

    async def get_all_analyses(self, db: AsyncSession) -> List[AnalysisResponse]:
        """
        Get all analyses
        """
        query = select(Analysis).order_by(Analysis.created_at.desc())
        result = await db.execute(query)
        analyses = result.scalars().all()

        return analyses

    async def get_analysis_by_id(
        self, analysis_id: uuid.UUID, db: AsyncSession
    ) -> AnalysisResponse:
        """
        Get a specific analysis by ID
        """
        return await get_one_or_error(
            db=db,
            model_class=Analysis,
            condition=Analysis.id == analysis_id,
            resource_name="Analysis",
        )
