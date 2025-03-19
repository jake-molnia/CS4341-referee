# LaskerMorris

The `LaskerMorris` class implements the Lasker Morris game for the CS4341 Game Referee system. This class extends `AbstractGame` and provides a comprehensive implementation of Lasker Morris rules, including piece placement, movement, mill formation, capturing, and win conditions.

## Class Definition

```python
class LaskerMorris(AbstractGame):
    """Implementation of Lasker Morris game."""

    def __init__(
        self,
        player1_command: str,
        player2_command: str,
        visual: bool = True,
        select_rand: bool = True,
        timeout: int = 5,
        debug: bool = False,
        logging: bool = False,
        port: int = 8000,
        print_board: bool = False
    ):
        # Initialize game state and players

    def _create_web_interface(self):
        from .web import LaskerMorrisWeb
        return LaskerMorrisWeb(self)

    def initialize_game(self) -> None:
        # Set up initial game state

    def make_move(self, move: str) -> bool:
        # Process and execute a player's move

    def _has_valid_moves(self, player_color: str) -> bool:
        # Check if player has valid moves available

    def _is_oscillating_moves(self) -> bool:
        # Check for repetitive moves (draw condition)

    def _is_valid_move(self, source: str, target: str, remove: str) -> bool:
        # Validate move against game rules

    def _position_is_in_mill(self, position: str, color: str) -> bool:
        # Check if a position is part of a mill

    def _count_stones_outside_mills(self, color: str) -> int:
        # Count number of stones not part of any mill

    def _is_mill(self, source: str, target: str) -> bool:
        # Check if moving from source to target forms a mill

    def _check_corret_step(self, source: str, target: str) -> bool:
        # Check if move is to an adjacent position

    def _count_player_pieces(self, color: str) -> int:
        # Count total pieces for a player (hand + board)

    def _execute_move(self, source: str, target: str, remove: str) -> None:
        # Execute a validated move

    def _show_state(self, move: Optional[str] = None) -> None:
        # Display current board state

    def determine_winner(self) -> Optional[LaskerPlayer]:
        # Determine winner based on game state

    def _get_move_with_timeout(self) -> Optional[str]:
        # Get a move from the current player with timeout

    def run_game(self) -> Optional[LaskerPlayer]:
        # Main game loop

    def _cleanup_game(self) -> None:
        # Clean up resources when game ends
```

## Constructor Parameters

| Parameter         | Type   | Description                        | Default  |
| ----------------- | ------ | ---------------------------------- | -------- |
| `player1_command` | `str`  | Command to run the first player    | Required |
| `player2_command` | `str`  | Command to run the second player   | Required |
| `visual`          | `bool` | Enable web visualization           | `True`   |
| `select_rand`     | `bool` | Randomize player colors            | `True`   |
| `timeout`         | `int`  | Timeout in seconds for each move   | `5`      |
| `debug`           | `bool` | Enable debug output                | `False`  |
| `logging`         | `bool` | Enable detailed logging            | `False`  |
| `port`            | `int`  | Port for web visualization         | `8000`   |
| `print_board`     | `bool` | Print board to console after moves | `False`  |

## Attributes

| Attribute              | Type                        | Description                            |
| ---------------------- | --------------------------- | -------------------------------------- |
| `move_timeout`         | `float`                     | Timeout for each player's move         |
| `game_history`         | `List[Dict]`                | History of game moves and states       |
| `board_states`         | `List[Dict]`                | History of board states                |
| `hand_states`          | `List[Dict]`                | History of hand states                 |
| `debug`                | `bool`                      | Whether debug mode is enabled          |
| `port`                 | `int`                       | Port for web visualization             |
| `prin_board`           | `bool`                      | Whether to print board after moves     |
| `moves_without_taking` | `int`                       | Counter for moves without captures     |
| `board`                | `Dict[str, Optional[str]]`  | Current board state                    |
| `player_hands`         | `Dict[str, int]`            | Number of pieces in each player's hand |
| `invalid_fields`       | `Set[str]`                  | Set of invalid board positions         |
| `visual`               | `bool`                      | Whether visualization is enabled       |
| `web`                  | `Optional[LaskerMorrisWeb]` | Web interface instance                 |

## Key Method Details

### initialize_game()

Sets up the initial game state, including:

- Creating an empty board
- Starting player processes
- Starting the web server (if visualization is enabled)
- Notifying players of their colors

**Return type**: `None`

### make_move(move)

Processes a player's move, validating and executing it if valid.

**Parameters**:

- `move` (str): The move in format "source target remove"

**Return type**: `bool`

- `True` if the move was valid and executed
- `False` if the move was invalid

### \_is_valid_move(source, target, remove)

Performs comprehensive validation of a move against game rules.

