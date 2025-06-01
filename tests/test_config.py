# tests/test_config.py
import pytest
import os
from pathlib import Path
from src.config.config import (
    BaseConfig,
    DevelopmentConfig,
    ProductionConfig,
    TestingConfig,
    ConfigFactory
)

# Base Config Tests
def test_base_config_initialization():
    settings = BaseConfig.get_settings()
    assert isinstance(settings.SRC_DIR, Path)
    assert isinstance(settings.PROJECT_ROOT, Path)
    assert settings.SUPPORTED_ENCODINGS == ('utf-8', 'cp1251')
    assert settings.SUPPORTED_FILE_TYPES == ('.txt',)
    assert settings.MAX_FILE_SIZE == 1024 * 1024 * 10

def test_base_config_error_messages():
    settings = BaseConfig.get_settings()
    assert 'file_not_found' in settings.ERROR_MESSAGES
    assert 'invalid_file' in settings.ERROR_MESSAGES
    assert 'decode_error' in settings.ERROR_MESSAGES
    assert 'dir_access_error' in settings.ERROR_MESSAGES
    assert 'file_size_error' in settings.ERROR_MESSAGES

# Environment-specific Config Tests
def test_development_config():
    settings = DevelopmentConfig.get_settings()
    assert settings.DEBUG is True
    assert settings.LOGGING_LEVEL == 'DEBUG'
    assert settings.LOGGING_FORMAT == '%(asctime)s - %(name)s - %(levelname)s - %(message)s'

def test_production_config():
    settings = ProductionConfig.get_settings()
    assert settings.DEBUG is False
    assert settings.LOGGING_LEVEL == 'INFO'
    assert settings.LOGGING_FORMAT == '%(asctime)s - %(levelname)s - %(message)s'

def test_testing_config():
    settings = TestingConfig.get_settings()
    assert settings.DEBUG is True
    assert settings.TESTING is True
    assert settings.LOGGING_LEVEL == 'DEBUG'

# ConfigFactory Tests
@pytest.fixture
def reset_env():
    """Reset environment and config between tests."""
    # Store original environment
    original_env = os.environ.copy()

    # Reset config
    ConfigFactory.reset_config()

    yield

    # Restore original environment
    os.environ.clear()
    os.environ.update(original_env)

    # Reset config again
    ConfigFactory.reset_config()

def test_config_factory_development(reset_env):
    os.environ['ENV'] = 'development'
    config = ConfigFactory.get_config()
    assert isinstance(config, DevelopmentConfig.Settings)
    assert config.DEBUG is True
    assert config.LOGGING_LEVEL == 'DEBUG'

def test_config_factory_production(reset_env):
    """Test production configuration creation."""
    os.environ['ENV'] = 'production'
    ConfigFactory.reset_config()  # Ensure clean state
    config = ConfigFactory.get_config()
    assert isinstance(config, ProductionConfig.Settings)
    assert config.DEBUG is False
    assert config.LOGGING_LEVEL == 'INFO'

def test_config_factory_testing(reset_env):
    """Test testing configuration creation."""
    os.environ['ENV'] = 'testing'
    ConfigFactory.reset_config()  # Ensure clean state
    config = ConfigFactory.get_config()
    assert isinstance(config, TestingConfig.Settings)
    assert config.TESTING is True

def test_config_factory_default(reset_env):
    """Test default configuration creation."""
    if 'ENV' in os.environ:
        del os.environ['ENV']
    ConfigFactory.reset_config()  # Ensure clean state
    config = ConfigFactory.get_config()
    assert isinstance(config, DevelopmentConfig.Settings)

def test_config_factory_invalid_env(reset_env):
    """Test invalid environment handling."""
    os.environ['ENV'] = 'invalid_environment'
    ConfigFactory.reset_config()  # Ensure clean state
    config = ConfigFactory.get_config()
    assert isinstance(config, DevelopmentConfig.Settings)

def test_config_factory_caching(reset_env):
    os.environ['ENV'] = 'development'
    config1 = ConfigFactory.get_config()
    config2 = ConfigFactory.get_config()
    assert config1 is config2  # Test LRU cache is working
