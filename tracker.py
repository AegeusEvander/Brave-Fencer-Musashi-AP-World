from typing import TYPE_CHECKING, Any, ClassVar

from BaseClasses import CollectionState, Entrance, Location, Region
from NetUtils import JSONMessagePart
from Options import Option

if TYPE_CHECKING:
    from worlds.AutoWorld import World
else:
    World = object


def map_page_index(data: Any) -> int:
    """Converts the area id provided by the game mod to a map index."""
    if not isinstance(data, int):
        return 0

    if data == 0x3014:
        # somnolent forest
        return 1
    if data == 0x301c:
        # steamwood forest
        return 2
    if data == 0x3021:
        # island of dragons
        return 3
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
    }