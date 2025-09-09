import json
from datetime import datetime
from typing import Any, Dict, Optional

import openai
from openai import APITimeoutError, OpenAIError, RateLimitError

from app.core.config import settings
from app.core.exceptions import EmptyInputError, LLMServiceError


class LLMService:
    """
    Service for analyzing text using OpenAI
    """

    def __init__(self):
        self.client = openai.OpenAI(api_key=settings.OPENAI_API_KEY)

    async def analyze_text(self, text: str) -> Dict[str, Any]:
        """
        Analyze text using OpenAI to extract summary, title, topics, and sentiment
        """
        # Validate input
        if not text or not text.strip():
            raise EmptyInputError("Text cannot be empty or contain only whitespace")

        # Check text length (reasonable limits)
        if len(text.strip()) < 10:
            raise EmptyInputError("Text must be at least 10 characters long")

        if len(text) > 10000:  # Reasonable limit to prevent abuse
            raise EmptyInputError("Text is too long. Maximum 10,000 characters allowed")

        try:
            prompt = f"""
            Analyze the following text and provide a structured response in JSON format:
            
            Text: {text}
            
            Please provide:
            1. A 1-2 sentence summary
            2. A title (if one can be inferred, otherwise null)
            3. Three key topics that best describe the content
            4. Sentiment analysis (positive, neutral, or negative)
            
            Return your response as a JSON object with these exact keys:
            {{
                "summary": "1-2 sentence summary here",
                "title": "title or null",
                "topics": ["topic1", "topic2", "topic3"],
                "sentiment": "positive/neutral/negative"
            }}
            """

            response = self.client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[
                    {
                        "role": "system",
                        "content": "You are a helpful assistant that analyzes text and extracts structured information. Always respond with valid JSON.",
                    },
                    {"role": "user", "content": prompt},
                ],
                max_tokens=500,
                temperature=0.3,
            )

            content = response.choices[0].message.content.strip()

            try:
                result = json.loads(content)
            except json.JSONDecodeError:
                # Fallback if JSON parsing fails
                result = {
                    "summary": content[:200] + "..." if len(content) > 200 else content,
                    "title": None,
                    "topics": ["general"],
                    "sentiment": "neutral",
                }

            # Validate required fields
            if "summary" not in result:
                result["summary"] = "Unable to generate summary"
            if "title" not in result:
                result["title"] = None
            if "topics" not in result or not isinstance(result["topics"], list):
                result["topics"] = ["general"]
            if "sentiment" not in result or result["sentiment"] not in [
                "positive",
                "neutral",
                "negative",
            ]:
                result["sentiment"] = "neutral"

            # Calculate a simple confidence score based on response quality
            confidence = self._calculate_confidence(result, text)
            result["confidence_score"] = confidence

            return result

        except RateLimitError as e:
            raise LLMServiceError(f"Rate limit exceeded. Please try again later: {str(e)}")
        except APITimeoutError as e:
            raise LLMServiceError(f"Request timed out. Please try again: {str(e)}")
        except OpenAIError as e:
            raise LLMServiceError(f"OpenAI API error: {str(e)}")
        except Exception as e:
            raise LLMServiceError(f"Unexpected error during LLM analysis: {str(e)}")

    def _calculate_confidence(self, result: Dict[str, Any], original_text: str) -> float:
        """
        Calculate a simple confidence score based on response quality
        """
        confidence = 0.5  # Base confidence

        # Check if summary is reasonable length
        if 10 <= len(result.get("summary", "")) <= 300:
            confidence += 0.2

        # Check if topics are provided
        if result.get("topics") and len(result["topics"]) >= 2:
            confidence += 0.2

        # Check if sentiment is determined
        if result.get("sentiment") in ["positive", "negative"]:
            confidence += 0.1

        return min(confidence, 1.0)
