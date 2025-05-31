from modules.path_manager import PathManager
from modules.file_handler import FileHandler
from modules.input_handler import InputHandler
from modules.text_analyzer import TextAnalyzer
from modules.output_formatter import OutputFormatter


class TextFileAnalyzer:
    """Main class that orchestrates the text file analysis"""

    def __init__(self):
        self.path_manager = PathManager()
        self.file_handler = FileHandler()
        self.input_handler = InputHandler()

    def run(self) -> None:
        """Run the text file analysis process"""
        print("Text File Analyzer")
        print("=================")
        print("This tool analyzes text files and generates statistics.")
        print("The results will be saved as a JSON file.")

        while True:
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

            try:
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

            except Exception as e:
                print(f"An error occurred: {str(e)}")

            if not self.input_handler.continue_analysis():
                print("Goodbye!")
                break


if __name__ == "__main__":
    analyzer = TextFileAnalyzer()
    analyzer.run()
