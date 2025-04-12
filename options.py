from dataclasses import dataclass
from Options import Choice, Toggle, PerGameCommonOptions, DeathLink
from typing import Dict, Any, TYPE_CHECKING
import logging
if TYPE_CHECKING:
    from . import BFMWorld

class LuminaRandomized(Toggle):
    """
    Not Implemented yet
    """
    internal_name = "lumina_randomzied"
    display_name = "Lumina Randomzied"

@dataclass
class BFMOptions(PerGameCommonOptions):
    lumina_randomzied: LuminaRandomized
    death_link: DeathLink