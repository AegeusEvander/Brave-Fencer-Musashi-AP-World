from typing import Dict, NamedTuple, Set, Optional, List


class BFMLocationData(NamedTuple):
    region: str
    location_group: Optional[str] = None


location_base_id = 0x06dc40

location_table: Dict[str, BFMLocationData] = {
    "Guard Bincho - Somnolent Forest": BFMLocationData("Somnolent Forest"),
    "Seer Bincho - Somnolent Forest": BFMLocationData("Somnolent Forest"),
    "Hawker Bincho - Somnolent Forest Deadend": BFMLocationData("Somnolent Forest Deadend"),
    "MusicianB Bincho - Steamwood Forest": BFMLocationData("Steamwood Forest"),
    "SoldierA Bincho - Twinpeak Entrance": BFMLocationData("Twinpeak Entrance"),
    "Acrobat Bincho - Steamwood Forest": BFMLocationData("Steamwood Forest"),
}

sphere_one: List[str] = [
    "Guard Bincho - Somnolent Forest",
    "Seer Bincho - Somnolent Forest",
    "Hawker Bincho - Somnolent Forest",
    "MusicianB Bincho - Steamwood Forest",
    "Acrobat Bincho - Steamwood Forest",
    "SoldierA Bincho - Twinpeak Entrance"
]

standard_location_name_to_id: Dict[str, int] = {name: location_base_id + index for index, name in enumerate(location_table)}

all_locations = location_table.copy()

location_name_groups: Dict[str, Set[str]] = {}
for loc_name, loc_data in location_table.items():
    loc_group_name = loc_name.split(" - ", 1)[1]
    location_name_groups.setdefault(loc_group_name, set()).add(loc_name)
    if loc_data.location_group:
        location_name_groups.setdefault(loc_data.location_group, set()).add(loc_name)