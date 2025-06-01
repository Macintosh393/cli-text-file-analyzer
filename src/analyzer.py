from modules.path_manager import PathManager
from modules.file_handler import FileHandler
from modules.validators import FileValidator
from modules.input_handler import InputHandler
from modules.text_analyzer import TextAnalyzer
from modules.output_formatter import OutputFormatter
from modules.exceptions import TextAnalyzerError


class TextFileAnalyzer:
    """Main class that orchestrates the text file analysis process.

    Coordinates between different components to:
    - List available text files
    - Handle user input
    - Process file content
    - Analyze text
    - Format and save results

    Attributes:
        path_manager (PathManager): Manages file paths and directories
        validator (FileValidator): Validates file operations
        file_handler (FileHandler): Handles file reading and writing
        input_handler (InputHandler): Manages user input operations
    """

    def __init__(self) -> None:
        """Initialize TextFileAnalyzer with required components."""
        self.path_manager = PathManager()
        self.validator = FileValidator()
        self.file_handler = FileHandler(validator=self.validator)
        self.input_handler = InputHandler()

    def run(self) -> None:
        """Run the text file analysis process.

        Main application loop that:
        1. Displays available text files
        2. Gets user input for file selection
        3. Gets N value for analysis
        4. Reads and analyzes text content
        5. Formats and saves results
        6. Handles errors and user continuation choice

        The process continues until the user chooses to quit or
        no valid files are found.

        Raises:
            TextAnalyzerError: For expected errors during analysis
            Exception: For unexpected errors during execution
        """
        print("Text File Analyzer")
        print("=================")
        print("This tool analyzes text files and generates statistics.")
        print("The results will be saved as a JSON file.")

        while True:
            try:
                # Get available files
                available_files = self.file_handler.get_available_files(
                    self.path_manager.input_dir
                )

                if not available_files:
                    print(f"No .txt files found in {self.path_manager.input_dir}")
                    return

                # Get user's file choice
                chosen_file = self.input_handler.get_file_choice(available_files)
                if chosen_file is None:
                    print("Goodbye!")
                    return

                n = self.input_handler.get_n_value()

                # Read and analyze text
                input_path = self.path_manager.get_input_path(chosen_file)
                text = self.file_handler.read_file(input_path)

                # Analyze text
                analyzer = TextAnalyzer(text, n)
                formatter = OutputFormatter(analyzer, n)
                results = formatter.format_results()

                # Save results
                self.path_manager.ensure_output_dir_exists()
                output_path = self.path_manager.get_output_path(chosen_file)
                self.file_handler.save_json(results, output_path)

                print(f"\nAnalysis complete! Results saved to: {output_path}")

            except TextAnalyzerError as e:
                print(f"\nError: {e}")
            except Exception as e:
                print(f"\nUnexpected error: {e}")

            if not self.input_handler.continue_analysis():
                print("Goodbye!")
                break


if __name__ == "__main__":
    analyzer = TextFileAnalyzer()
    analyzer.run()
