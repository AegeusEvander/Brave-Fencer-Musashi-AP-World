from typing import TYPE_CHECKING, Any, ClassVar

from BaseClasses import CollectionState, Entrance, Location, Region
from NetUtils import JSONMessagePart
from Options import Option

if TYPE_CHECKING:
    from . import BFMWorld
    from worlds.AutoWorld import World
else:
    World = object

tracker_map_groups = [
    ("Castle", [
        ("Outside", "castle_outside"),
        ("Bedroom", "castle_bedroom"),
        ("Library", "castle_library"),
        ("Castle Meeting Room", "castle_meeting_room"),
        ("Starting Forest", "starting_forest"),
        ("Spiral Tower Outside", "spiral_tower_outside"),
        ("Spiral Tower Inside", "spiral_tower_inside"),
        ("Spiral Tower Roof", "spiral_tower_roof"),
        ("Steam Knight", "castle_steam_knight_fight"),
        ("MOON Cutscene", "cutscene_moon"),
        ("Crystal Cutscene", "cutscene_summon_crystal"),
        ("Outside Steam Knight Cutscene", "cutscene_castle_outside_steam_knight")]),
    ("Village", [
        ("Grillin Village", "grillin_village"),
        ("Reservoir", "reservoir"),
        ("Toy Shop", "toy_shop"),
        ("Bakery", "bakery"),
        ("Grocery", "grocery"),
        ("Inn", "inn"),
        ("Conner's", "conner"),
        ("Church", "church"),
        ("Church Fight", "church_vambee_fight"),
        ("Restaurant", "restaurant"),
        ("Gondola", "castle_gondola")]),
    ("Forest", [
        ("Somnolent Forest", "somnolent_forest"),
        ("Steamwood Forest", "steamwood_forest"),
        ("Outside Steamwood", "steamwood_outside"),
        ("Meandering Forest", "meandering_forest"),
        ("Graveyard", "graveyard"),
        ("Steamwood Inside", "steamwood"),
        ("Island of Dragons", "island_of_dragons"),
        ("Reservoir Tunnel", "reservoir_tunnel"),
        ("Volcano", "volcano"),
        ("Sky Island", "sky_island")]),
    ("Twinpeak", [
        ("Twinpeak Entrance", "twinpeak_entrance"),
        ("First Peak", "first_peak"),
        ("Twinpeak Cave", "cave_1"),
        ("Rope Bridge", "rope_bridge"),
        ("Waterfall Cave", "waterfall_cave"),
        ("Second Peak", "second_peak"),
        ("Rafting", "rafting"),
        ("Path to Skullpion", "valley"),
        ("Skullpion Arena", "hells_valley_arena")]),
    ("Lower Mines", [
        ("Mine Entrance","lower_mines_entrance"),
        ("Ferris Wheels 1","ferris_wheel_1"),
        ("Lower Large Fan","lower_mines_large_fan"),
        ("Ferris Wheels 2","ferris_wheel_2"),
        ("Poison Elevators","poison_elevators"),
        ("Conveyor Belts","conveyor_belts"),
        ("Underground Lake","underground_lake"),
        ("Poison Ferris Wheels","poison_ferris_wheel"),
        ("Scrap Depository","scrap_depository")]),
    ("Restaurant Basement", [
        ("Basement Entrance", "basement_entrance"),
        ("Bowling Entrance", "bowling_entrance"),
        ("Bowling 1", "bowling_1"),
        ("Bowling 2", "bowling_2"),
        ("Teleport Maze Start", "teleport_maze_entrance"),
        ("Teleport Maze 1", "teleport_maze"),
        ("Teleport Maze Right Side Area", "teleport_maze_side_area"),
        ("Teleport Maze Arrow Traps", "teleport_maze_arrow_traps"),
        ("Teleport Maze End", "teleport_maze_end"),
        ("Dark Maze Entrance", "dark_maze_entrance"),
        ("Dark Maze Sliding Blocks", "dark_maze_sliding_block_puzzle"),
        ("Dark Maze 1", "dark_maze"),
        ("Dark Maze Vertical", "dark_maze_vertical_maze"),
        ("Dark Maze 3", "dark_maze_end"),
        ("Rotating Entrance", "rotating_platforms_entrance"),
        ("Rotating Long Platforms", "rotating_platforms_long_platforms"),
        ("Rotating First Lava Area", "rotating_platforms_first_lava_area"),
        ("Rotating Lava and Pendulums", "rotating_platforms_lava_and_pendulums"),
        ("Rotating Final Pendulums", "rotating_platforms_final_pendulum_room"),
        ("Moat and Platforming Over Lava", "moat_and_platforming_over_lava"),
        ("Gauntlet", "relic_keeper_gauntlet"),
        ("Outside Relic Keeper", "outside_relic_keeper"),
        ("Relic Keeper Arena", "relic_keeper_arena")]),
    ("Frozen Palace", [
        ("Courtyard", "courtyard"),
        ("Entrance", "frozen_palace_entrance"),
        ("Blue Eye Hallway", "frozen_palace_blue_eye_hallway"),
        ("Red Eye Room", "frozen_palace_red_eye_room"),
        ("Wolf Room", "frozen_palace_wolf_room"),
        ("Green Eye Maze", "frozen_palace_green_eye_maze"),
        ("Ramp Hallway", "frozen_palace_ramp_hallway"),
        ("Blue Eye Maze", "frozen_palace_blue_eye_maze"),
        ("Red Eye Hallway", "frozen_palace_red_eye_hallway"),
        ("Spike Bridge", "frozen_palace_spike_bridge"),
        ("Ramp to Dragon Church", "frozen_palace_ramp_to_dragon_church"),
        ("Dragon Church", "dragon_church"),
        ("Frost Dragon Arena", "frost_dragon_arena")]),
    ("Upper Mines", [
        ("Upper Entrance", "upper_mines_entrance"),
        ("Rock Slide Bridges", "rock_slide_bridges"),
        ("Upper Poison Elevators", "upper_poison_elevators"),
        ("Windy Path", "windy_path"),
        ("Upper Large Fan", "upper_mines_large_fan"),
        ("Ant Parade", "ant_parade"),
        ("Dig Area", "dig_area_near_knightd"),
        ("Gondola Station", "gondola_station"),
        ("Gondola Minigame", "gondola_minigame"),
        ("Above Queen Ant", "above_queen_ant"),
        ("Queen Ant Arena", "queen_ant_arena")]),
    ("Soda Fountain", [
        ("Electric Walls", "electric_walls"),
        ("Tumble Dryer", "tumble_dryer"),
        ("Ben Fight", "ben_fight"),
        ("Calendar Maze Entrance", "calendar_maze_entrance"),
        ("Calendar Maze Middle", "calendar_maze_middle"),
        ("Calendar Maze Torches", "calendar_maze_torches"),
        ("Calendar Maze End", "calendar_maze_end"),
        ("Ed Fight", "ed_fight"),
        ("Garden 1", "garden"),
        ("Garden 2 Hedge Maze", "garden_2_hedge_maze"),
        ("Garden 3 More Gates", "garden_3_more_gates"),
        ("Garden 4 Climb", "garden_4_climb"),
        ("Factory Entrance", "factory_entrance"),
        ("Factory Steam Knight Head", "factory_steam_knight_head"),
        ("Topo Dance Battle", "topo_dance_battle"),
        ("Spiral to ToD", "spiral_to_ToD"),
        ("ToD", "ToD"),
        ("DL1", "dark_lumina_1"),
        ("DL2 Climb", "dark_lumina_2_climb"),
        ("DL2 Fight", "dark_lumina_2_fight"),
        ("Outside Soda Fountain", "outside_soda_fountain"),
        ("CH3 Start", "chapter_3_start"),
        ("CH4 Start", "chapter_4_start"),
        ("CH5 Start", "chapter_5_start")])
]

