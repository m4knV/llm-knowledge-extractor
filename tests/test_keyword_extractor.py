import pytest

from app.utils.keyword_extractor import KeywordExtractor


class TestKeywordExtractor:
    def setup_method(self):
        self.extractor = KeywordExtractor()

    def test_extract_keywords_basic(self):
        text = "The chef prepared delicious pasta with fresh tomatoes and herbs. The pasta was perfectly cooked and seasoned."
        keywords = self.extractor.extract_keywords(text, top_n=3)
        assert len(keywords) <= 3
        assert "pasta" in keywords

    def test_extract_keywords_empty_text(self):
        keywords = self.extractor.extract_keywords("")
        assert keywords == []

    def test_extract_keywords_whitespace_only(self):
        keywords = self.extractor.extract_keywords("   \n\t   ")
        assert keywords == []

    def test_extract_keywords_long_text(self):
        text = """
        Gardening and plant care are becoming popular hobbies for many people.
        Growing vegetables and herbs at home provides fresh ingredients for cooking.
        The benefits of gardening include stress relief and physical exercise.
        Many communities are starting urban gardens and sharing knowledge about sustainable living.
        """
        keywords = self.extractor.extract_keywords(text, top_n=5)
        assert len(keywords) <= 5
        assert any(word in keywords for word in ["gardening", "plants", "vegetables", "cooking"])
