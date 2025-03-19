use csv::Writer;
use log::{debug, info, warn, LevelFilter};
use rand::seq::SliceRandom;
use rand::thread_rng;
use serde::{Deserialize, Serialize};
use std::collections::HashMap;
use std::fs::File;
use std::process::{Command, Stdio};
use std::fs;
use toml;
use simplelog::{WriteLogger, Config};

#[derive(Debug, Deserialize)]
struct TournamentConfig {
    game: String,
    settings: Option<GameSettings>,
    groups: Option<HashMap<String, Vec<String>>>,
    agents: HashMap<String, String>,
}

#[derive(Debug, Deserialize, Clone)]
struct GameSettings {
    timeout: Option<i32>,
    visual: Option<bool>,
    random_assignment: Option<bool>,
    debug: Option<bool>,
    port: Option<i32>,
}

#[derive(Debug, Clone, Serialize)]
struct MatchResult {
    round: String,
    group: String,
    game_number: i32,
    player1: String,
    player2: String,
    winner: Option<String>,
    is_draw: bool,
    error: Option<String>,
}

#[derive(Debug, Clone)]
struct PlayerStats {
    name: String,
    wins: i32,
    losses: i32,
    draws: i32,
    points: f32,
}

impl PlayerStats {
    fn new(name: &str) -> Self {
        PlayerStats {
            name: name.to_string(),
            wins: 0,
            losses: 0,
            draws: 0,
            points: 0.0,
        }
    }

    fn add_result(&mut self, result: &MatchResult) {
        if result.is_draw {
            self.draws += 1;
            self.points += 1.0;
        } else if Some(self.name.clone()) == result.winner {
            self.wins += 1;
            self.points += 2.0;
        } else {
            self.losses += 1;
        }
    }
}

#[derive(Debug)]
struct TournamentManager {
    config: TournamentConfig,
    round_results: HashMap<String, Vec<MatchResult>>,
    current_round: String,
    csv_writer: Writer<File>,
    groups: HashMap<String, Vec<String>>,
    player_stats: HashMap<String, HashMap<String, HashMap<String, PlayerStats>>>,
}

impl TournamentManager {
    fn new(config_path: &str) -> Result<Self, Box<dyn std::error::Error>> {
        // Read and parse the tournament configuration
        let config_str = fs::read_to_string(config_path)?;
        let config: TournamentConfig = toml::from_str(&config_str)?;

        // Create the CSV writer for results
        let file = File::create("tournament_results.csv")?;
        let csv_writer = csv::Writer::from_writer(file);

        // Initialize round results
        let round_results = HashMap::new();

        let player_stats = HashMap::new();

        Ok(TournamentManager {
            config,
            round_results,
            current_round: "First Round".to_string(),
            csv_writer,
            groups: HashMap::new(),
            player_stats,
        })
    }

    fn initialize_groups(&mut self) {
        info!("Initializing tournament groups");

        // If groups are predefined in config, use them
        if let Some(predefined_groups) = &self.config.groups {
            self.groups = predefined_groups.clone();
            info!("Using predefined groups from config");
        } else {
            // Otherwise, create random groups for the first round
            let mut players: Vec<String> = self.config.agents.keys().cloned().collect();
            let mut rng = thread_rng();
            players.shuffle(&mut rng);

            let num_players = players.len();
            let target_groups = 8; // We want 8 groups for the first round

            // Ensure we don't create more groups than players
            let num_groups = std::cmp::min(target_groups, num_players);

            self.groups.clear();

            // Calculate base size and remainder
            let base_size = num_players / num_groups;
            let remainder = num_players % num_groups;

            let mut start = 0;
            for i in 0..num_groups {
                // Groups with index < remainder get one extra player
                let group_size = if i < remainder { base_size + 1 } else { base_size };
                let end = start + group_size;

                let group_name = format!("Group {}", (b'A' + i as u8) as char);
                let group_players = players[start..end].to_vec();

                self.groups.insert(group_name, group_players);

                start = end;
            }

            info!("Created random groups for First Round");
        }

        // Initialize player stats for this round
        let mut round_stats = HashMap::new();
        for (group, players) in &self.groups {
            let mut group_stats = HashMap::new();
            for player in players {
                let player_stats = PlayerStats::new(player);
                group_stats.insert(player.clone(), player_stats);
            }
            round_stats.insert(group.clone(), group_stats);
        }
        self.player_stats.insert(self.current_round.clone(), round_stats);

        // Log the groups
        for (group, players) in &self.groups {
            info!("{}: {}", group, players.join(", "));
        }
    }

