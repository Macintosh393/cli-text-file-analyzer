# tests/test_path_manager.py
import os
import pytest
from unittest.mock import patch, Mock
from src.modules.path_manager import PathManager
from src.modules.exceptions import FileError


@pytest.fixture
def path_manager():
    """Create a PathManager instance"""
    with patch('os.path.dirname') as mock_dirname:
        # Mock the directory structure
        mock_dirname.side_effect = [
            '/fake/src/modules',  # First call for __file__
            '/fake/src',  # Second call
            '/fake'  # Third call for project root
        ]
        manager = PathManager()
        # Reset mock to not interfere with other tests
        mock_dirname.reset_mock()
        return manager


class TestPathManager:
    """Test suite for PathManager class"""

    def test_get_project_root(self):
        """Test project root path resolution"""
        with patch('os.path.dirname') as mock_dirname:
            with patch('os.path.abspath') as mock_abspath:
                mock_abspath.return_value = '/fake/src/modules/path_manager.py'
                mock_dirname.side_effect = [
                    '/fake/src/modules',
                    '/fake/src',
                    '/fake'
                ]

                root = PathManager.get_project_root()
                assert root == '/fake'
                assert mock_dirname.call_count == 3

    def test_initialization(self, path_manager):
        """Test PathManager initialization"""
        assert path_manager.project_root == '/fake'
        assert path_manager.input_dir == os.path.join('/fake', 'src', 'text-files')
        assert path_manager.output_dir == os.path.join('/fake', 'src', 'text-analyzed')

    def test_get_input_path(self, path_manager):
        """Test input path resolution"""
        filename = "test.txt"
        expected_path = os.path.join('/fake', 'src', 'text-files', filename)

        result = path_manager.get_input_path(filename)
        assert result == expected_path

    def test_get_output_path(self, path_manager):
        """Test output path resolution"""
        filename = "test"
        expected_path = os.path.join('/fake', 'src', 'text-analyzed', filename + '.json')

        result = path_manager.get_output_path(filename)
        assert result == expected_path

    def test_ensure_output_dir_exists_success(self, path_manager):
        """Test successful output directory creation"""
        with patch('os.makedirs') as mock_makedirs:
            with patch('os.access') as mock_access:
                mock_access.return_value = True  # Write permission granted

                path_manager.ensure_output_dir_exists()

                mock_makedirs.assert_called_once_with(
                    path_manager.output_dir,
                    exist_ok=True
                )
                mock_access.assert_called_once_with(
                    path_manager.output_dir,
                    os.W_OK
                )

    def test_ensure_output_dir_exists_no_permission(self, path_manager):
        """Test output directory creation with no write permission"""
        with patch('os.makedirs'):
            with patch('os.access') as mock_access:
                mock_access.return_value = False  # No write permission

                with pytest.raises(FileError) as exc_info:
                    path_manager.ensure_output_dir_exists()

                assert "No write permission" in str(exc_info.value)

    def test_ensure_output_dir_exists_creation_error(self, path_manager):
        """Test output directory creation failure"""
        with patch('os.makedirs') as mock_makedirs:
            mock_makedirs.side_effect = OSError("Permission denied")

            with pytest.raises(FileError) as exc_info:
                path_manager.ensure_output_dir_exists()

            assert "Failed to create output directory" in str(exc_info.value)
            assert "Permission denied" in str(exc_info.value)

    def test_path_separators(self, path_manager):
        """Test path separator handling across platforms"""
        filename = "test.txt"
        input_path = path_manager.get_input_path(filename)
        output_path = path_manager.get_output_path(filename)

        # Convert paths to use the platform-specific separator
        expected_input_path = os.path.normpath(os.path.join('/fake', 'src', 'text-files', filename))
        expected_output_path = os.path.normpath(os.path.join('/fake', 'src', 'text-analyzed', filename + '.json'))

        # Normalize the actual paths
        normalized_input_path = os.path.normpath(input_path)
        normalized_output_path = os.path.normpath(output_path)

        # Compare normalized paths
        assert normalized_input_path == expected_input_path, \
            f"Input path {normalized_input_path} doesn't match expected {expected_input_path}"
        assert normalized_output_path == expected_output_path, \
            f"Output path {normalized_output_path} doesn't match expected {expected_output_path}"

    @pytest.mark.parametrize("filename", [
        "test.txt",
        "path/with/slashes.txt",
        r"path\with\backslashes.txt",
        "../relative/path.txt",
        "special@#$chars.txt"
    ])
    def test_path_handling_special_cases(self, path_manager, filename):
        """Test path handling with special cases"""
        input_path = path_manager.get_input_path(filename)
        output_path = path_manager.get_output_path(filename.replace('.txt', ''))

        # Verify paths are properly joined
        assert os.path.basename(input_path).endswith(os.path.basename(filename))
        assert os.path.basename(output_path).endswith('.json')
        assert path_manager.input_dir in input_path
        assert path_manager.output_dir in output_path

    def test_ensure_output_dir_exists_with_context(self, path_manager):
        """Test output directory creation with error context"""
        with patch('os.makedirs') as mock_makedirs:
            error = OSError("Permission denied")
            error.errno = 13  # Permission denied errno
            mock_makedirs.side_effect = error

            with pytest.raises(FileError) as exc_info:
                path_manager.ensure_output_dir_exists()

            error_context = exc_info.value.args[1]
            assert error_context["path"] == path_manager.output_dir
            assert error_context["error"] == "Permission denied"
            assert error_context["error_code"] == 13
