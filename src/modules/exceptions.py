class TextAnalyzerError(Exception):
    """Base exception for text analyzer"""
    def __init__(self, message: str, details: dict = None):
        super().__init__(message)
        self.details = details or {}

class ValidationError(TextAnalyzerError):
    """Raised when input validation fails"""
    pass

class FileError(TextAnalyzerError):
    """Raised when file operations fail"""
    pass

class AnalysisError(TextAnalyzerError):
    """Raised when text analysis operations fail"""
    pass

class ConfigError(TextAnalyzerError):
    """Raised when configuration errors occur"""
    pass