map_order = [
    0x1010,# chapter 2 town
    0x3000,# castle Outside
    0x3001,# castle Bedroom
    0x3002,# castle library
    0x3003,# castle meeting room
    0x3004,# castle gondola
    0x3005,# castle MOON
    0x3006,# castle Crystal
    0x3008,# starting forest
    0x3009,# spiral tower outside
    0x300a,# spiral tower inside
    0x300b,# spiral tower roof
    0x300d,# castle outside Steam Knight
    0x300e,# Steam Knight
    0x4013,# chapter 2 toyshop
    #0x1011,# upper village
    0x3014,# somnolent forest
    0x4015,# chapter 2 bakery
    0x4016,# chapter 2 grocery
    0x4017,# chapter 2 inn
    0x4018,# chapter 2 conner
    0x4019,# chapter 2 church
    0x401a,# chapter 2 restaurant
    0x301b,# meandering forest
    0x301c,# steamwood forest
    0x301d,# steamwood
    0x301e,# outside steamwood
    0x3021,# island of dragons
    0x3022,# graveyard
    0x3023,# volcano
    0x3024,# skullpion arena
    0x3025,# Twinpeak Entrance
    0x3026,# First Peak
    0x3027,# Twinpeak Cave 1
    0x3028,# Rope Bridge
    0x3029,# Second Peak
    0x302a,# Rafting
    0x302b,# path to skullpion
    0x302c,# waterfall cave
    0x302d,# gauntlet
    0x302e,# bowling entrance
    0x302f,# bowling 1
    0x3030,# bowling 2
    0x3031,# teleport maze entrance
    0x3032,# teleport maze 1
    0x3033,# teleport maze side area
    0x3034,# basement entrance
    0x3035,# dark maze entrance
    0x3036,# dark maze sliding block
    0x3037,# dark maze 1
    0x3038,# dark maze Vertical
    0x3039,# dark maze end
    0x303a,# rotating platform entrance
    0x303b,# rotating platform long platform
    0x303c,# rotating platform first lava area
    0x303d,# rotating platform lava and pendulums
    0x303e,# rotating platform final pendulums
    0x303f,# Teleport Maze Arrow Trap
    0x3040,# Moat and Platforming Over Lava
    0x3041,# Teleport Maze End
    0x3042,# Relic Keeper Arena
    0x3043,# Lower Mine Entrance
    0x3044,# Lower Mine Ferris Wheel 1
    0x3045,# Lower Mine Large Fan
    0x3046,# Lower Mine Conveyor Belts
    0x3047,# Lower Mine Underground Lake
    0x3048,# Lower Mine Poison Ferris WHeel
    0x3049,# Lower Mine Poison Elevators
    0x304a,# Chapter 3 start
    0x304b,# Lower Mine scrap depository
    0x304c,# Basement outside Relic Keeper
    0x304d,# Reservoir Tunnel
    0x304e,# Reservoir
    0x3050,# Lower Mine Ferris Wheel 2
    0x3051,# Church Vambee Fight
    0x305c,# frost palace entrance
    0x305d,# frost palace blue eye hallway
    0x305e,# frost palace red eye room
    0x305f,# frost palace wolf room
    0x3060,# frost palace green eye maze
    0x3061,# frost palace ramp hallway
    0x3062,# frost palace blue eye maze
    0x3063,# frost palace red eye hallway
    0x3064,# frost palace spike bridge
    0x3065,# frost palace ramp to dragon church
    0x3066,# frost palace dragon church
    0x3067,# frost palace frost dragon
    0x3068,# frost palace courtyard
    0x306a,# Chapter 4 Start
    0x306b,# Upper Mines Entrance
    0x306c,# Upper Mines rock slide bridges
    0x306d,# Upper Mines poison elevators
    0x306e,# Upper Mines windy path
    0x306f,# Upper Mines Large Fan
    0x3070,# Upper Mines ant parade
    0x3071,# Upper Mines Dig Area near KnightD
    0x3072,# Upper Mines Gondola Station
    0x3073,# Upper Mines Gondola Minigame
    0x3074,# Upper Mines Above Queen Ant
    0x3075,# Upper Mines Queen Ant Arena
    0x3076,# Chapter 5 Start
    0x3081,# Sky Island
    0x3082,# Soda Fountain Electric Walls
    0x3083,# Soda Fountain Tumble Dryer
    0x3084,# Soda Fountain Calendar Maze Entrance
    0x3085,# Soda Fountain Calendar Maze Middle
    0x3086,# Soda Fountain Calendar Maze Torches
    0x3087,# Soda Fountain Calendar Maze End
    0x3088,# Soda Fountain Ed
    0x3089,# Soda Fountain Garden 1
    0x308a,# Soda Fountain Garden 2 hedge
    0x308b,# Soda Fountain Factory Entrance
    0x308c,# Soda Fountain Factory Steam Knight Head
    0x308d,# Soda Fountain Topo
    0x308e,# Soda Fountain Spiral to ToD
    0x308f,# Soda Fountain ToD
    0x3090,# Soda Fountain Ben
    0x3091,# Soda Fountain Garden 3 gates
    0x3092,# Soda Fountain Garden 4 climb
    0x309e,# Soda Fountain DL1
    0x309f,# Soda Fountain DL2 Climb
    0x30a0,# Soda Fountain DL2 Fight
    0x30a6,# Soda Fountain outside view
]

