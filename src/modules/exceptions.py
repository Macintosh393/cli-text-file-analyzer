class TextAnalyzerError(Exception):
    """Base exception class for the text analyzer application.

    This serves as the parent class for all custom exceptions in the application.
    All other exceptions in the application should inherit from this class.
    """
    pass


class ValidationError(TextAnalyzerError):
    """Exception raised for validation errors.

    This exception is raised when input validation fails, such as:
    - Invalid file paths
    - Invalid user inputs
    - Invalid parameter values
    - Format validation failures
    """
    pass


class FileError(TextAnalyzerError):
    """Exception raised for file operation errors.

    This exception is raised when file operations fail, such as:
    - File not found
    - Permission denied
    - File read/write errors
    - Directory access errors
    """
    pass


class AnalysisError(TextAnalyzerError):
    """Exception raised for text analysis errors.

    This exception is raised when text analysis operations fail, such as:
    - Text processing errors
    - Calculation errors
    - Empty or invalid content
    """
    pass
