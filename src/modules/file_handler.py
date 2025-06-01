import json
from pathlib import Path
from typing import List, Dict, Any
from src.config.config import ConfigFactory
from .exceptions import FileError, ValidationError


class FileHandler:
    """Handles file operations for the text analyzer application.

    This class manages file operations including reading text files,
    listing available files, and saving analysis results.

    Attributes:
        validator: File validator instance for path validation
        config: Application configuration instance
    """

    def __init__(self, validator) -> None:
        """Initialize FileHandler with validator.

        Args:
            validator: Validator instance for file validation
        """
        self.validator = validator
        self.config = ConfigFactory.get_config()

    def get_available_files(self, directory: str) -> List[str]:
        """List all valid text files in the specified directory.

        Lists files that:
        - Have supported extensions (defined in config)
        - Don't exceed maximum file size
        - Are accessible

        Args:
            directory (str): Path to directory to search

        Returns:
            List[str]: List of valid file names, sorted alphabetically

        Raises:
            FileError: If directory access fails or other file operations fail
        """
        path = Path(directory)
        try:
            files = [
                f.name for f in path.iterdir()
                if (f.is_file() and
                    f.suffix in self.config.SUPPORTED_FILE_TYPES and
                    f.stat().st_size <= self.config.MAX_FILE_SIZE)
            ]
            return sorted(files)
        except Exception as e:
            raise FileError(
                self.config.ERROR_MESSAGES['dir_access_error'].format(e)
            )

    def read_file(self, path: str) -> str:
        """Read and decode content from a text file.

        Attempts to read the file using supported encodings defined in config.

        Args:
            path (str): Path to the file to read

        Returns:
            str: Content of the file

        Raises:
            FileError: If file cannot be read or decoded
            ValidationError: If file path is invalid
        """
        path = Path(path)
        try:
            self.validator.validate_file_path(path)

            # Check file size
            if path.stat().st_size > self.config.MAX_FILE_SIZE:
                raise FileError(
                    self.config.ERROR_MESSAGES['file_size_error'].format(path)
                )

            for encoding in self.config.SUPPORTED_ENCODINGS:
                try:
                    with path.open('r', encoding=encoding) as f:
                        return f.read()
                except UnicodeDecodeError:
                    continue

            raise FileError(
                self.config.ERROR_MESSAGES['decode_error'].format(path)
            )

        except ValidationError as e:
            raise FileError(
                self.config.ERROR_MESSAGES['invalid_file'].format(e)
            )
        except Exception as e:
            raise FileError(f"Error reading file: {e}")

    def save_json(self, data: Dict[str, Any], path: str) -> None:
        """Save analysis results to a JSON file.

        Creates necessary directories if they don't exist.

        Args:
            data (Dict[str, Any]): Data to save
            path (str): Output file path

        Raises:
            FileError: If saving fails due to permissions or other IO errors
        """
        path = Path(path)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)

            with path.open('w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

        except Exception as e:
            raise FileError(f"Error saving results: {e}")
