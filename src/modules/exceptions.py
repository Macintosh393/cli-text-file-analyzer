class TextAnalyzerError(Exception):
    """Base exception for text analyzer"""
    pass

class ValidationError(TextAnalyzerError):
    """Raised when input validation fails"""
    pass

class FileError(TextAnalyzerError):
    """Raised when file operations fail"""
    pass

class ValidationError(Exception):
    """Raised when file validation fails"""
    pass

class FileError(Exception):
    """Raised when file operations fail"""
    pass