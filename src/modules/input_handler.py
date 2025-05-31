from typing import List, Optional


class InputHandler:
    """Handles user input operations"""

    @staticmethod
    def display_file_options(files: List[str]) -> None:
        """Display available files to user"""
        print("\nAvailable text files:")
        for idx, file in enumerate(files, 1):
            print(f"{idx}. {file}")

    def get_file_choice(self, files: List[str]) -> Optional[str]:
        """Get user's file choice"""
        while True:
            self.display_file_options(files)
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

    @staticmethod
    def get_n_value() -> int:
        """Get N value from user"""
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

    @staticmethod
    def continue_analysis() -> bool:
        """Ask if user wants to continue"""
        print("\nWould you like to analyze another file? (y/n)")
        return input().lower() == 'y'
