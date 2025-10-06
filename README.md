# Advanced Calculator Application with Design Patterns

A professional-grade command-line calculator application implementing advanced design patterns, persistent data management with pandas, and comprehensive testing.

## Features

- **REPL Interface**: Interactive Read-Eval-Print Loop for continuous user interaction
- **Advanced Operations**: Addition, subtraction, multiplication, division, power, root, and modulus
- **Design Patterns**:
  - **Strategy Pattern**: Interchangeable operation execution strategies
  - **Factory Pattern**: Dynamic operation instantiation
  - **Observer Pattern**: Event-driven calculation monitoring and auto-saving
  - **Memento Pattern**: Undo/redo functionality with state preservation
  - **Facade Pattern**: Simplified interface to complex subsystems
- **Data Management**: pandas DataFrames for calculation history with CSV persistence
- **Configuration**: Environment-based configuration using python-dotenv
- **Commands**: help, history, clear, undo, redo, save, load, stats, exit

## Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Setup

1. Clone the repository
2. Create and activate virtual environment
3. Install dependencies: `pip install -r requirements.txt`

## Usage

Run the calculator: `python main.py`

### Available Commands

- `help` - Display help menu
- `history` - Show calculation history
- `clear` - Clear calculation history
- `undo` - Undo last calculation
- `redo` - Redo last undone calculation
- `save` - Save history to CSV
- `load` - Reload history from CSV
- `stats` - Show history statistics
- `exit` - Exit the calculator

### Operations

- add, subtract, multiply, divide, power, root, modulus

## Configuration

Create a `.env` file with: HISTORY_FILE, AUTO_SAVE, MAX_HISTORY, DECIMAL_PLACES

## Testing

Run tests: `pytest`
Run with coverage: `pytest --cov=app tests/`

**Current test coverage: 90%+**

## Design Patterns Implemented

- **Strategy Pattern**: Operations as interchangeable strategies
- **Factory Pattern**: Dynamic operation instantiation
- **Observer Pattern**: Event-driven calculation monitoring
- **Memento Pattern**: Undo/redo functionality
- **Facade Pattern**: Simplified interface to subsystems

## Error Handling

Implements both LBYL and EAFP paradigms for robust error handling.

## CI/CD

GitHub Actions automatically runs tests and checks coverage on every push.

## Dependencies

- pandas==2.2.3
- python-dotenv==1.0.0
- pytest==8.3.3
- pytest-cov==5.0.0

## Author

Jailene Agosto