    fn run_tournament(&mut self) -> Result<(), Box<dyn std::error::Error>> {
        // Initialize first round groups
        self.initialize_groups();
        self.write_csv_header()?;

        // Run First Round
        info!("Starting First Round");
        self.current_round = "First Round".to_string();
        self.run_round()?;
        let first_round_winners = self.determine_winners();

        // Run Second Round
        info!("Starting Second Round");
        self.current_round = "Second Round".to_string();
        self.setup_next_round(&first_round_winners, 4)?; // 4 groups of 4 teams each
        self.run_round()?;
        let second_round_winners = self.determine_winners();

        // Run Third Round
        info!("Starting Third Round");
        self.current_round = "Third Round".to_string();
        self.setup_next_round(&second_round_winners, 2)?; // 2 groups of 4 teams each
        self.run_round()?;
        let third_round_winners = self.determine_winners();

        // Run Fourth Round
        info!("Starting Fourth Round");
        self.current_round = "Fourth Round".to_string();
        self.setup_next_round(&third_round_winners, 1)?; // 1 group of 4 teams
        self.run_round()?;
        let fourth_round_results = self.determine_fourth_round_rankings();

        // Run Final Round
        info!("Starting Final Round");
        self.current_round = "Final Round".to_string();
        self.setup_finals(&fourth_round_results)?;
        self.run_round()?;

        // Print final results
        self.print_final_results();
        self.print_overall_stats();

        Ok(())
    }

    fn run_round(&mut self) -> Result<(), Box<dyn std::error::Error>> {
        let mut all_results = Vec::new();

        for (group_name, players) in &self.groups.clone() {
            info!("Running matches for {}: {}", group_name, players.join(", "));

            let mut game_number = 1;

            // Each player plays against every other player in their group
            for i in 0..players.len() {
                for j in (i+1)..players.len() {
                    // Play two matches with swapped positions
                    for swap in [false, true] {
                        let (player1, player2) = if swap {
                            (&players[j], &players[i])
                        } else {
                            (&players[i], &players[j])
                        };

                        info!("Match: {} vs {}", player1, player2);

                        // Run the match
                        let result = self.run_match(
                            &self.current_round,
                            group_name,
                            game_number,
                            player1,
                            player2,
                        )?;

                        // Record the result
                        self.record_result(&result)?;
                        all_results.push(result);

                        game_number += 1;
                    }
                }
            }
        }

        // Save the results for this round
        self.round_results.insert(self.current_round.clone(), all_results);
        self.update_player_stats();

        // Display current standings
        self.print_standings();

        Ok(())
    }

