import typing

from typing import TypeVar
from dataclasses import dataclass


@dataclass
class Constants:
    """Constants for the FM world."""
    GAME_NAME: str = "Brave Fencer Musashi"
    GAME_OPTIONS_KEY: str = "o"
    GENERATED_WITH_KEY: str = "v"
    DEATHLINK_OPTION_KEY: str = "X"

