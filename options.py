from dataclasses import dataclass
from Options import Choice, Toggle, PerGameCommonOptions, DeathLink, FreeText
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

class HairColor(Choice):
    """
    Pick Hair Color, or choose custom for further customization
    """
    internal_name = "hair_color_selection"
    display_name = "Hair Color"
    option_white = 1
    option_red = 2
    option_blue = 3
    option_custom = 4
    default = 1

class CustomHairColor(FreeText):
    """
    Must select custom from hair color, write hex code of desired color in the format RRGGBB (see https://www.color-hex.com/ for assistance) do not include # must be exactly 6 digits and a valid hex code i.e. 0 through F values only
    """
    internal_name = "custom_hair_color_selection"
    display_name = "Custom Hair Color"
    default = "F2779D"

@dataclass
class BFMOptions(PerGameCommonOptions):
    #lumina_randomzied: LuminaRandomized
    death_link: DeathLink
    hair_color_selection: HairColor
    custom_hair_color_selection: CustomHairColor