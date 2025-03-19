# Quick Start

This guide will help you quickly get started with the CS4341 Game Referee system. We'll walk through installing the referee, running your first game, and providing a basic player implementation.

## Basic Installation

Install the referee directly from GitHub:

```bash
pip install git+https://github.com/jake-molnia/cs4341-referee.git
```

## Running Your First Tic-tac-toe Game

Let's create a simple player that makes random moves and use it to run a Tic-tac-toe game:

1. Create a file called `random_player.py`:

```python
import sys
import random

def main():
    # Read initial symbol (X or O)
    player_symbol = input().strip()
    print(f"I am player {player_symbol}", file=sys.stderr)

    # Start with an empty board
    board = {f"{col}{row}": None for col in "abc" for row in "123"}

    while True:
        try:
            # Read opponent's move or game start
            game_input = input().strip()

            # If this isn't the first move, update the board with opponent's move
            if game_input:
                col, row = game_input[0], game_input[1]
                board[game_input] = "opponent"
                print(f"Opponent moved: {game_input}", file=sys.stderr)

            # Find all empty positions
            empty_positions = [pos for pos, value in board.items() if value is None]

            # Choose a random empty position
            if empty_positions:
                move = random.choice(empty_positions)
                # Update our internal board
                board[move] = "me"
                # Send the move to the referee
                print(move, flush=True)
                print(f"I moved: {move}", file=sys.stderr)

        except EOFError:
            break

if __name__ == "__main__":
    main()
```

2. Run a game with two instances of your random player:

```bash
cs4341-referee tictactoe -p "python random_player.py" --visual
```

This will open a web browser with a visualization of the game. You'll see the two players making random moves until one wins or the game ends in a draw.

## Running a Lasker Morris Game

Let's run a Lasker Morris game with the same random player strategy:

1. Create a file called `random_lasker_player.py`:

```python
import sys
import random

def main():
    # Read initial color (blue or orange)
    color = input().strip()
    print(f"I am the {color} player", file=sys.stderr)

    # Track pieces in hand
    pieces_in_hand = 10

    # Track board state (simplified)
    board = {}

    while True:
        try:
            # Read opponent's move or game start
            game_input = input().strip()

            # If this isn't the first move and not the end game message
            if game_input and game_input != "END":
                print(f"Opponent moved: {game_input}", file=sys.stderr)
                # Parse opponent's move
                parts = game_input.split()
                # Update our board state based on opponent's move
                # (Implementation simplified for this example)

            # Generate a move
            if pieces_in_hand > 0:
                # If we have pieces in hand, place one
                # Choose a random valid position (avoiding invalid fields)
                valid_positions = ['a1', 'a4', 'a7', 'b2', 'b4', 'b6', 'c3',
                                  'c4', 'c5', 'd1', 'd2', 'd3', 'd5', 'd6',
                                  'd7', 'e3', 'e4', 'e5', 'f2', 'f4', 'f6',
                                  'g1', 'g4', 'g7']

                # Filter out occupied positions
                valid_positions = [pos for pos in valid_positions if pos not in board]

                target = random.choice(valid_positions)
                move = f"h1 {target} r0"  # h1 for hand, r0 for no capture
                pieces_in_hand -= 1
            else:
                # For simplicity, we'll just make a random move
                # In a real player, you'd implement proper movement rules
                move = "h1 d1 r0"  # Placeholder move

            # Send the move to the referee
            print(move, flush=True)
            print(f"I moved: {move}", file=sys.stderr)

        except EOFError:
            break

if __name__ == "__main__":
    main()
```

2. Run a Lasker Morris game:

```bash
cs4341-referee laskermorris -p1 "python random_lasker_player.py" -p2 "python random_lasker_player.py" --visual
```

## Next Steps

Now that you've run your first games, you can:

1. Improve your player implementations with actual game strategy
2. Explore the referee system's features and options
3. Set up a tournament to test your AI against others

Check out the [Common Options](common-options.md) guide to learn about the various configuration options available for running games.
