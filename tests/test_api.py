import uuid
from unittest.mock import AsyncMock, patch

import pytest
from fastapi.testclient import TestClient

from app.main import app

# Mock data for testing
MOCK_ANALYSIS = {
    "id": str(uuid.uuid4()),
    "original_text": "This is a sample text about cooking and recipes for healthy meals.",
    "summary": "A brief overview of cooking techniques and healthy meal preparation",
    "title": "Healthy Cooking Guide",
    "topics": ["cooking", "nutrition", "healthy eating"],
    "sentiment": "positive",
    "keywords": ["cooking", "recipes", "healthy", "meals"],
    "confidence_score": 0.92,
    "created_at": "2024-01-01T00:00:00Z",
    "updated_at": "2024-01-01T00:00:00Z",
    "deleted_at": None,
}


class TestHealthAPI:
    """Test health check endpoint"""

    def test_health_check(self):
        """Test health endpoint returns healthy status"""
        client = TestClient(app)
        response = client.get("/api/v1/health")

        assert response.status_code == 200
        data = response.json()
        assert data["status"] == "healthy"
        assert "service" in data
        assert "version" in data
        assert "timestamp" in data


class TestAnalysisAPI:
    """Test analysis endpoints"""

    @patch("app.services.analysis_service.AnalysisService.analyze_texts")
    def test_analyze_texts_success(self, mock_analyze_texts):
        """Test analyze endpoint with valid input"""
        # Mock the service to return successful analysis
        mock_analyze_texts.return_value = [MOCK_ANALYSIS]

        client = TestClient(app)
        payload = {
            "texts": [
                "This is a sample text about cooking and healthy recipes.",
                "Another text about gardening and plant care techniques.",
            ]
        }

        response = client.post("/api/v1/analysis/", json=payload)

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
        assert data[0]["title"] == "Healthy Cooking Guide"

    def test_analyze_texts_empty_list(self):
        """Test analyze endpoint with empty texts list"""
        client = TestClient(app)
        payload = {"texts": []}

        response = client.post("/api/v1/analysis/", json=payload)

        # Should return 422 for validation error (empty list)
        assert response.status_code == 422

    @patch("app.services.analysis_service.AnalysisService.get_all_analyses")
    def test_get_all_analyses(self, mock_get_all):
        """Test get all analyses endpoint"""
        # Mock the service to return list of analyses
        mock_get_all.return_value = [MOCK_ANALYSIS]

        client = TestClient(app)
        response = client.get("/api/v1/analysis/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1

    @patch("app.services.analysis_service.AnalysisService.get_analysis_by_id")
    def test_get_analysis_by_id_not_found(self, mock_get_by_id):
        """Test get analysis by ID with non-existent ID"""
        # Mock the service to raise 404 error
        from app.utils.error_handler import create_error_response

        mock_get_by_id.side_effect = create_error_response(
            status_code=404,
            error_type="Not Found",
            message="Analysis not found",
            error_code="ANALYSIS_NOT_FOUND",
        )

        client = TestClient(app)
        fake_id = str(uuid.uuid4())

        response = client.get(f"/api/v1/analysis/{fake_id}")

        assert response.status_code == 404
        data = response.json()
        assert "detail" in data
        assert data["detail"]["error"] == "Not Found"

    def test_get_analysis_by_id_invalid_uuid(self):
        """Test get analysis by ID with invalid UUID format"""
        client = TestClient(app)

        response = client.get("/api/v1/analysis/invalid-uuid")

        assert response.status_code == 422  # Validation error for invalid UUID


class TestSearchAPI:
    """Test search endpoints"""

    @patch("app.services.analysis_service.AnalysisService.search_analyses")
    def test_search_analyses_no_params(self, mock_search):
        """Test search endpoint with no parameters"""
        # Mock the service to return empty list
        mock_search.return_value = []

        client = TestClient(app)
        response = client.get("/api/v1/search/")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 0

    @patch("app.services.analysis_service.AnalysisService.search_analyses")
    def test_search_analyses_by_topic(self, mock_search):
        """Test search endpoint with topic parameter"""
        # Mock the service to return matching analyses
        mock_search.return_value = [MOCK_ANALYSIS]

        client = TestClient(app)
        response = client.get("/api/v1/search/?topic=cooking")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1

    @patch("app.services.analysis_service.AnalysisService.search_analyses")
    def test_search_analyses_by_keyword(self, mock_search):
        """Test search endpoint with keyword parameter"""
        # Mock the service to return matching analyses
        mock_search.return_value = [MOCK_ANALYSIS]

        client = TestClient(app)
        response = client.get("/api/v1/search/?keyword=recipes")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1

    @patch("app.services.analysis_service.AnalysisService.search_analyses")
    def test_search_analyses_by_sentiment(self, mock_search):
        """Test search endpoint with sentiment parameter"""
        # Mock the service to return matching analyses
        mock_search.return_value = [MOCK_ANALYSIS]

        client = TestClient(app)
        response = client.get("/api/v1/search/?sentiment=positive")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1

    @patch("app.services.analysis_service.AnalysisService.search_analyses")
    def test_search_analyses_multiple_params(self, mock_search):
        """Test search endpoint with multiple parameters"""
        # Mock the service to return matching analyses
        mock_search.return_value = [MOCK_ANALYSIS]

        client = TestClient(app)
        response = client.get("/api/v1/search/?topic=cooking&keyword=recipes&sentiment=positive")

        assert response.status_code == 200
        data = response.json()
        assert isinstance(data, list)
        assert len(data) == 1
