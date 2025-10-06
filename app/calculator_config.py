"""
Configuration management for the calculator application.
"""

import os
from pathlib import Path
from typing import Optional
from dotenv import load_dotenv
from app.exceptions import ConfigurationError


class CalculatorConfig:
    """Manages calculator application configuration."""
    
    def __init__(self, env_file: str = ".env"):
        """
        Initialize configuration.
        
        Args:
            env_file: Path to .env file
        """
        self.env_file = env_file
        self.load_config()
    
    def load_config(self) -> None:
        """
        Load configuration from environment variables.
        
        Raises:
            ConfigurationError: If configuration is invalid
        """
        # Load .env file if it exists
        if Path(self.env_file).exists():
            load_dotenv(self.env_file, override=True)
        
        # Load configuration with defaults
        self.history_file = os.getenv('HISTORY_FILE', 'calculation_history.csv')
        self.auto_save = os.getenv('AUTO_SAVE', 'true').lower() in ['true', '1', 'yes']
        
        try:
            self.max_history = int(os.getenv('MAX_HISTORY', '1000'))
            self.decimal_places = int(os.getenv('DECIMAL_PLACES', '2'))
        except ValueError as e: # pragma: no cover
            raise ConfigurationError(f"Invalid configuration value: {e}")
        
        # Validate configuration
        self.validate_config()
    
    def validate_config(self) -> None:
        """
        Validate configuration settings.
        
        Raises:
            ConfigurationError: If configuration is invalid
        """
        if self.max_history < 1:
            raise ConfigurationError("MAX_HISTORY must be at least 1")
        
        if self.decimal_places < 0:
            raise ConfigurationError("DECIMAL_PLACES must be non-negative")
        
        if not self.history_file: # pragma: no cover
            raise ConfigurationError("HISTORY_FILE cannot be empty")
    
    def get_history_file(self) -> str:
        """Get history file path."""
        return self.history_file
    
    def is_auto_save_enabled(self) -> bool:
        """Check if auto-save is enabled."""
        return self.auto_save
    
    def get_max_history(self) -> int:
        """Get maximum history size."""
        return self.max_history
    
    def get_decimal_places(self) -> int:
        """Get decimal places for formatting."""
        return self.decimal_places
    
    def set_config(self, key: str, value: str) -> None:
        """
        Set a configuration value.
        
        Args:
            key: Configuration key
            value: Configuration value
        """
        os.environ[key] = value
        self.load_config()