from dataclasses import dataclass
from Options import Choice, Toggle, PerGameCommonOptions, DeathLink, FreeText, DefaultOnToggle, Range
from typing import Dict, Any, TYPE_CHECKING
import logging
if TYPE_CHECKING:
    from . import BFMWorld

class SetLang(Choice):
    """
    Select which language of items and locations to send to the multiworld (not the version of the game to be played)
    en- English
    jp- 日本語
    """
    internal_name = "set_lang"
    display_name = "Set Language"
    option_en = 1
    option_jp = 2
    default = 1

class SpoilerItemsInEnglish(DefaultOnToggle):
    """
    Only considered if Set Language is JP (also is not saved to slot data)
    Spoiler log shows progression with Japanese locations but English items
    """
    internal_name = "spoiler_items_in_english"
    display_name = "Spoiler Items Displayed in English"

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

class StartingMaxHP(Range):
    """
    Amount of max hp to start the game with (max hp will never go over 500)
    Setting max hp to 1 will remove all max hp up from itempool (and disable deathlink)
    """
    internal_name = "starting_hp"
    display_name = "Starting Max Hp"
    range_start = 1
    range_end = 200
    default = 150

class MaxHpLogic(Range):
    """
    Amount of max hp expected logically before going to Soda Fountain (ignored if starting max hp is 1)
    """
    internal_name = "max_hp_logic"
    display_name = "Max Hp Logic for Soda Fountain"
    range_start = 150
    range_end = 500
    default = 400

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

class GrocerySanityHealLogic(DefaultOnToggle):
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

class LevelSanity(Toggle):
    """
    Randomize the stats gained from leveling into the multiworld
    """
    internal_name = "level_sanity"
    display_name = "Level Sanity"

class LevelBundles(Range):
    """
    Number of bundles to receive lvl 30 stats (Body, Mind, Fusion, Lumina)
    Lowering number bundles will leave more room for Traps/Filler
    Only active if Level Sanity is True
    """
    internal_name = "level_bundles"
    display_name = "Number of bundles for combat stats"
    range_start = 1
    range_end = 29
    default = 29

class StatGainModifier(Choice):
    """
    change how stats are gained
    Early - Most stats are gained in the first couple bundles (maybe better for shorter goals)
    Vanilla - Stats are gained roughly the same rate as the base game
    Enhanced - Stats start similar to Vanilla but dramatically increase after receiving half of the stat up bundles (may make Wind Crest Guardian and path to Sky Crest Guardian easier)
    Only active if Level Sanity is True
    """
    internal_name = "stat_gain_modifier"
    display_name = "Stat Game Modifier"
    option_early = 1
    option_vanilla = 2
    option_enhanced = 3
    default = 2

class XPGain(Choice):
    """
    Amount to multiply XP receieved, higher multiplier is faster leveling. Leveling may be required for progression so it is recommended to have increased XP gain.
    No XP Gain - Challenge run modifier (level 1 the entire game), checks for leveling are removed (if enabled)
    """
    internal_name = "xp_gain"
    display_name = "XP Gain Multiplier"
    option_no_xp_gain = 1
    option_quarter = 2
    option_half = 3
    option_vanilla = 4
    option_double = 5
    option_quadruple = 6
    option_ten_fold = 7
    option_one_hundred_fold = 8
    default = 6

class XPGainMind(Choice):
    """
    Amount to multiply XP receieved for Mind, higher multiplier is faster leveling. Mind is gained by taking steps which can be a slow process to get to max level. Consider a high XP gain overall or at least a higher xp gain for Mind
    defaults to the same multiplier chosen in xp_gain
    """
    internal_name = "xp_gain_mind"
    display_name = "XP Gain Multiplier for Mind"
    option_same_as_above = 1
    option_half = 2
    option_vanilla = 3
    option_double = 4
    option_quadruple = 5
    option_ten_fold = 6
    option_one_hundred_fold = 7
    default = 1

class EarlySkullpion(Toggle):
    """
    Add the NPCs required for Skullpion, Lumina (if randomized), and Bracelet to the early generation (Will likely place in Sphere 1, this setting is only recommended for multiworld generations to avoid being stuck in chapter 2)
    """
    internal_name = "early_skullpion"
    display_name = "Early Skullpion"