    fn run_match(
        &self,
        _round: &str,
        group: &str,
        game_number: i32,
        player1: &str,
        player2: &str,
    ) -> Result<MatchResult, Box<dyn std::error::Error>> {
        let p1_cmd = self.config.agents.get(player1).unwrap();
        let p2_cmd = self.config.agents.get(player2).unwrap();

        // Set up the command arguments based on the game type
        let settings = self.config.settings.clone().unwrap_or_else(|| {
            GameSettings {
                timeout: Some(5),
                visual: Some(false),
                random_assignment: Some(false),
                debug: Some(false),
                port: Some(8000),
            }
        });

        let mut cmd_args = Vec::new();

        // Determine which game to run
        let game_cmd = match self.config.game.as_str() {
            "tictactoe" => "tictactoe",
            "laskermorris" | "lasker_morris" | "lasker-morris" => "laskermorris",
            _ => {
                return Err(format!("Unsupported game type: {}", self.config.game).into());
            }
        };

        cmd_args.push(game_cmd.to_string());
        cmd_args.push("--player1".to_string());
        cmd_args.push(p1_cmd.clone());
        cmd_args.push("--player2".to_string());
        cmd_args.push(p2_cmd.clone());

        // Add optional settings
        if let Some(timeout) = settings.timeout {
            cmd_args.push("--timeout".to_string());
            cmd_args.push(timeout.to_string());
        }

        if let Some(visual) = settings.visual {
            if visual {
                cmd_args.push("--visual".to_string());
            } else {
                cmd_args.push("--no-visual".to_string());
            }
        } else {
            cmd_args.push("--no-visual".to_string()); // Default to no visual
        }

        if let Some(random) = settings.random_assignment {
            if random {
                cmd_args.push("--random-assignment".to_string());
            } else {
                cmd_args.push("--no-random-assignment".to_string());
            }
        }

        if let Some(debug) = settings.debug {
            if debug {
                cmd_args.push("--debug".to_string());
            } else {
                cmd_args.push("--no-debug".to_string());
            }
        }

        if let Some(port) = settings.port {
            cmd_args.push("--port".to_string());
            cmd_args.push(port.to_string());
        }

        // Log the command being executed
        let cmd_str = format!("uv run cs4341-referee {}", cmd_args.join(" "));
        debug!("Executing command: {}", cmd_str);

        // Run the command
        let output = Command::new("uv")
            .arg("run")
            .arg("cs4341-referee")
            .args(&cmd_args)
            .stdout(Stdio::piped())
            .stderr(Stdio::piped())
            .output()?;

        let stdout = String::from_utf8_lossy(&output.stdout).to_string();
        let stderr = String::from_utf8_lossy(&output.stderr).to_string();

        // Log the output
        debug!("Command stdout: {}", stdout);
        if !stderr.is_empty() {
            warn!("Command stderr: {}", stderr);
        }

        // Parse result to determine winner
        let mut result = self.parse_game_result(&stdout, &stderr, player1, player2);

        // Set the group and game number in the result
        result.group = group.to_string();
        result.game_number = game_number;

        info!("Match result: {} vs {} - Winner: {:?}, Draw: {}",
              player1, player2, result.winner, result.is_draw);

        Ok(result)
    }

    fn parse_game_result(
        &self,
        stdout: &str,
        stderr: &str,
        player1: &str,
        player2: &str,
    ) -> MatchResult {
        let mut result = MatchResult {
            round: self.current_round.clone(),
            group: String::new(), // Will be filled later
            game_number: 0,       // Will be filled later
            player1: player1.to_string(),
            player2: player2.to_string(),
            winner: None,
            is_draw: false,
            error: None,
        };

        // Check for errors
        if !stderr.is_empty() && (stderr.contains("Error") || stderr.contains("error")) {
            result.error = Some(stderr.to_string());
            return result;
        }

        // Look for game over message
        if stdout.contains("Game over! Draw!") || stdout.contains("Game over! It's a draw!") {
            result.is_draw = true;
            return result;
        }

        // Check for winner
        if stdout.contains("Game over! Winner:") {
            // For tictactoe
            if stdout.contains("Winner: Player X") {
                result.winner = Some(player1.to_string());
            } else if stdout.contains("Winner: Player O") {
                result.winner = Some(player2.to_string());
            }
            // For Lasker Morris
            else if stdout.contains("Winner: blue") {
                result.winner = Some(player1.to_string());
            } else if stdout.contains("Winner: orange") {
                result.winner = Some(player2.to_string());
            }
        }

        result
    }

    fn record_result(&mut self, result: &MatchResult) -> Result<(), Box<dyn std::error::Error>> {
        // Write the result to CSV
        self.csv_writer.serialize(result)?;
        self.csv_writer.flush()?;

        Ok(())
    }

    fn update_player_stats(&mut self) {
        if let Some(results) = self.round_results.get(&self.current_round) {
            let round_stats = self.player_stats.entry(self.current_round.clone())
                                             .or_insert_with(HashMap::new);

            for result in results {
                let group_name = result.group.clone();
                let group_stats = round_stats.entry(group_name).or_insert_with(HashMap::new);

                // Update player1 stats if in this group
                if let Some(player1_stats) = group_stats.get_mut(&result.player1) {
                    player1_stats.add_result(result);
                }

                // Update player2 stats if in this group
                if let Some(player2_stats) = group_stats.get_mut(&result.player2) {
                    player2_stats.add_result(result);
                }
            }
        }
    }

