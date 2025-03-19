from dataclasses import dataclass
from typing import Final


@dataclass(frozen=True)
class GameConfig:
    DEFAULT_WEB_PORT: Final[int] = 8000
    DEFAULT_TIMEOUT: Final[int] = 5
    DEFAULT_VISUALIZATION: Final[bool] = True
    DEFAULT_LOGGING: Final[bool] = False
    DEFAULT_DEBUG: Final[bool] = False
    DEFAULT_RANDOM_ASSIGNMENT: Final[bool] = False
    WEB_TEMPLATE_FOLDER: Final[str] = "../web/"


@dataclass(frozen=True)
class LaskerConfig(GameConfig):
    HAND_SIZE: Final[int] = 10
    DEFAULT_RANDOM_ASSIGNMENT: Final[bool] = True


@dataclass(frozen=True)
class TicTacToeConfig(GameConfig):
    pass
