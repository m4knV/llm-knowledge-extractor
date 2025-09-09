"""
Custom exceptions for the LLM Knowledge Extractor application.
"""


class LLMKnowledgeExtractorError(Exception):
    """Base exception for all application errors."""

    pass


class EmptyInputError(LLMKnowledgeExtractorError):
    """Raised when input text is empty or invalid."""

    pass


class LLMServiceError(LLMKnowledgeExtractorError):
    """Raised when LLM service fails."""

    pass


class AnalysisError(LLMKnowledgeExtractorError):
    """Raised when analysis processing fails."""

    pass


class ValidationError(LLMKnowledgeExtractorError):
    """Raised when input validation fails."""

    pass
