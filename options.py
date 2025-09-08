from dataclasses import dataclass
from Options import Choice, Toggle, PerGameCommonOptions, DeathLink, FreeText, DefaultOnToggle, Range
from typing import Dict, Any, TYPE_CHECKING
import logging
if TYPE_CHECKING:
    from . import BFMWorld

class SetGoal(Choice):
    """
    Select which Goal in order to win this game of Brave Fencer Musashi

    Rescue All NPCs - save all 35 Castle NPCs lost in the multiworld
    Rescue [X] NPCs - save a portion of Castle NPCs, check 'NPCs Required to Goal' to adjust count
    Defeat [ ] Guardian/Boss - Win after defeating the respective boss (listed in order of occurrence)
    """
    internal_name = "goal"
    display_name = "Set Winning Goal"
    option_rescue_all_npcs = 1
    option_rescue_x_npcs = 2
    option_defeat_earth_crest_guardian = 3
    option_defeat_water_crest_guardian = 4
    option_defeat_fire_crest_guardian = 5
    option_defeat_wind_crest_guardian = 6
    option_defeat_sky_crest_guardian = 7
    option_defeat_final_boss = 8
    default = 1

class NPCGoal(Range):
    """
    How many Castle NPCs will need to be rescued in order to goal. Only relevant when 'Rescue X NPCs' is set as the goal.
    10 - very very short playthrough possibly all in sphere 1 (<30 minutes solo)
    20 - short playthrough (1-3 hours solo)
    35 - same as rescue all NPCs (4-7 hours solo)
    """
    internal_name = "npc_goal"
    display_name = "NPCs Required to Goal"
    range_start = 10
    range_end = 35
    default = 20

class MaxHpLogic(Range):
    """
    Amount of max hp expected logically before going to Soda Fountain
    0 - 150 max hp 
    1 - 200 max hp
    2 - 225 max hp
    ...
    13 - 500 max hp
    """
    internal_name = "max_hp_logic"
    display_name = "Max Hp Logic for Soda Fountain"
    range_start = 0
    range_end = 13
    default = 9

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

class GrocerySanityHealLogic(Toggle):
    """
    Require either C-Drink or W-Gel logically before being required to defeat a Crest Guardian (only relevant when Grocery Sanity is 'true')
    """
    internal_name = "grocery_sanity_heal_logic"
    display_name = "Grocery Sanity Healing Item Combat Logic"

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

class CoreSanity(Toggle):
    """
    Randomize the first four elemental Boss Cores needed to activate the elemental crests into the multiworld
    """
    internal_name = "core_sanity"
    display_name = "Boss Core Sanity"

class EarlySkullpion(Toggle):
    """
    Add the NPCs required for Skullpion, Lumina (if randomized), and Bracelet to the early generation (Will likely place in Sphere 1, this setting is only recommended for multiworld generations to avoid being stuck in chapter 2)
    """
    internal_name = "early_skullpion"
    display_name = "Early Skullpion"

class SkipMinigameAntGondola(Toggle):
    """
    Skip over the minigame get through the mines to reach the Wind Crest Guardian (still need to turn on the power and hop in the basket)
    """
    internal_name = "skip_minigame_ant_gondola"
    display_name = "Skip Minigame Ant Gondola"

class FastWalk(Toggle):
    """
    Hold L1 to go super fast (while on solid ground)
    """
    internal_name = "fast_walk"
    display_name = "Fast Walking Speed"

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
    goal: SetGoal
    npc_goal: NPCGoal
    max_hp_logic: MaxHpLogic
    lumina_randomzied: LuminaRandomized
    bakery_sanity: BakerySanity
    restaurant_sanity: RestaurantSanity
    grocery_sanity: GrocerySanity
    grocery_s_revive: GroceryRevive
    grocery_sanity_heal_logic: GrocerySanityHealLogic
    toy_sanity: ToySanity
    tech_sanity: TechSanity
    scroll_sanity: ScrollSanity
    sky_scroll_logic: SkyScrollLogic
    core_sanity: CoreSanity
    early_skullpion: EarlySkullpion
    skip_minigame_ant_gondola: SkipMinigameAntGondola
    death_link: DeathLink
    fast_walk: FastWalk
    hair_color_selection: HairColor
    custom_hair_color_selection: CustomHairColor