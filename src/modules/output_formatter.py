from typing import Dict, Any

class OutputFormatter:
    """Handles formatting of analysis results"""

    def __init__(self, analyzer, n: int):
        self.analyzer = analyzer
        self.n = n

    def format_results(self) -> Dict[str, Any]:
        """Format analysis results"""
        return {
            "total_symbols": self.analyzer.get_symbol_counts(),
            "sentence-count": self.analyzer.get_sentence_count(),
            "word-count": self.analyzer.get_word_count(),
            f"{self.n}-most-frequent-words": self.analyzer.get_most_frequent_words(),
            "average-word-length": self.analyzer.get_average_word_length(),
            "symbols-frequency": self.analyzer.get_symbol_frequency()
        }
