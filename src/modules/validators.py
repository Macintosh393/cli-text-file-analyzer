import os
from typing import Any, List, Optional
from pathlib import Path
from .exceptions import ValidationError


class FileValidator:
    """Handles validation of file paths and their properties.

    Provides comprehensive validation for file paths including existence,
    type checking, permissions, and file size verification.
    """

    def validate_file_path(self, path: Path) -> None:
        """Validate file path and its properties.

        Performs comprehensive validation including:
        - Type checking of the path object
        - File existence
        - File type verification
        - Read permissions
        - File size validation

        Args:
            path (Path): Path object to validate

        Raises:
            ValidationError: If any validation check fails, with context in
                           the error details dictionary
        """
        if not isinstance(path, Path):
            raise ValidationError(
                "Invalid path type",
                {"expected": "Path", "received": type(path).__name__}
            )

        try:
            if not path.exists():
                raise ValidationError(
                    f"File does not exist: {path}",
                    {"path": str(path)}
                )
            if not path.is_file():
                raise ValidationError(
                    f"Path is not a file: {path}",
                    {"path": str(path), "type": "directory"}
                )
            if not os.access(path, os.R_OK):
                raise ValidationError(
                    f"No read permission: {path}",
                    {"path": str(path)}
                )
            if path.stat().st_size == 0:
                raise ValidationError(
                    f"File is empty: {path}",
                    {"path": str(path)}
                )
        except OSError as e:
            raise ValidationError(
                f"OS error during validation: {e}",
                {"path": str(path), "error": str(e)}
            )


class InputValidator:
    """Handles validation of user input.

    Provides methods to validate various types of user input including
    numeric values, file selections, and yes/no responses.
    """

    @staticmethod
    def validate_n_value(n: Any) -> int:
        """Validate N value for word frequency analysis.

        Validates that the input can be converted to an integer and
        falls within the acceptable range (1-100).

        Args:
            n (Any): Value to validate, typically a string from user input

        Returns:
            int: Validated integer value between 1 and 100

        Raises:
            ValidationError: If value isn't numeric or is out of range
        """
        try:
            n = int(n)
            if not 1 <= n <= 100:
                raise ValidationError("N must be between 1 and 100")
            return n
        except ValueError:
            raise ValidationError("N must be an integer")

    @staticmethod
    def validate_file_choice(choice: Any, available_files: List[str]) -> Optional[str]:
        """Validate user's file selection choice.

        Validates the user's input for file selection, allowing either
        a numeric choice or 'q' to quit.

        Args:
            choice (Any): User's input choice (number or 'q')
            available_files (List[str]): List of available files to choose from

        Returns:
            Optional[str]: Selected filename or None if user chooses to quit

        Raises:
            ValidationError: If choice is invalid or no files are available
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
        """Validate user's choice to continue analysis.

        Ensures the input is either 'y' or 'n' for yes/no decision.

        Args:
            choice (str): User's input choice ('y' or 'n')

        Returns:
            bool: True if continue ('y'), False if not ('n')

        Raises:
            ValidationError: If input is neither 'y' nor 'n'
        """
        choice = choice.lower().strip()
        if choice not in ['y', 'n']:
            raise ValidationError("Please enter 'y' or 'n'")
        return choice == 'y'

    @staticmethod
    def validate_file_path(path: Path) -> None:
        """Validate file path and type.

        Ensures the file exists, is a regular file (not a directory),
        and has a .txt extension.

        Args:
            path (Path): Path object to validate

        Raises:
            ValidationError: If path is invalid, file doesn't exist,
                           or file isn't a .txt file
        """
        if not path.exists():
            raise ValidationError(f"File not found: {path}")
        if not path.is_file():
            raise ValidationError(f"Not a file: {path}")
        if not path.suffix == '.txt':
            raise ValidationError(f"Not a text file: {path}")
