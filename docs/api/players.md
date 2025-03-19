# Players

The CS4341 Game Referee system includes game-specific player classes that extend the `AbstractPlayer` base class. These player classes handle the specifics of player symbols, colors, and game-specific functionality.

## Player Class Hierarchy

```
AbstractPlayer (Abstract Base Class)
├── TicTacToePlayer
└── LaskerPlayer
```

## TicTacToePlayer

The `TicTacToePlayer` class represents a player in the Tic-tac-toe game.

### Class Definition

```python
class TicTacToePlayer(AbstractPlayer):
    """Player implementation for Tic-tac-toe game."""

    def __init__(self, command: str, symbol: str, log: bool = False):
        super().__init__(command, log)
        try:
            self.symbol = PlayerSymbol(symbol.upper())
        except ValueError:
            raise ValueError(f"Invalid symbol: {symbol}. Must be either 'blue' or 'orange'")

    def get_symbol(self) -> str:
        return self.symbol.value

    def is_x(self) -> bool:
        return self.symbol == PlayerSymbol.X

    def is_o(self) -> bool:
        return self.symbol == PlayerSymbol.O
```

### Attributes

| Attribute | Type           | Description              |
| --------- | -------------- | ------------------------ |
| `symbol`  | `PlayerSymbol` | Player's symbol (X or O) |

### Methods

#### get_symbol()

Gets the player's symbol.

**Return type**: `str`

- The player's symbol as a string ("BLUE" for X or "ORANGE" for O)

#### is_x()

Checks if the player is X.

**Return type**: `bool`

- `True` if the player is X, `False` otherwise

#### is_o()

Checks if the player is O.

**Return type**: `bool`

- `True` if the player is O, `False` otherwise

### Symbol Enum

The player symbols are defined in an enum:

```python
class PlayerSymbol(Enum):
    """Enum for valid player symbols in TicTacToe."""
    X = "BLUE"
    O = "ORANGE"
```

## LaskerPlayer

The `LaskerPlayer` class represents a player in the Lasker Morris game.

### Class Definition

```python
class LaskerPlayer(AbstractPlayer):
    """Player implementation for Lasker Morris game."""

    def __init__(self, command: str, color: str, log: bool = False, debug: bool = False):
        super().__init__(command, log, debug)
        try:
            self.color = PlayerColor(color.lower())
        except ValueError:
            raise ValueError(f"Invalid color: {color}. Must be either 'blue' or 'orange'")

    def get_color(self) -> str:
        return self.color.value

    def is_blue(self) -> bool:
        return self.color == PlayerColor.BLUE

    def is_orange(self) -> bool:
        return self.color == PlayerColor.ORANGE
```

### Attributes

| Attribute | Type          | Description                     |
| --------- | ------------- | ------------------------------- |
| `color`   | `PlayerColor` | Player's color (blue or orange) |

### Methods

#### get_color()

Gets the player's color.

**Return type**: `str`

- The player's color as a string ("blue" or "orange")

#### is_blue()

Checks if the player is blue.

**Return type**: `bool`

- `True` if the player is blue, `False` otherwise

#### is_orange()

Checks if the player is orange.

**Return type**: `bool`

- `True` if the player is orange, `False` otherwise

### Color Enum

The player colors are defined in an enum:

```python
class PlayerColor(Enum):
    """Enum for valid player colors in Lasker Morris."""
    BLUE = "blue"
    ORANGE = "orange"
```

## Usage Examples

### TicTacToePlayer

```python
# Create a TicTacToe player with the X symbol
player = TicTacToePlayer("python player.py", "blue", log=True)

# Start the player process
player.start()

# Send initial symbol
player.write("blue")

# Read a move from the player
move = player.read()
print(f"Player moved: {move}")

# Check if player is X
if player.is_x():
    print("Player is X")
else:
    print("Player is O")

# Get player's symbol
symbol = player.get_symbol()
print(f"Player's symbol: {symbol}")

# Stop the player process
player.stop()
```

### LaskerPlayer

```python
# Create a Lasker Morris player with the blue color
player = LaskerPlayer("python player.py", "blue", log=True, debug=True)

# Start the player process
player.start()

# Send initial color
player.write("blue")

# Read a move from the player
move = player.read()
print(f"Player moved: {move}")

# Check if player is blue
if player.is_blue():
    print("Player is blue")
else:
    print("Player is orange")

# Get player's color
color = player.get_color()
print(f"Player's color: {color}")

# Stop the player process
player.stop()
```

## Player Process Communication

The player classes communicate with external processes via standard input/output:

1. **Start**: The player process is started with the specified command.
2. **Initialization**: The player receives its symbol or color.
3. **Move Requests**: The player reads the opponent's move and responds with its own move.
4. **Termination**: The player process is terminated when the game ends.

### Input/Output Format

The player process communicates with the referee through text:

- **Input** (referee to player):

  - First input: Player's symbol or color
  - Subsequent inputs: Opponent's move or empty string for first move

- **Output** (player to referee):
  - Player's move in the appropriate format for the game

## Exception Handling

The player classes include validation to ensure that valid symbols and colors are used:

```python
try:
    self.color = PlayerColor(color.lower())
except ValueError:
    raise ValueError(f"Invalid color: {color}. Must be either 'blue' or 'orange'")
```

This validation helps prevent issues with invalid player attributes.

## Implementation Notes

- Player classes extend `AbstractPlayer` to inherit process management functionality
- Game-specific attributes (symbols, colors) are encapsulated in the player classes
- Enums are used to restrict valid symbols and colors
- Helper methods provide convenient ways to check player properties
- Error handling ensures valid player initialization
