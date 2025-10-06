"""
Calculator REPL with Facade Pattern providing simplified interface.
"""

import sys
from typing import List
from app.calculation import Calculation
from app.operations import OperationFactory
from app.history import CalculationHistory
from app.calculator_memento import CalculatorCaretaker
from app.calculator_config import CalculatorConfig
from app.input_validators import InputValidator
from app.exceptions import (
    CalculatorError, InvalidInputError, InvalidOperationError,
    DivisionByZeroError, ConfigurationError, HistoryError
)


class Calculator:
    """
    Facade class providing simplified interface to calculator subsystems.
    Implements Facade Pattern to hide complexity.
    """
    
    def __init__(self):
        """Initialize calculator with all subsystems."""
        try:
            self.config = CalculatorConfig()
            self.history = CalculationHistory(self.config.get_history_file())
            self.caretaker = CalculatorCaretaker()
            self.validator = InputValidator()
            self.calculations: List[Calculation] = []
            self.running = True
        except ConfigurationError as e: # pragma: no cover
            print(f"Configuration error: {e}")
            print("Using default configuration.")
            self.config = None
            self.history = CalculationHistory()
            self.caretaker = CalculatorCaretaker()
            self.validator = InputValidator()
            self.calculations = []
            self.running = True
    
    def display_help(self) -> None:
        """Display help information."""
        help_text = """
╔══════════════════════════════════════════════════════════════╗
║              CALCULATOR HELP MENU                            ║
╚══════════════════════════════════════════════════════════════╝

COMMANDS:
  help                - Display this help menu
  history             - Show calculation history
  clear               - Clear calculation history
  undo                - Undo last calculation
  redo                - Redo last undone calculation
  save                - Save history to CSV
  load                - Reload history from CSV
  stats               - Show history statistics
  exit                - Exit the calculator

OPERATIONS:
  add <num1> <num2>      - Add two numbers
  subtract <num1> <num2> - Subtract num2 from num1
  multiply <num1> <num2> - Multiply two numbers
  divide <num1> <num2>   - Divide num1 by num2
  power <num1> <num2>    - Raise num1 to the power of num2
  root <num1> <num2>     - Calculate num2-th root of num1
  modulus <num1> <num2>  - Calculate num1 modulo num2

EXAMPLES:
  > add 5 3
  Result: 8.0
  
  > power 2 3
  Result: 8.0
  
  > root 16 2
  Result: 4.0
        """
        print(help_text)
    
    def display_history(self) -> None:
        """Display calculation history."""
        if self.history.is_empty():
            print("No calculations in history yet.")
            return
        
        print("\n" + "="*60)
        print("CALCULATION HISTORY")
        print("="*60)
        
        df = self.history.get_last_n(20)
        for idx, row in df.iterrows():
            print(f"{idx + 1}. {row['operand1']} {row['operation']} {row['operand2']} = {row['result']}")
        
        print("="*60 + "\n")
    
    def display_stats(self) -> None:
        """Display history statistics."""
        stats = self.history.get_statistics()
        
        print("\n" + "="*60)
        print("HISTORY STATISTICS")
        print("="*60)
        print(f"Total calculations: {stats['total_calculations']}")
        
        if stats['operations']:
            print("\nOperations breakdown:")
            for op, count in stats['operations'].items():
                print(f"  {op}: {count}")
        
        print("="*60 + "\n")
    
    def perform_calculation(self, operation: str, num1: float, num2: float) -> None:
        """
        Perform a calculation.
        
        Args:
            operation: Operation name
            num1: First operand
            num2: Second operand
        """
        # Save state before performing calculation
        self.caretaker.save_state(self.calculations.copy())
        
        # Create operation strategy
        strategy = OperationFactory.create_operation(operation)
        
        # Create calculation and attach history observer
        calc = Calculation(num1, num2, operation, strategy)
        calc.attach_observer(self.history)
        
        # Execute calculation
        result = calc.execute()
        
        # Add to internal list
        self.calculations.append(calc)
        
        # Auto-save if enabled
        if self.config and self.config.is_auto_save_enabled():
            self.history.save_history()
        
        print(f"Result: {result}")
    
    def undo_last(self) -> None:
        """Undo the last calculation."""
        if not self.caretaker.can_undo():
            print("Nothing to undo.")
            return
        
        previous_state = self.caretaker.undo()
        if previous_state is not None:
            self.calculations = previous_state
            print("Last calculation undone.")
        else:
            print("Cannot undo further.")
    
    def redo_last(self) -> None:
        """Redo the last undone calculation."""
        if not self.caretaker.can_redo():
            print("Nothing to redo.")
            return
        
        next_state = self.caretaker.redo()
        if next_state is not None:
            self.calculations = next_state
            print("Calculation redone.")
        else:
            print("Cannot redo further.")
    
    def process_command(self, user_input: str) -> None:
        """
        Process user commands and operations.
        
        Args:
            user_input: Raw user input
        """
        command = self.validator.validate_command(user_input)
        
        if not command:
            return
        
        # Handle special commands
        if command == "exit":
            print("Exiting calculator. Goodbye!")
            self.running = False
            return
        
        if command == "help":
            self.display_help()
            return
        
        if command == "history":
            self.display_history()
            return
        
        if command == "clear":
            self.history.clear_history()
            self.caretaker.clear()
            self.calculations.clear()
            print("History cleared.")
            return
        
        if command == "undo":
            self.undo_last()
            return
        
        if command == "redo":
            self.redo_last()
            return
        
        if command == "save":
            try:
                self.history.save_history()
                print(f"History saved to {self.config.get_history_file() if self.config else 'calculation_history.csv'}")
            except HistoryError as e: # pragma: no cover
                print(f"Error saving history: {e}")
            return
        
        if command == "load":
            try:
                self.history.load_history()
                print("History loaded successfully.")
            except HistoryError as e: # pragma: no cover
                print(f"Error loading history: {e}")
            return
        
        if command == "stats":
            self.display_stats()
            return
        
        # Try to parse as operation
        try:
            operation, num1, num2 = self.validator.validate_operation_input(user_input)
            self.perform_calculation(operation, num1, num2)
        except InvalidInputError as e:
            print(f"Input error: {e}")
        except InvalidOperationError as e:
            print(f"Operation error: {e}")
        except DivisionByZeroError as e:
            print(f"Math error: {e}")
        except CalculatorError as e: # pragma: no cover
            print(f"Calculator error: {e}")
    
    def run(self) -> None:
        """Run the calculator REPL."""
        print("╔══════════════════════════════════════════════════════════════╗")
        print("║     Welcome to the Advanced Calculator REPL!                ║")
        print("╚══════════════════════════════════════════════════════════════╝")
        print("Type 'help' for instructions or 'exit' to quit.\n")
        
        while self.running:
            try:
                user_input = input("calculator> ")
                self.process_command(user_input)
            except KeyboardInterrupt:  # pragma: no cover
                print("\nExiting calculator. Goodbye!")
                break
            except EOFError:  # pragma: no cover
                print("\nExiting calculator. Goodbye!")
                break


def calculator(): # pragma: no cover
    """Entry point for the calculator application."""
    calc = Calculator()
    calc.run()