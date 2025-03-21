# Game Referee

[![Build and Test](https://github.com/jake-molnia/cs4341-referee/actions/workflows/build.yml/badge.svg)](https://github.com/jake-molnia/cs4341-referee/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/jake-molnia/cs4341-referee/branch/main/graph/badge.svg)](https://codecov.io/gh/{username}/cs4341-referee)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)

A modern game referee system developed for WPI's CS4341 - Introduction to Artificial Intelligence course, taught by Professor Ruiz in C Term 2025. This referee system powers both Tic-tac-toe and Lasker Morris competitions, providing a robust platform for AI development and testing.

## 📚 Documentation

Full documentation is available at: https://jake-molnia.github.io/CS4341-referee/

## 🚀 Quick Start

### Prerequisites

- Python 3.10 or higher ([Check your Python version](docs/checking-python-version.md))
- pip package manager ([Check pip installation](docs/checking-pip.md))
- git ([Check git installation](docs/checking-git.md))

### Installation

```bash
pip install git+https://github.com/jake-molnia/cs4341-referee.git
```

## 🎮 Running Games

### Tic-tac-toe

```bash
cs4341-referee tictactoe -p "python <your_own_player>.py" --visual
```

### Lasker Morris

```bash
cs4341-referee laskermorris -p1 "python <your_own_player>.py" -p2 "python <your_own_player>.py" --visual
```

## 🛠️ Command Line Options

### Common Options

| Flag                      | Description                                          | Default |
| ------------------------- | ---------------------------------------------------- | ------- |
| `-v, --visual`            | Enable web visualization                             | True    |
| `-r, --random-assignment` | Randomize player colors/symbols                      | True    |
| `-t, --timeout`           | Move timeout in seconds                              | 5       |
| `-l, --log`               | Enable detailed logging                              | False   |
| `-d, --debug`             | Enable debug output                                  | False   |
| `--port`                  | Specify the port the game visualization is hosted on | 8000    |

### Game-Specific Options

#### Tic-tac-toe

- `-p, --player`: Command to run the player program
- `-p2, --player2`: Optional command to run second player program (leave blank for self play)

#### Lasker Morris

- `-p1, --player1`: Command for first player
- `-p2, --player2`: Command for second player

## 🤖 Player Communication Protocol

Players communicate with the referee through standard input/output streams. Here's how it works:

### Game Start

- First player receives: `"blue"` (Lasker Morris) or `"X"` (Tic-tac-toe)
- Second player receives: `"orange"` (Lasker Morris) or `"O"` (Tic-tac-toe)

### Move Format

#### Tic-tac-toe

```
<column><row>
Example: "b2" (center position)
```

#### Lasker Morris

```
<source> <target> <remove>
Example: "h1 d1 r0" (place piece from hand)
Example: "d1 d2 e3" (move piece and capture)
```

### Python Player Template

```python
import sys

def main():
    # Read initial color/symbol
    player_id = input().strip()

    while True:
        try:
            # Read opponent's move or game start
            game_input = input().strip()

            # Your move logic here
            move = "your_move_here"

            # Send move to referee
            print(move, flush=True)

        except EOFError:
            break

if __name__ == "__main__":
    main()
```

## 🎯 Game Rules

### Tic-tac-toe

- 3x3 grid
- Players alternate placing X's and O's
- First to get three in a row wins
- Game ends in draw if board fills without winner

### Lasker Morris

- Players start with 10 pieces each
- Pieces can be placed from hand or moved on board
- Moving to adjacent positions only (except when player has 3 pieces)
- Forming three in a row (mill) allows capturing opponent's piece
- Player loses when reduced to fewer than 3 pieces
- Draw occurs if same position repeats 3 times

## 🖥️ Web Visualization

The referee includes a modern web interface that shows:

<div align="center">
  <img src="docs/images/tictactoe-viz.png" alt="Tic-tac-toe Visualization" width="600"/>
  <p><em>Tic-tac-toe game visualization showing move history and game state</em></p>
</div>

<div align="center">
  <img src="docs/images/laskermorris-viz.png" alt="Lasker Morris Visualization" width="600"/>
  <p><em>Lasker Morris game in progress with piece placement and capture visualization</em></p>
</div>

### Features:

- Real-time game state
- Move history with navigation
- Player information
- Game status and results

To use:

1. Start game with `--visual` flag
2. Open browser to displayed URL (typically `http://localhost:8000`)
3. Watch game progress in real-time

## 🔍 Error Handling

The referee handles various game situations:

- Invalid moves: Game ends, opponent wins
- Timeout violations: Player loses turn
- Communication errors: Game ends, opponent wins
- Protocol violations: Game ends, opponent wins

## 👥 Contributing

Contributions are welcome! Please feel free to submit issues and pull requests.

## 🙏 Acknowledgments

- Professor Ruiz - CS4341 Introduction to AI
- Contributing students and faculty

---

_This referee system is part of the CS4341 course at WPI. For course-specific questions, please contact the teaching team._