    fn determine_winners(&self) -> HashMap<String, Vec<String>> {
        let mut winners = HashMap::new();

        if let Some(round_stats) = self.player_stats.get(&self.current_round) {
            for (group_name, group_stats) in round_stats {
                // Convert HashMap to Vec for sorting
                let mut players: Vec<(String, &PlayerStats)> = group_stats.iter()
                    .map(|(name, stats)| (name.clone(), stats))
                    .collect();

                // Sort by points (descending)
                players.sort_by(|a, b| b.1.points.partial_cmp(&a.1.points).unwrap_or(std::cmp::Ordering::Equal));

                // Take the top 2 players from each group
                let num_to_advance = 2;

                let group_winners: Vec<String> = players.iter()
                    .take(num_to_advance)
                    .map(|(name, _)| name.clone())
                    .collect();

                winners.insert(group_name.clone(), group_winners);
            }
        }

        winners
    }

    fn determine_fourth_round_rankings(&self) -> Vec<String> {
        let mut ranked_players = Vec::new();

        if let Some(round_stats) = self.player_stats.get("Fourth Round") {
            // Get the first (and only) group in the fourth round
            if let Some((_, group_stats)) = round_stats.iter().next() {
                // Convert HashMap to Vec for sorting
                let mut players: Vec<(String, &PlayerStats)> = group_stats.iter()
                    .map(|(name, stats)| (name.clone(), stats))
                    .collect();

                // Sort by points (descending)
                players.sort_by(|a, b| b.1.points.partial_cmp(&a.1.points).unwrap_or(std::cmp::Ordering::Equal));

                // Return all players in ranked order
                ranked_players = players.into_iter()
                    .map(|(name, _)| name)
                    .collect();
            }
        }

        ranked_players
    }

    fn setup_next_round(
        &mut self,
        winners: &HashMap<String, Vec<String>>,
        num_groups: usize,
    ) -> Result<(), Box<dyn std::error::Error>> {
        // Flatten all winners
        let mut all_winners = Vec::new();
        for group_winners in winners.values() {
            all_winners.extend(group_winners.clone());
        }

        // Shuffle winners for random assignment
        let mut rng = thread_rng();
        all_winners.shuffle(&mut rng);

        // Create new groups
        self.groups.clear();
        let players_per_group = all_winners.len() / num_groups;

        for i in 0..num_groups {
            let start = i * players_per_group;
            let end = if i == num_groups - 1 {
                all_winners.len()
            } else {
                start + players_per_group
            };

            let group_name = format!("Group {}", (b'A' + i as u8) as char);

            // Make sure we don't go out of bounds
            if start < all_winners.len() {
                let end_idx = std::cmp::min(end, all_winners.len());
                let group_players = all_winners[start..end_idx].to_vec();

                if !group_players.is_empty() {
                    self.groups.insert(group_name, group_players);
                }
            }
        }

        // Initialize player stats for this round
        let mut round_stats = HashMap::new();
        for (group, players) in &self.groups {
            let mut group_stats = HashMap::new();
            for player in players {
                let player_stats = PlayerStats::new(player);
                group_stats.insert(player.clone(), player_stats);
            }
            round_stats.insert(group.clone(), group_stats);
        }
        self.player_stats.insert(self.current_round.clone(), round_stats);

        // Log the new groups
        info!("New groups for {}:", self.current_round);
        for (group, players) in &self.groups {
            info!("{}: {}", group, players.join(", "));
        }

        Ok(())
    }

