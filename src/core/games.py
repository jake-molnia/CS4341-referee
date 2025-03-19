import random
from concurrent.futures import ThreadPoolExecutor, TimeoutError
from typing import Optional, Tuple

import click
from colorama import Fore, Style

from ..config import GameConfig, LaskerConfig
from .abstract import AbstractGame
from .players import LaskerPlayer, TicTacToePlayer
from .utils import BoardUtils


class TicTacToe(AbstractGame):
    VALID_COLUMNS = set("abc")
    VALID_ROWS = set("123")

    def __init__(
        self,
        player1_command: str,
        player2_command: str,
        visual: bool = True,
        random_assignment: bool = False,
        move_timeout: int = 5,
        enable_logging: bool = False,
        debug: bool = False,
        port: int = GameConfig.DEFAULT_WEB_PORT,
    ):
        self.move_timeout = move_timeout
        self.debug = debug
        self.enable_logging = enable_logging
        self.port = port

        # Assign player symbols, possibly randomized
        colors = ["blue", "orange"]
        if random_assignment:
            random.shuffle(colors)

        # Create players
        player1 = TicTacToePlayer(player1_command, colors[0], enable_logging)
        player2 = TicTacToePlayer(player2_command, colors[1], enable_logging)
        super().__init__(player1, player2)

        self.board = {}
        self.visual = visual
        self.web = self._create_web_interface() if visual else None
        self.move_history = []
        self.initialize_game()

    def _create_web_interface(self):
        from .web import TicTacToeWeb
        return TicTacToeWeb(self)

    def initialize_game(self) -> None:
        # Initialize empty board
        self.board = BoardUtils.create_empty_board(self.VALID_COLUMNS, self.VALID_ROWS)

        # Start player processes
        self._player1.start()
        self._player2.start()

        # Start web server if visualization enabled
        if self.visual and self.web:
            self.web.start_web_server(self.port)

        # Set first player and notify players of their colors
        self._current_player = self._player1 if self._player1.is_x() else self._player2
        self._current_player.write("blue")
        other_player = self._player2 if self._current_player == self._player1 else self._player1
        other_player.write("orange")

    def _validate_move_format(self, move: str) -> Tuple[bool, Optional[str]]:
        move = move.strip().lower()
        if len(move) != 2:
            return False, f"Invalid move format: {move}. Must be in format 'a1'"

        col, row = move[0], move[1]
        if col not in self.VALID_COLUMNS:
            return False, f"Invalid column: {col}. Must be one of: {', '.join(sorted(self.VALID_COLUMNS))}"
        if row not in self.VALID_ROWS:
            return False, f"Invalid row: {row}. Must be one of: {', '.join(sorted(self.VALID_ROWS))}"

        return True, None

    def make_move(self, move: str) -> bool:
        try:
            # Validate move format
            is_valid, error_msg = self._validate_move_format(move)
            if not is_valid:
                click.echo(f"\n{Fore.RED}{error_msg}{Style.RESET_ALL}")
                return False

            move = move.lower()
            if not BoardUtils.is_position_empty(self.board, move):
                click.echo(f"\n{Fore.RED}Invalid move: Position {move} is already occupied{Style.RESET_ALL}")
                return False

            # Execute move
            self.board[move] = self._current_player.get_symbol()
            self.move_history.append(move)

            if self.visual and self.web:
                self.web.update_history(move)

            if self.debug:
                self._show_state(move)

            return True
        except Exception as e:
            click.echo(f"\n{Fore.RED}Error processing move: {str(e)}{Style.RESET_ALL}")
            return False

    def _show_state(self, last_move: Optional[str] = None) -> None:
        """Display current board state in terminal"""
        if not self.debug:
            return

        click.echo("\nBoard:")
        for row in "321":  # Reversed for display
            row_str = f"{row} "
            for col in "abc":
                pos = f"{col}{row}"
                symbol = self.board[pos]
                if symbol is None:
                    row_str += ". "
                else:
                    color = Fore.BLUE if symbol == "BLUE" else Fore.YELLOW
                    row_str += f"{color}{'X' if symbol == 'BLUE' else 'O'}{Style.RESET_ALL} "
            click.echo(row_str)
        click.echo("  a b c")

        if last_move:
            click.echo(f"Last move: {last_move}")

    def _check_winner(self) -> Optional[str]:
        win_combinations = [
            # Rows
            ["a1", "b1", "c1"], ["a2", "b2", "c2"], ["a3", "b3", "c3"],
            # Columns
            ["a1", "a2", "a3"], ["b1", "b2", "b3"], ["c1", "c2", "c3"],
            # Diagonals
            ["a1", "b2", "c3"], ["a3", "b2", "c1"],
        ]

        for combo in win_combinations:
            values = [self.board[pos] for pos in combo]
            if None not in values and len(set(values)) == 1:
                return values[0]
        return None

    def _is_board_full(self) -> bool:
        """Check if the board is completely filled."""
        if all(value is not None for value in self.board.values()):
            self._is_game_over = True
            return True
        return False

    def determine_winner(self) -> Optional[TicTacToePlayer]:
        winning_symbol = self._check_winner()
        if winning_symbol:
            self._is_game_over = True
            return (
                self._player1 if self._player1.get_symbol() == winning_symbol else self._player2
            )
        return None

    def _get_move_with_timeout(self) -> Optional[str]:
        with ThreadPoolExecutor(max_workers=1) as executor:
            try:
                future = executor.submit(self.current_player.read)
                return future.result(timeout=self.move_timeout)
            except TimeoutError:
                click.echo(
                    f"\n{Fore.RED}Move timeout: Player {self.current_player.get_symbol()} "
                    f"took too long to respond{Style.RESET_ALL}"
                )
                return None

    def run_game(self) -> Optional[TicTacToePlayer]:
        """Main game loop."""
        while not self.is_game_over:
            move = self._get_move_with_timeout()

            # Handle timeout or invalid move
            if move is None or not self.make_move(move):
                self._is_game_over = True
                winner = self._player2 if self.current_player == self._player1 else self._player1
                reason = "Time out!" if move is None else f"Invalid move {move}!"
                message = f"END: {winner.get_symbol()} WINS! {self.current_player.get_symbol()} LOSES! {reason}"

                if self.visual and self.web:
                    self.web.end_message = message

                self._cleanup_game()
                return winner

            # Write move to other player
            other_player = self._player2 if self.current_player == self._player1 else self._player1
            other_player.write(move)

            # Check for winner or draw
            winner = self.determine_winner()
            if winner is not None:
                message = f"END: {winner.get_symbol()} WINS! {other_player.get_symbol()} LOSES! Three in a row!"
                if self.visual and self.web:
                    self.web.end_message = message
                self._cleanup_game()
                return winner
            elif self._is_board_full():
                message = "Draw!"
                if self.visual and self.web:
                    self.web.end_message = message
                self._cleanup_game()
                return None

            self.switch_player()

        return None

    def _cleanup_game(self) -> None:
        """Clean up game resources."""
        self._player1.stop()
        self._player2.stop()


