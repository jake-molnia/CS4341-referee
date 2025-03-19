# Adding New Games

This guide walks through the process of adding a new game to the CS4341 Game Referee system. We'll use a hypothetical game called "Connect4" as an example.

## Step 1: Create Game Player Class

First, define a player class for your game in `src/core/players.py`:

```python
class Connect4Player(AbstractPlayer):
    """Player implementation for Connect4 game."""

    def __init__(self, command: str, color: str, log: bool = False, debug: bool = False):
        super().__init__(command, log, debug)
        self.color = color  # "red" or "yellow"

    def get_color(self) -> str:
        return self.color

    def is_red(self) -> bool:
        return self.color == "red"

    def is_yellow(self) -> bool:
        return self.color == "yellow"
```

## Step 2: Create Game Configuration

Add configuration for your game in `src/config.py`:

```python
@dataclass(frozen=True)
class Connect4Config(GameConfig):
    BOARD_WIDTH: Final[int] = 7
    BOARD_HEIGHT: Final[int] = 6
    DEFAULT_RANDOM_ASSIGNMENT: Final[bool] = True
```

## Step 3: Implement Game Logic

Create the main game class in `src/core/games.py`:

```python
class Connect4(AbstractGame):
    """Implementation of Connect4 game."""

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
    ):
        # Initialize game settings
        self.move_timeout = timeout + 0.5
        self.debug = debug
        self.port = port
        self.board = [[None for _ in range(Connect4Config.BOARD_WIDTH)]
                     for _ in range(Connect4Config.BOARD_HEIGHT)]
        self.moves_history = []

        # Initialize players with randomly assigned colors
        colors = ["red", "yellow"]
        if select_rand:
            random.shuffle(colors)

        player1 = Connect4Player(player1_command, colors[0], logging, debug)
        player2 = Connect4Player(player2_command, colors[1], logging, debug)
        super().__init__(player1, player2)

        # Initialize visualization
        self.visual = visual
        self.web = self._create_web_interface() if visual else None

    def _create_web_interface(self):
        from .web import Connect4Web
        return Connect4Web(self)

    def initialize_game(self) -> None:
        """Initialize the game state."""
        # Start player processes
        self._player1.start()
        self._player2.start()

        # Start web server if visualization enabled
        if self.visual and self.web:
            self.web.start_web_server(self.port)

        # Send initial color information to players
        self._player1.write(self._player1.get_color())
        self._player2.write(self._player2.get_color())

    def make_move(self, move: str) -> bool:
        """Process a player's move."""
        try:
            # Validate column number (0-6)
            column = int(move.strip())
            if column < 0 or column >= Connect4Config.BOARD_WIDTH:
                return False

            # Find the first empty spot in the column (bottom to top)
            for row in range(Connect4Config.BOARD_HEIGHT - 1, -1, -1):
                if self.board[row][column] is None:
                    # Place the piece
                    self.board[row][column] = self.current_player.get_color()
                    self.moves_history.append((column, row))
                    return True

            # Column is full
            return False

        except ValueError:
            # Not a valid integer
            return False

    def _check_winner(self) -> Optional[str]:
        """Check if there's a winner."""
        # Check horizontal, vertical, and diagonal win conditions
        # (implementation details omitted for brevity)
        pass

    def _is_board_full(self) -> bool:
        """Check if the board is completely full."""
        return all(cell is not None for row in self.board for cell in row)

    def determine_winner(self) -> Optional[Connect4Player]:
        """Determine if there's a winner or draw."""
        winning_color = self._check_winner()
        if winning_color:
            self._is_game_over = True
            return (
                self._player1 if self._player1.get_color() == winning_color
                else self._player2
            )

        if self._is_board_full():
            self._is_game_over = True
            return None

        return None

    def _get_move_with_timeout(self) -> Optional[str]:
        """Get a move from the current player with timeout."""
        with ThreadPoolExecutor(max_workers=1) as executor:
            try:
                future = executor.submit(self.current_player.read)
                return future.result(timeout=self.move_timeout)
            except TimeoutError:
                return None

    def run_game(self) -> Optional[Connect4Player]:
        """Run the main game loop."""
        while not self.is_game_over:
            # Get move from current player
            move = self._get_move_with_timeout()

            # Handle timeout or invalid move
            if move is None or not self.make_move(move):
                self._is_game_over = True
                winner = self._player2 if self.current_player == self._player1 else self._player1
                return winner

            # Send move to other player
            other_player = self._player2 if self.current_player == self._player1 else self._player1
            other_player.write(move)

            # Check for winner
            winner = self.determine_winner()
            if winner is not None:
                return winner
            elif self._is_board_full():
                return None

            self.switch_player()

        return None
```

## Step 4: Implement Web Interface

Create a web interface in `src/core/web.py`:

