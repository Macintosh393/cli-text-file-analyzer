import os
from pathlib import Path
from typing import Union
from .exceptions import FileError


class PathManager:
    """Handles all path-related operations for the text analyzer application.

    This class manages file paths, directory creation, and path resolution
    for both input and output operations.

    Attributes:
        project_root (str): Absolute path to project root directory
        input_dir (str): Path to directory containing input text files
        output_dir (str): Path to directory for analysis output files
    """

    @staticmethod
    def get_project_root() -> str:
        """Get the absolute path to project root directory.

        Determines the project root by navigating up from the current
        module's location.

        Returns:
            str: Absolute path to project root directory
        """
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.dirname(current_dir)

    def __init__(self) -> None:
        """Initialize PathManager with project directory structure.

        Sets up paths for project root, input, and output directories.
        """
        self.project_root = self.get_project_root()
        self.input_dir = os.path.join(self.project_root, "src", "text-files")
        self.output_dir = os.path.join(self.project_root, "src", "text-analyzed")

    def get_input_path(self, filename: str) -> str:
        """Get full absolute path for an input file.

        Args:
            filename (str): Name of the input file

        Returns:
            str: Absolute path to the input file
        """
        return os.path.join(self.input_dir, filename)

    def get_output_path(self, filename: str) -> str:
        """Get full absolute path for an output file.

        Appends .json extension to the filename for analysis results.

        Args:
            filename (str): Base name for the output file (without extension)

        Returns:
            str: Absolute path to the output file with .json extension
        """
        return os.path.join(self.output_dir, filename + ".json")

    def ensure_output_dir_exists(self) -> None:
        """Ensure output directory exists, creating it if necessary.

        Creates the output directory and any necessary parent directories
        if they don't exist.

        Raises:
            FileError: If directory creation fails or if there are
                      permission issues
        """
        try:
            os.makedirs(self.output_dir, exist_ok=True)

            # Verify write permissions
            if not os.access(self.output_dir, os.W_OK):
                raise FileError(
                    "No write permission for output directory",
                    {"path": self.output_dir}
                )
        except OSError as e:
            raise FileError(
                f"Failed to create output directory: {e}",
                {
                    "path": self.output_dir,
                    "error": str(e),
                    "error_code": e.errno
                }
            )
