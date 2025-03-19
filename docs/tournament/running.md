# Running Tournaments

This guide explains how to run tournaments using the CS4341 Tournament Runner, including command-line options, execution modes, and managing tournament results.

## Prerequisites

Before running a tournament:

1. Ensure the CS4341 Game Referee is installed
2. Prepare your tournament configuration file (see [Tournament Configuration](configuration.md))
3. Ensure all player programs are accessible and executable
4. Make sure the tournament runner is properly built

## Running the Tournament

The tournament runner is a Rust application located in the `tournament/` directory. You can run it with:

```bash
cd tournament
cargo run -- tournament.toml
```

Where `tournament.toml` is your tournament configuration file.

## Command-Line Options

The tournament runner supports several command-line options:

```bash
cargo run -- [options] <config_file>
```

### Logging Options

| Option          | Description                  | Default |
| --------------- | ---------------------------- | ------- |
| `--quiet`, `-q` | Minimal output (errors only) | Off     |
| `--debug`, `-d` | Enable debug output          | Off     |
| `--no-log`      | Disable logging completely   | Off     |

### Tournament Options

| Option                 | Description                                | Default |
| ---------------------- | ------------------------------------------ | ------- |
| `--resume`             | Resume a previously interrupted tournament | Off     |
| `--skip-validation`    | Skip validation of player executables      | Off     |
| `--random-seed <seed>` | Set random seed for reproducibility        | None    |

### Example Commands

Run with minimal output:

```bash
cargo run -- --quiet tournament.toml
```

Run with debug output:

```bash
cargo run -- --debug tournament.toml
```

Resume an interrupted tournament:

```bash
cargo run -- --resume tournament.toml
```

## Tournament Execution Process

When running a tournament, the system follows these steps:

1. **Configuration Loading**: The tournament configuration is parsed from the TOML file
2. **Player Validation**: Checks that all player commands are valid
3. **Group Setup**: Creates groups based on configuration or automatically
4. **Match Scheduling**: Schedules all matches for the first round
5. **First Round Execution**: Runs all matches in the first round
6. **Advancement**: Determines which players advance to the next round
7. **Subsequent Rounds**: Repeats the process for each tournament round
8. **Final Placement**: Determines final rankings and generates results

### Round Execution

For each round, the tournament runner:

1. Creates groups for the round
2. Schedules matches within each group
3. Executes all matches
4. Calculates standings and winners
5. Determines which players advance

### Match Execution

For each match, the tournament runner:

1. Starts the referee process with the appropriate game
2. Provides player commands to the referee
3. Captures the match result
4. Updates tournament standings
5. Records the result in the CSV file

## Tournament Progress Display

During the tournament, the runner displays:

### Group Information

At the start of each round:

```
=== Starting First Round ===

Group A: player1, player2, player3, player4
Group B: player5, player6, player7, player8
...
```

### Match Progress

For each match:

```
Running match: player1 vs player2
player1 wins!
```

### Round Standings

After each round:

```
=== Current Standings (First Round) ===

Group A:
Player      W    L    D    Pts
player1     3    0    0    6.0
player2     2    1    0    4.0
player3     1    2    0    2.0
player4     0    3    0    0.0

...

Advancing to next round:
From Group A: player1, player2
From Group B: player5, player6
...
```

### Final Results

At the end of the tournament:

```
=== TOURNAMENT FINAL RESULTS ===

🏆 CHAMPION: player1
🥈 RUNNER-UP: player6
🥉 THIRD PLACE: player2
    FOURTH PLACE: player5

Tournament completed! Full results saved in tournament_results.csv
```

## Tournament Results

The tournament runner generates a CSV file with detailed results:

```
Round,Group,Game Number,Player 1,Player 2,Winner,Is Draw,Error
First Round,Group A,1,player1,player2,player1,false,
First Round,Group A,2,player3,player4,player3,false,
...
```

This file contains:

- Round name
- Group name
- Game number within the group
- Player identifiers
- Winner (if any)
- Whether the game was a draw
- Any errors that occurred

## Handling Errors

The tournament runner includes robust error handling:

- **Match Errors**: If a match fails, the runner logs the error and continues with the next match
- **Player Errors**: If a player process fails, the match is awarded to the opponent
- **Referee Errors**: If the referee process fails, the match is marked as an error and skipped
- **Tournament Interruption**: If the tournament is interrupted, it can be resumed from the last completed match

## Resuming Tournaments

If a tournament is interrupted, you can resume it:

```bash
cargo run -- --resume tournament.toml
```

The runner will:

1. Load the existing results from `tournament_results.csv`
2. Determine the last completed match
3. Continue from the next scheduled match

## Tournament Visualization

While the tournament itself runs in the console, individual matches can use the referee's web visualization if the `visual` setting is enabled:

```toml
[settings]
visual = true
port = 8080
```

This allows observers to watch matches in real-time via a web browser.

## Advanced Usage

### Running Multiple Tournaments

To run multiple tournaments sequentially:

```bash
cargo run -- tournament1.toml && cargo run -- tournament2.toml
```

### Tournament Automation

You can integrate the tournament runner into scripts or CI/CD pipelines:

```bash
#!/bin/bash
# Run tournament and capture exit code
cargo run -- --quiet tournament.toml
if [ $? -ne 0 ]; then
    echo "Tournament failed!"
    exit 1
fi

# Process results
python3 analyze_results.py
```

### Custom Result Analysis

After the tournament, you can analyze the results with custom scripts:

```python
import pandas as pd

# Load tournament results
df = pd.read_csv('tournament_results.csv')

# Analyze player performance
player_stats = {}
for _, row in df.iterrows():
    # Process each match result
    # ...

# Generate custom reports
# ...
```

## Performance Considerations

For large tournaments:

- Disable visualization (`visual = false`)
- Use shorter timeouts to speed up matches
- Use the `--quiet` flag to reduce console output
- Consider running the tournament on a powerful machine with sufficient RAM

## Troubleshooting

If you encounter issues:

1. **No matches running**: Check that player commands are correct and executable
2. **Slow execution**: Consider disabling visualization and reducing timeouts
3. **Referee errors**: Ensure the referee is properly installed and accessible
4. **CSV parsing errors**: Check if the results file is corrupted (backup before resuming)
5. **Memory issues**: For very large tournaments, consider splitting into smaller tournaments

## Next Steps

After running a tournament, you can:

1. Analyze the results to identify the strongest players
2. Use the match history to improve player algorithms
3. Run additional tournaments with modified parameters
4. Generate reports and visualizations from the results data
