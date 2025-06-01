import re
from collections import Counter
from typing import Dict, List
from .exceptions import AnalysisError, ValidationError


class TextAnalyzer:
    """Handles text analysis operations on a given text.

    This class provides various methods for analyzing text content including
    word counting, sentence analysis, and frequency calculations.

    Attributes:
        text (str): The text content to analyze
        n (int): Number of most frequent words to return
        words (List[str]): List of words extracted from the text
    """

    def __init__(self, text: str, n: int) -> None:
        """Initialize TextAnalyzer with text content and N parameter.

        Args:
            text (str): The text content to analyze
            n (int): Number of most frequent words to return

        Raises:
            ValidationError: If text is empty or not a string
            AnalysisError: If no valid words found in text
        """
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
        """Calculate total symbol counts in the text.

        Returns:
            Dict[str, int]: Dictionary containing counts:
                - 'with_spaces': Total character count including spaces
                - 'without_spaces': Character count excluding spaces
        """
        return {
            "with_spaces": len(self.text),
            "without_spaces": len(self.text.replace(" ", ""))
        }

    def get_sentence_count(self) -> int:
        """Count the number of sentences in the text.

        A sentence is considered to end with '.', '!' or '?'.

        Returns:
            int: Number of sentences found

        Raises:
            AnalysisError: If error occurs during sentence counting
        """
        try:
            sentences = [s.strip() for s in re.split('[.!?]', self.text) if s.strip()]
            return len(sentences)
        except Exception as e:
            raise AnalysisError(f"Error counting sentences: {str(e)}")

    def get_word_count(self) -> int:
        """Get the total number of words in the text.

        Returns:
            int: Total number of words
        """
        return len(self.words)

    def get_most_frequent_words(self) -> Dict[str, int]:
        """Get the N most frequently occurring words.

        Returns:
            Dict[str, int]: Dictionary of words and their frequencies

        Raises:
            ValidationError: If N is larger than available words
        """
        if self.n > len(self.words):
            raise ValidationError(
                f"N ({self.n}) is larger than available words ({len(self.words)})"
            )
        return dict(Counter(self.words).most_common(self.n))

    def get_average_word_length(self) -> float:
        """Calculate the average word length.

        Returns:
            float: Average length of words, rounded to 2 decimal places.
                Returns 0.0 if no words are present.
        """
        if not self.words:
            return 0.0
        return round(sum(len(word) for word in self.words) / len(self.words), 2)

    def get_symbol_frequency(self) -> Dict[str, int]:
        """Get frequency of each symbol in the text.

        Returns:
            Dict[str, int]: Dictionary of symbols and their frequencies,
                sorted by frequency (descending) and then by symbol

        Raises:
            AnalysisError: If error occurs during frequency calculation
        """
        try:
            return dict(sorted(
                Counter(self.text).items(),
                key=lambda x: (-x[1], x[0])
            ))
        except Exception as e:
            raise AnalysisError(f"Error calculating symbol frequency: {str(e)}")
