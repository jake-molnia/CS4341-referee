from enum import Enum

from .abstract import AbstractPlayer


class PlayerColor(Enum):
    """Enum for valid player colors in Lasker Morris."""
    BLUE = "blue"
    ORANGE = "orange"


class PlayerSymbol(Enum):
    """Enum for valid player symbols in TicTacToe."""
    X = "BLUE"
    O = "ORANGE"


class LaskerPlayer(AbstractPlayer):
    """Player implementation for Lasker Morris game."""

    def __init__(self, command: str, color: str, log: bool = False, debug: bool = False):
        super().__init__(command, log, debug)
        try:
            self.color = PlayerColor(color.lower())
        except ValueError:
            raise ValueError(f"Invalid color: {color}. Must be either 'blue' or 'orange'")

    def get_color(self) -> str:
        return self.color.value

    def is_blue(self) -> bool:
        return self.color == PlayerColor.BLUE

    def is_orange(self) -> bool:
        return self.color == PlayerColor.ORANGE


class TicTacToePlayer(AbstractPlayer):
    """Player implementation for Tic-tac-toe game."""

    def __init__(self, command: str, symbol: str, log: bool = False):
        super().__init__(command, log)
        try:
            self.symbol = PlayerSymbol(symbol.upper())
        except ValueError:
            raise ValueError(f"Invalid symbol: {symbol}. Must be either 'blue' or 'orange'")

    def get_symbol(self) -> str:
        return self.symbol.value

    def is_x(self) -> bool:
        return self.symbol == PlayerSymbol.X

    def is_o(self) -> bool:
        return self.symbol == PlayerSymbol.O
