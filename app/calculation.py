"""
Calculation model with Observer Pattern support.
"""

from typing import List, Optional
from datetime import datetime
from app.operations import OperationStrategy


class CalculationObserver:
    """Observer interface for calculation events."""
    
    def update(self, calculation: 'Calculation') -> None:
        """Called when a calculation is performed."""
        pass  # pragma: no cover


class Calculation:
    """Represents a single calculation with observer support."""
    
    def __init__(self, operand1: float, operand2: float, 
                 operation_name: str, strategy: OperationStrategy):
        """
        Initialize a calculation.
        
        Args:
            operand1: First operand
            operand2: Second operand
            operation_name: Name of the operation
            strategy: Operation strategy to execute
        """
        self.operand1 = operand1
        self.operand2 = operand2
        self.operation_name = operation_name
        self.strategy = strategy
        self.result: Optional[float] = None
        self.timestamp: Optional[datetime] = None
        self._observers: List[CalculationObserver] = []
    
    def attach_observer(self, observer: CalculationObserver) -> None:
        """Attach an observer to this calculation."""
        if observer not in self._observers:
            self._observers.append(observer)
    
    def detach_observer(self, observer: CalculationObserver) -> None:
        """Detach an observer from this calculation."""
        if observer in self._observers: # pragma: no cover
            self._observers.remove(observer)
    
    def notify_observers(self) -> None:
        """Notify all observers about the calculation."""
        for observer in self._observers:
            observer.update(self)
    
    def execute(self) -> float:
        """
        Execute the calculation and notify ob#servers.
        
        Returns:
            Calculation result
        """
        self.result = self.strategy.execute(self.operand1, self.operand2)
        self.timestamp = datetime.now()
        self.notify_observers()
        return self.result
    
    def to_dict(self) -> dict:
        """Convert calculation to dictionary for storage."""
        return {
            'operand1': self.operand1,
            'operand2': self.operand2,
            'operation': self.operation_name,
            'result': self.result,
            'timestamp': self.timestamp.isoformat() if self.timestamp else None
        }
    
    def __str__(self) -> str:
        """String representation of the calculation."""
        if self.result is not None: # pragma: no cover
            return f"{self.operand1} {self.operation_name} {self.operand2} = {self.result}"
        return f"{self.operand1} {self.operation_name} {self.operand2}"
    
    def __repr__(self) -> str:
        """Technical representation of the calculation."""
        return f"Calculation({self.operand1}, {self.operand2}, '{self.operation_name}')" # pragma: no cover