class LaskerMorris(AbstractGame):
    """Implementation of Lasker Morris game."""

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
        print_board: bool = False
    ):
        self.move_timeout = timeout + 0.5
        self.game_history = []
        self.board_states = []
        self.hand_states = []
        self.debug = debug
        self.port = port
        self.prin_board = print_board
        self.moves_without_taking = 0

        # Initialize players with randomly assigned colors
        colors = ["blue", "orange"]
        if select_rand:
            random.shuffle(colors)

        player1 = LaskerPlayer(player1_command, colors[0], logging, debug)
        player2 = LaskerPlayer(player2_command, colors[1], logging, debug)
        super().__init__(player1, player2)

        # Initialize game state
        self.board = {}
        self.player_hands = {"blue": LaskerConfig.HAND_SIZE, "orange": LaskerConfig.HAND_SIZE}

        # Define invalid board positions
        self.invalid_fields = {
            "a2", "a3", "a5", "a6", "b1", "b3", "b5", "b7", "c1", "c2", "c6", "c7",
            "d4", "e1", "e2", "e6", "e7", "f1", "f3", "f5", "f7", "g2", "g3", "g5", "g6",
        }

        self.visual = visual
        self.web = self._create_web_interface() if visual else None
        self.initialize_game()

    def _create_web_interface(self):
        from .web import LaskerMorrisWeb
        return LaskerMorrisWeb(self)

    def initialize_game(self) -> None:
        # Initialize empty board positions
        for num in range(1, 8):
            for letter in "abcdefg":
                self.board[f"{letter}{num}"] = None

        # Start player processes and web server
        self._player1.start()
        self._player2.start()

        if self.visual and self.web:
            self.web.start_web_server(self.port)

        # Ensure blue player goes first
        self._current_player = self._player1 if self._player1.is_blue() else self._player2
        self._current_player.write("blue")
        other_player = self._player2 if self._current_player == self._player1 else self._player1
        other_player.write("orange")

    def make_move(self, move: str) -> bool:
        try:
            parts = move.strip().split()
            if len(parts) != 3:
                return False

            source, target, remove = parts
            if not self._is_valid_move(source, target, remove):
                return False

            self._execute_move(source, target, remove)

            if self.prin_board:
                self._show_state(move)

            return True
        except Exception:
            return False

    def _has_valid_moves(self, player_color: str) -> bool:
        # If player has pieces in hand, they can place on any empty valid position
        if self.player_hands[player_color] > 0:
            return any(pos not in self.invalid_fields and self.board[pos] is None
                      for pos in self.board)

        # Get all pieces of the player
        player_pieces = [pos for pos, color in self.board.items() if color == player_color]

        # With exactly 3 pieces, player can move to any empty position
        if len(player_pieces) == 3:
            return any(pos not in self.invalid_fields and self.board[pos] is None
                      for pos in self.board)

        # Check if any piece can move to an adjacent empty position
        neighbors = {
            "a1": ["a4", "d1"], "a4": ["a1", "a7", "b4"], "a7": ["a4", "d7"],
            "b2": ["b4", "d2"], "b4": ["b2", "b6", "a4", "c4"], "b6": ["b4", "d6"],
            "c3": ["c4", "d3"], "c4": ["c3", "c5", "b4"], "c5": ["c4", "d5"],
            "d1": ["a1", "d2", "g1"], "d2": ["b2", "d1", "d3", "f2"],
            "d3": ["c3", "d2", "e3"], "d5": ["c5", "d6", "e5"],
            "d6": ["b6", "d5", "d7", "f6"], "d7": ["a7", "d6", "g7"],
            "e3": ["d3", "e4"], "e4": ["e3", "e5", "f4"], "e5": ["d5", "e4"],
            "f2": ["d2", "f4"], "f4": ["e4", "f2", "f6", "g4"], "f6": ["d6", "f4"],
            "g1": ["d1", "g4"], "g4": ["f4", "g1", "g7"], "g7": ["d7", "g4"],
        }

        for piece_pos in player_pieces:
            if piece_pos in neighbors and any(self.board[n] is None for n in neighbors[piece_pos]):
                return True

        return False

    def _is_valid_move(self, source: str, target: str, remove: str) -> bool:
        # Validate target position
        if target in self.invalid_fields or target not in self.board:
            click.echo(f"\n{Fore.RED}Invalid target position: {target}{Style.RESET_ALL}")
            return False

        if self.board[target] is not None:
            click.echo(f"\n{Fore.RED}Target position {target} is occupied{Style.RESET_ALL}")
            return False

        # Validate source position (hand or board)
        if source in ["h1", "h2"]:
            is_player1 = self._current_player.get_color() == "blue"
            correct_hand = "h1" if is_player1 else "h2"

            if source != correct_hand:
                click.echo(f"\n{Fore.RED}Invalid hand: {source}{Style.RESET_ALL}")
                return False

            if self.player_hands[self._current_player.get_color()] <= 0:
                click.echo(f"\n{Fore.RED}No stones left in hand{Style.RESET_ALL}")
                return False
        else:
            # Board move validation
            if source in self.invalid_fields or source not in self.board:
                click.echo(f"\n{Fore.RED}Invalid source position: {source}{Style.RESET_ALL}")
                return False

            if self.board[source] != self._current_player.get_color():
                click.echo(f"\n{Fore.RED}Not your stone at {source}{Style.RESET_ALL}")
                return False

            # Movement rules check (3+ pieces = adjacent only, ≤3 pieces = anywhere)
            if self._count_player_pieces(self._current_player.get_color()) > 3:
                if not self._check_corret_step(source, target):
                    click.echo(f"\n{Fore.RED}Must move to adjacent position{Style.RESET_ALL}")
                    return False

        # Validate remove position
        if remove != "r0":
            self.moves_without_taking = 0
            if remove in self.invalid_fields or remove not in self.board:
                click.echo(f"\n{Fore.RED}Invalid remove position: {remove}{Style.RESET_ALL}")
                return False

            if self.board[remove] is None:
                click.echo(f"\n{Fore.RED}No stone at position {remove}{Style.RESET_ALL}")
                return False

            if self.board[remove] == self._current_player.get_color():
                click.echo(f"\n{Fore.RED}Cannot remove your own stone{Style.RESET_ALL}")
                return False

            opponent_color = "orange" if self._current_player.get_color() == "blue" else "blue"

            # Mill rules check
            if self._position_is_in_mill(remove, opponent_color) and self._count_stones_outside_mills(opponent_color) > 0:
                click.echo(f"\n{Fore.RED}Cannot remove stone in mill when stones outside mills exist{Style.RESET_ALL}")
                return False

            if not self._is_mill(source, target):
                click.echo(f"\n{Fore.RED}Can only remove when forming a mill{Style.RESET_ALL}")
                return False
        elif self._is_mill(source, target):
            click.echo(f"\n{Fore.RED}Must remove stone after forming mill{Style.RESET_ALL}")
            return False
        else:
            self.moves_without_taking += 1

        return True

    def _position_is_in_mill(self, position: str, color: str) -> bool:
        mills = [
            # Horizontal mills
            ["a1", "a4", "a7"], ["b2", "b4", "b6"], ["c3", "c4", "c5"],
            ["d1", "d2", "d3"], ["d5", "d6", "d7"], ["e3", "e4", "e5"],
            ["f2", "f4", "f6"], ["g1", "g4", "g7"],
            # Vertical mills
            ["a1", "d1", "g1"], ["b2", "d2", "f2"], ["c3", "d3", "e3"],
            ["a4", "b4", "c4"], ["e4", "f4", "g4"], ["c5", "d5", "e5"],
            ["b6", "d6", "f6"], ["a7", "d7", "g7"],
        ]

        return any(position in mill and all(self.board.get(pos) == color for pos in mill)
                  for mill in mills)

    def _count_stones_outside_mills(self, color: str) -> int:
        positions = [pos for pos, stone_color in self.board.items() if stone_color == color]
        return sum(1 for pos in positions if not self._position_is_in_mill(pos, color))

    def _is_mill(self, source: str, target: str) -> bool:
        color = self._current_player.get_color()
        mills = [
            # Horizontal mills
            ["a1", "a4", "a7"], ["b2", "b4", "b6"], ["c3", "c4", "c5"],
            ["d1", "d2", "d3"], ["d5", "d6", "d7"], ["e3", "e4", "e5"],
            ["f2", "f4", "f6"], ["g1", "g4", "g7"],
            # Vertical mills
            ["a1", "d1", "g1"], ["b2", "d2", "f2"], ["c3", "d3", "e3"],
            ["a4", "b4", "c4"], ["e4", "f4", "g4"], ["c5", "d5", "e5"],
            ["b6", "d6", "f6"], ["a7", "d7", "g7"],
        ]

        for mill in mills:
            if target in mill:
                stones_in_mill = 0
                for pos in mill:
                    if pos == target:
                        stones_in_mill += 1
                    elif pos != source and self.board[pos] == color:
                        stones_in_mill += 1

                if stones_in_mill == 3:
                    return True

        return False

    def _check_corret_step(self, source: str, target: str) -> bool:
        neighbors = {
            "a1": ["a4", "d1"], "a4": ["a1", "a7", "b4"], "a7": ["a4", "d7"],
            "b2": ["b4", "d2"], "b4": ["b2", "b6", "a4", "c4"], "b6": ["b4", "d6"],
            "c3": ["c4", "d3"], "c4": ["c3", "c5", "b4"], "c5": ["c4", "d5"],
            "d1": ["a1", "d2", "g1"], "d2": ["b2", "d1", "d3", "f2"],
            "d3": ["c3", "d2", "e3"], "d5": ["c5", "d6", "e5"],
            "d6": ["b6", "d5", "d7", "f6"], "d7": ["a7", "d6", "g7"],
            "e3": ["d3", "e4"], "e4": ["e3", "e5", "f4"], "e5": ["d5", "e4"],
            "f2": ["d2", "f4"], "f4": ["e4", "f2", "f6", "g4"], "f6": ["d6", "f4"],
            "g1": ["d1", "g4"], "g4": ["f4", "g1", "g7"], "g7": ["d7", "g4"],
        }

        return source in neighbors and target in neighbors[source]

    def _count_player_pieces(self, color: str) -> int:
        return sum(1 for pos in self.board.values() if pos == color) + self.player_hands[color]

    def _execute_move(self, source: str, target: str, remove: str) -> None:
        current_color = self._current_player.get_color()

        # Update board state
        if source in ["h1", "h2"]:
            self.player_hands[current_color] -= 1
        else:
            self.board[source] = None

        self.board[target] = current_color

        if remove != "r0":
            self.board[remove] = None

        # Record move history
        move_data = {
            "move": f"{source} {target} {remove}",
            "player": current_color,
            "board": self.board.copy(),
            "hands": self.player_hands.copy(),
        }
        self.game_history.append(move_data)
        self.board_states.append(self.board.copy())
        self.hand_states.append(self.player_hands.copy())

    def _show_state(self, move: Optional[str] = None) -> None:
        if not self.debug and not self.prin_board:
            return

        click.echo("-------------------------------------------------")
        if move:
            click.echo(f"Move: {move}")

        current_color = self._current_player.get_color()
        color_code = Fore.BLUE if current_color == "blue" else Fore.YELLOW
        click.echo(f"{color_code}{current_color}'s turn{Style.RESET_ALL}")

        # Display board
        click.echo("\nBoard:")
        for num in range(1, 8):
            row = ""
            for letter in "abcdefg":
                pos = f"{letter}{num}"
                if pos in self.invalid_fields:
                    row += "  "
                elif self.board.get(pos) is None:
                    row += ". "
                else:
                    color = Fore.BLUE if self.board[pos] == "blue" else Fore.YELLOW
                    row += f"{color}●{Style.RESET_ALL} "
            click.echo(f"{num} {row}")
        click.echo("  a b c d e f g")

        # Display stones in hand
        click.echo("\nStones in hand:")
        click.echo(f"{Fore.BLUE}Blue: {self.player_hands['blue']}{Style.RESET_ALL}")
        click.echo(f"{Fore.YELLOW}Orange: {self.player_hands['orange']}{Style.RESET_ALL}")
        click.echo("-------------------------------------------------")

    def determine_winner(self) -> Optional[LaskerPlayer]:
        # Check for draw condition
        if self.moves_without_taking >= 20:
            self._is_game_over = True
            message = "Draw!"
            click.echo(message)
            if self.visual and self.web:
                self.web.end_message = message
            self._cleanup_game()
            return None

        # Check if any player has fewer than 3 pieces
        for player in [self._player1, self._player2]:
            color = player.get_color()
            if self._count_player_pieces(color) < 3:
                self._is_game_over = True
                return self._player1 if player == self._player2 else self._player2

        return None

    def _get_move_with_timeout(self) -> Optional[str]:
        with ThreadPoolExecutor(max_workers=1) as executor:
            try:
                future = executor.submit(self._current_player.read)
                return future.result(timeout=self.move_timeout)
            except TimeoutError:
                click.echo(f"\n{Fore.RED}Move timeout: {self._current_player.get_color()}{Style.RESET_ALL}")
                return None

    def run_game(self) -> Optional[LaskerPlayer]:
        while not self.is_game_over:
            # Check for immobilization
            if not self._has_valid_moves(self._current_player.get_color()):
                self._is_game_over = True
                winner = self._player2 if self._current_player == self._player1 else self._player1
                winner_color = winner.get_color()
                loser_color = self._current_player.get_color()
                message = f"END: {winner_color} WINS! {loser_color} LOSES! No valid moves available!"
                if self.visual and self.web:
                    self.web.end_message = message
                self._cleanup_game()
                return winner

            # Get and validate current player's move
            move = self._get_move_with_timeout()
            if not move or not self.make_move(move):
                self._is_game_over = True
                winner = self._player2 if self._current_player == self._player1 else self._player1
                winner_color = winner.get_color()
                loser_color = self._current_player.get_color()

                # Error message based on failure reason
                reason = "Time out!" if not move else f"Invalid move {move}!"
                message = f"END: {winner_color} WINS! {loser_color} LOSES! {reason}"

                if self.visual and self.web:
                    self.web.end_message = message
                self._cleanup_game()
                return winner

            # Send move to other player
            other_player = self._player2 if self._current_player == self._player1 else self._player1
            other_player.write(move)

            # Check for winner
            winner = self.determine_winner()
            if winner:
                winner_color = winner.get_color()
                loser_color = other_player.get_color()
                message = f"END: {winner_color} WINS! {loser_color} LOSES! Ran out of pieces!"
                if self.visual and self.web:
                    self.web.end_message = message
                self._cleanup_game()
                return winner

            self.switch_player()

        return None

    def _cleanup_game(self) -> None:
        """Clean up game resources."""
        self._player1.write("END")
        self._player2.write("END")
        self._player1.stop()
        self._player2.stop()