**Parameters**:

- `source` (str): Source position or hand ("h1"/"h2")
- `target` (str): Target position
- `remove` (str): Position to remove or "r0" for no capture

**Return type**: `bool`

- `True` if the move is valid
- `False` if any rule is violated

### \_is_mill(source, target)

Checks if moving from source to target would form a mill.

**Parameters**:

- `source` (str): Source position or hand
- `target` (str): Target position

**Return type**: `bool`

- `True` if the move forms a mill
- `False` otherwise

### \_count_player_pieces(color)

Counts the total number of pieces a player has (hand + board).

**Parameters**:

- `color` (str): The player's color ("blue" or "orange")

**Return type**: `int`

- Total number of pieces

### determine_winner()

Determines if there is a winner based on current game state.

**Return type**: `Optional[LaskerPlayer]`

- The winning player if there is one
- `None` if the game is a draw or not yet over

### run_game()

Main game loop that runs until a player wins or the game ends in a draw.

**Return type**: `Optional[LaskerPlayer]`

- The winning player if there is one
- `None` if the game ended in a draw

## Game Rules Implementation

### Board Layout

The board is represented as a dictionary where:

- Keys are positions in the format `<column><row>` (e.g., "a1", "d3", "g7")
- Values are player colors ("blue", "orange") or `None` for empty positions

Invalid positions are stored in the `invalid_fields` set:

```python
self.invalid_fields = {
    "a2", "a3", "a5", "a6", "b1", "b3", "b5", "b7", "c1", "c2", "c6", "c7",
    "d4", "e1", "e2", "e6", "e7", "f1", "f3", "f5", "f7", "g2", "g3", "g5", "g6",
}
```

### Player Hands

Each player starts with 10 pieces in their hand, tracked in the `player_hands` dictionary:

```python
self.player_hands = {"blue": 10, "orange": 10}
```

### Mill Detection

Mills are detected by checking if three pieces of the same color are in a line:

```python
mills = [
    # Horizontal mills
    ["a1", "a4", "a7"], ["b2", "b4", "b6"], ["c3", "c4", "c5"],
    ["d1", "d2", "d3"], ["d5", "d6", "d7"], ["e3", "e4", "e5"],
    ["f2", "f4", "f6"], ["g1", "g4", "g7"],
    # Vertical mills
    ["a1", "d1", "g1"], ["b2", "d2", "f2"], ["c3", "d3", "e3"],
    ["a4", "b4", "c4"], ["e4", "f4", "g4"], ["c5", "d5", "e5"],
    ["b6", "d6", "f6"], ["a7", "d7", "g7"],
]
```

### Movement Rules

Movement is restricted to adjacent positions, defined in a neighbors dictionary:

```python
neighbors = {
    "a1": ["a4", "d1"], "a4": ["a1", "a7", "b4"], "a7": ["a4", "d7"],
    # ... (more positions)
}
```

When a player has exactly 3 pieces, they can "fly" to any empty position (not just adjacent ones).

### Capture Rules

When a player forms a mill, they can capture an opponent's piece with these restrictions:

- Cannot capture a piece that is part of a mill unless no other pieces are available
- Must capture after forming a mill

### Game End Conditions

The game ends when:

- A player has fewer than 3 pieces (loss)
- Players make 20 moves without any captures (draw)
- A player has no valid moves available (loss)

## Usage Example

Here's how to create and run a Lasker Morris game:

```python
# Create a LaskerMorris game instance
game = LaskerMorris(
    player1_command="python player1.py",
    player2_command="python player2.py",
    visual=True,
    select_rand=True,
    timeout=5,
    debug=True,
    logging=True,
    port=8000,
    print_board=True
)

# Run the game and get the winner
winner = game.run_game()

# Handle the game result
if winner:
    print(f"Winner: {winner.get_color()}")
else:
    print("Game ended in a draw")

# Clean up resources
game._cleanup_game()
```

## Game Flow

The typical game flow is:

1. Initialize the board and player processes
2. Notify players of their colors
3. First player makes a move
4. Validate the move against game rules
5. Execute the move and update the game state
6. Check for win or draw conditions
7. Send the move to the second player
8. Repeat steps 3-7, alternating players, until the game ends
9. Return the winner or `None` for a draw

## Error Handling

The `LaskerMorris` class includes robust error handling for:

- Invalid move formats
- Moves to invalid or occupied positions
- Mill and capture rule violations
- Movement rule violations
- Player timeouts
- Process communication errors

## Implementation Notes

- The game includes a comprehensive move validation system
- Mill detection and verification is thorough to ensure rule compliance
- An oscillation detection system prevents endless games
- The adjacent movement rule is enforced when a player has more than 3 pieces
- The visualization shows the board, player hands, and move history