class BoulderChaseZoomLevel(Choice):
    """
    slightly change zoom level during Chapter 1 boulder chase sequence
    """
    internal_name = "boulder_chase_zoom"
    display_name = "Boulder Chase Zoom Level"
    option_tight = 1
    option_vanilla = 2
    option_wide = 3
    default = 2

class LenoSniffModifier(Range):
    """
    Modify how long Leno spends sniffing when attempting to find the path to the graveyard
    10 -> 10% of the vanilla time
    100 -> 100% vanilla
    200 -> 200% spend twice the time
    """
    internal_name = "leno_sniff_modifier"
    display_name = "Leno Sniff Modifier"
    range_start = 10
    range_end = 200
    default = 80

class SkipMinigameFollowLeno(Toggle):
    """
    Skip over the minigame follow Leno through meandering forest to get to the graveyard
    Going into meandering forest with Leno will instead take you directly to the graveyard
    """
    internal_name = "skip_minigame_follow_leno"
    display_name = "Skip Minigame Follow Leno"

class RaftStartingHP(Range):
    """
    How many logs to start with when doing the rafting minigame
    """
    internal_name = "raft_hp"
    display_name = "Raft Starting HP"
    range_start = 1
    range_end = 4
    default = 4

class RaftDifficulty(Choice):
    """
    Adjust the difficulty for the rafting minigame
    Vanilla - No adjustments
    Invincible - Never lose logs
    Regrow Logs - Regain logs after a period of time
    """
    internal_name = "raft_difficulty"
    display_name = "Raft Difficulty"
    option_vanilla = 1
    option_invincible = 2
    option_regrow_logs = 3
    default = 1

class RaftRegrow(Range):
    """
    Time before regrowing a log during rafting (needs difficulty set to regrow logs to work)
    # -> time in seconds before regrowing a log
    logs that are regained are currently invisible
    """
    internal_name = "raft_regrow"
    display_name = "Raft Regrow"
    range_start = 1
    range_end = 50
    default = 20

class SteamwoodTimerModifier(Range):
    """
    Modify how fast the 24 hour timer for Steamwood ticks down (both first and second visit)
    1 -> 1% of the vanilla time (roughly IRL time)
    100 -> 100% vanilla
    150 -> 150% timer ticks down 50% faster
    """
    internal_name = "steamwood_timer"
    display_name = "Steamwood Timer Modifier"
    range_start = 1
    range_end = 150
    default = 50

class SteamwoodValveTimeModifier(Range):
    """
    Modify the starting timer inbetween valves for Steamwood ticks down (both first and second visit)
    90 -> 90% of the vanilla time to complete the next valve (harder)
    100 -> 100% vanilla
    165 -> 165% timer starts 65% higher
    """
    internal_name = "steamwood_valve_timer"
    display_name = "Steamwood Valve Time Modifier"
    range_start = 90
    range_end = 165
    default = 130

class SteamwoodDisableValveCountdown(Toggle):
    """
    Whether to disable the countdown for the inbetween valve timer
    """
    internal_name = "steamwood_disable_countdown"
    display_name = "Steamwood Disable Valve Countdown"

class SteamwoodNumberOfValves(Range):
    """
    The number of valves to be closed to finish steamwood. In the vanilla game you need to complete all 8 but reducing this number will skip over numbers
    If set to 1 only valve 8 will need to be completed, otherwise starts on valve 1 and finishes on valve 8
    """
    internal_name = "steamwood_number_valves"
    display_name = "Steamwood Number of Valves"
    range_start = 1
    range_end = 8
    default = 8

class SteamwoodRandomizeValveOrder(Toggle):
    """
    Whether to randomize valve order or not. Randomized on entering steamwood. The lowest number valve that has a red light is the next valve to be completed.
    """
    internal_name = "steamwood_random_valves"
    display_name = "Steamwood Randomize Valve Order"