alternate_map_ids = {
    #0x1011: [0x1053, 0x1078, 0x1095],
    #0x3034: [0x302d, 0x302e, 0x302f, 0x3030, 0x3031, 0x3032, 0x3033, 0x3035, 0x3036, 0x3037, 0x3038, 0x3039, 0x303a, 0x303b, 0x303c, 0x303d, 0x303e, 0x303f, 0x3040, 0x3041, 0x3042, 0x304c],
    0x301d: [0x3020],
    0x301e: [0x301f],
    0x309f: [0x30a1],
    0x3005: [0x30a2],
}

def map_page_index(data: Any) -> int:
    """Converts the area id provided by the game mod to a map index."""
    if not isinstance(data, int):
        return 0
    mapping = {k: i for i,k in enumerate(map_order)}
    alt_id_mapping = {l:mapping[k] for k, j in alternate_map_ids.items() for l in j}
    mapping.update(alt_id_mapping)

    return mapping.get(data,0) 
    
def location_icon_coords(index: int | None, coords: dict[str, Any]) -> tuple[int, int, str] | None:
    """Converts player coordinates provided by the game mod into image coordinates for the map page."""
    if index is None or not coords:
        return None
    return None
    """
    dx, dy = MAP_OFFSETS[index]
    x = int((coords.get("X", 0) + (ROOM_WIDTH / 2) + dx) / MAP_SCALE_X)
    y = int((coords.get("Y", 0) - (ROOM_HEIGHT / 2) + dy) / MAP_SCALE_Y)
    icon = CHARACTER_ICONS.get(coords.get("Character", 1), "algus")
    return x, y, f
    
    """

