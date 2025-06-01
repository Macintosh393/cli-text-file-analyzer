import json
import os
from pathlib import Path
from typing import List, Dict, Any
from src.config.config import ConfigFactory
from .exceptions import FileError, ValidationError


class FileHandler:
    def __init__(self, validator):
        self.validator = validator
        self.config = ConfigFactory.get_config()

    def get_available_files(self, directory: str) -> List[str]:
        """List all txt files in directory"""
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
        """Read content from file with encoding handling"""
        path = Path(path)
        encoding_errors = []

        try:
            self.validator.validate_file_path(path)

            # Check file permissions early
            if not os.access(path, os.R_OK):
                raise FileError(
                    "Permission denied",
                    {"path": str(path)}
                )

            # Check file size
            file_size = path.stat().st_size
            if file_size > self.config.MAX_FILE_SIZE:
                raise FileError(
                    self.config.ERROR_MESSAGES['file_size_error'].format(path),
                    {
                        "path": str(path),
                        "size": file_size,
                        "max_size": self.config.MAX_FILE_SIZE
                    }
                )

            for encoding in self.config.SUPPORTED_ENCODINGS:
                try:
                    with path.open('r', encoding=encoding) as f:
                        return f.read()
                except UnicodeDecodeError as e:
                    encoding_errors.append({
                        "encoding": encoding,
                        "error": str(e)
                    })
                    continue

            raise FileError(
                "Failed to decode file with any supported encoding",
                {
                    "path": str(path),
                    "attempted_encodings": encoding_errors
                }
            )

        except ValidationError as e:
            raise FileError(str(e), {"path": str(path)})
        except OSError as e:
            raise FileError(
                f"OS error while reading file: {e}",
                {
                    "path": str(path),
                    "error_code": e.errno,
                    "error_type": e.__class__.__name__
                }
            )

    def save_json(self, data: Dict[str, Any], path: str) -> None:
        """Save data to JSON file"""
        path = Path(path)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)

            with path.open('w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

        except Exception as e:
            raise FileError(f"Error saving results: {e}")
