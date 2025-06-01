# tests/test_input_handler.py
import pytest
from unittest.mock import patch, MagicMock
from src.modules.input_handler import InputHandler
from src.modules.exceptions import ValidationError


@pytest.fixture
def mock_validator():
    """Create a mock validator"""
    return MagicMock()


@pytest.fixture
def input_handler(mock_validator):
    """Create an InputHandler instance with mocked validator"""
    handler = InputHandler()
    handler.validator = mock_validator  # Replace the real validator with our mock
    return handler


@pytest.fixture
def sample_files():
    """Provide sample list of files"""
    return ["file1.txt", "file2.txt", "test.txt"]


class TestInputHandler:
    """Test suite for InputHandler class"""

    @patch('builtins.input', side_effect=['1'])
    @patch('builtins.print')
    def test_get_file_choice_valid(self, mock_print, mock_input, input_handler, sample_files):
        """Test valid file selection"""
        # Mock validator to return the first file
        input_handler.validator.validate_file_choice.return_value = sample_files[0]

        result = input_handler.get_file_choice(sample_files)

        assert result == sample_files[0]
        mock_input.assert_called_once()
        input_handler.validator.validate_file_choice.assert_called_once_with('1', sample_files)

    @patch('builtins.input', side_effect=['invalid', '1'])
    @patch('builtins.print')
    def test_get_file_choice_invalid_then_valid(self, mock_print, mock_input, input_handler, sample_files):
        """Test invalid file selection followed by valid selection"""
        input_handler.validator.validate_file_choice.side_effect = [
            ValidationError("Invalid choice"),
            sample_files[0]
        ]

        result = input_handler.get_file_choice(sample_files)

        assert result == sample_files[0]
        assert mock_input.call_count == 2
        assert input_handler.validator.validate_file_choice.call_count == 2

    @patch('builtins.input', side_effect=['q'])
    @patch('builtins.print')
    def test_get_file_choice_quit(self, mock_print, mock_input, input_handler, sample_files):
        """Test quitting file selection"""
        input_handler.validator.validate_file_choice.return_value = None

        result = input_handler.get_file_choice(sample_files)

        assert result is None
        mock_input.assert_called_once()

    @patch('builtins.input', side_effect=['50'])
    @patch('builtins.print')
    def test_get_n_value_valid(self, mock_print, mock_input, input_handler):
        """Test valid N value input"""
        input_handler.validator.validate_n_value.return_value = 50

        result = input_handler.get_n_value()

        assert result == 50
        mock_input.assert_called_once()
        input_handler.validator.validate_n_value.assert_called_once_with('50')

    @patch('builtins.input', side_effect=['invalid', '25'])
    @patch('builtins.print')
    def test_get_n_value_invalid_then_valid(self, mock_print, mock_input, input_handler):
        """Test invalid N value followed by valid input"""
        input_handler.validator.validate_n_value.side_effect = [
            ValidationError("Invalid number"),
            25
        ]

        result = input_handler.get_n_value()

        assert result == 25
        assert mock_input.call_count == 2
        assert input_handler.validator.validate_n_value.call_count == 2

    @patch('builtins.input', side_effect=['y'])
    @patch('builtins.print')
    def test_continue_analysis_yes(self, mock_print, mock_input, input_handler):
        """Test continue analysis with 'yes' response"""
        input_handler.validator.validate_continue_choice.return_value = True

        result = input_handler.continue_analysis()

        assert result is True
        mock_input.assert_called_once()
        input_handler.validator.validate_continue_choice.assert_called_once_with('y')

    @patch('builtins.input', side_effect=['invalid', 'n'])
    @patch('builtins.print')
    def test_continue_analysis_invalid_then_no(self, mock_print, mock_input, input_handler):
        """Test invalid continue choice followed by 'no'"""
        input_handler.validator.validate_continue_choice.side_effect = [
            ValidationError("Invalid choice"),
            False
        ]

        result = input_handler.continue_analysis()

        assert result is False
        assert mock_input.call_count == 2
        assert input_handler.validator.validate_continue_choice.call_count == 2

    def test_display_file_options(self, input_handler, sample_files, capsys):
        """Test file options display"""
        input_handler.display_file_options(sample_files)
        captured = capsys.readouterr()

        expected_output = "\nAvailable text files:\n1. file1.txt\n2. file2.txt\n3. test.txt\n"
        assert captured.out == expected_output
