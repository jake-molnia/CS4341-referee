# Utilities

The CS4341 Game Referee system includes several utility classes and functions that support game implementations. These utilities handle common tasks such as error management, logging, and board operations.

## Error Classes

The system defines several custom exception classes for specific error scenarios:

### GameError

Base class for all game-related errors.

```python
class GameError(Exception):
    """Base class for game-related errors"""
    pass
```

### InvalidMoveError

Error raised when a player makes an invalid move.

```python
class InvalidMoveError(GameError):
    """Error raised when a move is invalid"""
    pass
```

### TimeoutError

Error raised when a player takes too long to respond.

```python
class TimeoutError(GameError):
    """Error raised when a player takes too long to respond"""
    pass
```

## GameLogger

The `GameLogger` class provides a standardized logging interface for games.

### Class Definition

```python
class GameLogger:
    """Handles logging for games"""

    def __init__(self, name: str, enable_logging: bool = False):
        self.logger = logging.getLogger(name)
        if enable_logging:
            self._setup_logging()

    def _setup_logging(self) -> None:
        handler = logging.FileHandler(f"{self.logger.name}.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def debug(self, message: str) -> None:
        self.logger.debug(message)
```

### Methods

#### \_\_init\_\_(name, enable_logging=False)

Initializes a new logger instance.

**Parameters**:

- `name` (str): Name of the logger (typically the game name)
- `enable_logging` (bool): Whether to enable logging (default: False)

#### \_setup_logging()

Internal method to set up logging handlers and formatters.

**Return type**: `None`

#### info(message)

Logs an informational message.

**Parameters**:

- `message` (str): The message to log

**Return type**: `None`

#### error(message)

Logs an error message.

**Parameters**:

- `message` (str): The error message to log

**Return type**: `None`

#### debug(message)

Logs a debug message.

**Parameters**:

- `message` (str): The debug message to log

**Return type**: `None`

## BoardUtils

The `BoardUtils` class provides static methods for common board operations.

### Class Definition

```python
class BoardUtils:
    @staticmethod
    def create_empty_board(cols: str, rows: str) -> Dict[str, Optional[str]]:
        """Create an empty game board with given columns and rows"""
        return {f"{col}{row}": None for col in cols for row in rows}

    @staticmethod
    def is_position_empty(board: Dict[str, Optional[str]], position: str) -> bool:
        """Check if a board position is empty"""
        return position in board and board[position] is None

    @staticmethod
    def is_position_valid(board: Dict[str, Optional[str]],
                         position: str,
                         invalid_fields: Optional[Set[str]] = None) -> bool:
        """Check if a position is valid on the board"""
        if invalid_fields and position in invalid_fields:
            return False
        return position in board
```

### Methods

#### create_empty_board(cols, rows)

Creates an empty game board with the specified columns and rows.

**Parameters**:

- `cols` (str): String containing valid column identifiers (e.g., "abc")
- `rows` (str): String containing valid row identifiers (e.g., "123")

**Return type**: `Dict[str, Optional[str]]`

- A dictionary representing the empty board

#### is_position_empty(board, position)

Checks if a position on the board is empty.

**Parameters**:

- `board` (Dict[str, Optional[str]]): The board state
- `position` (str): The position to check

**Return type**: `bool`

- `True` if the position is empty
- `False` if the position is occupied or invalid

#### is_position_valid(board, position, invalid_fields=None)

Checks if a position is valid on the board.

**Parameters**:

- `board` (Dict[str, Optional[str]]): The board state
- `position` (str): The position to check
- `invalid_fields` (Optional[Set[str]]): Set of invalid positions (optional)

**Return type**: `bool`

- `True` if the position is valid
- `False` if the position is invalid

## Usage Examples

### Error Handling

```python
try:
    # Attempt to make a move
    if not game.make_move(move):
        raise InvalidMoveError(f"Invalid move: {move}")

    # Check for timeout
    if timeout_occurred:
        raise TimeoutError("Player took too long to respond")

except InvalidMoveError as e:
    print(f"Move error: {e}")
    # Handle invalid move

except TimeoutError as e:
    print(f"Timeout error: {e}")
    # Handle timeout

except GameError as e:
    print(f"Game error: {e}")
    # Handle other game errors
```

### Logging

```python
# Create a logger for a Tic-tac-toe game
logger = GameLogger("tictactoe", enable_logging=True)

# Log game events
logger.info("Game started")
logger.info(f"Player 1: {player1_command}")
logger.info(f"Player 2: {player2_command}")

# Log moves
logger.info(f"Player 1 moved: {move}")

# Log errors
try:
    # Game logic
    pass
except Exception as e:
    logger.error(f"Error occurred: {str(e)}")

# Log debug information
logger.debug(f"Current board state: {board}")
```

### Board Utilities

```python
# Create an empty Tic-tac-toe board
board = BoardUtils.create_empty_board("abc", "123")
print(board)  # {'a1': None, 'a2': None, 'a3': None, 'b1': None, ...}

# Check if a position is empty
if BoardUtils.is_position_empty(board, "b2"):
    print("Center position is empty")

# Check if a position is valid
invalid_fields = {"a2", "a3", "b1", "c2"}  # Example invalid fields
if BoardUtils.is_position_valid(board, "a1", invalid_fields):
    print("Position a1 is valid")
else:
    print("Position a1 is invalid")
```

## Integration with Games

These utilities are designed to be used by game implementations to handle common tasks:

### Error Handling in Game Loop

```python
def run_game(self) -> Optional[AbstractPlayer]:
    """Main game loop."""
    while not self.is_game_over:
        try:
            move = self._get_move_with_timeout()

            # Handle timeout
            if move is None:
                raise TimeoutError(f"Player {self.current_player.get_symbol()} timed out")

            # Handle invalid move
            if not self.make_move(move):
                raise InvalidMoveError(f"Invalid move: {move}")

            # Continue game logic...

        except TimeoutError as e:
            # Handle timeout
            self._is_game_over = True
            return self._player2 if self.current_player == self._player1 else self._player1

        except InvalidMoveError as e:
            # Handle invalid move
            self._is_game_over = True
            return self._player2 if self.current_player == self._player1 else self._player1

        except GameError as e:
            # Handle other game errors
            self._is_game_over = True
            return None
```

### Creating Game Boards

```python
def initialize_game(self) -> None:
    """Initialize the game state."""
    # Create empty board
    self.board = BoardUtils.create_empty_board(self.VALID_COLUMNS, self.VALID_ROWS)

    # Start player processes
    self._player1.start()
    self._player2.start()

    # Start web server
    if self.visual and self.web:
        self.web.start_web_server(self.port)

    # Send initial player information
    self._player1.write(self._player1.get_symbol())
    self._player2.write(self._player2.get_symbol())
```

### Validating Moves

```python
def make_move(self, move: str) -> bool:
    """Process a player's move."""
    # Validate move format
    is_valid, error_msg = self._validate_move_format(move)
    if not is_valid:
        return False

    # Check if position is empty
    if not BoardUtils.is_position_empty(self.board, move):
        return False

    # Execute the move
    self.board[move] = self.current_player.get_symbol()
    self.move_history.append(move)

    return True
```

## Implementation Notes

- The error classes follow Python's exception hierarchy
- The logger provides standardized logging with configurable output
- The board utilities handle common operations independent of specific game rules
- These utilities help maintain consistency across different game implementations
- Using these utilities can reduce code duplication and improve maintainability