class SteamwoodPressureRiseRate(Choice):
    """
    Adjust the rate of pressure gain on some valves
    Vanilla - No adjustments
    Faster - Valves 1 through 4 will have the same pressure rise as vanilla valve 5
    Slower - Valves 5 through 8 will have slightly lower pressure rise
    Even - All valves have the same pressure rise as vanilla valve 4
    """
    internal_name = "steamwood_pressure_rise_rate"
    display_name = "Steamwood Pressure Rise Rate"
    option_vanilla = 1
    option_Faster = 2
    option_Slower = 3
    option_Even = 4
    default = 4

class SteamwoodAdjustProgressLost(Range):
    """
    The amount of progress lost when confirming while in the red range
    -96 -> all progress lost
    -16 -> vanilla progress lost
    >0 -> gain progress instead
    """
    internal_name = "steamwood_progress_lost"
    display_name = "Steamwood Adjust Progress Lost"
    range_start = -96
    range_end = 8
    default = -8

class SteamwoodWidthOfOkPressure(Range):
    """
    The width in pixels of acceptable range for pressure
    10 - slightly narrower acceptable range
    12 - vanilla
    96 - the entire range is green
    """
    internal_name = "steamwood_width_of_ok_pressure"
    display_name = "Steamwood Width of Okay Pressure"
    range_start = 10
    range_end = 96
    default = 18

class SteamwoodValveProgressModifier(Range):
    """
    Modify the amount of progressed gained when selecting within the acceptable pressure range
    50 -> 50% gain half progress when succeeding
    100 -> 100% vanilla
    200 -> 200% gain double progress when succeeding
    """
    internal_name = "steamwood_valve_progress_modifier"
    display_name = "Steamwood Valve Progress Modifier"
    range_start = 50
    range_end = 200
    default = 100

class SteamwoodNoFailOverPressure(Toggle):
    """
    Vanilla overpressure resets bar to 0, if enabled will keep pressure level within acceptable levels 
    effectively making it have no failure state after letting pressure rise
    """
    internal_name = "steamwood_no_fail_over_pressure"
    display_name = "Steamwood No fail Over Pressure"

class SteamwoodElevatorLogic(Choice):
    """
    Adjust the logic for the elevator
    Vanilla - No adjustments
    Patient - Elevator will wait until you step on it before proceeding to the next floor (may need to cycle up and down first)
    Troll - Elevator will wait until you step on it before proceeding downwards (may need to cycle up and down first)
    """
    internal_name = "steamwood_elevator_logic"
    display_name = "Steamwood Elevator Logic"
    option_vanilla = 1
    option_patient = 2
    option_troll = 3
    default = 2

class AqualinTimerModifier(Range):
    """
    Modify how fast the 12 hour timer for collecting Aqualin ticks down
    1 -> 1% of the vanilla time (roughly IRL time)
    100 -> 100% vanilla
    150 -> 150% timer ticks down 50% faster
    """
    internal_name = "aqualin_timer"
    display_name = "Aqualin Timer Modifier"
    range_start = 1
    range_end = 150
    default = 50

class RestaurantTeleportMazeNoFail(DefaultOnToggle):
    """
    Vanilla logic for picking the wrong teleporter is to send Musashi back to the start or much earlier part of the dungeon
    Enabling this makes picking the wrong teleport send Musashi back to the start of the same room until the correct teleport is selected
    """
    internal_name = "restaurant_teleport_maze_no_fail"
    display_name = "Restaurant Teleport Maze No Fail"

class ChurchFightTimeModifier(Range):
    """
    Modify how fast the day timer progresses during the church fight
    50 -> 50% time progresses at half speed
    100 -> 100% vanilla
    600 -> 600% time progresses 6x faster than vanilla (may still need to move to not lose)
    """
    internal_name = "church_fight_time_modifier"
    display_name = "Church Fight Time Modifier"
    range_start = 50
    range_end = 600
    default = 100

class SkipTownOnFireMinigame(Toggle):
    """
    Skip over the minigame to extinguish the town's fire with water scroll
    """
    internal_name = "skip_minigame_town_on_fire"
    display_name = "Skip Minigame Town On Fire"