class UTMxin(World):
    tracker_world: ClassVar = {
        "map_page_folder": "tracker",
        "map_page_maps": "maps/maps.json",
        #"map_page_maps": ["maps/maps.json"],
        "map_page_locations": "locations/locations.json",
        #"map_page_locations": ["locations/locations.json"],
        "map_page_setting_key": "{player}_{team}_bfm_area",
        "map_page_index": map_page_index,
        #"location_setting_key": "{player}_{team}_bfm_coords",
        #"location_icon_coords": location_icon_coords,
        #"external_pack_key": "ut_pack_path",
        "map_page_groups": tracker_map_groups,
    }


def setup_options_from_slot_data(world: "BFMWorld") -> None:
    if hasattr(world.multiworld, "re_gen_passthrough"):
        if "Brave Fencer Musashi" in world.multiworld.re_gen_passthrough:
            world.using_ut = True
            world.passthrough = world.multiworld.re_gen_passthrough["Brave Fencer Musashi"]
            world.options.set_lang.value = world.passthrough["set_lang"]
            world.options.playthrough_method.value = world.passthrough["playthrough_method"]
            world.options.skip_over_bosses.value = world.passthrough["skip_over_bosses"]
            world.options.goal.value = world.passthrough["goal"]
            world.options.npc_goal.value = world.passthrough["npc_goal"]
            world.options.guardian_goal.value = world.passthrough["guardian_goal"]
            world.options.force_soda_fountain_last.value = world.passthrough["force_soda_fountain_last"]
            world.options.starting_hp.value = world.passthrough["starting_hp"]
            world.options.max_hp_logic.value = world.passthrough["max_hp_logic"]
            world.options.lumina_randomzied.value = world.passthrough["lumina_randomzied"]
            world.options.bakery_sanity.value = world.passthrough["bakery_sanity"]
            world.options.restaurant_sanity.value = world.passthrough["restaurant_sanity"]
            world.options.grocery_sanity.value = world.passthrough["grocery_sanity"]
            world.options.grocery_sanity_heal_logic.value = world.passthrough["grocery_sanity_heal_logic"]
            world.options.toy_sanity.value = world.passthrough["toy_sanity"]
            world.options.tech_sanity.value = world.passthrough["tech_sanity"]
            world.options.scroll_sanity.value = world.passthrough["scroll_sanity"]
            world.options.wind_scroll_logic.value = world.passthrough["wind_scroll_logic"]
            world.options.sky_scroll_logic.value = world.passthrough["sky_scroll_logic"]
            world.options.core_sanity.value = world.passthrough["core_sanity"]
            world.options.level_sanity.value = world.passthrough["level_sanity"]
            world.options.xp_gain.value = world.passthrough["xp_gain"]
            world.options.quest_item_sanity.value = world.passthrough["quest_item_sanity"]
            world.options.bp_sanity.value = world.passthrough["bp_sanity"]
            world.options.time_sanity.value = world.passthrough["time_sanity"]
            world.options.time_sanity_settings.value = world.passthrough["time_sanity_settings"]
            world.options.early_skullpion.value = world.passthrough["early_skullpion"]
            world.options.rumparoni_logic.value = world.passthrough["rumparoni_logic"]
            world.options.double_jump_logic.value = world.passthrough["double_jump_logic"]
            world.options.starting_location.value = world.passthrough["starting_location"]
            world.er_pairings = world.passthrough["er_pairings"]
            world.options.entrance_rando.value = len(world.passthrough["er_pairings"]) > 0
        else:
            world.using_ut = False
    else:
        world.using_ut = False