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
        """Read content from file"""
        with open(path, 'r') as f:
            return f.read()

    @staticmethod
    def save_json(data: Dict[str, Any], path: str) -> None:
        """Save data to JSON file"""
        with open(path, 'w') as f:
            json.dump(data, f, indent=4)