```python
class Connect4Web(WebGame):
    """Web interface for Connect4 game."""

    def __init__(self, game):
        super().__init__(GameConfig.WEB_TEMPLATE_FOLDER)
        self.game = game
        self.game_history = []
        self.end_message = None

    def get_game_state_json(self):
        """Return current game state as JSON."""
        game_data = {
            "board": self.game.board,
            "currentPlayer": self.game.current_player.get_color(),
            "isGameOver": self.game.is_game_over,
            "history": self.game.moves_history,
            "endMessage": self.end_message if self.game.is_game_over else None,
        }
        return jsonify(game_data)

    def get_index(self):
        """Render template with game state data."""
        game_data = {
            "board": self.game.board,
            "currentPlayer": self.game.current_player.get_color(),
            "isGameOver": self.game.is_game_over,
            "history": self.game.moves_history,
            "endMessage": self.end_message if self.game.is_game_over else None,
        }
        return render_template("./connect4/index.html", game_data=game_data)
```

## Step 5: Create HTML Template

Create a template in `src/web/connect4/index.html` for visualization:

```html
<!DOCTYPE html>
<html lang="en">
  <head>
    <meta charset="UTF-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1.0" />
    <title>Connect4 Game</title>
    <style>
      /* CSS styles for Connect4 board */
      body {
        font-family:
          system-ui,
          -apple-system,
          sans-serif;
        background: #f8fafc;
        color: #475569;
        padding: 2rem;
      }
      .board {
        display: grid;
        grid-template-columns: repeat(7, 50px);
        grid-template-rows: repeat(6, 50px);
        gap: 5px;
        background: #2563eb;
        padding: 10px;
        border-radius: 10px;
      }
      .cell {
        width: 50px;
        height: 50px;
        background: white;
        border-radius: 50%;
      }
      .red {
        background: #ef4444;
      }
      .yellow {
        background: #eab308;
      }
      /* Additional styles omitted for brevity */
    </style>
  </head>
  <body>
    <div class="container">
      <header>
        <h1>Connect4</h1>
        <p>Part of the CS4341 Referee Implementation</p>
      </header>

      <div class="game-container">
        <div class="board" id="board">
          <!-- Board will be populated by JavaScript -->
        </div>

        <div class="controls">
          <div class="status" id="currentPlayer">
            Current Player: <span id="player"></span>
          </div>
          <!-- Additional controls -->
        </div>
      </div>
    </div>

    <script>
      // JavaScript for the Connect4 board and game logic
      let gameState = {{ game_data|tojson|safe }};

      function updateBoard() {
          const board = document.getElementById('board');
          board.innerHTML = '';

          for (let row = 0; row < gameState.board.length; row++) {
              for (let col = 0; col < gameState.board[row].length; col++) {
                  const cell = document.createElement('div');
                  cell.className = 'cell';

                  if (gameState.board[row][col] === 'red') {
                      cell.classList.add('red');
                  } else if (gameState.board[row][col] === 'yellow') {
                      cell.classList.add('yellow');
                  }

                  board.appendChild(cell);
              }
          }
      }

      async function fetchGameState() {
          try {
              const response = await fetch('/game-state');
              const data = await response.json();
              gameState = data;
              updateBoard();
          } catch (error) {
              console.error('Error fetching game state:', error);
          }
      }

      updateBoard();
      setInterval(fetchGameState, 1000);
    </script>
  </body>
</html>
```

## Step 6: Add CLI Command

Add a CLI command in `src/cli/commands.py`:

```python
@click.command(name="connect4")
@click.option("--player1", "-p1", prompt="Enter Player 1 command", help="Command to run Player 1.")
@click.option("--player2", "-p2", prompt="Enter Player 2 command", help="Command to run Player 2.")
@click.option("--visual/--no-visual", "-v/-nv", default=Connect4Config.DEFAULT_VISUALIZATION,
              help="Enable/disable game visualization")
@click.option("--random-assignment/--no-random-assignment", "-r/-nr",
              default=Connect4Config.DEFAULT_RANDOM_ASSIGNMENT, help="Enable/disable random selection of first player")
@click.option("--timeout", "-t", type=int, default=Connect4Config.DEFAULT_TIMEOUT,
              help="Timeout in seconds for each player's move")
@click.option("--port", type=int, default=GameConfig.DEFAULT_WEB_PORT,
              help="Port for visualization webserver")
@click.option("--log/--no-log", "-l/-nl", default=Connect4Config.DEFAULT_LOGGING,
              help="Enable/disable logging")
@click.option("--debug/--no-debug", "-d/-nd", default=Connect4Config.DEFAULT_DEBUG,
              help="Enable/disable debug output")
def start_connect4(player1, player2, visual, random_assignment, timeout, port, log, debug):
    """🎮 Start a new game of Connect4!"""
    try:
        game = Connect4(
            player1_command=player1,
            player2_command=player2,
            visual=visual,
            select_rand=random_assignment,
            timeout=timeout,
            debug=debug,
            logging=log,
            port=port
        )
        winner = game.run_game()
        _handle_game_result(winner, visual, game)

    except Exception as e:
        click.echo(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")
        raise click.Abort()
```

