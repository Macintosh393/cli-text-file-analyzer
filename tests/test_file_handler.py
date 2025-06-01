# tests/test_file_handler.py
import pytest
from pathlib import Path
import json
from src.modules.file_handler import FileHandler
from src.modules.exceptions import FileError


@pytest.fixture
def mock_file_validator(mocker):
    """Create a mock FileValidator"""
    mock = mocker.MagicMock()
    mock.validate_file_path.return_value = None  # Validation passes
    return mock


@pytest.fixture
def file_handler(mock_file_validator):
    """Create a FileHandler instance with mock validator"""
    return FileHandler(mock_file_validator)


def test_get_available_files(file_handler, input_dir_with_files):
    """Test listing available files from directory"""
    files = file_handler.get_available_files(input_dir_with_files)
    assert len(files) == 2
    assert "file1.txt" in files
    assert "file2.txt" in files
    assert "not_txt.doc" not in files
    assert files == ["file1.txt", "file2.txt"]  # Check sorting


def test_get_available_files_invalid_dir(file_handler):
    """Test handling of invalid directory"""
    with pytest.raises(FileError) as exc_info:
        file_handler.get_available_files("/nonexistent/directory")
    assert "Error accessing directory" in str(exc_info.value)


def test_read_file_success(file_handler, sample_text_file):
    """Test successful file reading"""
    content = file_handler.read_file(str(sample_text_file))
    assert content.startswith("This is a sample text file")
    assert len(content) > 0


def test_read_empty_file(file_handler, empty_text_file):
    """Test reading empty file"""
    content = file_handler.read_file(str(empty_text_file))
    assert content == ""


def test_read_file_size_limit(file_handler, tmp_path, mocker):
    """Test file size limit enforcement"""
    # Create a file that exceeds size limit
    big_file = tmp_path / "big.txt"
    mocker.patch.object(Path, 'stat', return_value=mocker.Mock(st_size=1024 * 1024 * 20))

    with pytest.raises(FileError) as exc_info:
        file_handler.read_file(str(big_file))
    assert "exceeds maximum allowed size" in str(exc_info.value)


def test_read_nonexistent_file(file_handler):
    """Test handling of nonexistent file"""
    with pytest.raises(FileError):
        file_handler.read_file("/nonexistent/file.txt")


def test_save_json_success(file_handler, output_dir, sample_analysis_results):
    """Test successful JSON saving"""
    output_file = output_dir / "results.json"
    file_handler.save_json(sample_analysis_results, str(output_file))

    # Verify file was created and contains correct data
    assert output_file.exists()
    with output_file.open('r', encoding='utf-8') as f:
        saved_data = json.load(f)
    assert saved_data == sample_analysis_results


def test_save_json_creates_directories(file_handler, tmp_path, sample_analysis_results):
    """Test JSON saving creates necessary directories"""
    deep_path = tmp_path / "deep" / "nested" / "path" / "results.json"
    file_handler.save_json(sample_analysis_results, str(deep_path))
    assert deep_path.exists()


def test_save_json_invalid_path(file_handler, sample_analysis_results):
    """Test handling of invalid save path"""
    # Use a path that will definitely be invalid on Windows
    # CON is a reserved name in Windows and can't be used as a filename
    invalid_path = "CON/invalid.json"

    with pytest.raises(FileError) as exc_info:
        file_handler.save_json(sample_analysis_results, invalid_path)
    assert "Error saving results" in str(exc_info.value)


def test_save_json_permission_denied(file_handler, sample_analysis_results, tmp_path, mocker):
    """Test handling of permission denied error"""
    test_file = tmp_path / "test.json"

    # Mock mkdir to raise PermissionError
    mocker.patch.object(
        Path,
        'mkdir',
        side_effect=PermissionError("Permission denied")
    )

    with pytest.raises(FileError) as exc_info:
        file_handler.save_json(sample_analysis_results, str(test_file))
    assert "Error saving results" in str(exc_info.value)


def test_validator_integration(file_handler, sample_text_file):
    """Test integration with file validator"""
    file_handler.read_file(str(sample_text_file))
    file_handler.validator.validate_file_path.assert_called_once_with(Path(sample_text_file))
