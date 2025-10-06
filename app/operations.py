"""
Operations module implementing the Strategy Pattern for arithmetic operations.
"""

from abc import ABC, abstractmethod
import math
from app.exceptions import DivisionByZeroError


class OperationStrategy(ABC):
    """Abstract base class for operation strategies."""
    
    @abstractmethod
    def execute(self, a: float, b: float) -> float:
        """Execute the operation on two operands."""
        pass  # pragma: no cover


class AdditionStrategy(OperationStrategy):
    """Strategy for addition operation."""
    
    def execute(self, a: float, b: float) -> float:
        """Add two numbers."""
        return a + b


class SubtractionStrategy(OperationStrategy):
    """Strategy for subtraction operation."""
    
    def execute(self, a: float, b: float) -> float:
        """Subtract b from a."""
        return a - b


class MultiplicationStrategy(OperationStrategy):
    """Strategy for multiplication operation."""
    
    def execute(self, a: float, b: float) -> float:
        """Multiply two numbers."""
        return a * b


class DivisionStrategy(OperationStrategy):
    """Strategy for division operation."""
    
    def execute(self, a: float, b: float) -> float:
        """Divide a by b."""
        if b == 0:
            raise DivisionByZeroError("Cannot divide by zero.")
        return a / b


class PowerStrategy(OperationStrategy):
    """Strategy for power operation."""
    
    def execute(self, a: float, b: float) -> float:
        """Raise a to the power of b."""
        return a ** b


class RootStrategy(OperationStrategy):
    """Strategy for root operation."""
    
    def execute(self, a: float, b: float) -> float:
        """Calculate the b-th root of a."""
        if b == 0:
            raise DivisionByZeroError("Cannot calculate 0th root.")
        return a ** (1 / b)


class ModulusStrategy(OperationStrategy):
    """Strategy for modulus operation."""
    
    def execute(self, a: float, b: float) -> float:
        """Calculate a modulo b."""
        if b == 0:
            raise DivisionByZeroError("Cannot perform modulus by zero.")
        return a % b


class OperationFactory:
    """Factory for creating operation strategies."""
    
    _strategies = {
        'add': AdditionStrategy,
        'subtract': SubtractionStrategy,
        'multiply': MultiplicationStrategy,
        'divide': DivisionStrategy,
        'power': PowerStrategy,
        'root': RootStrategy,
        'modulus': ModulusStrategy
    }
    
    @classmethod
    def create_operation(cls, operation_name: str) -> OperationStrategy:
        """
        Create and return an operation strategy based on the operation name.
        
        Args:
            operation_name: Name of the operation
            
        Returns:
            OperationStrategy instance
            
        Raises:
            InvalidOperationError: If operation is not supported
        """
        from app.exceptions import InvalidOperationError
        
        strategy_class = cls._strategies.get(operation_name.lower())
        if not strategy_class:
            available = ', '.join(cls._strategies.keys())
            raise InvalidOperationError(
                f"Unsupported operation: '{operation_name}'. Available: {available}"
            )
        return strategy_class()
    
    @classmethod
    def get_available_operations(cls) -> list:
        """Return list of available operation names."""
        return list(cls._strategies.keys())