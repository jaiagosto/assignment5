"""
Unit tests for history management with pandas.
"""

import pytest
import pandas as pd
from pathlib import Path
from app.history import CalculationHistory
from app.calculation import Calculation
from app.operations import AdditionStrategy, MultiplicationStrategy
from app.exceptions import HistoryError


@pytest.fixture
def temp_csv_file(tmp_path):
    """Fixture to provide temporary CSV file path."""
    return str(tmp_path / "test_history.csv")


@pytest.fixture
def history(temp_csv_file):
    """Fixture to provide fresh history instance."""
    return CalculationHistory(csv_file=temp_csv_file)


class TestCalculationHistory:
    """Test suite for CalculationHistory class."""
    
    def test_history_initialization(self, history):
        """Test history initialization."""
        assert isinstance(history.df, pd.DataFrame)
        assert history.is_empty()
    
    def test_add_calculation(self, history):
        """Test adding calculation to history."""
        strategy = AdditionStrategy()
        calc = Calculation(5, 3, "add", strategy)
        calc.execute()
        
        history.add_calculation(calc)
        
        assert history.get_count() == 1
        assert not history.is_empty()
    
    def test_observer_update(self, history):
        """Test observer pattern updates history."""
        strategy = AdditionStrategy()
        calc = Calculation(5, 3, "add", strategy)
        calc.attach_observer(history)
        
        calc.execute()
        
        assert history.get_count() == 1
    
    def test_get_history(self, history):
        """Test retrieving history as DataFrame."""
        strategy = AdditionStrategy()
        calc1 = Calculation(5, 3, "add", strategy)
        calc1.execute()
        calc2 = Calculation(10, 2, "multiply", MultiplicationStrategy())
        calc2.execute()
        
        history.add_calculation(calc1)
        history.add_calculation(calc2)
        
        df = history.get_history()
        
        assert isinstance(df, pd.DataFrame)
        assert len(df) == 2
    
    def test_get_last_n(self, history):
        """Test getting last n calculations."""
        strategy = AdditionStrategy()
        
        for i in range(5):
            calc = Calculation(i, i+1, "add", strategy)
            calc.execute()
            history.add_calculation(calc)
        
        last_3 = history.get_last_n(3)
        
        assert len(last_3) == 3
    
    def test_clear_history(self, history):
        """Test clearing history."""
        strategy = AdditionStrategy()
        calc = Calculation(5, 3, "add", strategy)
        calc.execute()
        
        history.add_calculation(calc)
        assert history.get_count() == 1
        
        history.clear_history()
        assert history.is_empty()
        assert history.get_count() == 0
    
    def test_save_and_load_history(self, history, temp_csv_file):
        """Test saving and loading history from CSV."""
        strategy = AdditionStrategy()
        calc = Calculation(5, 3, "add", strategy)
        calc.execute()
        
        history.add_calculation(calc)
        history.save_history()
        
        # Create new history instance and load
        new_history = CalculationHistory(csv_file=temp_csv_file)
        
        assert new_history.get_count() == 1
        df = new_history.get_history()
        assert df.iloc[0]['operand1'] == 5.0
        assert df.iloc[0]['operand2'] == 3.0
    
    def test_get_statistics(self, history):
        """Test getting history statistics."""
        strategy = AdditionStrategy()
        
        calc1 = Calculation(5, 3, "add", strategy)
        calc1.execute()
        calc2 = Calculation(10, 5, "add", strategy)
        calc2.execute()
        calc3 = Calculation(7, 2, "multiply", MultiplicationStrategy())
        calc3.execute()
        
        history.add_calculation(calc1)
        history.add_calculation(calc2)
        history.add_calculation(calc3)
        
        stats = history.get_statistics()
        
        assert stats['total_calculations'] == 3
        assert stats['operations']['add'] == 2
        assert stats['operations']['multiply'] == 1
    
    def test_statistics_empty_history(self, history):
        """Test statistics on empty history."""
        stats = history.get_statistics()
        
        assert stats['total_calculations'] == 0
        assert stats['operations'] == {}
    
    def test_get_count(self, history):
        """Test getting calculation count."""
        assert history.get_count() == 0
        
        strategy = AdditionStrategy()
        calc = Calculation(5, 3, "add", strategy)
        calc.execute()
        history.add_calculation(calc)
        
        assert history.get_count() == 1
    
    def test_is_empty(self, history):
        """Test checking if history is empty."""
        assert history.is_empty() is True
        
        strategy = AdditionStrategy()
        calc = Calculation(5, 3, "add", strategy)
        calc.execute()
        history.add_calculation(calc)
        
        assert history.is_empty() is False