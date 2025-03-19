import logging
from typing import Dict, Optional, Set


class GameError(Exception):
    """Base class for game-related errors"""
    pass


class InvalidMoveError(GameError):
    """Error raised when a move is invalid"""
    pass


class TimeoutError(GameError):
    """Error raised when a player takes too long to respond"""
    pass


class GameLogger:
    """Handles logging for games"""

    def __init__(self, name: str, enable_logging: bool = False):
        self.logger = logging.getLogger(name)
        if enable_logging:
            self._setup_logging()

    def _setup_logging(self) -> None:
        handler = logging.FileHandler(f"{self.logger.name}.log")
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)

    def info(self, message: str) -> None:
        self.logger.info(message)

    def error(self, message: str) -> None:
        self.logger.error(message)

    def debug(self, message: str) -> None:
        self.logger.debug(message)


# Common board utilities that can be shared across games
class BoardUtils:
    @staticmethod
    def create_empty_board(cols: str, rows: str) -> Dict[str, Optional[str]]:
        """Create an empty game board with given columns and rows"""
        return {f"{col}{row}": None for col in cols for row in rows}

    @staticmethod
    def is_position_empty(board: Dict[str, Optional[str]], position: str) -> bool:
        """Check if a board position is empty"""
        return position in board and board[position] is None

    @staticmethod
    def is_position_valid(board: Dict[str, Optional[str]],
                         position: str,
                         invalid_fields: Optional[Set[str]] = None) -> bool:
        """Check if a position is valid on the board"""
        if invalid_fields and position in invalid_fields:
            return False
        return position in board
