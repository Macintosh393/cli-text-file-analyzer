from typing import List, Optional
from .validators import InputValidator
from .exceptions import ValidationError


class InputHandler:
    """Handles user input operations for the text analyzer application.

    This class manages all user interactions, including file selection,
    parameter input, and continuation prompts. It uses InputValidator
    to ensure all inputs are valid.

    Attributes:
        validator (InputValidator): Validator instance for input validation
    """

    def __init__(self) -> None:
        """Initialize InputHandler with a new InputValidator instance."""
        self.validator = InputValidator()

    def get_file_choice(self, files: List[str]) -> Optional[str]:
        """Get user's file choice from available files.

        Displays available files and prompts user to select one.
        Continues prompting until a valid choice is made or user quits.

        Args:
            files (List[str]): List of available file names

        Returns:
            Optional[str]: Selected filename or None if user chooses to quit

        Raises:
            ValidationError: If input validation fails
        """
        while True:
            self.display_file_options(files)
            print("\nEnter the number of the file to analyze (or 'q' to quit):")
            choice = input().strip()

            try:
                return self.validator.validate_file_choice(choice, files)
            except ValidationError as e:
                print(f"Error: {e}")

    def get_n_value(self) -> int:
        """Get N value from user for word frequency analysis.

        Prompts user to enter a number between 1 and 100 for the
        number of most frequent words to analyze. Continues prompting
        until a valid value is entered.

        Returns:
            int: Validated N value between 1 and 100

        Raises:
            ValidationError: If input validation fails
        """
        while True:
            print("\nEnter N for the number of most frequent words to analyze (1-100):")
            n = input().strip()

            try:
                return self.validator.validate_n_value(n)
            except ValidationError as e:
                print(f"Error: {e}")

    def continue_analysis(self) -> bool:
        """Ask if user wants to analyze another file.

        Prompts user for yes/no input and continues prompting
        until a valid response is received.

        Returns:
            bool: True if user wants to continue, False otherwise

        Raises:
            ValidationError: If input validation fails
        """
        while True:
            print("\nWould you like to analyze another file? (y/n)")
            choice = input().strip()

            try:
                return self.validator.validate_continue_choice(choice)
            except ValidationError as e:
                print(f"Error: {e}")

    @staticmethod
    def display_file_options(files: List[str]) -> None:
        """Display available text files to user.

        Prints numbered list of available files for user selection.

        Args:
            files (List[str]): List of available file names
        """
        print("\nAvailable text files:")
        for idx, file in enumerate(files, 1):
            print(f"{idx}. {file}")
