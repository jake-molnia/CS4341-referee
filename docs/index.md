# CS4341 Game Referee

[![Build and Test](https://github.com/jake-molnia/cs4341-referee/actions/workflows/build.yml/badge.svg)](https://github.com/jake-molnia/cs4341-referee/actions/workflows/build.yml)
[![codecov](https://codecov.io/gh/jake-molnia/cs4341-referee/branch/main/graph/badge.svg)](https://codecov.io/gh/{username}/cs4341-referee)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)

A modern game referee system developed for WPI's CS4341 - Introduction to Artificial Intelligence course, taught by Professor Ruiz in C Term 2025. This referee system powers both Tic-tac-toe and Lasker Morris competitions, providing a robust platform for AI development and testing.

## Overview

The CS4341 Game Referee is designed to:

- Enforce game rules for various two-player board games
- Manage player communication via standard input/output
- Provide a rich web visualization for game monitoring
- Support tournament management with a dedicated runner

Currently, the system supports:

- **Tic-tac-toe**: The classic 3x3 grid game
- **Lasker Morris**: A variant of Nine Men's Morris with special movement rules

## Key Features

- **Modular architecture**: Easy to extend with new games
- **Real-time visualization**: Web-based interface for monitoring games
- **Robust communication**: Manages external player processes
- **Error handling**: Gracefully handles timeouts, crashes, and invalid moves
- **Tournament support**: Automated multi-round competition management

## Quick Start

```bash
# Install the referee
pip install git+https://github.com/jake-molnia/cs4341-referee.git

# Run a Tic-tac-toe game
cs4341-referee tictactoe -p "python your_player.py" --visual

# Run a Lasker Morris game
cs4341-referee laskermorris -p1 "python player1.py" -p2 "python player2.py" --visual
```

## Project Structure

```
cs4341-referee/
├── src/                 # Source code
│   ├── cli/             # Command line interface
│   ├── core/            # Core game logic
│   │   ├── abstract.py  # Base game and player classes
│   │   ├── games.py     # Game implementations
│   │   ├── players.py   # Player implementations
│   │   ├── utils.py     # Utility functions
│   │   └── web.py       # Web interface
│   └── web/             # Web templates
├── tests/               # Test suite
└── tournament/          # Tournament runner
```

Visit the [Getting Started](getting-started/installation.md) section to begin using the CS4341 Game Referee.
