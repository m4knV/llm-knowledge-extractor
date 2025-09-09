import re
from collections import Counter
from typing import List

import nltk
from nltk.corpus import stopwords
from nltk.tag import pos_tag
from nltk.tokenize import word_tokenize

# Download required NLTK data
try:
    nltk.data.find("tokenizers/punkt")
except LookupError:
    nltk.download("punkt")

try:
    nltk.data.find("corpora/stopwords")
except LookupError:
    nltk.download("stopwords")

try:
    nltk.data.find("taggers/averaged_perceptron_tagger")
except LookupError:
    nltk.download("averaged_perceptron_tagger")


class KeywordExtractor:
    """
    Keyword extractor using NLTK
    """

    def __init__(self):
        self.stop_words = set(stopwords.words("english"))
        # Add common words that aren't useful as keywords
        self.stop_words.update(["said", "says", "would", "could", "should", "may", "might"])

    def extract_keywords(self, text: str, top_n: int = 3) -> List[str]:
        """
        Extract the most frequent nouns from the text
        """
        if not text or not text.strip():
            return []

        # Clean and tokenize text
        text = re.sub(r"[^\w\s]", " ", text.lower())
        tokens = word_tokenize(text)

        # Filter out stop words and get only nouns
        tagged_tokens = pos_tag(tokens)
        nouns = []

        for word, pos in tagged_tokens:
            # Check if it's a noun
            if pos not in ["NN", "NNS", "NNP", "NNPS"]:
                continue

            # Check if it's not a stop word
            if word.lower() in self.stop_words:
                continue

            # Check if it's long enough
            if len(word) <= 2:
                continue

            # If all checks pass, add it
            nouns.append(word)

        # Count frequency and return top N
        word_freq = Counter(nouns)
        most_common = word_freq.most_common(top_n)

        # Extract the words
        keywords = []
        for word, count in most_common:
            keywords.append(word)

        return keywords