## Step 7: Register CLI Command

Register your command in `src/cli/parser.py`:

```python
def create_cli() -> click.Group:
    """Create the main CLI group with all commands"""
    @click.group()
    @click.version_option("1.1.1")
    def cli():
        pass

    cli.add_command(start_game)      # Lasker Morris
    cli.add_command(start_tictactoe)
    cli.add_command(start_connect4)  # Add your new command here

    return cli
```

## Step 8: Update Imports

Add the necessary imports in `src/core/__init__.py`:

```python
from .abstract import AbstractGame, AbstractPlayer, WebGame
from .games import LaskerMorris, TicTacToe, Connect4
from .players import LaskerPlayer, TicTacToePlayer, Connect4Player
from .utils import BoardUtils, GameError, GameLogger, InvalidMoveError, TimeoutError
from .web import LaskerMorrisWeb, TicTacToeWeb, Connect4Web

__all__ = [
    "AbstractGame", "AbstractPlayer", "WebGame",
    "LaskerPlayer", "TicTacToePlayer", "Connect4Player",
    "LaskerMorris", "TicTacToe", "Connect4",
    "LaskerMorrisWeb", "TicTacToeWeb", "Connect4Web",
    "GameError", "InvalidMoveError", "TimeoutError",
    "GameLogger", "BoardUtils"
]
```

## Step 9: Create Tests

Create tests in `tests/game/test_connect4.py`:

```python
import unittest
from unittest.mock import Mock, patch

from src.core.games import Connect4

class TestConnect4(unittest.TestCase):
    @patch("subprocess.Popen")
    def setUp(self, mock_popen) -> None:
        """Set up test environment before each test."""
        # Mock subprocess.Popen
        mock_process = Mock()
        mock_process.stdout.readline.return_value = b"3\n"  # Middle column
        mock_process.poll.return_value = None
        mock_popen.return_value = mock_process

        with patch("random.shuffle") as mock_shuffle:
            # Ensure consistent color assignment for tests
            mock_shuffle.side_effect = lambda x: x
            self.game = Connect4("player1", "player2", visual=False)

        # Mock the players after initialization
        self.game._player1 = Mock()
        self.game._player2 = Mock()
        self.game._player1.get_color.return_value = "red"
        self.game._player2.get_color.return_value = "yellow"
        self.game._current_player = self.game._player1

    def test_initialization(self) -> None:
        """Test game initialization."""
        self.assertEqual(len(self.game.board), 6)  # 6 rows
        self.assertEqual(len(self.game.board[0]), 7)  # 7 columns
        self.assertEqual(self.game.current_player.get_color(), "red")

    def test_make_move(self) -> None:
        """Test making valid and invalid moves."""
        # Valid move in middle column
        self.assertTrue(self.game.make_move("3"))
        self.assertEqual(self.game.board[5][3], "red")  # Bottom row, middle column

        # Test more cases...

    # Additional test methods...
```

## Step 10: Document the New Game

Create documentation in `docs/games/connect4.md`:

```markdown
# Connect4

Connect4 is a two-player connection game where players take turns dropping colored discs into a vertically suspended grid. The objective is to connect four of one's own discs of the same color consecutively vertically, horizontally, or diagonally before the opponent.

## Rules

- Players take turns dropping their colored discs into a 7×6 grid
- The pieces fall straight down, occupying the lowest available position in the column
- The first player to connect four of their discs horizontally, vertically, or diagonally wins
- The game is a draw if the grid fills completely without a winner

## Player Communication

### Game Start

- First player receives: `"red"`
- Second player receives: `"yellow"`

### Move Format
```

<column>
Example: "3" (center column, 0-indexed)
```

## Running Connect4

```bash
cs4341-referee connect4 -p1 "python player1.py" -p2 "python player2.py" --visual
```

## Python Player Template

```python
import sys

def main():
    # Read initial color
    color = input().strip()  # "red" or "yellow"

    while True:
        try:
            # Read opponent's move or game start
            game_input = input().strip()

            # If this is the first move and you're the first player,
            # game_input will be empty

            # Your move logic here: choose column 0-6
            # For example, always choose the middle column:
            move = "3"

            # Send move to referee
            print(move, flush=True)

        except EOFError:
            break

if __name__ == "__main__":
    main()
```

## Strategy Tips

1. **Center control**: The center column provides the most connection opportunities
2. **Blocking**: Prevent your opponent from forming connections
3. **Two threats**: Create positions where you have two potential winning moves
4. **Look ahead**: Plan several moves ahead to create winning opportunities

```

## Key Implementation Details

When implementing a new game, focus on these key aspects:

1. **Game rules**: Ensure all game rules are correctly enforced
2. **Player communication**: Define clear protocols for player input/output
3. **Error handling**: Properly handle timeouts, invalid moves, and other issues
4. **Visualization**: Create an intuitive web interface for game monitoring
5. **Testing**: Write comprehensive tests for your game implementation

By following this template, you can add any turn-based board game to the referee system.
```
