import os
import json
from pathlib import Path
from typing import List, Dict, Any
from .exceptions import FileError, ValidationError
from .validators import InputValidator


class FileHandler:
    """Handles file operations"""

    def __init__(self):
        self.validator = InputValidator()

    def get_available_files(self, directory: str) -> List[str]:
        """Get list of available .txt files"""
        try:
            path = Path(directory)
            if not path.exists():
                raise FileError(f"Directory not found: {directory}")
            if not path.is_dir():
                raise FileError(f"Not a directory: {directory}")

            files = [
                f.name for f in path.iterdir()
                if f.is_file() and f.suffix == '.txt'
            ]
            return sorted(files)
        except Exception as e:
            raise FileError(f"Error accessing directory: {e}")

    def read_file(self, path: str) -> str:
        """Read content from file with encoding handling"""
        path = Path(path)
        try:
            self.validator.validate_file_path(path)

            encodings = ['utf-8', 'cp1251']
            for encoding in encodings:
                try:
                    with path.open('r', encoding=encoding) as f:
                        return f.read()
                except UnicodeDecodeError:
                    continue

            raise FileError(
                f"Could not decode file {path} with supported encodings"
            )

        except ValidationError as e:
            raise FileError(f"Invalid file: {e}")
        except Exception as e:
            raise FileError(f"Error reading file: {e}")

    def save_json(self, data: Dict[str, Any], path: str) -> None:
        """Save data to JSON file"""
        path = Path(path)
        try:
            path.parent.mkdir(parents=True, exist_ok=True)

            with path.open('w', encoding='utf-8') as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

        except Exception as e:
            raise FileError(f"Error saving results: {e}")
