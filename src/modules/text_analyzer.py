import re
from collections import Counter
from typing import Dict, Tuple
from .exceptions import ValidationError, AnalysisError


class TextAnalyzer:
    """Handles text analysis operations"""

    def __init__(self, text: str, n: int):
        if not isinstance(text, str):
            raise ValidationError("Text must be a string")
        if not text.strip():
            raise ValidationError("Text cannot be empty")

        self.text = text
        self.n = n
        self.words = re.findall(r'\b\w+\b', text.lower(), re.UNICODE)

        if not self.words:
            raise AnalysisError("No valid words found in text")

    def get_symbol_counts(self) -> Dict[str, int]:
        """Calculate total symbols"""
        return {
            "with_spaces": len(self.text),
            "without_spaces": len(self.text.replace(" ", ""))
        }

    def get_sentence_count(self) -> int:
        """Count sentences in text"""
        try:
            sentences = [s.strip() for s in re.split('[.!?]', self.text) if s.strip()]
            return len(sentences)
        except Exception as e:
            raise AnalysisError(f"Error counting sentences: {str(e)}")

    def get_word_count(self) -> int:
        """Get total word count"""
        return len(self.words)

    def get_most_frequent_words(self) -> Dict[str, int]:
        """Get N most frequent words"""
        if self.n > len(self.words):
            raise ValidationError(
                f"N ({self.n}) is larger than available words ({len(self.words)})"
            )
        return dict(Counter(self.words).most_common(self.n))

    def get_average_word_length(self) -> float:
        """Calculate average word length"""
        if not self.words:
            return 0.0
        return round(sum(len(word) for word in self.words) / len(self.words), 2)

    def get_symbol_frequency(self) -> Dict[str, int]:
        """Get symbol frequency in descending order"""
        try:
            return dict(sorted(
                Counter(self.text).items(),
                key=lambda x: (-x[1], x[0])
            ))
        except Exception as e:
            raise AnalysisError(f"Error calculating symbol frequency: {str(e)}")