    fn setup_finals(&mut self, ranked_players: &[String]) -> Result<(), Box<dyn std::error::Error>> {
        // Clear old groups
        self.groups.clear();

        // We need at least 4 players for the final setup
        if ranked_players.len() >= 4 {
            // Top 2 play for 1st/2nd place
            self.groups.insert(
                "Championship".to_string(),
                vec![ranked_players[0].clone(), ranked_players[1].clone()]
            );

            // 3rd and 4th play for 3rd/4th place
            self.groups.insert(
                "Third Place Match".to_string(),
                vec![ranked_players[2].clone(), ranked_players[3].clone()]
            );
        } else {
            warn!("Not enough players from Fourth Round for proper finals. Setting up with available players.");
            if ranked_players.len() >= 2 {
                self.groups.insert(
                    "Championship".to_string(),
                    vec![ranked_players[0].clone(), ranked_players[1].clone()]
                );
            }
        }

        // Initialize player stats for this round
        let mut round_stats = HashMap::new();
        for (group, players) in &self.groups {
            let mut group_stats = HashMap::new();
            for player in players {
                let player_stats = PlayerStats::new(player);
                group_stats.insert(player.clone(), player_stats);
            }
            round_stats.insert(group.clone(), group_stats);
        }
        self.player_stats.insert(self.current_round.clone(), round_stats);

        // Log finals setup
        info!("Finals setup:");
        if let Some(championship_players) = self.groups.get("Championship") {
            if championship_players.len() >= 2 {
                info!("Championship match: {} vs {}", championship_players[0], championship_players[1]);
            }
        }

        if let Some(third_place_players) = self.groups.get("Third Place Match") {
            if third_place_players.len() >= 2 {
                info!("Third place match: {} vs {}", third_place_players[0], third_place_players[1]);
            }
        }

        Ok(())
    }

    fn print_standings(&self) {
        println!("\n=== Current Standings ({}) ===", self.current_round);

        if let Some(round_stats) = self.player_stats.get(&self.current_round) {
            for (group_name, group_stats) in round_stats {
                println!("\n{}:", group_name);

                // Convert HashMap to Vec for sorting
                let mut players: Vec<(String, &PlayerStats)> = group_stats.iter()
                    .map(|(name, stats)| (name.clone(), stats))
                    .collect();

                players.sort_by(|a, b| b.1.points.partial_cmp(&a.1.points).unwrap_or(std::cmp::Ordering::Equal));

                println!("{:<20} {:<5} {:<5} {:<5} {:<5}", "Player", "W", "L", "D", "Pts");
                println!("{}", "-".repeat(40));

                for (name, stats) in players {
                    println!("{:<20} {:<5} {:<5} {:<5} {:<5.1}",
                            name, stats.wins, stats.losses, stats.draws, stats.points);
                }
            }
        }

        // If this is the end of a round, show who advances
        if self.current_round == "First Round" || self.current_round == "Second Round" ||
           self.current_round == "Third Round" || self.current_round == "Fourth Round" {

            if self.current_round == "Fourth Round" {
                let ranked_players = self.determine_fourth_round_rankings();
                println!("\nFinal ranking from Fourth Round:");
                for (i, player) in ranked_players.iter().enumerate() {
                    println!("{}. {}", i + 1, player);
                }
                println!("\nAdvancing to Championship: {} and {}", ranked_players[0], ranked_players[1]);
                println!("Playing for 3rd place: {} and {}", ranked_players[2], ranked_players[3]);
            } else {
                let winners = self.determine_winners();
                println!("\nAdvancing to next round:");
                for (group, players) in &winners {
                    println!("From {}: {}", group, players.join(", "));
                }
            }
        }

        println!();
    }

