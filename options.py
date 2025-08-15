from dataclasses import dataclass
from Options import Choice, Toggle, PerGameCommonOptions, DeathLink, FreeText, DefaultOnToggle
from typing import Dict, Any, TYPE_CHECKING
import logging
if TYPE_CHECKING:
    from . import BFMWorld

class LuminaRandomized(Toggle):
    """
    Randomize the sword of legend
    """
    internal_name = "lumina_randomzied"
    display_name = "Lumina Randomzied"

class BakerySanity(Toggle):
    """
    Randomize the bakery's list of items for sale into the multiworld
    """
    internal_name = "bakery_sanity"
    display_name = "Bakery Sanity"
    
class RestaurantSanity(Toggle):
    """
    Randomize the restaurant's list of items for sale into the multiworld
    """
    internal_name = "restaurant_sanity"
    display_name = "Restaurant Sanity"

class GrocerySanity(Toggle):
    """
    Randomize the grocery's list of items for sale into the multiworld
    """
    internal_name = "grocery_sanity"
    display_name = "Grocery Sanity"

class GroceryRevive(Toggle):
    """
    Force S-Revive to always show up in the shop, collecting a S-Revive from the multiworld will give a price discount
    """
    internal_name = "grocery_s_revive"
    display_name = "Grocery S-Revive"

class ToySanity(Toggle):
    """
    Randomize the toy shop's list of items for sale into the multiworld, only includes Series 1 through 5 (Does not require Soda Fountain)
    """
    internal_name = "toy_sanity"
    display_name = "Toy Sanity"

class TechSanity(Toggle):
    """
    Randomize the Weapon Techniques and Fusion upgrade into the multiworld
    """
    internal_name = "tech_sanity"
    display_name = "Tech Sanity"

class ScrollSanity(Toggle):
    """
    Randomize the Five Legendary Scrolls into the multiworld
    """
    internal_name = "scroll_sanity"
    display_name = "Scroll Sanity"

class SkyScrollLogic(Choice):
    """
    Only Considered when Scroll Sanity is On. Changes what is considered in logic when Sky Scroll is available

    Vanilla - Sky Scroll is not considered, some easy to reach checks may show as out of logic
    Simple - Sky Scroll maybe expected to be used to cross gaps or go up a certain slope
    Complex - Sky Scroll maybe expected to be used to access areas early or out of order (may expect player to softlock if needed to reach a location [Save often])
    """
    internal_name = "sky_scroll_logic"
    display_name = "Sky Scroll Logic"
    option_vanilla = 1
    option_simple = 2
    option_complex = 3
    default = 1

class HairColor(Choice):
    """
    Pick Hair Color, or choose custom for further customization
    """
    internal_name = "hair_color_selection"
    display_name = "Hair Color"
    option_custom = 1
    option_white = 2
    option_red = 3
    option_blue = 4
    option_green = 5
    option_orange = 6
    option_pink = 7
    option_yellow = 8
    default = 2

class CustomHairColor(FreeText):
    """
    Must select custom from hair color, write hex code of desired color in the format RRGGBB (see https://www.color-hex.com/ for assistance) do not include # must be exactly 6 digits and a valid hex code i.e. 0 through F values only
    """
    internal_name = "custom_hair_color_selection"
    display_name = "Custom Hair Color"
    default = "B751A7"

@dataclass
class BFMOptions(PerGameCommonOptions):
    lumina_randomzied: LuminaRandomized
    bakery_sanity: BakerySanity
    restaurant_sanity: RestaurantSanity
    grocery_sanity: GrocerySanity
    grocery_s_revive: GroceryRevive
    toy_sanity: ToySanity
    tech_sanity: TechSanity
    scroll_sanity: ScrollSanity
    sky_scroll_logic: SkyScrollLogic
    death_link: DeathLink
    hair_color_selection: HairColor
    custom_hair_color_selection: CustomHairColor