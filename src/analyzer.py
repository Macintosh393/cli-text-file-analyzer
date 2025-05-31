import os
import json
import re
from collections import Counter


def get_project_root() -> str:
    """Get the project root directory"""
    # Assuming analyzer.py is in the src directory
    current_dir = os.path.dirname(os.path.abspath(__file__))
    return os.path.dirname(current_dir)


def get_available_files(directory: str = None) -> list:
    """Get list of available .txt files in the directory"""
    if directory is None:
        # Construct path relative to project root
        project_root = get_project_root()
        directory = os.path.join(project_root, "src", "text-files")

    try:
        files = [f for f in os.listdir(directory) if f.endswith('.txt')]
        return sorted(files)
    except Exception as e:
        print(f"Error accessing directory: {e}")
        print(f"Tried to access: {directory}")
        return []


def display_file_options(files: list) -> None:
    """Display available files to the user"""
    print("\nAvailable text files:")
    for idx, file in enumerate(files, 1):
        print(f"{idx}. {file}")


def get_file_choice(files: list) -> str:
    """Get user's file choice"""
    while True:
        display_file_options(files)
        print("\nEnter the number of the file to analyze (or 'q' to quit):")
        choice = input().strip()

        if choice.lower() == 'q':
            return None

        try:
            idx = int(choice) - 1
            if 0 <= idx < len(files):
                return files[idx]
            else:
                print("Invalid file number. Please try again.")
        except ValueError:
            print("Please enter a valid number.")


def get_valid_n():
    """
    Prompts user for N value and validates it.
    Returns:
        int: Valid N value between 1 and 100
    """
    while True:
        try:
            print("\nEnter N for the number of most frequent words to analyze (1-100):")
            n = int(input().strip())
            if n <= 0:
                print("Please enter a positive number.")
                continue
            if n > 100:
                print("Please enter a number less than or equal to 100.")
                continue
            return n
        except ValueError:
            print("Please enter a valid number.")


def get_text_file(path: str) -> str:
    """
    Reads and returns the contents of a text file.
    Args:
        path (str): Path to the text file
    Returns:
        str: Contents of the text file
    """
    with open(path, 'r') as f:
        return f.read()


def analyze_text_file():
    """
    Main function that handles text file analysis process.

    The function performs the following operations:
    1. Gets and validates file path from user
    2. Gets and validates N value for word frequency analysis
    3. Reads and analyzes text file contents
    4. Calculates various text statistics:
        - Total symbols (with and without spaces)
        - Number of sentences
        - Word count
        - N most frequent words
        - Average word length (rounded to 2 decimal places)
        - Symbol frequency (in descending order)
    5. Saves results to a JSON file
    6. Offers option to analyze another file

    The analysis results are saved in a JSON file with the following structure:
    {
        "total_symbols": {
            "with_spaces": int,
            "without_spaces": int
        },
        "sentence-count": int,
        "word-count": int,
        "N-most-frequent-words": dict[str, int],
        "average-word-length": float,
        "symbols-frequency": dict[str, int]
    }
    """
    project_root = get_project_root()
    base_input_dir = os.path.join(project_root, "src", "text-files")
    base_output_dir = os.path.join(project_root, "src", "text-analyzed")

    while True:
        # Get available files
        available_files = get_available_files(base_input_dir)

        if not available_files:
            print(f"No .txt files found in {base_input_dir}")
            return

        # Get user's file choice
        chosen_file = get_file_choice(available_files)
        if chosen_file is None:
            print("Goodbye!")
            return

        # Construct full file path
        input_path = os.path.join(base_input_dir, chosen_file)

        n = get_valid_n()

        try:
            # Read the text file
            text = get_text_file(input_path)

            # Calculate total symbols with and without spaces
            total_symbols_with_spaces = len(text)
            total_symbols_without_spaces = len(text.replace(" ", ""))

            # Count sentences
            sentences = [s.strip() for s in re.split('[.!?]', text) if s.strip()]
            sentence_count = len(sentences)

            # Get words and calculate frequencies
            words = re.findall(r'\b\w+\b', text.lower())
            word_count = len(words)
            word_freq = Counter(words)
            most_frequent_words = dict(word_freq.most_common(n))

            # Calculate average word length (rounded to 2 decimal places)
            average_word_length = round(sum(len(word) for word in words) / len(words) if words else 0, 2)

            # Calculate symbol frequency (in descending order)
            symbol_frequency = dict(sorted(
                Counter(text).items(),
                key=lambda x: (-x[1], x[0])  # Sort by frequency desc, then by character asc
            ))

            # Prepare output data structure
            output_data = {
                "total_symbols": {
                    "with_spaces": total_symbols_with_spaces,
                    "without_spaces": total_symbols_without_spaces
                },
                "sentence-count": sentence_count,
                "word-count": word_count,
                f"{n}-most-frequent-words": most_frequent_words,
                "average-word-length": average_word_length,
                "symbols-frequency": symbol_frequency
            }

            # Ensure output directory exists and create output path
            output_path = os.path.join(base_output_dir, chosen_file + ".json")
            os.makedirs(os.path.dirname(output_path), exist_ok=True)

            # Save results to JSON file
            with open(output_path, 'w') as f:
                json.dump(output_data, f, indent=4)

            print(f"\nAnalysis complete! Results saved to: {output_path}")

        except Exception as e:
            print(f"An error occurred: {str(e)}")

        # Ask user if they want to analyze another file
        print("\nWould you like to analyze another file? (y/n)")
        if input().lower() != 'y':
            print("Goodbye!")
            break


if __name__ == "__main__":
    print("Text File Analyzer")
    print("=================")
    print("This tool analyzes text files and generates statistics.")
    print("The results will be saved as a JSON file.")
    analyze_text_file()
