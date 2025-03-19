# AbstractGame

`AbstractGame` is the core abstract base class that defines the interface for all game implementations in the CS4341 Game Referee system. It provides the essential structure for turn-based games between two players.

## Class Definition

```python
class AbstractGame(ABC):
    """Abstract base class for turn-based games between two players."""

    def __init__(self, player1: AbstractPlayer, player2: AbstractPlayer) -> None:
        self._player1 = player1
        self._player2 = player2
        self._current_player = player1
        self._is_game_over = False

    @property
    def current_player(self) -> AbstractPlayer:
        return self._current_player

    def switch_player(self) -> None:
        self._current_player = self._player2 if self._current_player == self._player1 else self._player1

    @property
    def is_game_over(self) -> bool:
        return self._is_game_over

    @abstractmethod
    def initialize_game(self) -> None:
        pass

    @abstractmethod
    def make_move(self, move: Any) -> bool:
        pass

    @abstractmethod
    def determine_winner(self) -> Optional[AbstractPlayer]:
        pass
```

## Properties

### current_player

Returns the player whose turn it is currently.

**Return type**: `AbstractPlayer`

### is_game_over

Indicates whether the game has ended.

**Return type**: `bool`

## Methods

### \_\_init\_\_(player1, player2)

Initializes a new game instance with two players.

**Parameters**:

- `player1` (AbstractPlayer): The first player
- `player2` (AbstractPlayer): The second player

### switch_player()

Switches the current player to the other player.

**Return type**: `None`

### initialize_game()

Abstract method that must be implemented by game classes. Sets up the initial game state.

**Return type**: `None`

### make_move(move)

Abstract method that must be implemented by game classes. Validates and executes a move.

**Parameters**:

- `move` (Any): The move to execute, format depends on the specific game

**Return type**: `bool`

- `True` if the move was valid and executed successfully
- `False` if the move was invalid

### determine_winner()

Abstract method that must be implemented by game classes. Checks the current game state to determine if there's a winner.

**Return type**: `Optional[AbstractPlayer]`

- The winning player if there is one
- `None` if the game is a draw or not yet over

## Usage Example

Game implementations must inherit from `AbstractGame` and implement all abstract methods:

```python
class TicTacToe(AbstractGame):
    def initialize_game(self) -> None:
        # Initialize empty board
        self.board = {f"{col}{row}": None for col in "abc" for row in "123"}

        # Start player processes
        self._player1.start()
        self._player2.start()

        # Notify players of their symbols
        self._player1.write("X")
        self._player2.write("O")

    def make_move(self, move: str) -> bool:
        # Validate move format
        if not self._validate_move_format(move):
            return False

        # Check if position is empty
        if self.board[move] is not None:
            return False

        # Execute the move
        self.board[move] = self._current_player.get_symbol()
        return True

    def determine_winner(self) -> Optional[AbstractPlayer]:
        # Check win conditions
        winning_symbol = self._check_winner()
        if winning_symbol:
            self._is_game_over = True
            return (
                self._player1 if self._player1.get_symbol() == winning_symbol
                else self._player2
            )

        # Check for draw
        if self._is_board_full():
            self._is_game_over = True
            return None

        return None
```

## Implementation Guidelines

When implementing the `AbstractGame` class, follow these guidelines:

1. **State Management**: Maintain the game state, including the board, player information, and move history.

2. **Player Communication**: Handle communication with player processes through the `AbstractPlayer` interface.

3. **Move Validation**: Implement thorough validation for player moves according to game rules.

4. **Win Detection**: Implement logic to detect win conditions and determine the winner.

5. **Draw Detection**: Implement logic to detect when a game ends in a draw.

6. **Error Handling**: Handle player timeouts, invalid moves, and other potential issues.

7. **Visualization Support**: Provide necessary hooks for the web visualization system.

## Extending AbstractGame

To create a new game:

1. Inherit from `AbstractGame`
2. Implement all abstract methods
3. Add game-specific state and logic
4. Create corresponding player and web visualization classes
5. Register your game with the CLI system

## Notes

- The `AbstractGame` class does not include a default implementation of `run_game()`. Each game typically provides its own implementation of the main game loop, handling the specifics of player interaction and game progression.

- Game-specific player classes (like `TicTacToePlayer`) should inherit from `AbstractPlayer` and be used by the game implementation.

- Consider using the `_get_move_with_timeout()` pattern seen in existing games to handle move timeouts gracefully.
