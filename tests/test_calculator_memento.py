"""
Unit tests for Memento Pattern implementation.
"""

import pytest
from app.calculator_memento import CalculatorMemento, CalculatorCaretaker
from app.calculation import Calculation
from app.operations import AdditionStrategy


class TestCalculatorMemento:
    """Test suite for CalculatorMemento class."""
    
    def test_memento_initialization(self):
        """Test memento initialization."""
        strategy = AdditionStrategy()
        calc = Calculation(5, 3, "add", strategy)
        calculations = [calc]
        
        memento = CalculatorMemento(calculations)
        
        assert memento is not None
    
    def test_memento_get_state(self):
        """Test getting state from memento."""
        strategy = AdditionStrategy()
        calc = Calculation(5, 3, "add", strategy)
        calculations = [calc]
        
        memento = CalculatorMemento(calculations)
        state = memento.get_state()
        
        assert len(state) == 1
        assert state[0].operand1 == 5
        assert state[0].operand2 == 3
    
    def test_memento_deep_copy(self):
        """Test that memento creates deep copy."""
        strategy = AdditionStrategy()
        calc = Calculation(5, 3, "add", strategy)
        calculations = [calc]
        
        memento = CalculatorMemento(calculations)
        state = memento.get_state()
        
        # Modify original
        calculations[0].operand1 = 100
        
        # State should be unchanged
        assert state[0].operand1 == 5


class TestCalculatorCaretaker:
    """Test suite for CalculatorCaretaker class."""
    
    def test_caretaker_initialization(self):
        """Test caretaker initialization."""
        caretaker = CalculatorCaretaker()
        
        assert caretaker.can_undo() is False
        assert caretaker.can_redo() is False
    
    def test_save_state(self):
        """Test saving state."""
        caretaker = CalculatorCaretaker()
        strategy = AdditionStrategy()
        calc = Calculation(5, 3, "add", strategy)
        calculations = [calc]
        
        caretaker.save_state(calculations)
        
        assert caretaker.can_undo() is True
    
    def test_undo_single_state(self):
        """Test undo with single state."""
        caretaker = CalculatorCaretaker()
        strategy = AdditionStrategy()
        
        calc1 = Calculation(5, 3, "add", strategy)
        calculations1 = [calc1]
        caretaker.save_state(calculations1)
        
        calc2 = Calculation(10, 5, "add", strategy)
        calculations2 = [calc1, calc2]
        caretaker.save_state(calculations2)
        
        previous_state = caretaker.undo()
        
        assert len(previous_state) == 1
        assert previous_state[0].operand1 == 5
    
    def test_undo_empty_stack(self):
        """Test undo with empty stack."""
        caretaker = CalculatorCaretaker()
        
        result = caretaker.undo()
        
        assert result is None
    
    def test_redo_after_undo(self):
        """Test redo after undo."""
        caretaker = CalculatorCaretaker()
        strategy = AdditionStrategy()
        
        calc1 = Calculation(5, 3, "add", strategy)
        calculations1 = [calc1]
        caretaker.save_state(calculations1)
        
        calc2 = Calculation(10, 5, "add", strategy)
        calculations2 = [calc1, calc2]
        caretaker.save_state(calculations2)
        
        caretaker.undo()
        next_state = caretaker.redo()
        
        assert len(next_state) == 2
    
    def test_redo_empty_stack(self):
        """Test redo with empty stack."""
        caretaker = CalculatorCaretaker()
        
        result = caretaker.redo()
        
        assert result is None
    
    def test_redo_cleared_after_new_save(self):
        """Test redo stack is cleared after new save."""
        caretaker = CalculatorCaretaker()
        strategy = AdditionStrategy()
        
        calc1 = Calculation(5, 3, "add", strategy)
        calculations1 = [calc1]
        caretaker.save_state(calculations1)
        
        calc2 = Calculation(10, 5, "add", strategy)
        calculations2 = [calc1, calc2]
        caretaker.save_state(calculations2)
        
        caretaker.undo()
        assert caretaker.can_redo() is True
        
        # Save new state
        calc3 = Calculation(7, 2, "add", strategy)
        calculations3 = [calc1, calc3]
        caretaker.save_state(calculations3)
        
        assert caretaker.can_redo() is False
    
    def test_can_undo(self):
        """Test can_undo method."""
        caretaker = CalculatorCaretaker()
        
        assert caretaker.can_undo() is False
        
        strategy = AdditionStrategy()
        calc = Calculation(5, 3, "add", strategy)
        caretaker.save_state([calc])
        
        assert caretaker.can_undo() is True
    
    def test_can_redo(self):
        """Test can_redo method."""
        caretaker = CalculatorCaretaker()
        strategy = AdditionStrategy()
        
        calc = Calculation(5, 3, "add", strategy)
        caretaker.save_state([calc])
        
        assert caretaker.can_redo() is False
        
        caretaker.undo()
        
        assert caretaker.can_redo() is True
    
    def test_clear(self):
        """Test clearing caretaker stacks."""
        caretaker = CalculatorCaretaker()
        strategy = AdditionStrategy()
        
        calc = Calculation(5, 3, "add", strategy)
        caretaker.save_state([calc])
        caretaker.undo()
        
        caretaker.clear()
        
        assert caretaker.can_undo() is False
        assert caretaker.can_redo() is False