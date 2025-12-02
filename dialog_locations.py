from typing import Dict, NamedTuple, Set, Optional, List
from .locations import standard_location_name_to_id

#standard_location_name_to_id[]: 0x

dialog_location_table: Dict[int, Dict[int, List[int]]] = {
    0x3014: {standard_location_name_to_id["Guard Bincho - Somnolent Forest"]: [0x191b3c, 0x191b8c], 
    standard_location_name_to_id["Seer Bincho - Somnolent Forest"]: [0x191be0, 0x191bfc], 
    standard_location_name_to_id["Hawker Bincho - Somnolent Forest Deadend"]: [0x191cbc, 0x191c98], 
    standard_location_name_to_id["Maid Bincho - Somnolent Forest Behind Steam"]: [0x191abc, 0x191b24],
    standard_location_name_to_id["Old Crown Chest - Somnolent Forest"]: [0x1911c0, 0x19121c],
    standard_location_name_to_id["Glasses Chest - Somnolent Forest"]: [0x1913b0, 0x1913b4],
    standard_location_name_to_id["500 Drans Chest - Somnolent Forest Behind Steam"]: [0x1912a4, 0x1912cc]},
    0x301c: {standard_location_name_to_id["MusicianB Bincho - Steamwood Forest"]: [0x189880, 0x1899dc], 
    standard_location_name_to_id["Acrobat Bincho - Steamwood Forest"]: [0x18992c, 0x189a50],
    standard_location_name_to_id["Aged Coin Chest - Steamwood Forest"]: [0x189628, 0x1897fc]},
    0x3021: {standard_location_name_to_id["Artisan Bincho - Island of Dragons"]: [0x197d90, 0x197f10],
    standard_location_name_to_id["500 Drans Chest - Island of Dragons"]: [0x197c1c, 0x197dd0]},
    0x3025: {standard_location_name_to_id["SoldierA Bincho - Twinpeak Entrance"]: [0x18ede0, 0x18ef1c],
    standard_location_name_to_id["Bracelet Chest - Twinpeak Entrance"]: [0x18eb14, 0x18ece8]},
    0x3026: {standard_location_name_to_id["MercenC Bincho - Twinpeak Around the Bend"]: [0x196d9c, 0x196d30], 
    standard_location_name_to_id["Doctor Bincho - Twinpeak Around the Bend"]: [0x196e38, 0x196d84],
    standard_location_name_to_id["Old Book Chest - Twinpeak Around the Bend"]: [0x1967f8, 0x196884],
    standard_location_name_to_id["200 Drans Chest - Twinpeak Around the Bend"]: [0x1968d8, 0x196938]},
    0x3028: {standard_location_name_to_id["Shepherd Bincho - Twinpeak Rope Bridge"]: [0x18bcd8, 0x18be7c],
    standard_location_name_to_id["Dagger Chest - Twinpeak Rope Bridge"]: [0x18bbf8, 0x18bdcc]},
    0x3029: {standard_location_name_to_id["CarpentA Bincho - Twinpeak Second Peak"]: [0x192ee4, 0x192f00], 
    standard_location_name_to_id["KnightB Bincho - Twinpeak Second Peak"]: [0x192dfc, 0x192e50], 
    standard_location_name_to_id["Weaver Bincho - Twinpeak Second Peak"]: [0x192f80, 0x192f80],
    standard_location_name_to_id["Rock Chest - Twinpeak Second Peak"]: [0x192ad0, 0x192b84]},
    0x302b: {standard_location_name_to_id["Knitter Bincho - Twinpeak Path to Skullpion"]: [0x1868c4, 0x186a30],
    standard_location_name_to_id["200 Drans Chest - Twinpeak Path to Skullpion"]: [0x1866fc, 0x1868c0]},
    0x302d: {standard_location_name_to_id["Taster Bincho - Restaurant Basement Path to Crest Guardian"]: [0x187ad8, 0x187c84]},
    0x302e: {standard_location_name_to_id["Shield Chest - Restaurant Basement Bowling 1"]: [0x189cd8, 0x189eac]},
    0x302f: {standard_location_name_to_id["MercenA Bincho - Restaurant Basement Bowling 1"]: [0x18f58c, 0x18f760],
    standard_location_name_to_id["Odd Hat Chest - Restaurant Basement Bowling 1"]: [0x18f644, 0x18f7d8]},
    0x3030: {standard_location_name_to_id["MercenB Bincho - Restaurant Basement Bowling 2"]: [0x18f3bc, 0x18f58c]},
    0x3033: {standard_location_name_to_id["Baliff Bincho - Restaurant Basement Behind Pole Jumps"]: [0x190844, 0x190a18]},
    0x3034: {standard_location_name_to_id["Old Sword Chest - Restaurant Basement"]: [0x18a2b4, 0x18a14c],
    standard_location_name_to_id["300 Drans Chest - Restaurant Basement"]: [0x18a474, 0x18a2a4],
    standard_location_name_to_id["Cloth Chest - Restaurant Basement"]: [0x18a3a0, 0x18a1f8]},
    0x3035: {standard_location_name_to_id["CarpentB Bincho - Restaurant Basement Dark Platform Maze 2"]: [0x189d5c, 0x189f30]},
    0x3039: {standard_location_name_to_id["KnightC Bincho - Restaurant Basement Dark Platform Maze 3"]: [0x189ddc, 0x189f7c],
    standard_location_name_to_id["Helmet Chest - Restaurant Basement Dark Platform Maze 3"]: [0x189d00, 0x189ed0]},
    0x303a: {standard_location_name_to_id["Librarian Bincho - Restaurant Basement Near Rotating Platforms"]: [0x189060, 0x189234]},
    0x303d: {standard_location_name_to_id["SoldierB Bincho - Restaurant Basement Planks Over Lava"]: [0x18866c, 0x188840],
    standard_location_name_to_id["Old Pipe Chest - Restaurant Basement Planks Over Lava"]: [0x188724, 0x188898]},
    0x3041: {standard_location_name_to_id["Powder Chest - Restaurant Basement Teleport Maze"]: [0x18e92c, 0x18eafc]},
    0x3046: {standard_location_name_to_id["KnightA Bincho - Mine Conveyor Belt Room"]: [0x185b2c, 0x185d00], 
    standard_location_name_to_id["CarpentC Bincho - Mine Conveyor Belt Room"]: [0x185bd4, 0x185d78]},
    0x3047: {standard_location_name_to_id["CookA Bincho - Misteria Underground Lake"]: [0x188e5c, 0x188ffc], 
    standard_location_name_to_id["Chief Bincho - Misteria Underground Lake"]: [0x188ecc, 0x18905c],
    standard_location_name_to_id["Old Glove Chest - Misteria Underground Lake"]: [0x188d78, 0x188f4c]},
    0x304d: {standard_location_name_to_id["Armor Chest - Reservoir Tunnel"]: [0x188d9c, 0x188f84]},
    0x304e: {standard_location_name_to_id["Old Shirt Chest - Grillin Reservoir"]: [0x1949cc, 0x194b20],
    standard_location_name_to_id["Used Boot Chest - Grillin Reservoir"]: [0x194ac4, 0x194bf4]},
    0x305c: {standard_location_name_to_id["Butcher Bincho - Frozen Palace Atrium Right Balcony"]: [0x187964, 0x187ae0],
    standard_location_name_to_id["Red Shoes Chest - Frozen Palace Atrium Left Balcony"]: [0x18786c, 0x187a04]},
    0x305d: {standard_location_name_to_id["Janitor Bincho - Frozen Palace Blue Eye Door"]: [0x18c778, 0x18c8f8]},
    0x305e: {standard_location_name_to_id["Red Eye Chest - Frozen Palace Red Eye Room"]: [0x185df0, 0x185fc4]},
    0x305f: {standard_location_name_to_id["Chef Bincho - Frozen Palace Crate Pile"]: [0x18881c, 0x1889f0]},
    0x3060: {standard_location_name_to_id["MusicianC Bincho - Frozen Palace Green Eye Maze"]: [0x18bc74, 0x18bde0],
    standard_location_name_to_id["Green Eye Chest - Frozen Palace Green Eye Maze"]: [0x18ba54, 0x18bc28],
    standard_location_name_to_id["White Cloth Chest - Frozen Palace Green Eye Maze"]: [0x18bb94, 0x18bd30]},
    0x3061: {standard_location_name_to_id["Red Cloth Chest - Frozen Palace Green Eye Maze"]: [0x18382c, 0x183a00]},
    0x3062: {standard_location_name_to_id["Alchemist Bincho - Frozen Palace Red Eye Maze"]: [0x1899e8, 0x189bac],
    standard_location_name_to_id["Blue Eye Chest - Frozen Palace Red Eye Maze"]: [0x189984, 0x189b58]},
    0x3063: {standard_location_name_to_id["Long Tube Chest - Frozen Palace Red Eye Door"]: [0x188db4, 0x188f88]},
    0x3065: {standard_location_name_to_id["Black Cloth Chest - Frost Dragon Door"]: [0x1828b8, 0x182a8c]},
    0x306c: {standard_location_name_to_id["CookB Bincho - Upper Mines"]: [0x189cf0, 0x189dfc],
    standard_location_name_to_id["Large Tool Chest - Upper Mines"]: [0x189c10, 0x189d4c]},
    0x306d: {standard_location_name_to_id["Odd Bone Chest - Upper Mines"]: [0x184218, 0x1843f0]},
    0x3070: {standard_location_name_to_id["Conductor Bincho - Upper Mines Ant Parade"]: [0x186368, 0x186540]},
    0x3071: {standard_location_name_to_id["KnightD Bincho - Upper Mines Before Digging"]: [0x1831a8, 0x183380]}
}

