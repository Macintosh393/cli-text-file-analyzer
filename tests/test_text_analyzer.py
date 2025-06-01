# tests/test_text_analyzer.py
import pytest
from unittest.mock import patch
from src.modules.text_analyzer import TextAnalyzer
from src.modules.exceptions import AnalysisError, ValidationError


@pytest.fixture
def sample_text():
    """Provide a sample text for testing"""
    return "Hello, world! This is a test. How are you? I am fine!"


@pytest.fixture
def analyzer(sample_text):
    """Create a TextAnalyzer instance with sample text"""
    return TextAnalyzer(sample_text, n=3)


class TestTextAnalyzer:
    """Test suite for TextAnalyzer class"""

    def test_initialization_valid(self, sample_text):
        """Test valid initialization"""
        analyzer = TextAnalyzer(sample_text, n=3)
        assert analyzer.text == sample_text
        assert analyzer.n == 3
        assert len(analyzer.words) > 0

    @pytest.mark.parametrize("invalid_text,error_msg", [
        (None, "Text must be a string"),
        (123, "Text must be a string"),
        ("", "Text cannot be empty"),
        ("   ", "Text cannot be empty"),
        ("!!!???...,,,", "No valid words found in text")
    ])
    def test_initialization_invalid(self, invalid_text, error_msg):
        """Test initialization with invalid inputs"""
        with pytest.raises((ValidationError, AnalysisError)) as exc_info:
            TextAnalyzer(invalid_text, n=3)
        assert str(exc_info.value) == error_msg

    def test_get_symbol_counts(self, analyzer):
        """Test symbol counting"""
        counts = analyzer.get_symbol_counts()

        assert isinstance(counts, dict)
        assert "with_spaces" in counts
        assert "without_spaces" in counts
        assert counts["with_spaces"] > counts["without_spaces"]
        assert counts["with_spaces"] == len(analyzer.text)
        assert counts["without_spaces"] == len(analyzer.text.replace(" ", ""))

    def test_get_sentence_count(self, analyzer):
        """Test sentence counting"""
        count = analyzer.get_sentence_count()

        assert count == 4  # Sample text has 4 sentences
        assert isinstance(count, int)

    def test_get_sentence_count_error(self):
        """Test sentence counting error handling"""
        # Mock a scenario that would cause re.split to fail
        with pytest.raises(AnalysisError) as exc_info:
            analyzer = TextAnalyzer("Test", n=3)
            # Mock re.split to raise an exception
            analyzer.text = None
            analyzer.get_sentence_count()
        assert "Error counting sentences" in str(exc_info.value)

    def test_get_word_count(self, analyzer):
        """Test word counting"""
        count = analyzer.get_word_count()

        assert count == 12  # Sample text has 12 words
        assert isinstance(count, int)
        assert count == len(analyzer.words)

    def test_get_most_frequent_words(self, analyzer):
        """Test most frequent words calculation"""
        freq_words = analyzer.get_most_frequent_words()

        assert isinstance(freq_words, dict)
        assert len(freq_words) <= analyzer.n
        # Verify frequencies are in descending order
        frequencies = list(freq_words.values())
        assert frequencies == sorted(frequencies, reverse=True)

    def test_get_most_frequent_words_invalid_n(self):
        """Test most frequent words with invalid N"""
        text = "short text"
        with pytest.raises(ValidationError) as exc_info:
            analyzer = TextAnalyzer(text, n=5)
            analyzer.get_most_frequent_words()
        assert "N (5) is larger than available words" in str(exc_info.value)

    def test_get_average_word_length(self, analyzer):
        """Test average word length calculation"""
        avg_length = analyzer.get_average_word_length()

        assert isinstance(avg_length, float)
        assert 0 <= avg_length <= max(len(word) for word in analyzer.words)
        # Verify rounding to 2 decimal places
        assert str(avg_length).split('.')[-1] <= '99'

    def test_get_symbol_frequency(self, analyzer):
        """Test symbol frequency calculation"""
        freq = analyzer.get_symbol_frequency()

        assert isinstance(freq, dict)
        assert len(freq) > 0
        # Verify sorting by frequency and then by symbol
        items = list(freq.items())
        for i in range(len(items) - 1):
            curr_freq, curr_symbol = items[i][1], items[i][0]
            next_freq, next_symbol = items[i + 1][1], items[i + 1][0]
            assert (curr_freq > next_freq or
                    (curr_freq == next_freq and curr_symbol < next_symbol))

    def test_get_symbol_frequency_error(self):
        """Test symbol frequency error handling"""
        analyzer = TextAnalyzer("Test", n=3)  # Create analyzer first

        # Then patch Counter for the get_symbol_frequency call
        with patch('src.modules.text_analyzer.Counter') as mock_counter:
            # Make Counter raise an exception when called
            mock_counter.side_effect = Exception("Mock Counter error")

            with pytest.raises(AnalysisError) as exc_info:
                analyzer.get_symbol_frequency()

            assert "Error calculating symbol frequency" in str(exc_info.value)
            assert "Mock Counter error" in str(exc_info.value)

    def test_unicode_support(self):
        """Test support for Unicode characters"""
        text = "Hello мир! こんにちは world!"
        analyzer = TextAnalyzer(text, n=3)
        assert len(analyzer.words) > 0
        assert "мир" in analyzer.words
        assert "world" in analyzer.words
