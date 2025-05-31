import os


class PathManager:
    """Handles all path-related operations"""

    @staticmethod
    def get_project_root() -> str:
        """Get the project root directory"""
        current_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        return os.path.dirname(current_dir)

    def __init__(self):
        self.project_root = self.get_project_root()
        self.input_dir = os.path.join(self.project_root, "src", "text-files")
        self.output_dir = os.path.join(self.project_root, "src", "text-analyzed")

    def get_input_path(self, filename: str) -> str:
        """Get full input file path"""
        return os.path.join(self.input_dir, filename)

    def get_output_path(self, filename: str) -> str:
        """Get full output file path"""
        return os.path.join(self.output_dir, filename + ".json")

    def ensure_output_dir_exists(self) -> None:
        """Ensure output directory exists"""
        os.makedirs(self.output_dir, exist_ok=True)
