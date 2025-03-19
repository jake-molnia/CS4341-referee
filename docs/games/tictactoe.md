# Tic-tac-toe

Tic-tac-toe is a classic game where two players take turns marking spaces on a 3×3 grid, aiming to place three of their marks in a horizontal, vertical, or diagonal row.

## Game Rules

- Players take turns placing their symbol (X or O) on an empty cell of the 3×3 grid
- The first player to form a line of three of their own symbol (horizontally, vertically, or diagonally) wins
- If all cells are filled and no player has formed a line, the game ends in a draw

## Board Representation

The Tic-tac-toe board is represented as a 3×3 grid with positions labeled as follows:

```
    a   b   c
  +---+---+---+
3 | a3| b3| c3|  3
  +---+---+---+
2 | a2| b2| c2|  2
  +---+---+---+
1 | a1| b1| c1|  1
  +---+---+---+
    a   b   c
```

- Columns are labeled as 'a', 'b', and 'c'
- Rows are labeled as '1', '2', and '3'
- Each position is referenced by its column followed by its row (e.g., 'b2' for the center position)

## Running a Game

To run a Tic-tac-toe game:

```bash
cs4341-referee tictactoe -p "python your_player.py" --visual
```

This will run a game where your player plays against itself. To specify a different opponent:

```bash
cs4341-referee tictactoe -p "python your_player.py" -p2 "python opponent_player.py" --visual
```

## Player Communication

### Initialization

At the start of the game, each player receives their symbol:

- First player receives: `"blue"` (representing X)
- Second player receives: `"orange"` (representing O)

### Move Format

The move format for Tic-tac-toe is simply the position where the player wants to place their symbol:

```
<column><row>
```

Examples:

- `a1` (bottom-left corner)
- `b2` (center position)
- `c3` (top-right corner)

### Game Flow

1. The referee starts both player processes
2. Each player is notified of their symbol
3. Players take turns making moves:
   - The current player is expected to send a valid move
   - The referee validates the move and updates the game state
   - The opponent receives the move made by the current player
4. The game continues until someone wins or the board is full (draw)

## Player Implementation

Here's a basic template for implementing a Tic-tac-toe player:

```python
import sys

def main():
    # Read initial symbol (X or O)
    player_symbol = input().strip()  # Will be "blue" or "orange"

    # Initialize board (None represents empty cells)
    board = {f"{col}{row}": None for col in "abc" for row in "123"}

    while True:
        try:
            # Read opponent's move or game start
            game_input = input().strip()

            # Update board with opponent's move (if not first move)
            if game_input:
                board[game_input] = "opponent"

            # Your move logic here
            # For example, find the first empty cell:
            move = next(pos for pos, val in board.items() if val is None)

            # Update our internal board
            board[move] = "me"

            # Send move to referee
            print(move, flush=True)

        except EOFError:
            break

if __name__ == "__main__":
    main()
```

## Web Visualization

When run with the `--visual` flag, the referee provides a web-based visualization of the game:

![Tic-tac-toe Visualization](../assets/tictactoe-viz.png)

The visualization includes:

- Current board state
- Move history
- Player information
- Game status and results

## Tips for Building a Strong Player

1. **Corner Strategy**: Starting with corner moves gives more opportunities for creating winning lines

2. **Center Control**: The center position (b2) provides the most opportunities for creating winning lines

3. **Block Opponent**: Always check if your opponent is about to win and block them

4. **Fork Creation**: Create positions where you have two potential winning moves, forcing your opponent to defend one and allowing you to win with the other

5. **Minimax Algorithm**: Implement the minimax algorithm with alpha-beta pruning for optimal play

## Common Mistakes to Avoid

1. **Invalid Move Format**: Ensure your move is exactly in the format `<column><row>` (e.g., "b2")

2. **Playing Occupied Cells**: Always check that a cell is empty before making a move

3. **Slow Response**: Make sure your player responds within the timeout period

4. **Buffer Flushing**: Always use `flush=True` with print statements to ensure your move is sent immediately

5. **Error Handling**: Handle EOFError properly to gracefully exit when the game ends

## Advanced Topics

### Board Evaluation

For AI players, properly evaluating board positions is crucial. A simple evaluation function might assign:

- Win: +10
- Draw: 0
- Loss: -10

More sophisticated evaluations might consider:

- Number of potential winning lines
- Center control
- Corner occupation

### Minimax Implementation

The minimax algorithm allows your player to find the optimal move by exploring possible future states:

```python
def minimax(board, depth, is_maximizing):
    if is_win(board, "me"):
        return 10 - depth
    if is_win(board, "opponent"):
        return depth - 10
    if is_full(board):
        return 0

    if is_maximizing:
        best_score = -float('inf')
        for move in get_empty_cells(board):
            board[move] = "me"
            score = minimax(board, depth + 1, False)
            board[move] = None
            best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for move in get_empty_cells(board):
            board[move] = "opponent"
            score = minimax(board, depth + 1, True)
            board[move] = None
            best_score = min(score, best_score)
        return best_score
```

With this foundation, you can build a perfect Tic-tac-toe player that never loses!
