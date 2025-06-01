# tests/test_validators.py
import os
import pytest
from pathlib import Path
from unittest.mock import patch, Mock
from src.modules.validators import FileValidator, InputValidator
from src.modules.exceptions import ValidationError


class TestFileValidator:
    """Test suite for FileValidator class"""

    @pytest.fixture
    def validator(self):
        """Create a FileValidator instance"""
        return FileValidator()

    def test_validate_file_path_invalid_type(self, validator):
        """Test validation with invalid path type"""
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_file_path("not_a_path")
        assert "Invalid path type" in str(exc_info.value)

    def test_validate_file_path_not_exists(self, validator):
        """Test validation with non-existent file"""
        path = Path("nonexistent.txt")
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_file_path(path)
        assert "File does not exist" in str(exc_info.value)

    def test_validate_file_path_is_directory(self, validator, tmp_path):
        """Test validation with directory instead of file"""
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_file_path(tmp_path)
        assert "Path is not a file" in str(exc_info.value)

    def test_validate_file_path_no_read_permission(self, validator, tmp_path):
        """Test validation with file lacking read permissions"""
        test_file = tmp_path / "test.txt"
        test_file.write_text("test content")

        with patch('os.access') as mock_access:
            mock_access.return_value = False
            with pytest.raises(ValidationError) as exc_info:
                validator.validate_file_path(test_file)
            assert "No read permission" in str(exc_info.value)

    def test_validate_file_path_empty_file(self, validator, tmp_path):
        """Test validation with empty file"""
        test_file = tmp_path / "empty.txt"
        test_file.touch()

        with pytest.raises(ValidationError) as exc_info:
            validator.validate_file_path(test_file)
        assert "File is empty" in str(exc_info.value)

    def test_validate_file_path_os_error(self, validator):
        """Test validation with OS error"""
        with patch('pathlib.Path.exists') as mock_exists:
            mock_exists.side_effect = OSError("Mock OS error")
            path = Path("test.txt")

            with pytest.raises(ValidationError) as exc_info:
                validator.validate_file_path(path)

            assert "OS error during validation" in str(exc_info.value)
            error_context = exc_info.value.args[1]
            assert error_context["path"] == str(path)
            assert "Mock OS error" in error_context["error"]

    def test_validate_file_path_valid(self, validator, tmp_path):
        """Test validation with valid file"""
        test_file = tmp_path / "valid.txt"
        test_file.write_text("test content")

        # Should not raise any exception
        validator.validate_file_path(test_file)


class TestInputValidator:
    """Test suite for InputValidator class"""

    @pytest.fixture
    def validator(self):
        """Create an InputValidator instance"""
        return InputValidator()

    @pytest.mark.parametrize("value,expected", [
        ("1", 1),
        ("50", 50),
        ("100", 100)
    ])
    def test_validate_n_value_valid(self, validator, value, expected):
        """Test N value validation with valid inputs"""
        assert validator.validate_n_value(value) == expected

    @pytest.mark.parametrize("invalid_value", [
        "0", "101", "-1", "abc", "1.5", "", " "
    ])
    def test_validate_n_value_invalid(self, validator, invalid_value):
        """Test N value validation with invalid inputs"""
        with pytest.raises(ValidationError):
            validator.validate_n_value(invalid_value)

    def test_validate_file_choice_valid(self, validator):
        """Test file choice validation with valid input"""
        files = ["file1.txt", "file2.txt"]
        assert validator.validate_file_choice("1", files) == "file1.txt"
        assert validator.validate_file_choice("2", files) == "file2.txt"

    def test_validate_file_choice_quit(self, validator):
        """Test file choice validation with quit option"""
        files = ["file1.txt"]
        assert validator.validate_file_choice("q", files) is None
        assert validator.validate_file_choice("Q", files) is None

    @pytest.mark.parametrize("invalid_choice", [
        "0", "3", "abc", "", " ", "-1"
    ])
    def test_validate_file_choice_invalid(self, validator, invalid_choice):
        """Test file choice validation with invalid inputs"""
        files = ["file1.txt", "file2.txt"]
        with pytest.raises(ValidationError):
            validator.validate_file_choice(invalid_choice, files)

    def test_validate_file_choice_no_files(self, validator):
        """Test file choice validation with empty file list"""
        with pytest.raises(ValidationError) as exc_info:
            validator.validate_file_choice("1", [])
        assert "No files available" in str(exc_info.value)

    @pytest.mark.parametrize("choice,expected", [
        ("y", True),
        ("Y", True),
        ("n", False),
        ("N", False)
    ])
    def test_validate_continue_choice_valid(self, validator, choice, expected):
        """Test continue choice validation with valid inputs"""
        assert validator.validate_continue_choice(choice) == expected

    @pytest.mark.parametrize("invalid_choice", [
        "yes", "no", "1", "0", "", " ", "maybe"
    ])
    def test_validate_continue_choice_invalid(self, validator, invalid_choice):
        """Test continue choice validation with invalid inputs"""
        with pytest.raises(ValidationError):
            validator.validate_continue_choice(invalid_choice)

    def test_validate_file_path_txt(self, validator, tmp_path):
        """Test file path validation for text files"""
        # Valid .txt file
        txt_file = tmp_path / "test.txt"
        txt_file.touch()
        validator.validate_file_path(txt_file)

        # Invalid extension
        invalid_file = tmp_path / "test.pdf"
        invalid_file.touch()
        with pytest.raises(ValidationError):
            validator.validate_file_path(invalid_file)

        # Non-existent file
        with pytest.raises(ValidationError):
            validator.validate_file_path(tmp_path / "nonexistent.txt")

        # Directory instead of file
        with pytest.raises(ValidationError):
            validator.validate_file_path(tmp_path)
