import os
from pathlib import Path
from dataclasses import dataclass, field
from typing import List, Dict, Type
from functools import lru_cache
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class BaseConfig:
    """Base configuration class"""
    @dataclass(frozen=True)
    class Settings:
        SRC_DIR: Path = Path(__file__).parent.parent
        PROJECT_ROOT: Path = SRC_DIR.parent
        SUPPORTED_ENCODINGS: tuple = ('utf-8', 'cp1251')
        SUPPORTED_FILE_TYPES: tuple = ('.txt',)
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
        return cls.Settings()


class DevelopmentConfig(BaseConfig):
    """Development configuration"""
    @dataclass(frozen=True)
    class Settings(BaseConfig.Settings):
        DEBUG: bool = True
        LOGGING_LEVEL: str = 'DEBUG'
        LOGGING_FORMAT: str = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

class ProductionConfig(BaseConfig):
    """Production configuration"""
    @dataclass(frozen=True)
    class Settings(BaseConfig.Settings):
        DEBUG: bool = False
        LOGGING_LEVEL: str = 'INFO'
        LOGGING_FORMAT: str = '%(asctime)s - %(levelname)s - %(message)s'

class TestingConfig(BaseConfig):
    """Testing configuration"""
    @dataclass(frozen=True)
    class Settings(BaseConfig.Settings):
        DEBUG: bool = True
        TESTING: bool = True
        LOGGING_LEVEL: str = 'DEBUG'

class ConfigFactory:
    """Configuration factory with environment mapping"""
    _configs = {
        'development': DevelopmentConfig,
        'production': ProductionConfig,
        'testing': TestingConfig,
    }

    @classmethod
    @lru_cache
    def get_config(cls) -> Type[BaseConfig.Settings]:
        """Get configuration based on environment"""
        env = os.getenv('ENV', 'development').lower()
        config_class = cls._configs.get(env, DevelopmentConfig)
        return config_class.get_settings()
