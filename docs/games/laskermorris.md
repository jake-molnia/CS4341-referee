# Lasker Morris

Lasker Morris is a variant of the classic Nine Men's Morris board game, developed by Emanuel Lasker. It features special movement rules and strategic complexity that make it an excellent challenge for AI development.

## Game Rules

### Board Layout

The Lasker Morris board consists of 24 valid positions arranged in three concentric squares connected by lines:

```
7   a   b   c   d   e   f   g
  +---+---+---+---+---+---+---+
7 | a7|   |   | d7|   |   | g7| 7
  +   +   +   +   +   +   +   +
6 |   | b6|   | d6|   | f6|   | 6
  +   +   +   +   +   +   +   +
5 |   |   | c5| d5| e5|   |   | 5
  +   +   +   +   +   +   +   +
4 | a4| b4| c4|   | e4| f4| g4| 4
  +   +   +   +   +   +   +   +
3 |   |   | c3| d3| e3|   |   | 3
  +   +   +   +   +   +   +   +
2 |   | b2|   | d2|   | f2|   | 2
  +   +   +   +   +   +   +   +
1 | a1|   |   | d1|   |   | g1| 1
  +---+---+---+---+---+---+---+
    a   b   c   d   e   f   g
```

The empty spaces are invalid positions where pieces cannot be placed.

### Game Phases

Lasker Morris has three main phases:

1. **Placement Phase**: Players take turns placing pieces from their hand onto empty board positions
2. **Movement Phase**: After all pieces are placed, players move pieces to adjacent positions
3. **Flying Phase**: When a player has only 3 pieces left, they can "fly" to any empty position

### Basic Rules

- Players start with 10 pieces each (blue and orange)
- During the placement phase, players place one piece per turn
- During the movement phase, pieces can only move to adjacent empty positions along the lines
- When a player has exactly 3 pieces, they can move to any empty position on the board
- Forming a "mill" (three pieces in a straight line) allows capturing an opponent's piece
- A player loses when reduced to fewer than 3 pieces
- The game ends in a draw if the same position repeats 3 times or after 20 moves without captures

## Running a Game

To run a Lasker Morris game:

```bash
cs4341-referee laskermorris -p1 "python player1.py" -p2 "python player2.py" --visual
```

## Player Communication

### Initialization

At the start of the game, each player receives their color:

- First player receives: `"blue"`
- Second player receives: `"orange"`

### Move Format

Moves in Lasker Morris follow this format:

```
<source> <target> <remove>
```

Where:

- `<source>`: The source position (e.g., "d1") or "h1"/"h2" if placing from hand
- `<target>`: The target position (must be empty)
- `<remove>`: A position to remove an opponent's piece ("r0" if no capture)

Examples:

- `h1 d1 r0`: Place a piece from hand to position d1, no capture
- `d1 d2 e3`: Move piece from d1 to d2 and capture opponent's piece at e3
- `a1 g7 r0`: Flying move from a1 to g7 (only valid with exactly 3 pieces)

### Game Flow

1. The referee starts both player processes
2. Each player is notified of their color
3. Players take turns making moves:
   - The current player sends a valid move
   - The referee validates and executes the move
   - The opponent receives the move made
4. The game continues until someone wins or a draw occurs
5. The referee sends "END" to both players when the game is over

## Player Implementation

Here's a basic template for implementing a Lasker Morris player:

```python
import sys

def main():
    # Read initial color
    color = input().strip()  # "blue" or "orange"

    # Track pieces in hand
    pieces_in_hand = 10

    # Track board state
    board = {}  # position -> color mapping

    while True:
        try:
            # Read opponent's move or game start
            game_input = input().strip()

            # Check if game has ended
            if game_input == "END":
                break

            # Process opponent's move if not the first move
            if game_input:
                source, target, remove = game_input.split()
                # Update internal board state
                # ...

            # Determine move (simplified example)
            move = ""
            if pieces_in_hand > 0:
                # Placement phase - place from hand
                move = "h1 d1 r0"  # Example: place at center
                pieces_in_hand -= 1
            else:
                # Movement phase
                # Implement movement logic
                # ...

            # Send move to referee
            print(move, flush=True)

        except EOFError:
            break

if __name__ == "__main__":
    main()
```

