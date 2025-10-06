"""
Unit tests for calculator REPL with Facade Pattern.
"""

import pytest
from io import StringIO
import sys
from app.calculator_repl import Calculator
from app.exceptions import CalculatorError


@pytest.fixture
def calculator(tmp_path):
    """Fixture to provide calculator instance with temp files."""
    import os
    # Clear any existing environment variables that might interfere
    for key in ['HISTORY_FILE', 'AUTO_SAVE', 'MAX_HISTORY', 'DECIMAL_PLACES']:
        os.environ.pop(key, None)
    
    # Set test-specific environment
    os.environ['HISTORY_FILE'] = str(tmp_path / "test_history.csv")
    os.environ['MAX_HISTORY'] = '1000'
    os.environ['DECIMAL_PLACES'] = '2'
    
    calc = Calculator()
    calc.history.clear_history()  # Ensure clean history
    return calc

class TestCalculatorCommands:
    """Test suite for calculator commands."""
    
    def test_display_help(self, calculator, capsys):
        """Test help command displays help information."""
        calculator.display_help()
        captured = capsys.readouterr()
        
        assert "CALCULATOR HELP MENU" in captured.out
        assert "add" in captured.out
        assert "subtract" in captured.out
        assert "power" in captured.out
        assert "root" in captured.out
    
    def test_display_history_empty(self, calculator, capsys):
        """Test history command when empty."""
        calculator.display_history()
        captured = capsys.readouterr()
        
        assert "No calculations in history" in captured.out
    
    def test_display_history_with_calculations(self, calculator, capsys):
        """Test history command with calculations."""
        calculator.perform_calculation("add", 5, 3)
        calculator.display_history()
        captured = capsys.readouterr()
        
        assert "CALCULATION HISTORY" in captured.out
        assert "5" in captured.out
        assert "3" in captured.out
    
    def test_display_stats(self, calculator, capsys):
        """Test stats command."""
        calculator.perform_calculation("add", 5, 3)
        calculator.perform_calculation("multiply", 4, 2)
        calculator.display_stats()
        captured = capsys.readouterr()
        
        assert "HISTORY STATISTICS" in captured.out
        assert "Total calculations: 2" in captured.out


class TestCalculatorOperations:
    """Test suite for calculator operations."""
    
    def test_perform_addition(self, calculator, capsys):
        """Test addition operation."""
        calculator.perform_calculation("add", 10, 5)
        captured = capsys.readouterr()
        
        assert "Result: 15" in captured.out
    
    def test_perform_subtraction(self, calculator, capsys):
        """Test subtraction operation."""
        calculator.perform_calculation("subtract", 10, 3)
        captured = capsys.readouterr()
        
        assert "Result: 7" in captured.out
    
    def test_perform_multiplication(self, calculator, capsys):
        """Test multiplication operation."""
        calculator.perform_calculation("multiply", 6, 7)
        captured = capsys.readouterr()
        
        assert "Result: 42" in captured.out
    
    def test_perform_division(self, calculator, capsys):
        """Test division operation."""
        calculator.perform_calculation("divide", 20, 4)
        captured = capsys.readouterr()
        
        assert "Result: 5.0" in captured.out
    
    def test_perform_power(self, calculator, capsys):
        """Test power operation."""
        calculator.perform_calculation("power", 2, 3)
        captured = capsys.readouterr()
        
        assert "Result: 8" in captured.out
    
    def test_perform_root(self, calculator, capsys):
        """Test root operation."""
        calculator.perform_calculation("root", 16, 2)
        captured = capsys.readouterr()
        
        assert "Result: 4.0" in captured.out
    
    def test_perform_modulus(self, calculator, capsys):
        """Test modulus operation."""
        calculator.perform_calculation("modulus", 10, 3)
        captured = capsys.readouterr()
        
        assert "Result: 1" in captured.out


class TestCalculatorUndoRedo:
    """Test suite for undo/redo functionality."""
    
    def test_undo_calculation(self, calculator, capsys):
        """Test undo functionality."""
        calculator.perform_calculation("add", 5, 3)
        calculator.undo_last()
        captured = capsys.readouterr()
        
        assert "Last calculation undone" in captured.out
    
    def test_undo_empty(self, calculator, capsys):
        """Test undo with no calculations."""
        calculator.undo_last()
        captured = capsys.readouterr()
        
        assert "Nothing to undo" in captured.out
    
    def test_redo_calculation(self, calculator, capsys):
        """Test redo functionality."""
        calculator.perform_calculation("add", 5, 3)
        calculator.undo_last()
        calculator.redo_last()
        captured = capsys.readouterr()
        
        assert "Calculation redone" in captured.out
    
    def test_redo_empty(self, calculator, capsys):
        """Test redo with nothing to redo."""
        calculator.redo_last()
        captured = capsys.readouterr()
        
        assert "Nothing to redo" in captured.out


class TestCalculatorProcessCommand:
    """Test suite for command processing."""
    
    def test_process_exit_command(self, calculator):
        """Test exit command."""
        calculator.process_command("exit")
        
        assert calculator.running is False
    
    def test_process_help_command(self, calculator, capsys):
        """Test help command processing."""
        calculator.process_command("help")
        captured = capsys.readouterr()
        
        assert "CALCULATOR HELP MENU" in captured.out
    
    def test_process_history_command(self, calculator, capsys):
        """Test history command processing."""
        calculator.process_command("history")
        captured = capsys.readouterr()
        
        assert "No calculations" in captured.out or "CALCULATION HISTORY" in captured.out
    
    def test_process_clear_command(self, calculator, capsys):
        """Test clear command processing."""
        calculator.perform_calculation("add", 5, 3)
        calculator.process_command("clear")
        captured = capsys.readouterr()
        
        assert "History cleared" in captured.out
    
    def test_process_operation_command(self, calculator, capsys):
        """Test operation command processing."""
        calculator.process_command("add 5 3")
        captured = capsys.readouterr()
        
        assert "Result: 8.0" in captured.out
    
    def test_process_invalid_input(self, calculator, capsys):
        """Test invalid input handling."""
        calculator.process_command("add five three")
        captured = capsys.readouterr()
        
        assert "Input error" in captured.out or "Invalid" in captured.out
    
    def test_process_division_by_zero(self, calculator, capsys):
        """Test division by zero handling."""
        calculator.process_command("divide 10 0")
        captured = capsys.readouterr()
        
        assert "Math error" in captured.out or "divide by zero" in captured.out.lower()
    
    def test_process_empty_command(self, calculator):
        """Test empty command is ignored."""
        calculator.process_command("")
        # Should not raise error, just return
        assert calculator.running is True

class TestCalculatorCommandCoverage:
    """Tests to improve coverage of calculator commands."""
    
    def test_save_command_success(self, calculator, capsys):
        """Test save command saves history."""
        calculator.perform_calculation("add", 5, 3)
        calculator.process_command("save")
        captured = capsys.readouterr()
        assert "History saved" in captured.out
    
    def test_load_command_success(self, calculator, capsys):
        """Test load command."""
        calculator.process_command("load")
        captured = capsys.readouterr()
        assert "loaded" in captured.out.lower()
    
    def test_stats_command_execution(self, calculator, capsys):
        """Test stats command."""
        calculator.process_command("stats")
        captured = capsys.readouterr()
        assert "STATISTICS" in captured.out or "calculations" in captured.out