class SkipToFrostPalace(DefaultOnToggle):
    """
    If enabled, after reaching Frost Palace for the first time, Musashi can skip Meandering Forest Maze by going up on the first screen to get to Frost Palace
    """
    internal_name = "skip_to_frost_palace"
    display_name = "Skip to Frost Palace"

class SkipMinigameAntGondola(Toggle):
    """
    Skip over the minigame to get through the mines to reach the Wind Crest Guardian (still need to turn on the power and hop in the basket)
    """
    internal_name = "skip_minigame_ant_gondola"
    display_name = "Skip Minigame Ant Gondola"

class SkipSodaFountainCalendarMaze(Toggle):
    """
    If enabled, skip over the rotating door maze in Soda Fountain where Musashi needs to reference the calendar to find the right path (loading a save might still bring you to the begining of the maze)
    """
    internal_name = "skip_over_calendar_maze"
    display_name = "Skip Over Calendar Maze"

class TopoDanceBattleLogic(Choice):
    """
    Adjust the logic the pattern used by Topo
    Vanilla - No adjustments
    Simple - Easy pattern that is just clockwise or counter-clockwise
    Random - A completely random sequence will be generated on entering room
    """
    internal_name = "topo_dance_battle_logic"
    display_name = "Topo Dance Battle Logic"
    option_vanilla = 1
    option_simple = 2
    option_randomly = 3
    default = 1

class SodaFountainBossRush(Toggle):
    """
    If enabled, skip over all areas that are not a boss fight (no extra healing from chests or enemy drops)
    cutscene intro -> Ben Fight -> Ed Fight -> Topo Fight? -> ToD -> DL
    don't mash through cutscene or it wont apply the fix to connect to Ben
    """
    internal_name = "soda_fountain_boss_rush"
    display_name = "Soda Fountain Boss Rush"

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
    set_lang: SetLang
    spoiler_items_in_english: SpoilerItemsInEnglish
    goal: SetGoal
    npc_goal: NPCGoal
    starting_hp: StartingMaxHP
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
    level_sanity: LevelSanity
    level_bundles: LevelBundles
    stat_gain_modifier: StatGainModifier
    xp_gain: XPGain
    xp_gain_mind: XPGainMind
    early_skullpion: EarlySkullpion
    boulder_chase_zoom: BoulderChaseZoomLevel
    leno_sniff_modifier: LenoSniffModifier
    skip_minigame_follow_leno: SkipMinigameFollowLeno
    raft_hp: RaftStartingHP
    raft_difficulty: RaftDifficulty
    raft_regrow: RaftRegrow
    steamwood_timer: SteamwoodTimerModifier
    steamwood_valve_timer: SteamwoodValveTimeModifier
    steamwood_disable_countdown: SteamwoodDisableValveCountdown
    steamwood_number_valves: SteamwoodNumberOfValves
    steamwood_random_valves: SteamwoodRandomizeValveOrder
    steamwood_pressure_rise_rate: SteamwoodPressureRiseRate
    steamwood_progress_lost: SteamwoodAdjustProgressLost
    steamwood_width_of_ok_pressure: SteamwoodWidthOfOkPressure
    steamwood_valve_progress_modifier: SteamwoodValveProgressModifier
    steamwood_no_fail_over_pressure: SteamwoodNoFailOverPressure
    steamwood_elevator_logic: SteamwoodElevatorLogic
    aqualin_timer: AqualinTimerModifier
    restaurant_teleport_maze_no_fail: RestaurantTeleportMazeNoFail
    church_fight_time_modifier: ChurchFightTimeModifier
    skip_minigame_town_on_fire: SkipTownOnFireMinigame
    skip_to_frost_palace: SkipToFrostPalace
    skip_minigame_ant_gondola: SkipMinigameAntGondola
    skip_over_calendar_maze: SkipSodaFountainCalendarMaze
    topo_dance_battle_logic: TopoDanceBattleLogic
    soda_fountain_boss_rush: SodaFountainBossRush
    death_link: DeathLink
    fast_walk: FastWalk
    hair_color_selection: HairColor
    custom_hair_color_selection: CustomHairColor