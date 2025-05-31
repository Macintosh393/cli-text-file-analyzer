from typing import Any, List
from pathlib import Path
from .exceptions import ValidationError


class FileValidator:
    def validate_file_path(self, path: Path) -> None:
        """Validate if file path exists and is a file"""
        if not path.exists():
            raise ValidationError(f"File does not exist: {path}")
        if not path.is_file():
            raise ValidationError(f"Path is not a file: {path}")


class InputValidator:
    """Handles all input validation logic"""

    @staticmethod
    def validate_n_value(n: Any) -> int:
        """
        Validate N value for word frequency analysis.

        Args:
            n: Value to validate

        Returns:
            int: Validated N value

        Raises:
            ValidationError: If validation fails
        """
        try:
            n = int(n)
            if not 1 <= n <= 100:
                raise ValidationError("N must be between 1 and 100")
            return n
        except ValueError:
            raise ValidationError("N must be an integer")

    @staticmethod
    def validate_file_choice(choice: Any, available_files: List[str]) -> str:
        """
        Validate file choice input.

        Args:
            choice: User's input choice
            available_files: List of available files

        Returns:
            str: Chosen filename

        Raises:
            ValidationError: If validation fails
        """
        if not available_files:
            raise ValidationError("No files available to choose from")

        if choice.lower() == 'q':
            return None

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(available_files):
                return available_files[idx]
            else:
                raise ValidationError(
                    f"Please enter a number between 1 and {len(available_files)}"
                )
        except ValueError:
            raise ValidationError("Please enter a valid number or 'q' to quit")

    @staticmethod
    def validate_continue_choice(choice: str) -> bool:
        """
        Validate continue analysis choice.

        Args:
            choice: User's input choice

        Returns:
            bool: True if continue, False if not

        Raises:
            ValidationError: If validation fails
        """
        choice = choice.lower().strip()
        if choice not in ['y', 'n']:
            raise ValidationError("Please enter 'y' or 'n'")
        return choice == 'y'

    @staticmethod
    def validate_file_path(path: Path) -> None:
        """
        Validate file path.

        Args:
            path: Path to validate

        Raises:
            ValidationError: If validation fails
        """
        if not path.exists():
            raise ValidationError(f"File not found: {path}")
        if not path.is_file():
            raise ValidationError(f"Not a file: {path}")
        if not path.suffix == '.txt':
            raise ValidationError(f"Not a text file: {path}")
