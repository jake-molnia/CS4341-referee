# TicTacToe

The `TicTacToe` class provides a complete implementation of the Tic-tac-toe game for the CS4341 Game Referee system. This class extends `AbstractGame` and manages the game state, rules, player interaction, and win condition detection.

## Class Definition

```python
class TicTacToe(AbstractGame):
    VALID_COLUMNS = set("abc")
    VALID_ROWS = set("123")

    def __init__(
        self,
        player1_command: str,
        player2_command: str,
        visual: bool = True,
        random_assignment: bool = False,
        move_timeout: int = 5,
        enable_logging: bool = False,
        debug: bool = False,
        port: int = GameConfig.DEFAULT_WEB_PORT,
    ):
        # Initialize game with players and settings

    def _create_web_interface(self):
        from .web import TicTacToeWeb
        return TicTacToeWeb(self)

    def initialize_game(self) -> None:
        # Set up initial game state

    def _validate_move_format(self, move: str) -> Tuple[bool, Optional[str]]:
        # Validate move format (e.g., "a1", "b2")

    def make_move(self, move: str) -> bool:
        # Process and execute a player's move

    def _show_state(self, last_move: Optional[str] = None) -> None:
        # Display current board state (for debugging)

    def _check_winner(self) -> Optional[str]:
        # Check for win conditions

    def _is_board_full(self) -> bool:
        # Check if the board is full (draw condition)

    def determine_winner(self) -> Optional[TicTacToePlayer]:
        # Determine the winner based on game state

    def _get_move_with_timeout(self) -> Optional[str]:
        # Get a move from the current player with timeout handling

    def run_game(self) -> Optional[TicTacToePlayer]:
        # Main game loop

    def _cleanup_game(self) -> None:
        # Clean up resources when game ends
```

## Constructor Parameters

| Parameter           | Type   | Description                      | Default  |
| ------------------- | ------ | -------------------------------- | -------- |
| `player1_command`   | `str`  | Command to run the first player  | Required |
| `player2_command`   | `str`  | Command to run the second player | Required |
| `visual`            | `bool` | Enable web visualization         | `True`   |
| `random_assignment` | `bool` | Randomize player symbols (X/O)   | `False`  |
| `move_timeout`      | `int`  | Timeout in seconds for each move | `5`      |
| `enable_logging`    | `bool` | Enable detailed logging          | `False`  |
| `debug`             | `bool` | Enable debug output              | `False`  |
| `port`              | `int`  | Port for web visualization       | `8000`   |

## Attributes

| Attribute        | Type                       | Description                      |
| ---------------- | -------------------------- | -------------------------------- |
| `move_timeout`   | `int`                      | Timeout for each player's move   |
| `debug`          | `bool`                     | Whether debug mode is enabled    |
| `enable_logging` | `bool`                     | Whether logging is enabled       |
| `port`           | `int`                      | Port for web visualization       |
| `board`          | `Dict[str, Optional[str]]` | Current board state              |
| `visual`         | `bool`                     | Whether visualization is enabled |
| `web`            | `Optional[TicTacToeWeb]`   | Web interface instance           |
| `move_history`   | `List[str]`                | History of moves made            |

## Method Details

### initialize_game()

Sets up the initial game state, including:

- Creating an empty 3x3 board
- Starting player processes
- Starting the web server (if visualization is enabled)
- Notifying players of their symbols

**Return type**: `None`

### \_validate_move_format(move)

Validates that a move is in the correct format.

**Parameters**:

- `move` (str): The move to validate (e.g., "a1", "b3")

**Return type**: `Tuple[bool, Optional[str]]`

- First element: `True` if valid, `False` if invalid
- Second element: Error message if invalid, `None` if valid

### make_move(move)

Processes a player's move, updating the game state if valid.

**Parameters**:

- `move` (str): The move to make (e.g., "a1", "b3")

**Return type**: `bool`

- `True` if the move was valid and executed
- `False` if the move was invalid

### \_check_winner()

Checks all possible win combinations to determine if a player has won.

**Return type**: `Optional[str]`

- The symbol of the winning player if there is a winner
- `None` if there is no winner

### \_is_board_full()

Checks if the board is completely filled (draw condition).

**Return type**: `bool`

- `True` if the board is full
- `False` if there are still empty positions

### determine_winner()

Determines if there is a winner based on the current board state.

**Return type**: `Optional[TicTacToePlayer]`

- The winning player if there is one
- `None` if the game is a draw or not yet over

### \_get_move_with_timeout()

Gets a move from the current player with timeout handling.

**Return type**: `Optional[str]`

- The player's move if received within the timeout
- `None` if the player timed out

### run_game()

Main game loop that runs until the game ends.

**Return type**: `Optional[TicTacToePlayer]`

- The winning player if there is one
- `None` if the game ended in a draw

## Usage Example

Here's how to create and run a Tic-tac-toe game:

```python
# Create a TicTacToe game instance
game = TicTacToe(
    player1_command="python player1.py",
    player2_command="python player2.py",
    visual=True,
    random_assignment=True,
    move_timeout=5,
    enable_logging=True,
    debug=True,
    port=8000
)

# Run the game and get the winner
winner = game.run_game()

# Handle the game result
if winner:
    print(f"Winner: {winner.get_symbol()}")
else:
    print("Game ended in a draw")

# Clean up resources
game._cleanup_game()
```

## Board Representation

The Tic-tac-toe board is represented as a dictionary where:

- Keys are positions in the format `<column><row>` (e.g., "a1", "b2", "c3")
- Values are player symbols ("BLUE" for X, "ORANGE" for O) or `None` for empty positions

```
{
    "a1": None, "b1": "BLUE", "c1": None,
    "a2": None, "b2": "ORANGE", "c2": None,
    "a3": "BLUE", "b3": None, "c3": "ORANGE"
}
```

## Win Conditions

The game checks for these win combinations:

**Rows**:

- "a1", "b1", "c1"
- "a2", "b2", "c2"
- "a3", "b3", "c3"

**Columns**:

- "a1", "a2", "a3"
- "b1", "b2", "b3"
- "c1", "c2", "c3"

**Diagonals**:

- "a1", "b2", "c3"
- "a3", "b2", "c1"

## Game Flow

The typical game flow is:

1. Initialize the game board and player processes
2. Notify players of their symbols
3. First player makes a move
4. Validate the move and update the board
5. Check for win or draw conditions
6. Send the move to the second player
7. Repeat steps 3-6, alternating players, until the game ends
8. Return the winner or `None` for a draw

## Error Handling

The `TicTacToe` class includes robust error handling for:

- Invalid move formats
- Moves to occupied positions
- Player timeouts
- Game state inconsistencies
- Process communication errors

## Implementation Notes

- The game uses `ThreadPoolExecutor` for timeout handling
- Player processes communicate via standard input/output
- The game maintains a move history for analysis and visualization
- Debug mode provides console output of the current board state
- The web visualization shows the current state and move history
