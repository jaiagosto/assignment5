"""
Custom exceptions for the calculator application.
"""


class CalculatorError(Exception):
    """Base exception for calculator errors."""
    pass


class InvalidOperationError(CalculatorError):
    """Raised when an invalid operation is requested."""
    pass


class DivisionByZeroError(CalculatorError):
    """Raised when attempting to divide by zero."""
    pass


class InvalidInputError(CalculatorError):
    """Raised when user input is invalid."""
    pass


class ConfigurationError(CalculatorError):
    """Raised when there's a configuration error."""
    pass


class HistoryError(CalculatorError):
    """Raised when there's an error with history operations."""
    pass



