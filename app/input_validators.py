"""
Input validation utilities for the calculator application.
"""

from typing import Tuple
from app.exceptions import InvalidInputError


class InputValidator:
    """Validates user input for the calculator."""
    
    @staticmethod
    def validate_operation_input(user_input: str) -> Tuple[str, float, float]:
        """
        Validate and parse operation input.
        
        Args:
            user_input: Raw user input string
            
        Returns:
            Tuple of (operation_name, operand1, operand2)
            
        Raises:
            InvalidInputError: If input format is invalid
        """
        # LBYL: Check if input is empty
        if not user_input or not user_input.strip():
            raise InvalidInputError("Input cannot be empty.")
        
        parts = user_input.strip().split()
        
        # LBYL: Check if we have exactly 3 parts
        if len(parts) != 3:
            raise InvalidInputError(
                "Invalid input format. Expected: <operation> <num1> <num2>"
            )
        
        operation, num1_str, num2_str = parts
        
        # EAFP: Try to convert to floats
        try:
            num1 = float(num1_str)
            num2 = float(num2_str)
        except ValueError:
            raise InvalidInputError(
                f"Invalid numbers: '{num1_str}' and '{num2_str}' must be valid numbers."
            )
        
        return operation, num1, num2
    
    @staticmethod
    def validate_command(user_input: str) -> str:
        """
        Validate and return command.
        
        Args:
            user_input: Raw user input string
            
        Returns:
            Lowercase command string
        """
        if not user_input or not user_input.strip():
            return ""
        
        return user_input.strip().lower()