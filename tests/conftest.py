import pytest
from pathlib import Path
from typing import Dict, Any
import json


@pytest.fixture
def sample_text_content() -> str:
    """Provide sample text content for testing.

    Returns:
        str: Multi-line text with various patterns for testing analysis
    """
    return """This is a sample text file.
    It contains multiple lines for testing.
    Some words appear multiple times.
    This is to test word frequency.
    The text contains numbers like 123 and symbols @#$.
    This is the last line of the sample text."""


@pytest.fixture
def sample_text_file(tmp_path: Path, sample_text_content: str) -> Path:
    """Create a temporary text file with sample content.

    Args:
        tmp_path: pytest fixture providing temporary directory
        sample_text_content: fixture providing sample text

    Returns:
        Path: Path to created temporary file
    """
    file_path = tmp_path / "sample.txt"
    file_path.write_text(sample_text_content)
    return file_path


@pytest.fixture
def empty_text_file(tmp_path: Path) -> Path:
    """Create an empty temporary text file.

    Args:
        tmp_path: pytest fixture providing temporary directory

    Returns:
        Path: Path to created empty file
    """
    file_path = tmp_path / "empty.txt"
    file_path.touch()
    return file_path


@pytest.fixture
def sample_analysis_results() -> Dict[str, Any]:
    """Provide sample analysis results for testing.

    Returns:
        Dict[str, Any]: Dictionary containing analysis results
    """
    return {
        "total_symbols": {
            "with_spaces": 200,
            "without_spaces": 160
        },
        "sentence-count": 6,
        "word-count": 35,
        "5-most-frequent-words": {
            "this": 3,
            "is": 2,
            "text": 2,
            "sample": 2,
            "the": 2
        },
        "average-word-length": 4.5,
        "symbols-frequency": {
            "a": 10,
            "t": 8,
            "s": 7,
            "i": 6,
            "e": 5
        }
    }


@pytest.fixture
def input_dir_with_files(tmp_path: Path) -> Path:
    """Create a temporary directory with multiple text files.

    Args:
        tmp_path: pytest fixture providing temporary directory

    Returns:
        Path: Path to directory containing test files
    """
    input_dir = tmp_path / "text-files"
    input_dir.mkdir()

    # Create multiple test files
    (input_dir / "file1.txt").write_text("Content of file 1")
    (input_dir / "file2.txt").write_text("Content of file 2")
    (input_dir / "not_txt.doc").write_text("Not a text file")

    return input_dir


@pytest.fixture
def output_dir(tmp_path: Path) -> Path:
    """Create a temporary output directory.

    Args:
        tmp_path: pytest fixture providing temporary directory

    Returns:
        Path: Path to output directory
    """
    output_dir = tmp_path / "text-analyzed"
    output_dir.mkdir()
    return output_dir


@pytest.fixture
def mock_file_validator(mocker):
    """Create a mock FileValidator.

    Args:
        mocker: pytest-mock fixture

    Returns:
        MagicMock: Mocked FileValidator instance
    """
    mock = mocker.MagicMock()
    mock.validate_file_path.return_value = None  # Validation passes
    return mock


@pytest.fixture
def mock_input_handler(mocker):
    """Create a mock InputHandler with predefined responses.

    Args:
        mocker: pytest-mock fixture

    Returns:
        MagicMock: Mocked InputHandler instance
    """
    mock = mocker.MagicMock()
    mock.get_n_value.return_value = 5
    mock.get_file_choice.return_value = "sample.txt"
    mock.continue_analysis.return_value = False
    return mock


@pytest.fixture
def json_output_file(tmp_path: Path, sample_analysis_results: Dict[str, Any]) -> Path:
    """Create a temporary JSON file with analysis results.

    Args:
        tmp_path: pytest fixture providing temporary directory
        sample_analysis_results: fixture providing sample results

    Returns:
        Path: Path to created JSON file
    """
    file_path = tmp_path / "analysis_results.json"
    with open(file_path, 'w') as f:
        json.dump(sample_analysis_results, f)
    return file_path
