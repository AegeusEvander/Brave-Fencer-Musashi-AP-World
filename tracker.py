from typing import TYPE_CHECKING, Any, ClassVar

from BaseClasses import CollectionState, Entrance, Location, Region
from NetUtils import JSONMessagePart
from Options import Option

if TYPE_CHECKING:
    from worlds.AutoWorld import World
else:
    World = object

tracker_map_groups = [
    ("Grillin Village", "grillin_village"),
    ("Upper Grillin Village", "upper_grillin_village"),
    ("Somnolent Forest", "somnolent_forest"),
    ("Steamwood Forest", "steamwood_forest"),
    ("Island of Dragons", "island_of_dragons"),
    ("Twinpeak", [("Skullpion Arena", "hells_valley_arena"),
        ("Path to Skullpion", "valley")]),
    ("Frozen Palace", [("Entrance", "frozen_palace_entrance"),
        ("Blue Eye Hallway", "frozen_palace_blue_eye_hallway"),
        ("Red Eye Room", "frozen_palace_red_eye_room"),
        ("Wolf Room", "frozen_palace_wolf_room"),
        ("Green Eye Maze", "frozen_palace_green_eye_maze"),
        ("Ramp Hallway", "frozen_palace_ramp_hallway"),
        ("Red Eye Maze", "frozen_palace_red_eye_maze"),
        ("Red Eye Hallway", "frozen_palace_red_eye_hallway"),
        ("Spike Bridge", "frozen_palace_spike_bridge"),
        ("Ramp to Dragon Church", "frozen_palace_ramp_to_dragon_church")])
]

map_order = [
    0x1010,# chapter 2 town
    0x1011,# upper village
    0x3014,# somnolent forest
    0x301c,# steamwood forest
    0x3021,# island of dragons
    0x3024,# skullpion arena
    0x302b,# path to skullpion
    0x305c,# frost palace entrance
    0x305d,# frost palace blue eye hallway
    0x305e,# frost palace red eye room
    0x305f,# frost palace wolf room
    0x3060,# frost palace green eye maze
    0x3061,# frost palace ramp hallway
    0x3062,# frost palace red eye maze
    0x3063,# frost palace red eye hallway
    0x3064,# frost palace spike bridge
    0x3065# frost palace ramp to dragon church
]

alternate_map_ids = {
    0x1011: [0x1053, 0x1078, 0x1095]
}

def map_page_index(data: Any) -> int:
    """Converts the area id provided by the game mod to a map index."""
    if not isinstance(data, int):
        return 0
    mapping = {k: i for i,k in enumerate(map_order)}
    alt_id_mapping = {l:mapping[k] for k, j in alternate_map_ids.items() for l in j}
    mapping.update(alt_id_mapping)

    return mapping.get(data,0) 
    """
    if data in [0x1011, 0x1053, 0x1078, 0x1095]: #chapter 2, 3, 4, and 5/6
        # upper village
        return 1
    if data == 0x3014:
        # somnolent forest
        return 2
    if data == 0x301c:
        # steamwood forest
        return 3
    if data == 0x3021:
        # island of dragons
        return 4
    if data == 0x3024:
        # skullpion arena
        return 5
    if data == 0x302b:
        # path to skullpion
        return 6
    if data == 0x305c:
        # frost palace entrance
        return 7
    if data == 0x305d:
        # frost palace blue eye hallway
        return 8
    if data == 0x305f:
        # frost palace wolf room
        return 9
    if data == 0x3060:
        # frost palace green eye maze
        return 10
    if data == 0x3061:
        # frost palace ramp hallway
        return 11"""
    return 0
    
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
        "map_page_locations": "locations/locations.json",
        "map_page_setting_key": "{player}_{team}_bfm_area",
        "map_page_index": map_page_index,
        "location_setting_key": "{player}_{team}_bfm_coords",
        "location_icon_coords": location_icon_coords,
        "map_page_groups": tracker_map_groups
    }