short_text_boxes: List[int] = [
    standard_location_name_to_id["Bracelet Chest - Twinpeak Entrance"],
    standard_location_name_to_id["Glasses Chest - Somnolent Forest"],
    standard_location_name_to_id["Red Eye Chest - Frozen Palace Red Eye Room"],
    standard_location_name_to_id["Blue Eye Chest - Frozen Palace Red Eye Maze"],
    standard_location_name_to_id["Green Eye Chest - Frozen Palace Green Eye Maze"]
]

castle_dialog: List[List[int]] = [[
    0x18b9b4,  
    0x188ea4,
    0x188b30,
    0x189c9c,
    0x18aeb4,
    0x18c8a4,
    0x18cd90
], [
    0x18ab10,
    0x188788,
    0x188504,
    0x189300,
    0x18a1e8,
    0x18b7f4,
    0x18bc54
]]

scroll_dialog: Dict[int, Dict[int, List[int]]] = {
    0x3026: {standard_location_name_to_id["Earth Scroll - Twinpeak First Peak"]: [0x196960, 0x1969a8]},
    0x304e: {standard_location_name_to_id["Water Scroll - Grillin Reservoir"]: [0x19490c, 0x194a84]},
    0x3021: {standard_location_name_to_id["Fire Scroll - Island of Dragons"]: [0x197c68, 0x197e10]},
    0x3023: {standard_location_name_to_id["Wind Scroll - Grillin Volcano"]: [0x191d0c, 0x191ee4]},
    0x3081: {standard_location_name_to_id["Sky Scroll - Sky Island"]: [0x191f44, 0x192124]}
}

boss_core_dialog: Dict[int, Dict[int, List[List[int]]]] = {
    0x3024: {standard_location_name_to_id["Defeat Earth Crest Guardian - Skullpion Arena"]: [[0x191624, 78], [0x1916fc, 64]]},
    0x3042: {standard_location_name_to_id["Defeat Water Crest Guardian - Relic Keeper Arena"]: [[0x18f578, 85], [0x18f750, 63]]},
    0x3067: {standard_location_name_to_id["Defeat Fire Crest Guardian - Frost Dragon Arena"]: [[0x194ecc, 80], [0x1950a4, 64]]},
    0x3075: {standard_location_name_to_id["Defeat Wind Crest Guardian - Queen Ant Arena"]: [[0x194484, 77], [0x194620, 58]]}
}
boss_locations: List[int] = [
    0x3024,
    0x3042,
    0x3067,
    0x3075
]
boss_core_update: Dict[int, List[List[int]]] = {
    0x3024: [[0x173fb8, 0x18679c], [0x18699c]],
    0x3042: [[0x173ffc], [0x174268]],
    0x3067: [[0x174040], [0x1742ac]],
    0x3075: [[0x174084], [0x1742f0]]
}