## Web Visualization

When run with the `--visual` flag, the referee provides a web-based visualization:

![Lasker Morris Visualization](../assets/laskermorris-viz.png)

## Mill Combinations

A key aspect of Lasker Morris is forming and recognizing mills. Here are all possible mill combinations:

**Horizontal Mills:**

- a1, a4, a7
- b2, b4, b6
- c3, c4, c5
- d1, d2, d3
- d5, d6, d7
- e3, e4, e5
- f2, f4, f6
- g1, g4, g7

**Vertical Mills:**

- a1, d1, g1
- b2, d2, f2
- c3, d3, e3
- a4, b4, c4
- e4, f4, g4
- c5, d5, e5
- b6, d6, f6
- a7, d7, g7

## Strategic Elements

### Placement Phase

1. **Control the Intersections**: Positions like d3, d5, b4, and f4 are at the intersection of multiple potential mills
2. **Block Opponent Mills**: Place pieces to prevent your opponent from forming mills
3. **Create Mill Setups**: Position pieces to enable multiple potential mills in future turns

### Movement Phase

1. **Mill Creation**: Move pieces to form mills and capture opponent pieces
2. **Defend Against Capture**: Protect pieces that are part of formed mills
3. **Double Mills**: Create configurations where moving one piece forms two mills simultaneously
4. **Block Opponent Movement**: Position pieces to restrict opponent movement options

### Flying Phase

1. **Aggressive Flying**: When reduced to 3 pieces, use flying to create unexpected mills
2. **Defensive Flying**: Use flying to quickly respond to threats and avoid capture

## Advanced Topics

### Board Evaluation

A strong Lasker Morris AI needs an effective evaluation function. Consider these factors:

- Piece count difference
- Number of potential mills
- Mobility (number of possible moves)
- Control of strategic positions
- Number of pieces in potential mills

### Mill Detection Function

Here's a function to detect if a position is part of a mill:

```python
def is_mill(board, position, color):
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

    for mill in mills:
        if position in mill and all(board.get(pos) == color for pos in mill):
            return True
    return False
```

### Neighbor Mapping

For efficient move generation, maintain a map of adjacent positions:

```python
neighbors = {
    "a1": ["a4", "d1"], "a4": ["a1", "a7", "b4"], "a7": ["a4", "d7"],
    "b2": ["b4", "d2"], "b4": ["b2", "b6", "a4", "c4"], "b6": ["b4", "d6"],
    "c3": ["c4", "d3"], "c4": ["c3", "c5", "b4"], "c5": ["c4", "d5"],
    "d1": ["a1", "d2", "g1"], "d2": ["b2", "d1", "d3", "f2"],
    "d3": ["c3", "d2", "e3"], "d5": ["c5", "d6", "e5"],
    "d6": ["b6", "d5", "d7", "f6"], "d7": ["a7", "d6", "g7"],
    "e3": ["d3", "e4"], "e4": ["e3", "e5", "f4"], "e5": ["d5", "e4"],
    "f2": ["d2", "f4"], "f4": ["e4", "f2", "f6", "g4"], "f6": ["d6", "f4"],
    "g1": ["d1", "g4"], "g4": ["f4", "g1", "g7"], "g7": ["d7", "g4"],
}
```

## Testing Strategies

1. **Self-Play**: Test your player against itself to identify weaknesses
2. **Opening Book**: Develop a library of strong opening placements
3. **Endgame Tables**: Precompute optimal plays for common endgame scenarios
4. **Time Management**: Make simple, fast decisions in the opening, saving time for critical calculations later

By understanding these concepts, you'll be well-equipped to develop a competitive Lasker Morris AI player!
