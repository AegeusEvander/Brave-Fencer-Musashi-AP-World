from typing import Dict, NamedTuple, Set, Optional, List
from .locations import standard_location_name_to_id

#standard_location_name_to_id[]: 0x

dialog_location_table: Dict[int, Dict[int, int]] = {
    0x3014: {standard_location_name_to_id["Guard Bincho - Somnolent Forest"]: 0x191b3c, standard_location_name_to_id["Seer Bincho - Somnolent Forest"]: 0x191be0, standard_location_name_to_id["Hawker Bincho - Somnolent Forest Deadend"]: 0x191cbc, standard_location_name_to_id["Maid Bincho - Somnolent Forest Behind Steam"]: 0x191abc},
    0x301c: {standard_location_name_to_id["MusicianB Bincho - Steamwood Forest"]: 0x189880, standard_location_name_to_id["Acrobat Bincho - Steamwood Forest"]: 0x18992c},
    0x3021: {standard_location_name_to_id["Artisan Bincho - Island of Dragons"]: 0x197d90},
    0x3025: {standard_location_name_to_id["SoldierA Bincho - Twinpeak Entrance"]: 0x18ede0},
    0x3026: {standard_location_name_to_id["MercenC Bincho - Twinpeak Around the Bend"]: 0x196d9c, standard_location_name_to_id["Doctor Bincho - Twinpeak Around the Bend"]: 0x196e38},
    0x3028: {standard_location_name_to_id["Shepherd Bincho - Twinpeak Rope Bridge"]: 0x18bcd8},
    0x3029: {standard_location_name_to_id["CarpentA Bincho - Twinpeak Second Peak"]: 0x192ee4, standard_location_name_to_id["KnightB Bincho - Twinpeak Second Peak"]: 0x192dfc, standard_location_name_to_id["Weaver Bincho - Twinpeak Second Peak"]: 0x192f80},
    0x3030: {standard_location_name_to_id["MercenB Bincho - Restaurant Basement Bowling 2"]: 0x18f3bc},
    0x302b: {standard_location_name_to_id["Knitter Bincho - Twinpeak Path to Skullpion"]: 0x1868c4},
    0x302d: {standard_location_name_to_id["Taster Bincho - Restaurant Basement Path to Crest Guardian"]: 0x187ad8},
    0x302f: {standard_location_name_to_id["MercenA Bincho - Restaurant Basement Bowling 1"]: 0x18f58c},
    0x3033: {standard_location_name_to_id["Baliff Bincho - Restaurant Basement Behind Pole Jumps"]: 0x190844},
    0x3035: {standard_location_name_to_id["CarpentB Bincho - Restaurant Basement Dark Platform Maze 2"]: 0x189d5c},
    0x3039: {standard_location_name_to_id["KnightC Bincho - Restaurant Basement Dark Platform Maze 3"]: 0x189ddc},
    0x303a: {standard_location_name_to_id["Librarian Bincho - Restaurant Basement Near Rotating Platforms"]: 0x189060},
    0x303d: {standard_location_name_to_id["SoldierB Bincho - Restaurant Basement Planks Over Lava"]: 0x18866c},
    0x3046: {standard_location_name_to_id["KnightA Bincho - Mine Conveyor Belt Room"]: 0x185b2c, standard_location_name_to_id["CarpentC Bincho - Mine Conveyor Belt Room"]: 0x185bd4},
    0x3047: {standard_location_name_to_id["CookA Bincho - Misteria Underground Lake"]: 0x188e5c, standard_location_name_to_id["Chief Bincho - Misteria Underground Lake"]: 0x188ecc},
    0x305c: {standard_location_name_to_id["Butcher Bincho - Frozen Palace Atrium Right Balcony"]: 0x187964},
    0x305d: {standard_location_name_to_id["Janitor Bincho - Frozen Palace Blue Eye Door"]: 0x18c778},
    0x305f: {standard_location_name_to_id["Chef Bincho - Frozen Palace Crate Pile"]: 0x18881c},
    0x3060: {standard_location_name_to_id["MusicianC Bincho - Frozen Palace Green Eye Maze"]: 0x18bc74},
    0x3062: {standard_location_name_to_id["Alchemist Bincho - Frozen Palace Red Eye Maze"]: 0x1899e8},
    0x306c: {standard_location_name_to_id["CookB Bincho - Upper Mines"]: 0x189cf0},
    0x3070: {standard_location_name_to_id["Conductor Bincho - Upper Mines Ant Parade"]: 0x186368},
    0x3071: {standard_location_name_to_id["KnightD Bincho - Upper Mines Before Digging"]: 0x1831a8}
}