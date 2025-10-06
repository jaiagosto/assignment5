"""
Unit tests for operations module with Strategy Pattern.
"""

import pytest
from app.operations import (
    OperationStrategy,
    AdditionStrategy,
    SubtractionStrategy,
    MultiplicationStrategy,
    DivisionStrategy,
    PowerStrategy,
    RootStrategy,
    ModulusStrategy,
    OperationFactory
)
from app.exceptions import InvalidOperationError, DivisionByZeroError


class TestOperationStrategies:
    """Test suite for operation strategy classes."""
    
    def test_addition_strategy(self):
        """Test addition strategy."""
        strategy = AdditionStrategy()
        assert strategy.execute(5, 3) == 8
        assert strategy.execute(-5, 3) == -2
        assert strategy.execute(0, 0) == 0
    
    def test_subtraction_strategy(self):
        """Test subtraction strategy."""
        strategy = SubtractionStrategy()
        assert strategy.execute(5, 3) == 2
        assert strategy.execute(-5, 3) == -8
        assert strategy.execute(0, 0) == 0
    
    def test_multiplication_strategy(self):
        """Test multiplication strategy."""
        strategy = MultiplicationStrategy()
        assert strategy.execute(5, 3) == 15
        assert strategy.execute(-5, 3) == -15
        assert strategy.execute(0, 5) == 0
    
    def test_division_strategy(self):
        """Test division strategy."""
        strategy = DivisionStrategy()
        assert strategy.execute(10, 2) == 5
        assert strategy.execute(-10, 2) == -5
        assert strategy.execute(0, 5) == 0
    
    def test_division_by_zero(self):
        """Test division by zero raises error."""
        strategy = DivisionStrategy()
        with pytest.raises(DivisionByZeroError, match="Cannot divide by zero"):
            strategy.execute(10, 0)
    
    def test_power_strategy(self):
        """Test power strategy."""
        strategy = PowerStrategy()
        assert strategy.execute(2, 3) == 8
        assert strategy.execute(5, 2) == 25
        assert strategy.execute(10, 0) == 1
    
    def test_root_strategy(self):
        """Test root strategy."""
        strategy = RootStrategy()
        assert strategy.execute(16, 2) == 4
        assert strategy.execute(27, 3) == 3
        assert strategy.execute(100, 2) == 10
    
    def test_root_by_zero(self):
        """Test root by zero raises error."""
        strategy = RootStrategy()
        with pytest.raises(DivisionByZeroError, match="Cannot calculate 0th root"):
            strategy.execute(10, 0)
    
    def test_modulus_strategy(self):
        """Test modulus strategy."""
        strategy = ModulusStrategy()
        assert strategy.execute(10, 3) == 1
        assert strategy.execute(20, 6) == 2
        assert strategy.execute(15, 4) == 3
    
    def test_modulus_by_zero(self):
        """Test modulus by zero raises error."""
        strategy = ModulusStrategy()
        with pytest.raises(DivisionByZeroError, match="Cannot perform modulus by zero"):
            strategy.execute(10, 0)


class TestOperationFactory:
    """Test suite for operation factory."""
    
    @pytest.mark.parametrize("operation_name,strategy_class", [
        ('add', AdditionStrategy),
        ('subtract', SubtractionStrategy),
        ('multiply', MultiplicationStrategy),
        ('divide', DivisionStrategy),
        ('power', PowerStrategy),
        ('root', RootStrategy),
        ('modulus', ModulusStrategy),
    ])
    def test_factory_creates_correct_strategy(self, operation_name, strategy_class):
        """Test factory creates correct strategy for each operation."""
        strategy = OperationFactory.create_operation(operation_name)
        assert isinstance(strategy, strategy_class)
    
    def test_factory_case_insensitive(self):
        """Test factory handles case-insensitive operation names."""
        strategy_lower = OperationFactory.create_operation('add')
        strategy_upper = OperationFactory.create_operation('ADD')
        strategy_mixed = OperationFactory.create_operation('AdD')
        
        assert isinstance(strategy_lower, AdditionStrategy)
        assert isinstance(strategy_upper, AdditionStrategy)
        assert isinstance(strategy_mixed, AdditionStrategy)
    
    def test_factory_invalid_operation(self):
        """Test factory raises error for invalid operation."""
        with pytest.raises(InvalidOperationError, match="Unsupported operation"):
            OperationFactory.create_operation('invalid')
    
    def test_get_available_operations(self):
        """Test getting list of available operations."""
        operations = OperationFactory.get_available_operations()
        assert 'add' in operations
        assert 'subtract' in operations
        assert 'multiply' in operations
        assert 'divide' in operations
        assert 'power' in operations
        assert 'root' in operations
        assert 'modulus' in operations
        assert len(operations) == 7