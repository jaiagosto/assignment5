"""
History management using pandas DataFrames with Observer Pattern.
"""

import pandas as pd
from pathlib import Path
from typing import List, Optional
from datetime import datetime
from app.calculation import Calculation, CalculationObserver
from app.exceptions import HistoryError


class CalculationHistory(CalculationObserver):
    """
    Manages calculation history using pandas DataFrame.
    Implements Observer Pattern to auto-save calculations.
    """
    
    def __init__(self, csv_file: str = "calculation_history.csv"):
        """
        Initialize history manager.
        
        Args:
            csv_file: Path to CSV file for storing history
        """
        self.csv_file = csv_file
        self.df = pd.DataFrame(columns=['operand1', 'operand2', 'operation', 'result', 'timestamp'])
        self.load_history()
    
    def update(self, calculation: Calculation) -> None:
        """
        Observer method called when a calculation is performed.
        Automatically adds calculation to history.
        """
        self.add_calculation(calculation)
    
    def add_calculation(self, calculation: Calculation) -> None:
        """
        Add a calculation to history.
        """
        calc_dict = calculation.to_dict()
        new_row = pd.DataFrame([calc_dict])
        
        if self.df.empty:
            self.df = new_row
        else:
            self.df = pd.concat([self.df, new_row], ignore_index=True)
    
    def get_history(self) -> pd.DataFrame:
        """
        Get the entire history as a DataFrame.
        
        Returns:
            DataFrame containing all calculations
        """
        return self.df.copy()
    
    def get_last_n(self, n: int = 10) -> pd.DataFrame:
        """
        Get the last n calculations.
        
        Args:
            n: Number of calculations to retrieve
            
        Returns:
            DataFrame with last n calculations
        """
        return self.df.tail(n)
    
    def clear_history(self) -> None:
        """Clear all history."""
        self.df = pd.DataFrame(columns=['operand1', 'operand2', 'operation', 'result', 'timestamp'])
    
    def save_history(self) -> None:
        """
        Save history to CSV file.
        
        Raises:
            HistoryError: If saving fails
        """
        try:
            self.df.to_csv(self.csv_file, index=False)
        except Exception as e: # pragma: no cover
            raise HistoryError(f"Failed to save history: {e}")
    
    def load_history(self) -> None:
        """
        Load history from CSV file if it exists.
        
        Raises:
            HistoryError: If loading fails
        """
        try:
            if Path(self.csv_file).exists():
                self.df = pd.read_csv(self.csv_file)
                # Ensure all expected columns exist
                expected_cols = ['operand1', 'operand2', 'operation', 'result', 'timestamp']
                for col in expected_cols:
                    if col not in self.df.columns:
                        self.df[col] = None
        except Exception as e: # pragma: no cover
            raise HistoryError(f"Failed to load history: {e}")
    
    def get_count(self) -> int:
        """Get the number of calculations in history."""
        return len(self.df)
    
    def is_empty(self) -> bool:
        """Check if history is empty."""
        return len(self.df) == 0
    
    def get_statistics(self) -> dict:
        """
        Get statistics about the history.
        
        Returns:
            Dictionary with statistics
        """
        if self.is_empty():
            return {
                'total_calculations': 0,
                'operations': {}
            }
        
        stats = {
            'total_calculations': len(self.df),
            'operations': self.df['operation'].value_counts().to_dict()
        }
        
        return stats