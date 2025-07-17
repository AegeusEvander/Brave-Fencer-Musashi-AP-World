from typing import Dict, NamedTuple, Set, Optional, List


class BFMLocationData(NamedTuple):
    region: str
    location_group: Optional[str] = None


location_base_id = 0x06dc40

location_table: Dict[str, BFMLocationData] = {
    "Guard Bincho - Somnolent Forest": BFMLocationData("Somnolent Forest",location_group = "Bincho"),
    "Seer Bincho - Somnolent Forest": BFMLocationData("Somnolent Forest",location_group = "Bincho"),
    "Hawker Bincho - Somnolent Forest Deadend": BFMLocationData("Somnolent Forest Deadend",location_group = "Bincho"),
    "Maid Bincho - Somnolent Forest Behind Steam": BFMLocationData("Somnolent Forest Behind Steam",location_group = "Bincho"),
    "MusicianB Bincho - Steamwood Forest": BFMLocationData("Steamwood Forest",location_group = "Bincho"),
    "SoldierA Bincho - Twinpeak Entrance": BFMLocationData("Twinpeak Entrance",location_group = "Bincho"),
    "MercenC Bincho - Twinpeak Around the Bend": BFMLocationData("Twinpeak Around the Bend",location_group = "Bincho"),
    "CarpentA Bincho - Twinpeak Second Peak": BFMLocationData("Twinpeak Second Peak",location_group = "Bincho"),
    "KnightB Bincho - Twinpeak Second Peak": BFMLocationData("Twinpeak Second Peak",location_group = "Bincho"),
    "Shepherd Bincho - Twinpeak Rope Bridge": BFMLocationData("Twinpeak Rope Bridge",location_group = "Bincho"),
    "Baliff Bincho - Restaurant Basement Behind Pole Jumps": BFMLocationData("Restaurant Basement Behind Pole Jumps",location_group = "Bincho"),
    "Taster Bincho - Restaurant Basement Path to Crest Guardian": BFMLocationData("Restaurant Basement Path to Crest Guardian",location_group = "Bincho"),
    "CarpentB Bincho - Restaurant Basement Dark Platform Maze 2": BFMLocationData("Restaurant Basement Dark Platform Maze 2",location_group = "Bincho"),
    "Weaver Bincho - Twinpeak Second Peak": BFMLocationData("Twinpeak Second Peak",location_group = "Bincho"),
    "SoldierB Bincho - Restaurant Basement Planks Over Lava": BFMLocationData("Restaurant Basement Planks Over Lava",location_group = "Bincho"),
    "KnightA Bincho - Mine Conveyor Belt Room": BFMLocationData("Mine Conveyor Belt Room",location_group = "Bincho"),
    "CookA Bincho - Misteria Underground Lake": BFMLocationData("Misteria Underground Lake",location_group = "Bincho"),
    "Acrobat Bincho - Steamwood Forest": BFMLocationData("Steamwood Forest",location_group = "Bincho"),
    "MercenB Bincho - Restaurant Basement Bowling 2": BFMLocationData("Restaurant Basement Bowling 2",location_group = "Bincho"),
    "Janitor Bincho - Frozen Palace Blue Eye Door": BFMLocationData("Frozen Palace Blue Eye Door",location_group = "Bincho"),
    "Artisan Bincho - Island of Dragons": BFMLocationData("Island of Dragons",location_group = "Bincho"),
    "CarpentC Bincho - Mine Conveyor Belt Room": BFMLocationData("Mine Conveyor Belt Room",location_group = "Bincho"),
    "MusicianC Bincho - Frozen Palace Green Eye Maze": BFMLocationData("Frozen Palace Green Eye Maze",location_group = "Bincho"),
    "Knitter Bincho - Twinpeak Path to Skullpion": BFMLocationData("Twinpeak Path to Skullpion",location_group = "Bincho"),
    "Chef Bincho - Frozen Palace Crate Pile": BFMLocationData("Frozen Palace Crate Pile",location_group = "Bincho"),
    "MercenA Bincho - Restaurant Basement Bowling 1": BFMLocationData("Restaurant Basement Bowling 1",location_group = "Bincho"),
    "Chief Bincho - Misteria Underground Lake": BFMLocationData("Misteria Underground Lake",location_group = "Bincho"),
    "CookB Bincho - Upper Mines": BFMLocationData("Upper Mines",location_group = "Bincho"),
    "Conductor Bincho - Upper Mines Ant Parade": BFMLocationData("Upper Mines Ant Parade",location_group = "Bincho"),
    "Butcher Bincho - Frozen Palace Atrium Right Balcony": BFMLocationData("Frozen Palace Atrium Right Balcony",location_group = "Bincho"),
    "KnightC Bincho - Restaurant Basement Dark Platform Maze 3": BFMLocationData("Restaurant Basement Dark Platform Maze 3",location_group = "Bincho"),
    "Doctor Bincho - Twinpeak Around the Bend": BFMLocationData("Twinpeak Around the Bend",location_group = "Bincho"),
    "KnightD Bincho - Upper Mines Before Digging": BFMLocationData("Upper Mines Before Digging",location_group = "Bincho"),
    "Alchemist Bincho - Frozen Palace Red Eye Maze": BFMLocationData("Frozen Palace Red Eye Maze",location_group = "Bincho"),
    "Librarian Bincho - Restaurant Basement Near Rotating Platforms": BFMLocationData("Restaurant Basement Near Rotating Platforms",location_group = "Bincho"),
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
    "Lumina - Spiral Tower": BFMLocationData("Spiral Tower",location_group = "Equipment"),
    "Item 1 - Bakery": BFMLocationData("Grillin Village",location_group = "Bakery"),
    "Item 2 - Bakery": BFMLocationData("Grillin Village",location_group = "Bakery"),
    "Item 3 - Bakery": BFMLocationData("Grillin Village",location_group = "Bakery"),
    "Item 4 - Bakery": BFMLocationData("Grillin Village",location_group = "Bakery"),
    "Item 5 - Bakery": BFMLocationData("Grillin Village",location_group = "Bakery"),
    "Item 6 - Bakery": BFMLocationData("Grillin Village",location_group = "Bakery"),
    "Item 7 - Bakery": BFMLocationData("Grillin Village",location_group = "Bakery"),
    "Item 1 - Restaurant": BFMLocationData("Grillin Village",location_group = "Restaurant"),
    "Item 2 - Restaurant": BFMLocationData("Grillin Village",location_group = "Restaurant"),
    "Item 3 - Restaurant": BFMLocationData("Grillin Village",location_group = "Restaurant"),
    "Item 4 - Restaurant": BFMLocationData("Grillin Village",location_group = "Restaurant"),
    "Item 5 - Restaurant": BFMLocationData("Grillin Village",location_group = "Restaurant"),
    "Item 6 - Restaurant": BFMLocationData("Grillin Village",location_group = "Restaurant"),
    "Item 7 - Restaurant": BFMLocationData("Grillin Village",location_group = "Restaurant"),
    "Item 1 - Grocery": BFMLocationData("Grillin Village",location_group = "Grocery"),
    "Item 2 - Grocery": BFMLocationData("Grillin Village",location_group = "Grocery"),
    "Item 3 - Grocery": BFMLocationData("Grillin Village",location_group = "Grocery"),
    "Item 4 - Grocery": BFMLocationData("Grillin Village",location_group = "Grocery"),
    "Item 5 - Grocery": BFMLocationData("Grillin Village",location_group = "Grocery"),
    "Item 6 - Grocery": BFMLocationData("Grillin Village",location_group = "Grocery"),
    "Item 7 - Grocery": BFMLocationData("Grillin Village",location_group = "Grocery"),
    "Item 8 - Grocery": BFMLocationData("Grillin Village",location_group = "Grocery"),
    "Item 9 - Grocery": BFMLocationData("Grillin Village",location_group = "Grocery"),
    "Item 10 - Grocery": BFMLocationData("Grillin Village",location_group = "Grocery"),
    "Item 11 - Grocery": BFMLocationData("Grillin Village",location_group = "Grocery"),
    "Item 12 - Grocery": BFMLocationData("Grillin Village",location_group = "Grocery"),
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


location_name_groups: Dict[str, Set[str]] = {}
for loc_name, loc_data in location_table.items():
    loc_group_name = loc_name.split(" - ", 1)[1]
    location_name_groups.setdefault(loc_group_name, set()).add(loc_name)
    if loc_data.location_group:
        location_name_groups.setdefault(loc_data.location_group, set()).add(loc_name)


table_ids_to_hint: List[int] = []
for loc_name, loc_id in standard_location_name_to_id.items():
    if(location_table[loc_name].location_group):
        if(not location_table[loc_name].location_group in ["Bakery", "Equipment", "Minku", "Restaurant", "Grocery"]):
            table_ids_to_hint.append(loc_id)
    else:
        table_ids_to_hint.append(loc_id)
