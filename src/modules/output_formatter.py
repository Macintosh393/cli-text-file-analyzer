from typing import Dict, Any


class OutputFormatter:
    """Handles formatting of text analysis results.

    This class formats the results from text analysis operations
    into a standardized dictionary structure for output.

    Attributes:
        analyzer: Text analyzer instance containing analysis methods
        n (int): Number of most frequent words to include in results
    """

    def __init__(self, analyzer, n: int) -> None:
        """Initialize OutputFormatter with analyzer and N value.

        Args:
            analyzer: Text analyzer instance with analysis methods
            n (int): Number of most frequent words to include
        """
        self.analyzer = analyzer
        self.n = n

    def format_results(self) -> Dict[str, Any]:
        """Format analysis results into a structured dictionary.

        Collects and formats various text analysis results including:
        - Total symbol counts (with and without spaces)
        - Sentence count
        - Word count
        - N most frequent words
        - Average word length
        - Symbol frequency distribution

        Returns:
            Dict[str, Any]: Dictionary containing formatted analysis results:
                {
                    "total_symbols": {
                        "with_spaces": int,
                        "without_spaces": int
                    },
                    "sentence-count": int,
                    "word-count": int,
                    "N-most-frequent-words": Dict[str, int],
                    "average-word-length": float,
                    "symbols-frequency": Dict[str, int]
                }
        """
        return {
            "total_symbols": self.analyzer.get_symbol_counts(),
            "sentence-count": self.analyzer.get_sentence_count(),
            "word-count": self.analyzer.get_word_count(),
            f"{self.n}-most-frequent-words": self.analyzer.get_most_frequent_words(),
            "average-word-length": self.analyzer.get_average_word_length(),
            "symbols-frequency": self.analyzer.get_symbol_frequency()
        }
