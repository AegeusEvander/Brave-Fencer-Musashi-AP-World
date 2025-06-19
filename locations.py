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
    "Baliff Bincho - Restaurant Basement Behind Pole Jumps": BFMLocationData("Restaurant Basement Behind Pole Jumps"),
    "Taster Bincho - Restaurant Basement Path to Crest Guardian": BFMLocationData("Restaurant Basement Path to Crest Guardian"),
    "CarpentB Bincho - Restaurant Basement Dark Platform Maze 2": BFMLocationData("Restaurant Basement Dark Platform Maze 2"),
    "Weaver Bincho - Twinpeak Second Peak": BFMLocationData("Twinpeak Second Peak"),
    "SoldierB Bincho - Restaurant Basement Planks Over Lava": BFMLocationData("Restaurant Basement Planks Over Lava"),
    "KnightA Bincho - Mine Conveyor Belt Room": BFMLocationData("Mine Conveyor Belt Room"),
    "CookA Bincho - Misteria Underground Lake": BFMLocationData("Misteria Underground Lake"),
    "Acrobat Bincho - Steamwood Forest": BFMLocationData("Steamwood Forest"),
    "MercenB Bincho - Restaurant Basement Bowling 2": BFMLocationData("Restaurant Basement Bowling 2"),
    "Janitor Bincho - Frozen Palace Blue Eye Door": BFMLocationData("Frozen Palace Blue Eye Door"),
    "Artisan Bincho - Island of Dragons": BFMLocationData("Island of Dragons"),
    "CarpentC Bincho - Mine Conveyor Belt Room": BFMLocationData("Mine Conveyor Belt Room"),
    "MusicianC Bincho - Frozen Palace Green Eye Maze": BFMLocationData("Frozen Palace Green Eye Maze"),
    "Knitter Bincho - Twinpeak Path to Skullpion": BFMLocationData("Twinpeak Path to Skullpion"),
    "Chef Bincho - Frozen Palace Crate Pile": BFMLocationData("Frozen Palace Crate Pile"),
    "MercenA Bincho - Restaurant Basement Bowling 1": BFMLocationData("Restaurant Basement Bowling 1"),
    "Chief Bincho - Misteria Underground Lake": BFMLocationData("Misteria Underground Lake"),
    "CookB Bincho - Upper Mines": BFMLocationData("Upper Mines"),
    "Conductor Bincho - Upper Mines Ant Parade": BFMLocationData("Upper Mines Ant Parade"),
    "Butcher Bincho - Frozen Palace Atrium Right Balcony": BFMLocationData("Frozen Palace Atrium Right Balcony"),
    "KnightC Bincho - Restaurant Basement Dark Platform Maze 3": BFMLocationData("Restaurant Basement Dark Platform Maze 3"),
    "Doctor Bincho - Twinpeak Around the Bend": BFMLocationData("Twinpeak Around the Bend"),
    "KnightD Bincho - Upper Mines Before Digging": BFMLocationData("Upper Mines Before Digging"),
    "Alchemist Bincho - Frozen Palace Red Eye Maze": BFMLocationData("Frozen Palace Red Eye Maze"),
    "Librarian Bincho - Restaurant Basement Near Rotating Platforms": BFMLocationData("Restaurant Basement Near Rotating Platforms"),
    "Minku - Grillin Village Near Twinpeak": BFMLocationData("Upper Grillin Village",location_group = "Minku"),
    "Minku - Somnolent Forest Hidden Path": BFMLocationData("Somnolent Forest",location_group = "Minku"),
    "Minku - Twinpeak Around the Bend": BFMLocationData("Twinpeak Around the Bend",location_group = "Minku"), 
    "Minku - Grillin Village Above Gondola": BFMLocationData("Upper Grillin Village",location_group = "Minku"),
    "Minku - Skullpion Arena": BFMLocationData("Skullpion Arena",location_group = "Minku"),
    "Minku - Steamwood Forest": BFMLocationData("Steamwood Forest",location_group = "Minku"),
    "Minku - Somnolent Forest": BFMLocationData("Somnolent Forest",location_group = "Minku"),
    "Minku - Twinpeak End of Stream": BFMLocationData("Twinpeak Around the Bend",location_group = "Minku"),
    "Minku - Misteria Underground Lake": BFMLocationData("Misteria Underground Lake",location_group = "Minku"),
    "Minku - Grillin Reservoir": BFMLocationData("Grillin Reservoir",location_group = "Minku"),
    "Minku - Upper Mines Below Big Fan": BFMLocationData("Upper Mines Big Fan Room",location_group = "Minku"),
    "Minku - Upper Mines": BFMLocationData("Upper Mines",location_group = "Minku"),
    "Minku - Near Wind Scroll": BFMLocationData("Wind Scroll",location_group = "Minku"),
    "500 Drans Chest - Somnolent Forest Behind Steam": BFMLocationData("Somnolent Forest Behind Steam"),
    "Old Crown Chest - Somnolent Forest": BFMLocationData("Somnolent Forest",location_group = "Chest"),
    "Aged Coin Chest - Steamwood Forest": BFMLocationData("Steamwood Forest",location_group = "Chest"),
    "200 Drans Chest - Twinpeak Around the Bend": BFMLocationData("Twinpeak Around the Bend",location_group = "Chest"),
    "Old Book Chest - Twinpeak Around the Bend": BFMLocationData("Twinpeak Around the Bend",location_group = "Chest"),
    "Rock Chest - Twinpeak Second Peak": BFMLocationData("Twinpeak Second Peak",location_group = "Chest"),
    "Dagger Chest - Twinpeak Rope Bridge": BFMLocationData("Twinpeak Rope Bridge",location_group = "Chest"),
    "Bracelet Chest - Twinpeak Entrance": BFMLocationData("Twinpeak Entrance",location_group = "Chest"),
    "200 Drans Chest - Twinpeak Path to Skullpion": BFMLocationData("Twinpeak Path to Skullpion",location_group = "Chest"),
    "Red Eye Chest - Frozen Palace Red Eye Room": BFMLocationData("Frozen Palace Red Eye Room",location_group = "Chest"),
    "Blue Eye Chest - Frozen Palace Red Eye Maze": BFMLocationData("Frozen Palace Red Eye Maze",location_group = "Chest"),
    "Green Eye Chest - Frozen Palace Green Eye Maze": BFMLocationData("Frozen Palace Green Eye Maze",location_group = "Chest"),
    "Red Shoes Chest - Frozen Palace Atrium Left Balcony": BFMLocationData("Frozen Palace Atrium Left Balcony",location_group = "Chest"),
    "Long Tube Chest - Frozen Palace Red Eye Door": BFMLocationData("Frozen Palace Red Eye Door",location_group = "Chest"),
    "500 Drans Chest - Island of Dragons": BFMLocationData("Island of Dragons",location_group = "Chest"),
    "Shield Chest - Restaurant Basement Bowling 1": BFMLocationData("Restaurant Basement Bowling 1",location_group = "Chest"),
    "Odd Hat Chest - Restaurant Basement Bowling 1": BFMLocationData("Restaurant Basement Bowling 1",location_group = "Chest"),
    "Old Sword Chest - Restaurant Basement": BFMLocationData("Restaurant Basement",location_group = "Chest"),
    "Old Shirt Chest - Grillin Reservoir": BFMLocationData("Grillin Reservoir",location_group = "Chest"),
    "300 Drans Chest - Restaurant Basement": BFMLocationData("Restaurant Basement",location_group = "Chest"),
    "Old Pipe Chest - Restaurant Basement Planks Over Lava": BFMLocationData("Restaurant Basement Planks Over Lava",location_group = "Chest"),
    "Powder Chest - Restaurant Basement Teleport Maze": BFMLocationData("Restaurant Basement Teleport Maze",location_group = "Chest"),
    "Helmet Chest - Restaurant Basement Dark Platform Maze 3": BFMLocationData("Restaurant Basement Dark Platform Maze 3",location_group = "Chest"),
    "Old Glove Chest - Misteria Underground Lake": BFMLocationData("Misteria Underground Lake",location_group = "Chest"),
    "Cloth Chest - Restaurant Basement": BFMLocationData("Restaurant Basement",location_group = "Chest"),
    "Used Boot Chest - Grillin Reservoir": BFMLocationData("Grillin Reservoir",location_group = "Chest"),
    "White Cloth Chest - Frozen Palace Green Eye Maze": BFMLocationData("Frozen Palace Green Eye Maze",location_group = "Chest"),
    "Red Cloth Chest - Frozen Palace Green Eye Maze": BFMLocationData("Frozen Palace Green Eye Maze",location_group = "Chest"),
    "Black Cloth Chest - Frost Dragon Door": BFMLocationData("Frost Dragon Door",location_group = "Chest"),
    "Glasses Chest - Somnolent Forest": BFMLocationData("Somnolent Forest",location_group = "Chest"),
    "Large Tool Chest - Upper Mines": BFMLocationData("Upper Mines",location_group = "Chest"),
    "Odd Bone Chest - Upper Mines": BFMLocationData("Upper Mines",location_group = "Chest"),
    "Armor Chest - Reservoir Tunnel": BFMLocationData("Reservoir Tunnel",location_group = "Chest"),
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

all_locations = location_table.copy()

table_ids_to_hint: List[int] = []
for loc_name, loc_id in standard_location_name_to_id.items():
    table_ids_to_hint.append(loc_id)

location_name_groups: Dict[str, Set[str]] = {}
for loc_name, loc_data in location_table.items():
    loc_group_name = loc_name.split(" - ", 1)[1]
    location_name_groups.setdefault(loc_group_name, set()).add(loc_name)
    if loc_data.location_group:
        location_name_groups.setdefault(loc_data.location_group, set()).add(loc_name)