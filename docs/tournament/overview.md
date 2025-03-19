# Tournament Overview

The CS4341 Game Referee includes a powerful tournament system for organizing and running competitions between AI players. This system allows for multi-round tournaments with different formats, automated match scheduling, and comprehensive results tracking.

## Introduction

The tournament system is built as a separate Rust application that integrates with the game referee. It provides:

- **Multi-round tournaments**: Progress through preliminary, quarterfinal, semifinal, and final rounds
- **Group management**: Organize players into groups for round-robin play
- **Match scheduling**: Automatically schedule matches between players
- **Result tracking**: Record and analyze match outcomes
- **Statistics**: Calculate standings, win rates, and other performance metrics
- **Reporting**: Generate detailed tournament reports

## Tournament Structure

The tournament system supports a flexible competition structure:

### Rounds

A tournament typically consists of multiple rounds:

1. **First Round**: Initial group stage with all participants
2. **Second Round**: Qualified players from the first round
3. **Third Round**: Qualified players from the second round
4. **Fourth Round**: Final qualifying round
5. **Final Round**: Championship and placement matches

### Groups

Within each round, players are organized into groups:

- Each group contains a set of players who compete against each other
- Players in a group typically play a round-robin format (everyone plays against everyone)
- Top performers from each group advance to the next round
- Group assignment can be predefined or randomized

### Matches

Each match consists of:

- Two players competing in a specific game
- The referee managing the game rules and determining the winner
- Result recording for tournament standings

### Advancement

Players advance through the tournament based on performance:

- Typically, the top 2 players from each group advance to the next round
- Tiebreakers can be used when multiple players have the same number of points
- The final round determines the overall tournament rankings

## Points System

The tournament uses a standard points system:

- **Win**: 2 points
- **Draw**: 1 point
- **Loss**: 0 points

Players are ranked within their groups based on total points earned.

## Tournament Runner

The tournament runner is a Rust application located in the `tournament/` directory. It manages the entire tournament process:

1. **Configuration**: Reads tournament settings from a TOML file
2. **Initialization**: Sets up groups and schedules matches
3. **Execution**: Runs matches using the referee
4. **Progression**: Advances players between rounds
5. **Results**: Records and reports tournament outcomes

## Key Features

### Automated Match Execution

The tournament runner automatically:

- Starts referee processes for each match
- Provides player commands to the referee
- Captures and parses match results
- Handles timeouts and errors

### Randomization

The tournament supports randomization for fair competition:

- Random group assignments
- Random player order within matches
- Random color/symbol assignment

### Comprehensive Reporting

The tournament generates detailed reports:

- Match results for each round
- Group standings
- Player statistics
- Tournament progression
- Final rankings

### Error Handling

The tournament system includes robust error handling:

- Recovery from failed matches
- Logging of errors and exceptions
- Continuation despite individual match failures

## Visualization

While the tournament itself runs in the console, individual matches can use the referee's web visualization:

- View real-time match progress
- Analyze player strategies
- Understand game outcomes

## Usage Scenarios

The tournament system is designed for various scenarios:

### Classroom Competitions

- Organize competitions between student AI implementations
- Evaluate relative performance of different algorithms
- Provide a fair testing environment

### Algorithm Testing

- Compare different AI approaches in a structured environment
- Measure performance across multiple matches
- Identify strengths and weaknesses

### Research

- Run experiments with different AI techniques
- Collect comprehensive performance data
- Analyze strategic patterns

## Example Tournament

Here's an example of how a tournament might progress:

1. **First Round**:

   - 32 players divided into 8 groups of 4
   - Round-robin play within each group
   - Top 2 from each group advance (16 players)

2. **Second Round**:

   - 16 players divided into 4 groups of 4
   - Round-robin play within each group
   - Top 2 from each group advance (8 players)

3. **Third Round**:

   - 8 players divided into 2 groups of 4
   - Round-robin play within each group
   - Top 2 from each group advance (4 players)

4. **Fourth Round**:

   - 4 players in a single group
   - Round-robin play to determine rankings
   - All players advance to final placement matches

5. **Final Round**:
   - 1st vs 2nd: Championship match
   - 3rd vs 4th: Third-place match

The result is a comprehensive tournament that tests players against multiple opponents and provides a clear ranking of their performance.

See the [Tournament Configuration](configuration.md) and [Running Tournaments](running.md) guides for more details on setting up and running tournaments.
