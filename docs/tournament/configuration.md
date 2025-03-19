# Tournament Configuration

The CS4341 Tournament Runner uses a TOML configuration file to define tournament settings, games, and participants. This guide explains the configuration options and provides examples for setting up different tournament types.

## Configuration File Structure

The tournament configuration file (`tournament.toml`) has the following main sections:

1. **Game Settings**: Defines which game to use and its settings
2. **Group Definitions**: Optional predefined groups
3. **Agent Definitions**: Players participating in the tournament

Here's a basic structure:

```toml
# Game type and settings
game = "tictactoe"

[settings]
timeout = 3
visual = false
random_assignment = true
debug = false
port = 8000

# Optional predefined groups
[groups]
"Group A" = ["player1", "player2", "player3", "player4"]
"Group B" = ["player5", "player6", "player7", "player8"]

# Player definitions
[agents]
player1 = "python3 team1/player.py"
player2 = "python3 team2/player.py"
player3 = "java -jar team3/player.jar"
# ... more players
```

## Game Settings

### Game Type

The `game` field specifies which game to use for the tournament:

```toml
game = "tictactoe"  # Use Tic-tac-toe
```

or

```toml
game = "laskermorris"  # Use Lasker Morris
```

### Game Settings

The `[settings]` section defines game-specific settings:

```toml
[settings]
timeout = 5          # Move timeout in seconds
visual = false       # Disable visualization for faster tournament play
random_assignment = true  # Randomize player colors/symbols
debug = false        # Disable debug output
port = 8000          # Web visualization port (if enabled)
```

All settings are optional and will use defaults if not specified.

## Group Definitions

Groups can be predefined in the configuration or automatically created by the tournament runner.

### Predefined Groups

To predefine groups, use the `[groups]` section:

```toml
[groups]
"Group A" = ["player1", "player2", "player3", "player4"]
"Group B" = ["player5", "player6", "player7", "player8"]
```

Each group is defined as an array of player IDs.

### Automatic Group Creation

If you don't define groups, the tournament runner will automatically create them based on the number of players:

- For the first round, it creates up to 8 groups with roughly equal sizes
- Group assignments are randomized for fairness

## Agent Definitions

The `[agents]` section defines all players participating in the tournament:

```toml
[agents]
player1 = "python3 team1/player.py"
player2 = "python3 team2/player.py --strategy aggressive"
player3 = "java -jar team3/player.jar"
player4 = "node team4/player.js"
```

Each entry consists of:

- Player ID (e.g., `player1`)
- Command to run the player (e.g., `"python3 team1/player.py"`)

The command can include arguments and should match what you would use to run the player directly with the referee.

## Example Configurations

### Basic Tic-tac-toe Tournament

```toml
game = "tictactoe"

[settings]
timeout = 3
visual = false
random_assignment = true

[agents]
player1 = "python3 team1/player.py"
player2 = "python3 team2/player.py"
player3 = "python3 team3/player.py"
player4 = "python3 team4/player.py"
player5 = "python3 team5/player.py"
player6 = "python3 team6/player.py"
player7 = "python3 team7/player.py"
player8 = "python3 team8/player.py"
```

### Lasker Morris Tournament with Predefined Groups

```toml
game = "laskermorris"

[settings]
timeout = 10
visual = false
random_assignment = true

[groups]
"Group A" = ["team1", "team2", "team3", "team4"]
"Group B" = ["team5", "team6", "team7", "team8"]
"Group C" = ["team9", "team10", "team11", "team12"]
"Group D" = ["team13", "team14", "team15", "team16"]

[agents]
team1 = "python3 submissions/team1/player.py"
team2 = "python3 submissions/team2/player.py"
team3 = "python3 submissions/team3/player.py"
# ... more teams
```

### Mixed-Language Tournament

```toml
game = "tictactoe"

[settings]
timeout = 5
visual = true
port = 8080

[agents]
python_team = "python3 python_player.py"
java_team = "java -jar java_player.jar"
js_team = "node javascript_player.js"
cpp_team = "./cpp_player"
go_team = "./go_player"
rust_team = "./rust_player"
```

### Large Tournament with Performance Settings

```toml
game = "laskermorris"

[settings]
timeout = 3
visual = false
random_assignment = true
debug = false

# No predefined groups - tournament will create them automatically

[agents]
team01 = "python3 submissions/team01/player.py"
team02 = "python3 submissions/team02/player.py"
team03 = "python3 submissions/team03/player.py"
# ... many more teams
team32 = "python3 submissions/team32/player.py"
```

## Configuration Tips

### Performance Considerations

For faster tournament execution:

- Set `visual = false` to disable web visualization
- Use a shorter timeout (e.g., 3 seconds)
- Disable debug output with `debug = false`

### Group Balance

When defining groups manually:

- Keep group sizes equal when possible
- Aim for 4 players per group for standard round-robin play
- Ensure each player appears in exactly one group

### Command Formatting

Player commands should:

- Include the full path to the player executable/script
- Include necessary runtime (e.g., `python3`, `java`, `node`)
- Include any required arguments
- Use appropriate path separators for your OS

### Multiple Game Types

If you want to run tournaments for different games, create separate configuration files:

- `tictactoe_tournament.toml`
- `laskermorris_tournament.toml`

## Configuration Validation

The tournament runner validates your configuration and will report errors for:

- Missing required fields
- Invalid game types
- Unknown player references in groups
- Duplicate player assignments
- Invalid settings values

If errors are found, the tournament will not start until they are resolved.

## Environmental Variables

You can use environment variables in your configuration file using the `${VAR_NAME}` syntax:

```toml
[agents]
team1 = "python3 ${SUBMISSIONS_DIR}/team1/player.py"
```

This is useful for:

- Configuring paths that might change between environments
- Keeping sensitive information out of configuration files
- Setting up different tournament environments

## Next Steps

After creating your configuration file, proceed to [Running Tournaments](running.md) to learn how to execute the tournament.
