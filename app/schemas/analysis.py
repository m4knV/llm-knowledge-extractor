import uuid
from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field, validator


class AnalysisRequest(BaseModel):
    texts: List[str] = Field(
        ...,
        min_items=1,
        max_items=10,
        description="List of texts to analyze (1-10 texts, each 10-10,000 characters)",
    )

    @validator("texts")
    def validate_texts(cls, v):
        if not v:
            raise ValueError("At least one text is required")

        validated_texts = []
        for i, text in enumerate(v):
            if not text or not text.strip():
                raise ValueError(f"Text at index {i} cannot be empty or contain only whitespace")

            if len(text.strip()) < 10:
                raise ValueError(f"Text at index {i} must be at least 10 characters long")

            if len(text) > 10000:
                raise ValueError(f"Text at index {i} exceeds maximum length of 10,000 characters")

            validated_texts.append(text.strip())

        return validated_texts


class AnalysisResponse(BaseModel):
    id: uuid.UUID
    original_text: str
    summary: str
    title: Optional[str]
    topics: List[str]
    sentiment: Optional[str]
    keywords: List[str]
    confidence_score: float
    created_at: datetime
    updated_at: Optional[datetime] = None


class MultiAnalysisResponse(BaseModel):
    """Response for multiple text analysis"""

    results: List[AnalysisResponse] = Field(..., description="Individual analysis results")
