import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Type, Mapping
from functools import lru_cache
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class BaseConfig:
    """Base configuration class providing core settings.

    Defines the base configuration structure with common settings including
    directory paths, supported file types, and error messages.
    """

    @dataclass(frozen=True)
    class Settings:
        """Core settings dataclass with default configuration values.

        Attributes:
            SRC_DIR (Path): Source directory path
            PROJECT_ROOT (Path): Project root directory path
            SUPPORTED_ENCODINGS (tuple): Supported file encodings
            SUPPORTED_FILE_TYPES (tuple): Supported file extensions
            MAX_FILE_SIZE (int): Maximum allowed file size in bytes
            ERROR_MESSAGES (Dict[str, str]): Dictionary of error message templates
        """
        SRC_DIR: Path = Path(__file__).parent.parent
        PROJECT_ROOT: Path = SRC_DIR.parent
        SUPPORTED_ENCODINGS: tuple[str, ...] = ('utf-8', 'cp1251')
        SUPPORTED_FILE_TYPES: tuple[str, ...] = ('.txt',)
        MAX_FILE_SIZE: int = 1024 * 1024 * 10  # 10MB
        ERROR_MESSAGES: Dict[str, str] = field(default_factory=lambda: {
            'file_not_found': 'File not found: {}',
            'invalid_file': 'Invalid file: {}',
            'decode_error': 'Could not decode file {} with supported encodings',
            'dir_access_error': 'Error accessing directory: {}',
            'file_size_error': 'File size exceeds maximum allowed size: {}'
        })

    @classmethod
    def get_settings(cls) -> Settings:
        """Get configuration settings instance.

        Returns:
            Settings: Instance of configuration settings
        """
        return cls.Settings()


class DevelopmentConfig(BaseConfig):
    """Development configuration with debug settings enabled."""

    @dataclass(frozen=True)
    class Settings(BaseConfig.Settings):
        """Development environment settings.

        Attributes:
            DEBUG (bool): Debug mode flag
            LOGGING_LEVEL (str): Logging level for development
            LOGGING_FORMAT (str): Detailed logging format for development
        """
        DEBUG: bool = True
        LOGGING_LEVEL: str = 'DEBUG'
        LOGGING_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'


class ProductionConfig(BaseConfig):
    """Production configuration with secure settings."""

    @dataclass(frozen=True)
    class Settings(BaseConfig.Settings):
        """Production environment settings.

        Attributes:
            DEBUG (bool): Debug mode flag (disabled for production)
            LOGGING_LEVEL (str): Logging level for production
            LOGGING_FORMAT (str): Simplified logging format for production
        """
        DEBUG: bool = False
        LOGGING_LEVEL: str = 'INFO'
        LOGGING_FORMAT: str = '%(asctime)s - %(levelname)s - %(message)s'


class TestingConfig(BaseConfig):
    """Testing configuration for test environment."""

    @dataclass(frozen=True)
    class Settings(BaseConfig.Settings):
        """Testing environment settings.

        Attributes:
            DEBUG (bool): Debug mode flag
            TESTING (bool): Testing mode flag
            LOGGING_LEVEL (str): Logging level for testing
        """
        DEBUG: bool = True
        TESTING: bool = True
        LOGGING_LEVEL: str = 'DEBUG'


# src/config/config.py

class ConfigFactory:
    """Factory class for creating configuration objects based on environment."""

    _config = None  # Cache for singleton pattern

    @classmethod
    def get_config(cls):
        """Get configuration instance based on environment.

        Returns:
            Settings: Configuration instance for current environment
        """
        # Return cached config if exists
        if cls._config is not None:
            return cls._config

        # Get environment setting
        env = os.environ.get('ENV', 'development').lower()

        # Create appropriate config based on environment
        if env == 'production':
            cls._config = ProductionConfig.Settings()
        elif env == 'testing':
            cls._config = TestingConfig.Settings()
        else:
            # Default to development config
            cls._config = DevelopmentConfig.Settings()

        return cls._config

    @classmethod
    def reset_config(cls):
        """Reset the cached configuration instance."""
        cls._config = None
