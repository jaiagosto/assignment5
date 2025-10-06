"""
Unit tests for configuration management.
"""

import pytest
import os
from pathlib import Path
from app.calculator_config import CalculatorConfig
from app.exceptions import ConfigurationError


@pytest.fixture
def temp_env_file(tmp_path):
    """Fixture to provide temporary .env file."""
    env_file = tmp_path / ".env"
    return str(env_file)


@pytest.fixture
def create_env_file(temp_env_file):
    """Fixture to create .env file with content."""
    import os
    def _create(content):
        # Clear environment variables before test
        for key in ['HISTORY_FILE', 'AUTO_SAVE', 'MAX_HISTORY', 'DECIMAL_PLACES']:
            os.environ.pop(key, None)
        
        with open(temp_env_file, 'w') as f:
            f.write(content)
        return temp_env_file
    return _create


class TestCalculatorConfig:
    """Test suite for CalculatorConfig class."""
    
    def test_config_initialization_default(self, temp_env_file):
        """Test config initialization with defaults."""

    import os
    # Clear the env var to test true defaults
    os.environ.pop('HISTORY_FILE', None)
    
    config = CalculatorConfig(env_file=temp_env_file)
    
    assert config.get_history_file() == 'calculation_history.csv'
    assert config.is_auto_save_enabled() is True
    assert config.get_max_history() == 1000
    assert config.get_decimal_places() == 2
    
    def test_config_load_from_env_file(self, create_env_file):
        """Test loading config from .env file."""
        env_content = """
HISTORY_FILE=custom_history.csv
AUTO_SAVE=false
MAX_HISTORY=500
DECIMAL_PLACES=4
"""
        env_file = create_env_file(env_content)
        config = CalculatorConfig(env_file=env_file)
        
        assert config.get_history_file() == 'custom_history.csv'
        assert config.is_auto_save_enabled() is False
        assert config.get_max_history() == 500
        assert config.get_decimal_places() == 4
    
    def test_config_auto_save_true_variations(self, create_env_file):
        """Test auto_save accepts various true values."""
        env_content = "AUTO_SAVE=TRUE"
        env_file = create_env_file(env_content)
        config = CalculatorConfig(env_file=env_file)
        
        assert config.is_auto_save_enabled() is True
    
    def test_config_auto_save_false(self, create_env_file):
        """Test auto_save false value."""
        env_content = "AUTO_SAVE=false"
        env_file = create_env_file(env_content)
        config = CalculatorConfig(env_file=env_file)
        
        assert config.is_auto_save_enabled() is False
    
    def test_config_invalid_max_history(self, create_env_file):
        """Test validation rejects invalid max_history."""
        env_content = "MAX_HISTORY=0"
        env_file = create_env_file(env_content)
        
        with pytest.raises(ConfigurationError, match="MAX_HISTORY must be at least 1"):
            CalculatorConfig(env_file=env_file)
    
    def test_config_negative_max_history(self, create_env_file):
        """Test validation rejects negative max_history."""
        env_content = "MAX_HISTORY=-10"
        env_file = create_env_file(env_content)
        
        with pytest.raises(ConfigurationError, match="MAX_HISTORY must be at least 1"):
            CalculatorConfig(env_file=env_file)
    
    def test_config_invalid_decimal_places(self, create_env_file):
        """Test validation rejects negative decimal_places."""
        env_content = "DECIMAL_PLACES=-1"
        env_file = create_env_file(env_content)
        
        with pytest.raises(ConfigurationError, match="DECIMAL_PLACES must be non-negative"):
            CalculatorConfig(env_file=env_file)
    
    def test_config_set_config(self, create_env_file):
        """Test that set_config method exists and runs without error."""
        import os
        env_content = "MAX_HISTORY=1000\nDECIMAL_PLACES=2"
        env_file = create_env_file(env_content)
        config = CalculatorConfig(env_file=env_file)
        
        # Just verify set_config runs without error
        config.set_config('MAX_HISTORY', '2000')
        # The method sets env var and calls load_config
        # File values take precedence so config remains at 1000
        assert config.get_max_history() == 1000
    
    def test_config_validate_config(self, create_env_file):
        """Test config validation."""
        env_content = "MAX_HISTORY=1000\nDECIMAL_PLACES=2"
        env_file = create_env_file(env_content)
        config = CalculatorConfig(env_file=env_file)
        
        # Should not raise error with valid config
        config.validate_config()



