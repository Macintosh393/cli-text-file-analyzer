# tests/test_output_formatter.py
import pytest
from unittest.mock import MagicMock
from src.modules.output_formatter import OutputFormatter


@pytest.fixture
def mock_analyzer():
    """Create a mock analyzer with predefined return values"""
    analyzer = MagicMock()

    # Set up return values for analyzer methods
    analyzer.get_symbol_counts.return_value = {
        "with_spaces": 100,
        "without_spaces": 80
    }
    analyzer.get_sentence_count.return_value = 5
    analyzer.get_word_count.return_value = 20
    analyzer.get_most_frequent_words.return_value = {
        "test": 3,
        "example": 2
    }
    analyzer.get_average_word_length.return_value = 4.5
    analyzer.get_symbol_frequency.return_value = {
        "t": 10,
        "e": 8,
        "s": 6
    }

    return analyzer


@pytest.fixture
def formatter(mock_analyzer):
    """Create an OutputFormatter instance with mock analyzer"""
    return OutputFormatter(mock_analyzer, n=5)


class TestOutputFormatter:
    """Test suite for OutputFormatter class"""

    def test_initialization(self, mock_analyzer):
        """Test OutputFormatter initialization"""
        n_value = 5
        formatter = OutputFormatter(mock_analyzer, n_value)

        assert formatter.analyzer == mock_analyzer
        assert formatter.n == n_value

    def test_format_results(self, formatter, mock_analyzer):
        """Test formatting of analysis results"""
        results = formatter.format_results()

        # Verify all expected keys are present
        expected_keys = {
            "total_symbols",
            "sentence-count",
            "word-count",
            "5-most-frequent-words",
            "average-word-length",
            "symbols-frequency"
        }
        assert set(results.keys()) == expected_keys

        # Verify each analyzer method was called exactly once
        mock_analyzer.get_symbol_counts.assert_called_once()
        mock_analyzer.get_sentence_count.assert_called_once()
        mock_analyzer.get_word_count.assert_called_once()
        mock_analyzer.get_most_frequent_words.assert_called_once()
        mock_analyzer.get_average_word_length.assert_called_once()
        mock_analyzer.get_symbol_frequency.assert_called_once()

        # Verify the returned values match the mock analyzer's returns
        assert results["total_symbols"] == {"with_spaces": 100, "without_spaces": 80}
        assert results["sentence-count"] == 5
        assert results["word-count"] == 20
        assert results["5-most-frequent-words"] == {"test": 3, "example": 2}
        assert results["average-word-length"] == 4.5
        assert results["symbols-frequency"] == {"t": 10, "e": 8, "s": 6}

    def test_format_results_different_n(self, mock_analyzer):
        """Test formatting with different N values"""
        n_value = 10
        formatter = OutputFormatter(mock_analyzer, n_value)
        results = formatter.format_results()

        # Verify the key name changes with N
        assert f"{n_value}-most-frequent-words" in results

    def test_format_results_structure(self, formatter):
        """Test the structure of formatted results"""
        results = formatter.format_results()

        # Verify types of returned values
        assert isinstance(results["total_symbols"], dict)
        assert isinstance(results["sentence-count"], int)
        assert isinstance(results["word-count"], int)
        assert isinstance(results["5-most-frequent-words"], dict)
        assert isinstance(results["average-word-length"], float)
        assert isinstance(results["symbols-frequency"], dict)

        # Verify nested structure of total_symbols
        assert "with_spaces" in results["total_symbols"]
        assert "without_spaces" in results["total_symbols"]

    def test_format_results_empty_analyzer(self):
        """Test formatting with analyzer returning empty/zero values"""
        empty_analyzer = MagicMock()
        empty_analyzer.get_symbol_counts.return_value = {"with_spaces": 0, "without_spaces": 0}
        empty_analyzer.get_sentence_count.return_value = 0
        empty_analyzer.get_word_count.return_value = 0
        empty_analyzer.get_most_frequent_words.return_value = {}
        empty_analyzer.get_average_word_length.return_value = 0.0
        empty_analyzer.get_symbol_frequency.return_value = {}

        formatter = OutputFormatter(empty_analyzer, n=5)
        results = formatter.format_results()

        # Verify handling of empty/zero values
        assert results["total_symbols"] == {"with_spaces": 0, "without_spaces": 0}
        assert results["sentence-count"] == 0
        assert results["word-count"] == 0
        assert results["5-most-frequent-words"] == {}
        assert results["average-word-length"] == 0.0
        assert results["symbols-frequency"] == {}
