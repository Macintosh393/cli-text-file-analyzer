import os
import json
from typing import List, Dict, Any


class FileHandler:
    """Handles file operations"""

    @staticmethod
    def get_available_files(directory: str) -> List[str]:
        """Get list of available .txt files"""
        try:
            files = [f for f in os.listdir(directory) if f.endswith('.txt')]
            return sorted(files)
        except Exception as e:
            print(f"Error accessing directory: {e}")
            print(f"Tried to access: {directory}")
            return []

    @staticmethod
    def read_file(path: str) -> str:
        """
        Read content from file with UTF-8 encoding.
        Falls back to cp1251 (Cyrillic) if UTF-8 fails.
        """
        encodings = ['utf-8', 'cp1251']  # List of encodings to try

        for encoding in encodings:
            try:
                with open(path, 'r', encoding=encoding) as f:
                    return f.read()
            except UnicodeDecodeError:
                continue
            except Exception as e:
                raise Exception(f"Error reading file: {e}")

        raise Exception("Could not decode file with any supported encoding")

    @staticmethod
    def save_json(data: Dict[str, Any], path: str) -> None:
        """Save data to JSON file with UTF-8 encoding"""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
