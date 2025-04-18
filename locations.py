from typing import Dict, NamedTuple, Set, Optional, List


class BFMLocationData(NamedTuple):
    region: str
    location_group: Optional[str] = None


location_base_id = 0x06dc40

location_table: Dict[str, BFMLocationData] = {
    "Guard Bincho - Somnolent Forest": BFMLocationData("Somnolent Forest"),
    "Seer Bincho - Somnolent Forest": BFMLocationData("Somnolent Forest"),
    "Hawker Bincho - Somnolent Forest Deadend": BFMLocationData("Somnolent Forest Deadend"),
    "Maid Bincho - Somnolent Forest Behind Steam": BFMLocationData("Somnolent Forest Behind Steam"),
    "MusicianB Bincho - Steamwood Forest": BFMLocationData("Steamwood Forest"),
    "SoldierA Bincho - Twinpeak Entrance": BFMLocationData("Twinpeak Entrance"),
    "MercenC Bincho - Twinpeak Around the Bend": BFMLocationData("Twinpeak Around the Bend"),
    "CarpentA Bincho - Twinpeak Second Peak": BFMLocationData("Twinpeak Second Peak"),
    "KnightB Bincho - Twinpeak Second Peak": BFMLocationData("Twinpeak Second Peak"),
    "Shepherd Bincho - Twinpeak Rope Bridge": BFMLocationData("Twinpeak Rope Bridge"),
    "KnightA Bincho - Mine Conveyor Belt Room": BFMLocationData("Mine Conveyor Belt Room"),
    "CookA Bincho - Misteria Underground Lake": BFMLocationData("Misteria Underground Lake"),
    "Acrobat Bincho - Steamwood Forest": BFMLocationData("Steamwood Forest"),
    "CarpentC Bincho - Mine Conveyor Belt Room": BFMLocationData("Mine Conveyor Belt Room"),
    "Knitter Bincho - Twinpeak Path to Skullpeon": BFMLocationData("Twinpeak Path to Skullpeon"),
    "Chief Bincho - Misteria Underground Lake": BFMLocationData("Misteria Underground Lake"),
    "Doctor Bincho - Twinpeak Around the Bend": BFMLocationData("Twinpeak Around the Bend"),
}

sphere_one: List[str] = [
    "Guard Bincho - Somnolent Forest",
    "Seer Bincho - Somnolent Forest",
    "Hawker Bincho - Somnolent Forest",
    "MusicianB Bincho - Steamwood Forest",
    "SoldierA Bincho - Twinpeak Entrance",
    "Acrobat Bincho - Steamwood Forest"
]

standard_location_name_to_id: Dict[str, int] = {name: location_base_id + index for index, name in enumerate(location_table)}

#bandaid fix please remove
standard_location_name_to_id["KnightA Bincho - Mine Conveyor Belt Room"] += 5
standard_location_name_to_id["CookA Bincho - Misteria Underground Lake"] += 5
standard_location_name_to_id["Acrobat Bincho - Steamwood Forest"] += 5
standard_location_name_to_id["CarpentC Bincho - Mine Conveyor Belt Room"] += 8
standard_location_name_to_id["Knitter Bincho - Twinpeak Path to Skullpeon"] += 9
standard_location_name_to_id["Chief Bincho - Misteria Underground Lake"] += 11
standard_location_name_to_id["Doctor Bincho - Twinpeak Around the Bend"] += 15

all_locations = location_table.copy()

location_name_groups: Dict[str, Set[str]] = {}
for loc_name, loc_data in location_table.items():
    loc_group_name = loc_name.split(" - ", 1)[1]
    location_name_groups.setdefault(loc_group_name, set()).add(loc_name)
    if loc_data.location_group:
        location_name_groups.setdefault(loc_data.location_group, set()).add(loc_name)