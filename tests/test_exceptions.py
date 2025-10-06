"""
Unit tests for custom exceptions.
"""

import pytest
from app.exceptions import (
    CalculatorError,
    InvalidOperationError,
    DivisionByZeroError,
    InvalidInputError,
    ConfigurationError,
    HistoryError
)


class TestCustomExceptions:
    """Test suite for custom exception classes."""
    
    def test_calculator_error(self):
        """Test base CalculatorError."""
        with pytest.raises(CalculatorError):
            raise CalculatorError("Test error")
    
    def test_invalid_operation_error(self):
        """Test InvalidOperationError."""
        with pytest.raises(InvalidOperationError):
            raise InvalidOperationError("Invalid operation")
    
    def test_division_by_zero_error(self):
        """Test DivisionByZeroError."""
        with pytest.raises(DivisionByZeroError):
            raise DivisionByZeroError("Cannot divide by zero")
    
    def test_invalid_input_error(self):
        """Test InvalidInputError."""
        with pytest.raises(InvalidInputError):
            raise InvalidInputError("Invalid input")
    
    def test_configuration_error(self):
        """Test ConfigurationError."""
        with pytest.raises(ConfigurationError):
            raise ConfigurationError("Configuration error")
    
    def test_history_error(self):
        """Test HistoryError."""
        with pytest.raises(HistoryError):
            raise HistoryError("History error")
    
    def test_exception_inheritance(self):
        """Test that all custom exceptions inherit from CalculatorError."""
        assert issubclass(InvalidOperationError, CalculatorError)
        assert issubclass(DivisionByZeroError, CalculatorError)
        assert issubclass(InvalidInputError, CalculatorError)
        assert issubclass(ConfigurationError, CalculatorError)
        assert issubclass(HistoryError, CalculatorError)