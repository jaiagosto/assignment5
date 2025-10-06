"""
Unit tests for input validation.
"""

import pytest
from app.input_validators import InputValidator
from app.exceptions import InvalidInputError


class TestInputValidator:
    """Test suite for InputValidator class."""
    
    def test_validate_operation_input_valid(self):
        """Test validation of valid operation input."""
        validator = InputValidator()
        operation, num1, num2 = validator.validate_operation_input("add 5 3")
        
        assert operation == "add"
        assert num1 == 5.0
        assert num2 == 3.0
    
    def test_validate_operation_input_with_floats(self):
        """Test validation with float numbers."""
        validator = InputValidator()
        operation, num1, num2 = validator.validate_operation_input("multiply 2.5 3.7")
        
        assert operation == "multiply"
        assert num1 == 2.5
        assert num2 == 3.7
    
    def test_validate_operation_input_with_negatives(self):
        """Test validation with negative numbers."""
        validator = InputValidator()
        operation, num1, num2 = validator.validate_operation_input("subtract -5 -3")
        
        assert operation == "subtract"
        assert num1 == -5.0
        assert num2 == -3.0
    
    def test_validate_operation_input_empty(self):
        """Test validation rejects empty input."""
        validator = InputValidator()
        
        with pytest.raises(InvalidInputError, match="Input cannot be empty"):
            validator.validate_operation_input("")
    
    def test_validate_operation_input_whitespace_only(self):
        """Test validation rejects whitespace-only input."""
        validator = InputValidator()
        
        with pytest.raises(InvalidInputError, match="Input cannot be empty"):
            validator.validate_operation_input("   ")
    
    def test_validate_operation_input_too_few_parts(self):
        """Test validation rejects input with too few parts."""
        validator = InputValidator()
        
        with pytest.raises(InvalidInputError, match="Invalid input format"):
            validator.validate_operation_input("add 5")
    
    def test_validate_operation_input_too_many_parts(self):
        """Test validation rejects input with too many parts."""
        validator = InputValidator()
        
        with pytest.raises(InvalidInputError, match="Invalid input format"):
            validator.validate_operation_input("add 5 3 2")
    
    def test_validate_operation_input_invalid_numbers(self):
        """Test validation rejects non-numeric operands."""
        validator = InputValidator()
        
        with pytest.raises(InvalidInputError, match="Invalid numbers"):
            validator.validate_operation_input("add five three")
    
    def test_validate_operation_input_one_invalid_number(self):
        """Test validation rejects when one operand is non-numeric."""
        validator = InputValidator()
        
        with pytest.raises(InvalidInputError, match="Invalid numbers"):
            validator.validate_operation_input("add 5 three")
    
    def test_validate_command_valid(self):
        """Test validation of valid commands."""
        validator = InputValidator()
        
        assert validator.validate_command("help") == "help"
        assert validator.validate_command("HELP") == "help"
        assert validator.validate_command("  help  ") == "help"
    
    def test_validate_command_empty(self):
        """Test validation of empty command."""
        validator = InputValidator()
        
        assert validator.validate_command("") == ""
        assert validator.validate_command("   ") == ""
    
    def test_validate_command_case_insensitive(self):
        """Test command validation is case insensitive."""
        validator = InputValidator()
        
        assert validator.validate_command("EXIT") == "exit"
        assert validator.validate_command("History") == "history"
        assert validator.validate_command("CLEAR") == "clear"