    fn print_final_results(&self) {
        println!("\n=== TOURNAMENT FINAL RESULTS ===\n");

        if let Some(final_stats) = self.player_stats.get("Final Round") {
            // Championship result
            if let Some(championship_stats) = final_stats.get("Championship") {
                // Convert HashMap to Vec for sorting
                let mut finalists: Vec<(String, &PlayerStats)> = championship_stats.iter()
                    .map(|(name, stats)| (name.clone(), stats))
                    .collect();

                finalists.sort_by(|a, b| b.1.points.partial_cmp(&a.1.points).unwrap_or(std::cmp::Ordering::Equal));

                if finalists.len() >= 2 {
                    println!("🏆 CHAMPION: {}", finalists[0].0);
                    println!("🥈 RUNNER-UP: {}", finalists[1].0);
                } else if !finalists.is_empty() {
                    println!("🏆 CHAMPION: {}", finalists[0].0);
                }
            }

            // Third place result
            if let Some(third_place_stats) = final_stats.get("Third Place Match") {
                // Convert HashMap to Vec for sorting
                let mut third_place_contestants: Vec<(String, &PlayerStats)> = third_place_stats.iter()
                    .map(|(name, stats)| (name.clone(), stats))
                    .collect();

                third_place_contestants.sort_by(|a, b| {
                    b.1.points.partial_cmp(&a.1.points).unwrap_or(std::cmp::Ordering::Equal)
                });

                if third_place_contestants.len() >= 2 {
                    println!("🥉 THIRD PLACE: {}", third_place_contestants[0].0);
                    println!("    FOURTH PLACE: {}", third_place_contestants[1].0);
                } else if !third_place_contestants.is_empty() {
                    println!("🥉 THIRD PLACE: {}", third_place_contestants[0].0);
                }
            }
        }

        println!("\nTournament completed! Full results saved in tournament_results.csv");
    }

    fn print_overall_stats(&self) {
        println!("\n=== OVERALL TOURNAMENT STATISTICS ===\n");

        // Create a map to track overall player performance
        let mut overall_stats = HashMap::new();

        // Collect stats from all rounds
        for (_, round_stats) in &self.player_stats {
            for (_, group_stats) in round_stats {
                for (player_name, stats) in group_stats {
                    let entry = overall_stats.entry(player_name.clone())
                                          .or_insert_with(|| PlayerStats::new(player_name));
                    entry.wins += stats.wins;
                    entry.losses += stats.losses;
                    entry.draws += stats.draws;
                    entry.points += stats.points;
                }
            }
        }

        // Sort by total points
        let mut players: Vec<(String, &PlayerStats)> = overall_stats.iter()
            .map(|(name, stats)| (name.clone(), stats))
            .collect();
        players.sort_by(|a, b| b.1.points.partial_cmp(&a.1.points).unwrap_or(std::cmp::Ordering::Equal));

        println!("{:<20} {:<5} {:<5} {:<5} {:<5}", "Player", "W", "L", "D", "Pts");
        println!("{}", "-".repeat(40));

        for (name, stats) in players {
            println!("{:<20} {:<5} {:<5} {:<5} {:<5.1}",
                   name, stats.wins, stats.losses, stats.draws, stats.points);
        }
    }

    fn write_csv_header(&mut self) -> Result<(), Box<dyn std::error::Error>> {
        self.csv_writer.write_record(&[
            "Round", "Group", "Game Number", "Player 1", "Player 2", "Winner", "Is Draw", "Error"
        ])?;
        self.csv_writer.flush()?;
        Ok(())
    }
}

fn main() -> Result<(), Box<dyn std::error::Error>> {
    // Parse command line arguments
    let args: Vec<String> = std::env::args().collect();

    // Check for logging level
    let log_level = if args.iter().any(|arg| arg == "--quiet" || arg == "-q") {
        LevelFilter::Error // Only show errors
    } else if args.iter().any(|arg| arg == "--debug" || arg == "-d") {
        LevelFilter::Debug // Show debug and above
    } else if args.iter().any(|arg| arg == "--no-log") {
        LevelFilter::Off // Turn off logging completely
    } else {
        LevelFilter::Info // Default: Show info and above
    };

    // Initialize logging with selected level
    let log_file = File::create("tournament.log")?;
    WriteLogger::init(log_level, Config::default(), log_file)?;

    info!("Starting tournament manager");

    // Get config path from args
    let config_path = args.iter()
        .find(|arg| !arg.starts_with("-") && !arg.starts_with("--") && **arg != args[0])
        .map(|s| s.as_str())
        .unwrap_or("tournament.toml");

    info!("Using config file: {}", config_path);

    // Initialize and run the tournament
    let mut tournament = TournamentManager::new(config_path)?;
    tournament.run_tournament()?;

    info!("Tournament completed successfully");

    Ok(())
}
