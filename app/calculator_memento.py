"""
Memento Pattern implementation for undo/redo functionality.
"""

from typing import List, Optional
import copy
from app.calculation import Calculation


class CalculatorMemento:
    """Memento storing calculator state."""
    
    def __init__(self, calculations: List[Calculation]):
        """
        Initialize memento with calculator state.
        
        Args:
            calculations: List of calculations to save
        """
        self._calculations = copy.deepcopy(calculations)
    
    def get_state(self) -> List[Calculation]:
        """Get the saved state."""
        return copy.deepcopy(self._calculations)


class CalculatorCaretaker:
    """Manages mementos for undo/redo functionality."""
    
    def __init__(self):
        """Initialize caretaker."""
        self._undo_stack: List[CalculatorMemento] = []
        self._redo_stack: List[CalculatorMemento] = []
    
    def save_state(self, calculations: List[Calculation]) -> None:
        """
        Save current state to undo stack.
        
        Args:
            calculations: Current list of calculations
        """
        memento = CalculatorMemento(calculations)
        self._undo_stack.append(memento)
        # Clear redo stack when new state is saved
        self._redo_stack.clear()
    
    def undo(self) -> Optional[List[Calculation]]:
        """
        Undo last operation.
        
        Returns:
            Previous state or None if undo stack is empty
        """
        if not self._undo_stack:
            return None
        
        # Save current state to redo stack before undoing
        current_memento = self._undo_stack.pop()
        self._redo_stack.append(current_memento)
        
        # Return previous state if available
        if self._undo_stack:
            return self._undo_stack[-1].get_state()
        return []
    
    def redo(self) -> Optional[List[Calculation]]:
        """
        Redo last undone operation.
        
        Returns:
            Next state or None if redo stack is empty
        """
        if not self._redo_stack:
            return None
        
        # Move state from redo stack back to undo stack
        memento = self._redo_stack.pop()
        self._undo_stack.append(memento)
        
        return memento.get_state()
    
    def can_undo(self) -> bool:
        """Check if undo is available."""
        return len(self._undo_stack) > 0
    
    def can_redo(self) -> bool:
        """Check if redo is available."""
        return len(self._redo_stack) > 0
    
    def clear(self) -> None:
        """Clear both undo and redo stacks."""
        self._undo_stack.clear()
        self._redo_stack.clear()
        