# Common Options

The CS4341 Game Referee system provides a variety of command-line options to customize game execution. This guide covers the common options available for all games, as well as game-specific options.

## Global Options

These options work with all supported games:

| Option                                         | Short      | Description                               | Default        |
| ---------------------------------------------- | ---------- | ----------------------------------------- | -------------- |
| `--visual / --no-visual`                       | `-v / -nv` | Enable/disable web visualization          | Enabled        |
| `--random-assignment / --no-random-assignment` | `-r / -nr` | Randomize player colors/symbols           | Varies by game |
| `--timeout`                                    | `-t`       | Move timeout in seconds                   | 5              |
| `--log / --no-log`                             | `-l / -nl` | Enable/disable detailed logging           | Disabled       |
| `--debug / --no-debug`                         | `-d / -nd` | Enable/disable debug output               | Disabled       |
| `--port`                                       |            | Specify the port for visualization server | 8000           |

## Visualization

When `--visual` is enabled (the default), the referee starts a web server to visualize the game:

```bash
cs4341-referee tictactoe -p "python player.py" --visual
```

The visualization is available at `http://localhost:8000` by default. You can customize the port:

```bash
cs4341-referee tictactoe -p "python player.py" --port 8080
```

## Timeouts

Use the timeout option to change how long players have to respond with a move:

```bash
cs4341-referee tictactoe -p "python player.py" -t 10  # 10 seconds per move
```

If a player doesn't respond within the timeout period, they forfeit their turn or the game (depending on the specific game rules).

## Random Assignment

By default, the referee assigns colors/symbols randomly for fairness in competitive settings. You can disable this to have predictable assignments:

```bash
cs4341-referee laskermorris -p1 "python player1.py" -p2 "python player2.py" --no-random-assignment
```

With random assignment disabled:

- First player gets X in Tic-tac-toe
- First player gets blue in Lasker Morris

## Logging and Debugging

Enable logging to record the communication between the referee and players:

```bash
cs4341-referee tictactoe -p "python player.py" --log
```

This creates a log file with detailed communication records.

For even more information, enable debug mode:

```bash
cs4341-referee tictactoe -p "python player.py" --debug
```

In debug mode, the referee prints additional information to the console, including a text representation of the game board after each move.

## Game-Specific Options

### Tic-tac-toe

| Option      | Short | Description                                                            |
| ----------- | ----- | ---------------------------------------------------------------------- |
| `--player`  | `-p`  | Command to run the player program                                      |
| `--player2` | `-p2` | Command for second player (optional, defaults to same as first player) |

Example:

```bash
cs4341-referee tictactoe -p "python player1.py" -p2 "python player2.py"
```

Without `-p2`, the system uses the same player against itself:

```bash
cs4341-referee tictactoe -p "python player.py"  # Self-play
```

### Lasker Morris

| Option      | Short | Description               |
| ----------- | ----- | ------------------------- |
| `--player1` | `-p1` | Command for first player  |
| `--player2` | `-p2` | Command for second player |

Example:

```bash
cs4341-referee laskermorris -p1 "python player1.py" -p2 "python player2.py"
```

Unlike Tic-tac-toe, Lasker Morris requires specifying both players.

## Examples

### Running a tournament match with logging:

```bash
cs4341-referee tictactoe -p "python team1_player.py" -p2 "python team2_player.py" --log --timeout 3
```

### Testing a player against itself with increased timeout:

```bash
cs4341-referee tictactoe -p "python my_player.py" -t 10
```

### Running a headless game (no visualization):

```bash
cs4341-referee laskermorris -p1 "python player1.py" -p2 "python player2.py" --no-visual
```

### Debugging a player with fixed colors:

```bash
cs4341-referee laskermorris -p1 "python my_player.py" -p2 "python opponent.py" --debug --no-random-assignment
```

## Notes

- Player commands can include arguments, e.g., `python player.py --strategy defensive`
- For Windows, you might need to use `python` or `py` depending on your setup
- If your player is written in a language other than Python, just provide the appropriate command to run it
