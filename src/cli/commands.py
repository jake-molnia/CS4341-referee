from typing import Optional

import click
from colorama import Fore, Style, init

from ..config import GameConfig, LaskerConfig, TicTacToeConfig
from ..core import AbstractPlayer, LaskerMorris, TicTacToe

init()  # Initialize colorama for Windows compatibility


def _handle_game_result(winner: Optional[AbstractPlayer], visual: bool, game: any) -> None:
    """Handle and display game result"""
    if winner:
        color_code = Fore.BLUE if hasattr(winner, 'get_color') and winner.get_color() == "blue" else Fore.YELLOW
        display_value = winner.get_color() if hasattr(winner, 'get_color') else winner.get_symbol()
        click.echo(f"\n{color_code}Game over! Winner: {display_value}{Style.RESET_ALL}")
    else:
        click.echo(f"\n{Fore.GREEN}Game over! Draw!{Style.RESET_ALL}")

    # Keep webserver running if visualization is enabled
    if visual:
        click.echo(f"\n{Fore.YELLOW}Press <CTRL>+C to exit visualization{Style.RESET_ALL}")
        try:
            while True:
                pass
        except KeyboardInterrupt:
            pass


@click.command(name="laskermorris")
@click.option("--player1", "-p1", prompt="Enter Player 1 command", help="Command to run Player 1.")
@click.option("--player2", "-p2", prompt="Enter Player 2 command", help="Command to run Player 2.")
@click.option("--visual/--no-visual", "-v/-nv", default=LaskerConfig.DEFAULT_VISUALIZATION,
              help="Enable/disable game visualization")
@click.option("--random-assignment/--no-random-assignment", "-r/-nr",
              default=LaskerConfig.DEFAULT_RANDOM_ASSIGNMENT, help="Enable/disable random selection of first player")
@click.option("--timeout", "-t", type=int, default=LaskerConfig.DEFAULT_TIMEOUT,
              help="Timeout in seconds for each player's move")
@click.option("--port", type=int, default=GameConfig.DEFAULT_WEB_PORT,
              help="Port for visualization webserver")
@click.option("--log/--no-log", "-l/-nl", default=LaskerConfig.DEFAULT_LOGGING,
              help="Enable/disable logging")
@click.option("--debug/--no-debug", "-d/-nd", default=LaskerConfig.DEFAULT_DEBUG,
              help="Enable/disable debug output")
def start_game(player1, player2, visual, random_assignment, timeout, port, log, debug):
    """🎮 Start a new game of Lasker Morris!"""
    try:
        game = LaskerMorris(
            player1_command=player1,
            player2_command=player2,
            visual=visual,
            select_rand=random_assignment,
            timeout=timeout,
            debug=debug,
            logging=log,
            port=port,
            print_board=debug
        )
        winner = game.run_game()
        _handle_game_result(winner, visual, game)

    except Exception as e:
        click.echo(f"\n{Fore.RED}Error: {e}{Style.RESET_ALL}")
        raise click.Abort()


@click.command(name="tictactoe")
@click.option("--player", "-p", prompt="Enter Player command", help="Command to run Player.")
@click.option("--player2", "-p2", required=False, help="Command to run Player 2 (optional).")
@click.option("--visual/--no-visual", "-v/-nv", default=TicTacToeConfig.DEFAULT_VISUALIZATION,
              help="Enable/disable game visualization")
@click.option("--random-assignment/--no-random-assignment", "-r/-nr",
              default=TicTacToeConfig.DEFAULT_RANDOM_ASSIGNMENT, help="Enable/disable random assignment of X/O symbols")
@click.option("--timeout", "-t", type=int, default=TicTacToeConfig.DEFAULT_TIMEOUT,
              help="Timeout in seconds for each player's move")
@click.option("--log/--no-log", "-l/-nl", default=TicTacToeConfig.DEFAULT_LOGGING,
              help="Enable/disable logging")
@click.option("--debug/--no-debug", "-d/-nd", default=TicTacToeConfig.DEFAULT_DEBUG,
              help="Enable/disable debug output")
@click.option("--port", type=int, default=GameConfig.DEFAULT_WEB_PORT,
              help="Port for visualization webserver")
def start_tictactoe(player, player2, visual, random_assignment, timeout, log, debug, port):
    """🎮 Start a new game of TicTacToe!"""
    try:
        # Use same player command for both if player2 not provided
        player2 = player2 or player

        game = TicTacToe(
            player1_command=player,
            player2_command=player2,
            visual=visual,
            random_assignment=random_assignment,
            move_timeout=timeout,
            enable_logging=log,
            debug=debug,
            port=port,
        )

        winner = game.run_game()
        _handle_game_result(winner, visual, game)

    except Exception as e:
        click.echo(f"\n{Fore.RED}Error: {str(e)}{Style.RESET_ALL}")
        raise click.Abort()
    finally:
        if "game" in locals():
            game._cleanup_game()
