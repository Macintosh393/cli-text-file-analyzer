from typing import List, Optional
from .validators import InputValidator
from .exceptions import ValidationError


class InputHandler:
    """Handles user input operations"""

    def __init__(self):
        self.validator = InputValidator()

    def get_file_choice(self, files: List[str]) -> Optional[str]:
        """Get user's file choice"""
        while True:
            self.display_file_options(files)
            print("\nEnter the number of the file to analyze (or 'q' to quit):")
            choice = input().strip()

            try:
                return self.validator.validate_file_choice(choice, files)
            except ValidationError as e:
                print(f"Error: {e}")

    def get_n_value(self) -> int:
        """Get N value from user"""
        while True:
            print("\nEnter N for the number of most frequent words to analyze (1-100):")
            n = input().strip()

            try:
                return self.validator.validate_n_value(n)
            except ValidationError as e:
                print(f"Error: {e}")

    def continue_analysis(self) -> bool:
        """Ask if user wants to continue"""
        while True:
            print("\nWould you like to analyze another file? (y/n)")
            choice = input().strip()

            try:
                return self.validator.validate_continue_choice(choice)
            except ValidationError as e:
                print(f"Error: {e}")

    @staticmethod
    def display_file_options(files: List[str]) -> None:
        """Display available files to user"""
        print("\nAvailable text files:")
        for idx, file in enumerate(files, 1):
            print(f"{idx}. {file}")
