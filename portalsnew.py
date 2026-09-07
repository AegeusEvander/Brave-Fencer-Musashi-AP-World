from typing import Dict, NamedTuple, Set, Optional, List

class BFMConnection(NamedTuple):
    memory: int
    destination: int
    door: int
    short_name: str
    door_name: str
    other: Optional[int] = 0
    connection_group: Optional[str] = ""
    can_be_disconnected: Optional[bool] = True

class BFMConnectionData(NamedTuple):
	region: str
	jp_offset: int
	connections: tuple[BFMConnection]
	is_cutscene: Optional[bool] = False

bfm_portals: dict[int, BFMConnectionData] = {
	0x3000: BFMConnectionData("Castle Outside", 0x1d4, (
			BFMConnection(0x182db4, 0x3069, 0x0, "00", ""),
			BFMConnection(0x182d24, 0x1010, 0x3, "000", ""),
			BFMConnection(0x182d48, 0x1052, 0x3, "000", ""),
			BFMConnection(0x182d6c, 0x1077, 0x3, "000", ""),
			BFMConnection(0x182d90, 0x1094, 0x3, "000", ""),
			BFMConnection(0x182cbc, 0x3004, 0x1, "000", ""),
			BFMConnection(0x182c74, 0x3004, 0x0, "000", ""),
			BFMConnection(0x182c50, 0x3003, 0x0, "004", ""),
			BFMConnection(0x182c08, 0x3001, 0x1, "004", ""),
			BFMConnection(0x182c2c, 0x3002, 0x1, "004", ""),
		)),
	0x3001: BFMConnectionData("Castle Bedroom", 0x1d4, (
			#BFMConnection(0x185e5c, 0x3002, 0x0, "01", ""),
			BFMConnection(0x185e38, 0x3000, 0x4, "011", "Bedroom Door"),
		)),
	0x3002: BFMConnectionData("Castle Library", 0x1d4, (
			BFMConnection(0x18317c, 0x3000, 0x4, "021", "Library Door"),
		)),
	0x3003: BFMConnectionData("Castle Meeting Room", 0x1d4, (
			BFMConnection(0x186364, 0x3000, 0x4, "030", ""),
		)),
	0x3004: BFMConnectionData("Castle Gondola", 0x1d4, (
			BFMConnection(0x18202c, 0x1011, 0x5, "043", "Zipline", can_be_disconnected = False),
			#BFMConnection(0x182050, 0x3000, 0x0, "041", ""),
			BFMConnection(0x182008, 0x1095, 0x5, "043", "Bottom of Gondola"),
			#BFMConnection(0x182074, 0x1095, 0x6, "043", ""),
		)),
	0x3005: BFMConnectionData("Cutscene MOON", 0x1f0, (
			BFMConnection(0x182618, 0x3006, 0x0, "051", "End Moon Cutscene"),
			BFMConnection(0x18263c, 0x3008, 0x0, "052", "Skip Moon Cutscene"),
		), is_cutscene = True),
	0x3006: BFMConnectionData("Cutscene Summon Crystal", 0x30c, (
			BFMConnection(0x187268, 0x3008, 0x0, "061", "End Summon Crystal Cutscene"),
		), is_cutscene = True),
	0x3008: BFMConnectionData("Starting Forest", 0x1d4, (
			BFMConnection(0x18a55c, 0x3009, 0x0, "081", "Behind Statue"),
		)),
	0x3009: BFMConnectionData("Spiral Tower Outside", 0x1d4, (
			BFMConnection(0x18948c, 0x300a, 0x0, "091", "Spiral Tower Outside Door"),
		)),
	0x300a: BFMConnectionData("Spiral Tower Inside", 0x1d4, (
			BFMConnection(0x18a2cc, 0x300b, 0x0, "0a1", "Top of Ramp Teleport"),
		)),
	0x300b: BFMConnectionData("Spiral Tower Roof", 0x1dc, (
			BFMConnection(0x18ea48, 0x300d, 0x0, "0b1", "End of Chase"),
		)),
	0x300d: BFMConnectionData("Cutscene Castle Outside Steam Knight", 0x1d4, (
			BFMConnection(0x1816ec, 0x300e, 0x0, "0d1", "Through Wall"),
		), is_cutscene = True),
	0x300e: BFMConnectionData("Castle Steam Knight Fight", 0x1d0, (
			BFMConnection(0x194370, 0x3001, 0x0, "0e1", "Wrecking Ball Throw"),
		)),
	0x1010: BFMConnectionData("Chapter 2 Grillin Village", 0x22c, (
			#"100" Conners again
			BFMConnection(0x19113c, 0x1011, 0x1, "101", "Village Ramp", other=0x2),
			BFMConnection(0x191160, 0x301c, 0x1, "102", "Village Path by Windmill", other=0x2),
			BFMConnection(0x191184, 0x3000, 0x0, "103", "Village Through Portcullis", other=0x4),
			BFMConnection(0x1911a8, 0x2015, 0x0, "104", "Village Bakery", other=0x2),
			BFMConnection(0x1911cc, 0x3014, 0x1, "105", "Village to Somnolent Forest", other=0x2),
			BFMConnection(0x1911f0, 0x3014, 0x0, "106", "Village to Deadend Somnolent Forest", other=0x2),
			BFMConnection(0x191214, 0x201a, 0x0, "107", "Village Restaurant", other=0x2),
			BFMConnection(0x191238, 0x2016, 0x0, "108", "Village Grocery", other=0x2),
			BFMConnection(0x19125c, 0x2013, 0x0, "109", "Village Toy Shop", other=0x2),
			BFMConnection(0x191280, 0x2017, 0x0, "10a", "Village Inn", other=0x6),
			BFMConnection(0x1912a4, 0x2018, 0x0, "10b", "Village Conner", other=0x2),
			BFMConnection(0x1912c8, 0x2019, 0x0, "10c", "Village Church Door", other=0x6),
			#"10d" is Windmill door
			#"10e" is Well
			BFMConnection(0x191334, 0x3043, 0x0, "10f", "Village Lower Mine Door", other=0x2),
		)),
	0x1011: BFMConnectionData("Chapter 2 Upper Village", 0x1f4, (
			BFMConnection(0x189694, 0x1010, 0x1, "111", "Upper Village Ramp", other=0x2),
			BFMConnection(0x1896b8, 0x3025, 0x0, "112", "Upper Village Mountain Pass", other=0x2),
			BFMConnection(0x1896dc, 0x301e, 0x2, "113", "Upper Village Steam Pipe", other=0x2),
		)),
	0x3012: BFMConnectionData("Chapter 2 Nightmare", 0x1d4, (
			BFMConnection(0x182d08, 0x1010, 0xa, "121", "Bed", connection_group = "Ignore"),
		)),
	0x2013: BFMConnectionData("Chapter 2 Toy Shop", -0x248, (
			BFMConnection(0x1efeec, 0x1010, 0x9, "130", "Toy Store Door"),
		)),
	0x3014: BFMConnectionData("Somnolent Forest", 0x5c, (
			BFMConnection(0x1905cc, 0x1010, 0x6, "140", "Somnolent Forest Deadend Exit"),
			BFMConnection(0x1906e0, 0x1052, 0x6, "140", "Somnolent Forest Deadend Exit", connection_group = "Ignore"),
			BFMConnection(0x190728, 0x1077, 0x6, "140", "Somnolent Forest Deadend Exit", connection_group = "Ignore"),
			BFMConnection(0x190770, 0x1094, 0x6, "140", "Somnolent Forest Deadend Exit", connection_group = "Ignore"),
			BFMConnection(0x1905f0, 0x1010, 0x5, "141", "Somnolent Forest Town Exit"),
			BFMConnection(0x190704, 0x1052, 0x5, "141", "Somnolent Forest Town Exit", connection_group = "Ignore"),
			BFMConnection(0x19074c, 0x1077, 0x5, "141", "Somnolent Forest Town Exit", connection_group = "Ignore"),
			BFMConnection(0x190794, 0x1094, 0x5, "141", "Somnolent Forest Town Exit", connection_group = "Ignore"),
			BFMConnection(0x190614, 0x301b, 0x0, "142", "Somnolent Forest to Meandering"),
			BFMConnection(0x1906a4, 0x301b, 0x21, "142", "Somnolent Forest to Meandering", connection_group = "Ignore"),
			BFMConnection(0x190638, 0x301c, 0x0, "143", "Somnolent Forest Large Pipe"),
			BFMConnection(0x19065c, 0x3021, 0x0, "144", "Somnolent Forest to Island of Dragons"),
		)),
	0x2015: BFMConnectionData("Chapter 2 Bakery", -0x264, (
			BFMConnection(0x1eff94, 0x1010, 0x4, "150", "Bakery Door"),
		)),
	0x2016: BFMConnectionData("Chapter 2 Grocery", -0x248, (
			BFMConnection(0x1f045c, 0x1010, 0x8, "160", "Grocery Door"),
		)),
	0x2017: BFMConnectionData("Chapter 2 Inn", -0xc4, (
			BFMConnection(0x1f34dc, 0x1010, 0xa, "170", "Inn Door"),
		)),
	0x2018: BFMConnectionData("Chapter 2 Conner", -0x248, (
			BFMConnection(0x1f00e8, 0x1010, 0xb, "180", "Conner Door"),
		)),
	0x2019: BFMConnectionData("Chapter 2 Church", -0x248, (
			BFMConnection(0x1efe3c, 0x1010, 0xc, "190", "Church Door"),
		)),
	0x201a: BFMConnectionData("Chapter 2 Restaurant", -0x248, (
			BFMConnection(0x1eff60, 0x1010, 0x7, "1a0", "Restaurant Door"),
		)),
	0x301b: BFMConnectionData("Meandering Forest", 0x118, (
			BFMConnection(0x18b5a4, 0x3014, 0x2, "1b0", "Meandering South", can_be_disconnected = False),
			BFMConnection(0x18b5c8, 0x3022, 0x0, "1b1", "Meandering to Graveyard", other=0x4, can_be_disconnected = False),
			BFMConnection(0x18b514, 0x3068, 0x0, "1b2", "Meandering to Frozen Palace", other=0x4, can_be_disconnected = False),
		)),
	0x301c: BFMConnectionData("Steamwood Forest", 0x1d4, (
			BFMConnection(0x188c60, 0x3014, 0x3, "1c0", "Steamwood Forest Pipe"),
			BFMConnection(0x188c84, 0x1010, 0x2, "1c1", "Steamwood Forest to Village"),
			BFMConnection(0x188d00, 0x1052, 0x2, "1c1", "Steamwood Forest to Village", connection_group = "Ignore"),
			BFMConnection(0x188d24, 0x1077, 0x2, "1c1", "Steamwood Forest to Village", connection_group = "Ignore"),
			BFMConnection(0x188d48, 0x1094, 0x2, "1c1", "Steamwood Forest to Village", connection_group = "Ignore"),
			BFMConnection(0x188ca8, 0x301e, 0x0, "1c2", "Steamwood Forest top of Cliff"),
			BFMConnection(0x188ccc, 0x3081, 0x0, "1c3", "Steamwood Forest Wind Crest"),
		)),
	0x301d: BFMConnectionData("Steamwood 1", 0x1c8, (
			BFMConnection(0x183a5c, 0x301f, 0x0, "1d1", "Steamwood 1 Success", can_be_disconnected = False),
		)),
	0x301e: BFMConnectionData("Steamwood Outside", 0x1c8, (
			BFMConnection(0x184da8, 0x301c, 0x2, "1e0", "Outside Steamwood South"),
			BFMConnection(0x184dcc, 0x301d, 0x0, "1e1", "Outside Steamwood Enter Steamwood", connection_group = "Ignore"),
			BFMConnection(0x184e8c, 0x3020, 0x0, "1e1", "Outside Steamwood Enter Steamwood", connection_group = "Ignore"),
			BFMConnection(0x184df0, 0x1011, 0x3, "1e2", "Outside Steamwood Pipe"),
			BFMConnection(0x184e20, 0x1053, 0x3, "1e2", "Outside Steamwood Pipe", connection_group = "Ignore"),
			BFMConnection(0x184e44, 0x1078, 0x3, "1e2", "Outside Steamwood Pipe", connection_group = "Ignore"),
			BFMConnection(0x184e68, 0x1095, 0x3, "1e2", "Outside Steamwood Pipe", connection_group = "Ignore"),
		)),
	0x301f: BFMConnectionData("Cutscene Steamwood Success", 0x1d4, (
			BFMConnection(0x181b58, 0x301e, 0x1, "1f1", "Steamwood Cutscene", can_be_disconnected = False),
		), is_cutscene = True),
	0x3020: BFMConnectionData("Steamwood 2", 0x1c8, (
			BFMConnection(0x184a94, 0x301f, 0x0, "201", "Steamwood 2 Success"),
		)),
	0x3021: BFMConnectionData("Island of Dragons", 0x1d8, (
			BFMConnection(0x18f7d8, 0x3003, 0x0, "211", "Rescue Princess", connection_group = "Ignore", can_be_disconnected = False),
			BFMConnection(0x18f7b4, 0x3014, 0x4, "210", "Island of Dragons Exit"),
		)),
	0x3022: BFMConnectionData("Graveyard", 0x1d4, (
			BFMConnection(0x1828d4, 0x3014, 0x2, "221", "Graveyard Exit"),
		)),
	0x3023: BFMConnectionData("Grillin Volcano", 0x1d4, (
			BFMConnection(0x18aefc, 0x304d, 0x1, "230", "Volcano Caldera"),
			BFMConnection(0x18af20, 0x3014, 0x2, "231", "Exit Meandering Forest"),
		)),
	0x3024: BFMConnectionData("Skullpion Arena", 0x1d8, (
			BFMConnection(0x18f7c8, 0x302b, 0x1, "240", "Skullpion Arena Entrance"),
			BFMConnection(0x18f7ec, 0x30a6, 0x1, "241", "Defeat Skullpion"),
		)),
	0x3025: BFMConnectionData("Twinpeak Entrance", 0x1d4, (
			BFMConnection(0x18b3bc, 0x1011, 0x2, "250", "Twinpeak Entrance South Path", connection_group = "Ignore"),
			BFMConnection(0x18b4fc, 0x1053, 0x2, "250", "Twinpeak Entrance South Path", connection_group = "Ignore"),
			BFMConnection(0x18b520, 0x1078, 0x2, "250", "Twinpeak Entrance South Path", connection_group = "Ignore"),
			BFMConnection(0x18b544, 0x1095, 0x2, "250", "Twinpeak Entrance South Path", connection_group = "Ignore"),
			BFMConnection(0x18b3e0, 0x302b, 0x0, "251", "Twinpeak Entrance East Path", connection_group = "Ignore"),
			BFMConnection(0x18b428, 0x3026, 0x1, "253", "Twinpeak Entrance West Path", connection_group = "Ignore"),
			BFMConnection(0x18b4b8, 0x3029, 0x2, "257", "Twinpeak Entrance Dock", connection_group = "Ignore"),
		)),
	0x3026: BFMConnectionData("Twinpeak Around the Bend", 0x184, (
			BFMConnection(0x194f28, 0x3025, 0x3, "261", "Twinpeak Around the Bend Along River"),
			BFMConnection(0x194f70, 0x3027, 0x0, "263", "Twinpeak Around the Bend Cave Entrance"),
		)),
	0x3027: BFMConnectionData("Twinpeak Cave 1", 0x1d4, (
			BFMConnection(0x181c58, 0x3026, 0x3, "270", "Twinpeak Cave 1 East Entrance"),
			BFMConnection(0x181c7c, 0x3028, 0x0, "271", "Twinpeak Cave 1 South Entrance"),
		)),
	0x3028: BFMConnectionData("Twinpeak Rope Bridge", 0x1d4, (
			BFMConnection(0x188028, 0x3027, 0x1, "280", "Twinpeak Rope Bridge West"),
			BFMConnection(0x18804c, 0x302c, 0x0, "281", "Twinpeak Rope Bridge East"),
		)),
	0x3029: BFMConnectionData("Twinpeak Second Peak", 0xe8, (
			BFMConnection(0x18e094, 0x302c, 0x1, "290", "Twinpeak Second Peak Cave Entrance"),
			BFMConnection(0x18e0b8, 0x302a, 0x0, "291", "Twinpeak Second Peak Raft"),
			BFMConnection(0x18e0dc, 0x3025, 0x7, "292", "Twinpeak Second Peak Dock"),
		)),
	0x302a: BFMConnectionData("Twinpeak Rafting", 0x1d4, (
			BFMConnection(0x185884, 0x3026, 0x2, "2a1", "Rafting Shortcut"),
			#BFMConnection(0x78e50, 0x302a, 0x0, "2a", ""),
			BFMConnection(0x1858a8, 0x3025, 0x2, "2a2", "Rafting End"),
		)),
	0x302b: BFMConnectionData("Twinpeak Path to Skullpion", 0x1c4, (
			BFMConnection(0x185f00, 0x3025, 0x1, "2b0", "Path to Skullpion South"),
			BFMConnection(0x185f24, 0x3024, 0x0, "2b1", "Path to Skullpion North"),
		)),
	0x302c: BFMConnectionData("Twinpeak Waterfall Cave 2", 0x1b8, (
			BFMConnection(0x1834dc, 0x3028, 0x1, "2c0", "Waterfall Cave West"),
			BFMConnection(0x183500, 0x3029, 0x0, "2c1", "Waterfall Cave South"),
		)),
	0x302d: BFMConnectionData("Restaurant Basement Relic Keeper Gauntlet", 0x1d4, (
			BFMConnection(0x187790, 0x3040, 0x3, "2d0", "Basement Gauntlet South"),
			BFMConnection(0x1877b4, 0x304c, 0x0, "2d1", "Basement Gauntlet North"),
		)),
	0x302e: BFMConnectionData("Restaurant Basement Bowling Entrance", 0x1d4, (
			BFMConnection(0x189b1c, 0x3034, 0x1, "2e0", "Bowling Entrance South Door"),
			BFMConnection(0x189b40, 0x302e, 0x3, "2e1", "Bowling Entrance Broken Wall Behind Plant"),
			BFMConnection(0x189b64, 0x302f, 0x0, "2e2", "Bowling Entrance Upper Door"),
			BFMConnection(0x189b88, 0x302e, 0x1, "2e3", "Bowling Entrance Hidden Room South"),
		)),
	0x302f: BFMConnectionData("Restaurant Basement Bowling 1", 0x1d4, (
			BFMConnection(0x18edc4, 0x302e, 0x2, "2f0", "Bowling Arrow Trap East"),
			BFMConnection(0x18ede8, 0x302f, 0x2, "2f1", "Bowling Arrow Trap North"),
			BFMConnection(0x18ee0c, 0x302f, 0x1, "2f2", "Bowling 1 Plant Room South"),
			BFMConnection(0x18ee30, 0x302f, 0x4, "2f3", "Bowling 1 Plant Room East"),
			BFMConnection(0x18ee54, 0x302f, 0x3, "2f4", "Bowling 1 West"),
			BFMConnection(0x18ee78, 0x302f, 0x7, "2f5", "Bowling 1 North"),
			BFMConnection(0x18ee9c, 0x302f, 0xc, "2f6", "Bowling 1 Elevator"),
			BFMConnection(0x18eec0, 0x302f, 0x5, "2f7", "Bowling 1 MercenA Room South"),
			BFMConnection(0x18eee4, 0x302f, 0xa, "2f8", "Bowling 1 MercenA Room East"),
			BFMConnection(0x18ef08, 0x302f, 0xb, "2f9", "Bowling 1 MercenA Room Upper")
			BFMConnection(0x18ef2c, 0x302f, 0x8, "2fa", "Bowling 1 Odd Hat Room West"),
			BFMConnection(0x18ef50, 0x302f, 0x9, "2fb", "Fire Totem Room West"),,
			BFMConnection(0x18ef98, 0x302f, 0xe, "2fd", "Fire Totem Room East"),
			BFMConnection(0x18efbc, 0x302f, 0xd, "2fe", "Wall Crush Trap Room North"),
			BFMConnection(0x18efe0, 0x3030, 0x0, "2ff", "Wall Crush Trap Room East"),
		)),
	0x3030: BFMConnectionData("Restaurant Basement Bowling 2", 0x1d4, (
			BFMConnection(0x18efec, 0x3030, 0x2, "301", "Bowling 2 Piston Trap North"),
			BFMConnection(0x18f010, 0x3030, 0x1, "302", "Bowling 2 Plant Room South"),
			BFMConnection(0x18f034, 0x3030, 0x4, "303", "Bowling 2 Plant Room West"),
			BFMConnection(0x18f058, 0x3030, 0x3, "304", "Bowling 1 East"),
			BFMConnection(0x18f07c, 0x3030, 0x7, "305", "Bowling 1 North"),
			BFMConnection(0x18f0a0, 0x3030, 0x8, "306", "Bowling 2 Elevator"),
			BFMConnection(0x18f0c4, 0x3030, 0x5, "307", "Bowling 2 MercenB Room South"),
			BFMConnection(0x18f10c, 0x3030, 0xa, "309", "Bowling 2 Top of Elevator North"),
			BFMConnection(0x18f130, 0x3030, 0x9, "30a", "Bowling End South"),
			BFMConnection(0x18f154, 0x3034, 0x6, "30b", "Bowling Teleport Back"),
		)),
	0x3031: BFMConnectionData("Restaurant Basement Teleport Maze Entrance", 0x1d4, (
			BFMConnection(0x18d0ac, 0x3034, 0x2, "310", "Teleport Maze Start Room South"),
			BFMConnection(0x18d0d0, 0x3031, 0x2, "311", "Teleport Maze Start Room North"),
			BFMConnection(0x18d0f4, 0x3031, 0x1, "312", "Teleport Maze Sliding Platform Room South"),
			BFMConnection(0x18d118, 0x3031, 0x7, "313", "Teleport Maze Sliding Platform Room Lower North"),
			BFMConnection(0x18d1a8, 0x3031, 0x3, "317", "Teleport Maze Single Return Teleport South"),
			BFMConnection(0x18d280, 0x3031, 0xa, "31", ""),
			BFMConnection(0x18d13c, 0x3031, 0x8, "31", ""),
			BFMConnection(0x18d1cc, 0x3031, 0x4, "31", ""),
			BFMConnection(0x18d160, 0x3032, 0x0, "315", ""),
			BFMConnection(0x18d184, 0x3033, 0x0, "316", ""),
			BFMConnection(0x18d1f0, 0x303f, 0x0, "319", ""),
		)),
	0x3032: BFMConnectionData("Restaurant Basement Teleport Maze", 0x1d4, (
			BFMConnection(0x18f4f4, 0x3032, 0x3, "32", ""),
			BFMConnection(0x18f53c, 0x3032, 0x1, "32", ""),
			BFMConnection(0x18f560, 0x3032, 0x5, "32", ""),
			BFMConnection(0x18f584, 0x3032, 0x4, "32", ""),
			BFMConnection(0x18f518, 0x3032, 0x6, "32", ""),
			BFMConnection(0x18f5a8, 0x3032, 0x2, "32", ""),
			BFMConnection(0x18f5cc, 0x3032, 0x8, "32", ""),
			BFMConnection(0x18f5f0, 0x3032, 0x7, "32", ""),
			BFMConnection(0x18f4d0, 0x3031, 0x5, "320", ""),
			BFMConnection(0x18f638, 0x3031, 0xa, "320", ""),
			BFMConnection(0x18f680, 0x3031, 0xb, "320", ""),
			BFMConnection(0x18f6a4, 0x3031, 0xc, "320", ""),
			BFMConnection(0x18f65c, 0x3033, 0x9, "329", ""),
		)),
	0x3033: BFMConnectionData("Restaurant Basement Teleport Maze Side Area", 0x1d4, (
			BFMConnection(0x1904d8, 0x3033, 0x3, "33", ""),
			BFMConnection(0x190520, 0x3033, 0x1, "33", ""),
			BFMConnection(0x190544, 0x3033, 0x5, "33", ""),
			BFMConnection(0x190568, 0x3033, 0x4, "33", ""),
			BFMConnection(0x1904fc, 0x3033, 0x6, "33", ""),
			BFMConnection(0x19058c, 0x3033, 0x2, "33", ""),
			BFMConnection(0x1905b0, 0x3033, 0x8, "33", ""),
			BFMConnection(0x1904b4, 0x3031, 0x6, "330", ""),
			BFMConnection(0x19061c, 0x3031, 0xb, "330", ""),
			BFMConnection(0x190640, 0x3032, 0x9, "339", ""),
		)),
	0x3034: BFMConnectionData("Restaurant Basement Entrance", 0x1d4, (
			BFMConnection(0x188794, 0x1010, 0x7, "34", ""),
			BFMConnection(0x188890, 0x1052, 0x7, "34", ""),
			BFMConnection(0x1888b4, 0x1077, 0x7, "34", ""),
			BFMConnection(0x1888d8, 0x1094, 0x7, "34", ""),
			BFMConnection(0x1887b8, 0x302e, 0x0, "341", ""),
			BFMConnection(0x1887dc, 0x3031, 0x0, "342", ""),
			BFMConnection(0x188800, 0x3035, 0x0, "343", ""),
			BFMConnection(0x188824, 0x303a, 0x0, "344", ""),
			BFMConnection(0x188848, 0x3040, 0x0, "345", ""),
		)),
	0x3035: BFMConnectionData("Restaurant Basement Dark Maze Entrance", 0x1d4, (
			BFMConnection(0x189a80, 0x3035, 0x2, "35", ""),
			BFMConnection(0x189aa4, 0x3035, 0x1, "35", ""),
			BFMConnection(0x189b10, 0x3035, 0x6, "35", ""),
			BFMConnection(0x189b34, 0x3035, 0x5, "35", ""),
			BFMConnection(0x189a5c, 0x3034, 0x3, "350", ""),
			BFMConnection(0x189ac8, 0x3036, 0x0, "353", ""),
			BFMConnection(0x189aec, 0x3037, 0x3, "354", ""),
			BFMConnection(0x189b58, 0x3038, 0x0, "357", ""),
		)),
	0x3036: BFMConnectionData("Restaurant Basement Dark Maze Sliding Block Puzzle", 0x1d4, (
			BFMConnection(0x18b2e4, 0x3036, 0x4, "36", ""),
			BFMConnection(0x18b350, 0x3036, 0x1, "36", ""),
			BFMConnection(0x18b374, 0x3036, 0x6, "36", ""),
			BFMConnection(0x18b398, 0x3036, 0x5, "36", ""),
			BFMConnection(0x18b3bc, 0x3036, 0x8, "36", ""),
			BFMConnection(0x18b3e0, 0x3036, 0x7, "36", ""),
			BFMConnection(0x18b404, 0x3036, 0x2, "36", ""),
			BFMConnection(0x18b308, 0x3036, 0x9, "36", ""),
			BFMConnection(0x18b2c0, 0x3035, 0x3, "360", ""),
			BFMConnection(0x18b32c, 0x3037, 0x0, "363", ""),
		)),
	0x3037: BFMConnectionData("Restaurant Basement Dark Maze", 0x1d4, (
			BFMConnection(0x184944, 0x3037, 0x2, "37", ""),
			BFMConnection(0x184968, 0x3037, 0x1, "37", ""),
			BFMConnection(0x184920, 0x3036, 0x3, "370", ""),
			BFMConnection(0x18498c, 0x3035, 0x4, "373", ""),
		)),
	0x3038: BFMConnectionData("Restaurant Basement Dark Maze Vertical Maze", 0x1d4, (
			BFMConnection(0x1844a0, 0x3035, 0x7, "380", ""),
			BFMConnection(0x1844c4, 0x3039, 0x0, "381", ""),
		)),
	0x3039: BFMConnectionData("Restaurant Basement Dark Maze End", 0x1d4, (
			BFMConnection(0x189a60, 0x3039, 0x4, "39", ""),
			BFMConnection(0x189aa8, 0x3039, 0x2, "39", ""),
			BFMConnection(0x189af0, 0x3039, 0x5, "39", ""),
			BFMConnection(0x189a3c, 0x3039, 0x3, "39", ""),
			BFMConnection(0x189a84, 0x3039, 0x1, "39", ""),
			BFMConnection(0x189acc, 0x3034, 0x6, "39", ""),
			BFMConnection(0x189a18, 0x3038, 0x1, "390", ""),
		)),
	0x303a: BFMConnectionData("Restaurant Basement Rotating Platforms Entrance", 0x1d4, (
			BFMConnection(0x188ec8, 0x303a, 0x2, "3a", ""),
			BFMConnection(0x188eec, 0x303a, 0x1, "3a", ""),
			BFMConnection(0x188ea4, 0x3034, 0x4, "3a0", ""),
			BFMConnection(0x188f10, 0x303b, 0x0, "3a3", ""),
		)),
	0x303b: BFMConnectionData("Restaurant Basement Rotating Platforms Long Platforms", 0x1d4, (
			BFMConnection(0x187ebc, 0x303a, 0x3, "3b0", ""),
			BFMConnection(0x187ee0, 0x303c, 0x0, "3b1", ""),
		)),
	0x303c: BFMConnectionData("Restaurant Basement Rotating Platforms First Lava Area", 0x1d4, (
			BFMConnection(0x186e30, 0x303c, 0x2, "3c", ""),
			BFMConnection(0x186e54, 0x303c, 0x1, "3c", ""),
			BFMConnection(0x186e0c, 0x303b, 0x1, "3c0", ""),
			BFMConnection(0x186e78, 0x303d, 0x0, "3c3", ""),
		)),
	0x303d: BFMConnectionData("Restaurant Basement Rotating Platforms Lava and Pendulums", 0x1d4, (
			BFMConnection(0x188494, 0x303d, 0x2, "3d", ""),
			BFMConnection(0x1884b8, 0x303d, 0x1, "3d", ""),
			BFMConnection(0x188470, 0x303c, 0x3, "3d0", ""),
			BFMConnection(0x1884dc, 0x303e, 0x0, "3d3", ""),
		)),
	0x303e: BFMConnectionData("Restaurant Basement Rotating Platforms Final Pendulum Room", 0x1d4, (
			BFMConnection(0x187334, 0x303e, 0x2, "3e", ""),
			BFMConnection(0x187358, 0x303e, 0x1, "3e", ""),
			BFMConnection(0x18737c, 0x3034, 0x6, "3e", ""),
			BFMConnection(0x187310, 0x303d, 0x3, "3e0", ""),
		)),
	0x303f: BFMConnectionData("Restaurant Basement Teleport Maze Arrow Traps", 0x1d4, (
			BFMConnection(0x189b6c, 0x3031, 0x9, "3f0", ""),
			BFMConnection(0x189b90, 0x3041, 0x0, "3f1", ""),
		)),
	0x3040: BFMConnectionData("Restaurant Basement Moat and Platforming Over Lava", 0x1d4, (
			BFMConnection(0x187f68, 0x3040, 0x2, "40", ""),
			BFMConnection(0x187f8c, 0x3040, 0x1, "40", ""),
			BFMConnection(0x187f44, 0x3034, 0x5, "400", ""),
			BFMConnection(0x187fb0, 0x302d, 0x0, "403", ""),
		)),
	0x3041: BFMConnectionData("Restaurant Basement Teleport Maze End", 0x1d4, (
			BFMConnection(0x18e72c, 0x3041, 0x2, "41", ""),
			BFMConnection(0x18e750, 0x3041, 0x1, "41", ""),
			BFMConnection(0x18e774, 0x3034, 0x6, "41", ""),
			BFMConnection(0x18e708, 0x303f, 0x1, "410", ""),
		)),
	0x3042: BFMConnectionData("Relic Keeper Arena", 0x1d8, (
			BFMConnection(0x18de00, 0x30a6, 0x2, "42", ""),
			BFMConnection(0x18ddb8, 0x304c, 0x1, "420", ""),
		)),
	0x3043: BFMConnectionData("Lower Mine Entrance", 0xe0, (
			BFMConnection(0x185e94, 0x1010, 0xf, "430", ""),
			BFMConnection(0x185f34, 0x1052, 0xf, "430", ""),
			BFMConnection(0x185f58, 0x1077, 0xf, "430", ""),
			BFMConnection(0x185f7c, 0x1094, 0xf, "430", ""),
			BFMConnection(0x185eb8, 0x3044, 0x0, "431", ""),
			BFMConnection(0x185edc, 0x3049, 0x2, "432", ""),
			BFMConnection(0x185f00, 0x304e, 0x0, "433", ""),
		)),
	0x3044: BFMConnectionData("Lower Mine Ferris Wheel 1", 0x1d4, (
			BFMConnection(0x18468c, 0x3043, 0x1, "440", ""),
			BFMConnection(0x1846b0, 0x3045, 0x0, "441", ""),
		)),
	0x3045: BFMConnectionData("Lower Mine Large Fan", 0x1d4, (
			BFMConnection(0x181d70, 0x3044, 0x1, "450", ""),
			BFMConnection(0x181d94, 0x3046, 0x0, "451", ""),
			BFMConnection(0x181db8, 0x3050, 0x0, "452", ""),
			BFMConnection(0x181ddc, 0x3048, 0x0, "453", ""),
		)),
	0x3046: BFMConnectionData("Lower Mine Conveyor Belts", 0x1d4, (
			BFMConnection(0x1858f0, 0x3045, 0x1, "460", ""),
			BFMConnection(0x185914, 0x3047, 0x0, "461", ""),
		)),
	0x3047: BFMConnectionData("Misteria Underground Lake", 0x1d4, (
			BFMConnection(0x1889c4, 0x3046, 0x1, "470", ""),
		)),
	0x3048: BFMConnectionData("Lower Mine Poison Ferris Wheel", 0x138, (
			BFMConnection(0x18953c, 0x3045, 0x3, "480", ""),
			BFMConnection(0x189560, 0x304b, 0x0, "481", ""),
		)),
	0x3049: BFMConnectionData("Lower Mine Poison Elevators", 0x1d4, (
			BFMConnection(0x186ee4, 0x3050, 0x1, "490", ""),
			BFMConnection(0x186f08, 0x306b, 0x0, "491", ""),
			BFMConnection(0x186f2c, 0x3043, 0x2, "492", ""),
		)),
	0x304a: BFMConnectionData("Cutscene Chapter 3 Start", 0x1d4, (
			BFMConnection(0x182450, 0x1053, 0x2, "4a", ""),
		), is_cutscene = True),
	0x304b: BFMConnectionData("Lower Mine Scrap Depository", 0x138, (
			BFMConnection(0x183e98, 0x3048, 0x1, "4b0", ""),
		)),
	0x304c: BFMConnectionData("Restaurant Basement Outside Relic Keeper", 0x1d8, (
			BFMConnection(0x18629c, 0x302d, 0x1, "4c0", ""),
			BFMConnection(0x1862c0, 0x3042, 0x0, "4c1", ""),
		)),
	0x304d: BFMConnectionData("Grillin Reservoir Tunnel", 0x1d4, (
			BFMConnection(0x18842c, 0x304e, 0x1, "4d0", ""),
			BFMConnection(0x188450, 0x3023, 0x0, "4d1", ""),
		)),
	0x304e: BFMConnectionData("Grillin Reservoir", 0x1d4, (
			BFMConnection(0x18dcfc, 0x1010, 0xe, "4e", ""),
			BFMConnection(0x18dcb4, 0x3043, 0x3, "4e0", ""),
			BFMConnection(0x18dcd8, 0x304d, 0x0, "4e1", ""),
			BFMConnection(0x18dd2c, 0x1052, 0xe, "4e2", ""),
			BFMConnection(0x18dd50, 0x1077, 0xe, "4e2", ""),
			BFMConnection(0x18dd74, 0x1094, 0xe, "4e2", ""),
		)),
	0x3050: BFMConnectionData("Lower Mine Ferris Wheel 2", 0x1d4, (
			BFMConnection(0x182ae8, 0x3045, 0x2, "500", ""),
			BFMConnection(0x182b0c, 0x3049, 0x0, "501", ""),
		)),
	0x3051: BFMConnectionData("Chapter 3 Church Vambee Fight", 0x1d4, (
			BFMConnection(0x185bdc, 0x1052, 0xc, "510", ""),
		)),
	0x1052: BFMConnectionData("Chapter 3 Grillin Village", 0x1f0, (
			BFMConnection(0x18e6c0, 0x1053, 0x1, "521", "", other=0x2),
			BFMConnection(0x18e6e4, 0x301c, 0x1, "522", "", other=0x2),
			BFMConnection(0x18e708, 0x3000, 0x0, "523", "", other=0x6),
			BFMConnection(0x18e72c, 0x2056, 0x0, "524", "", other=0x2),
			BFMConnection(0x18e774, 0x3014, 0x0, "526", "", other=0x2),
			BFMConnection(0x18e750, 0x3014, 0x1, "526", "", other=0x2),
			BFMConnection(0x18e798, 0x205b, 0x0, "527", "", other=0x2),
			BFMConnection(0x18e7bc, 0x2057, 0x0, "528", "", other=0x2),
			BFMConnection(0x18e7e0, 0x2055, 0x0, "529", "", other=0x2),
			BFMConnection(0x18e804, 0x2058, 0x0, "52a", "", other=0x6),
			BFMConnection(0x18d130, 0x3054, 0x0, "52a", ""),
			BFMConnection(0x18e828, 0x2059, 0x0, "52b", "", other=0x2),
			BFMConnection(0x18e8dc, 0x3051, 0x0, "52c", "", other=0x2),
			BFMConnection(0x18e894, 0x304e, 0x2, "52e", ""),
			BFMConnection(0x18e8b8, 0x3043, 0x0, "52f", "", other=0x2),
		)),
	0x1053: BFMConnectionData("Chapter 3 Upper Village", 0x1d4, (
			BFMConnection(0x187c04, 0x2057, 0x3, "53", "", other=0x2),
			BFMConnection(0x187b74, 0x1052, 0x1, "531", "", other=0x2),
			BFMConnection(0x187b98, 0x3025, 0x0, "532", "", other=0x2),
			BFMConnection(0x187bbc, 0x301e, 0x2, "533", "", other=0x2),
			BFMConnection(0x187be0, 0x306b, 0x2, "534", "", other=0x4),
		)),
	0x3054: BFMConnectionData("Chapter 3 Nightmare", 0x1d4, (
			BFMConnection(0x181744, 0x1010, 0xa, "54", ""),
			BFMConnection(0x18178c, 0x1077, 0xa, "54", ""),
			BFMConnection(0x1817b0, 0x1094, 0xa, "54", ""),
			BFMConnection(0x182cbc, 0x1052, 0xa, "540", ""),
		)),
	0x2055: BFMConnectionData("Chapter 3 Toy Shop", -0x4b0, (
			BFMConnection(0x1e304c, 0x1052, 0x9, "550", ""),
		)),
	0x2056: BFMConnectionData("Chapter 3 Bakery", -0x4cc, (
			BFMConnection(0x1e30fc, 0x1052, 0x4, "560", ""),
		)),
	0x2057: BFMConnectionData("Chapter 3 Grocery", -0x4b0, (
			BFMConnection(0x1e35c4, 0x1052, 0x8, "570", ""),
		)),
	0x2058: BFMConnectionData("Chapter 3 Inn", -0x32c, (
			BFMConnection(0x1e6644, 0x1052, 0xa, "580", ""),
		)),
	0x2059: BFMConnectionData("Chapter 3 Conner", -0x4b0, (
			BFMConnection(0x1e3230, 0x1052, 0xb, "590", ""),
		)),
	0x205b: BFMConnectionData("Chapter 3 Restaurant", -0x4b0, (
			BFMConnection(0xd39cc, 0x3034, 0x0, "5b", ""),
			BFMConnection(0x1e334c, 0x1052, 0x7, "5b0", ""),
		)),
	0x305c: BFMConnectionData("Frozen Palace Lobby", 0x1d4, (
			BFMConnection(0x186e2c, 0x3068, 0x1, "5c0", ""),
			BFMConnection(0x186e50, 0x3063, 0x2, "5c1", ""),
			BFMConnection(0x186e74, 0x305d, 0x0, "5c2", ""),
			BFMConnection(0x186e98, 0x305d, 0x1, "5c2", ""),
			BFMConnection(0x186ebc, 0x3065, 0x0, "5c4", ""),
			BFMConnection(0x186f04, 0x305f, 0x0, "5c6", ""),
			BFMConnection(0x186f28, 0x3061, 0x0, "5c7", ""),
			BFMConnection(0x186ee0, 0x3061, 0x1, "5c7", ""),
		)),
	0x305d: BFMConnectionData("Frozen Palace Blue Door Hallway", 0x1b4, (
			BFMConnection(0x18c3a8, 0x305d, 0x5, "5d", ""),
			BFMConnection(0x18c3f0, 0x305d, 0x3, "5d", ""),
			BFMConnection(0x18c414, 0x305d, 0x4, "5d", ""),
			BFMConnection(0x18c3cc, 0x305d, 0x6, "5d", ""),
			BFMConnection(0x18c33c, 0x305c, 0x2, "5d0", ""),
			BFMConnection(0x18c360, 0x305c, 0x3, "5d0", ""),
			BFMConnection(0x18c384, 0x305e, 0x0, "5d2", ""),
		)),
	0x305e: BFMConnectionData("Frozen Palace Ice Block and Red Eye Room", 0x1d4, (
			BFMConnection(0x185b9c, 0x305e, 0x3, "5e", ""),
			BFMConnection(0x185be4, 0x305e, 0x1, "5e", ""),
			BFMConnection(0x185b78, 0x305d, 0x2, "5e0", ""),
			BFMConnection(0x185bc0, 0x305f, 0x2, "5e2", ""),
		)),
	0x305f: BFMConnectionData("Frozen Palace Wolf Room", 0x1d4, (
			BFMConnection(0x1882b0, 0x305f, 0x1, "5f", ""),
			BFMConnection(0x188268, 0x305f, 0x3, "5f", ""),
			BFMConnection(0x188244, 0x305c, 0x6, "5f0", ""),
			BFMConnection(0x18828c, 0x305e, 0x2, "5f2", ""),
			BFMConnection(0x1882d4, 0x3060, 0x0, "5f4", ""),
		)),
	0x3060: BFMConnectionData("Frozen Palace Green Eye Maze and Green Eye Room", 0x1d4, (
			BFMConnection(0x18b764, 0x3060, 0x3, "60", ""),
			BFMConnection(0x18b788, 0x3060, 0x2, "60", ""),
			BFMConnection(0x18b71c, 0x305f, 0x4, "600", ""),
			BFMConnection(0x18b740, 0x3061, 0x3, "601", ""),
		)),
	0x3061: BFMConnectionData("Frozen Palace Ramp Hallway", 0x1d4, (
			BFMConnection(0x183608, 0x3061, 0x4, "61", ""),
			BFMConnection(0x183650, 0x3061, 0x2, "61", ""),
			BFMConnection(0x1835c0, 0x305c, 0x7, "610", ""),
			BFMConnection(0x1835e4, 0x305c, 0x5, "610", ""),
			BFMConnection(0x18362c, 0x3060, 0x1, "613", ""),
			BFMConnection(0x183674, 0x3064, 0x0, "615", ""),
		)),
	0x3062: BFMConnectionData("Frozen Palace Blue Eye Maze and Blue Eye Room", 0x1d4, (
			BFMConnection(0x189734, 0x3062, 0x3, "62", ""),
			BFMConnection(0x18977c, 0x3062, 0x1, "62", ""),
			BFMConnection(0x189710, 0x3064, 0x1, "620", ""),
			BFMConnection(0x189758, 0x3063, 0x0, "622", ""),
		)),
	0x3063: BFMConnectionData("Frozen Palace Red Eye Hallway to Blue Eye Maze", 0x1d4, (
			BFMConnection(0x188bec, 0x3063, 0x1, "63", ""),
			BFMConnection(0x188ba4, 0x3063, 0x3, "63", ""),
			BFMConnection(0x188b80, 0x3062, 0x2, "630", ""),
			BFMConnection(0x188bc8, 0x305c, 0x1, "632", ""),
		)),
	0x3064: BFMConnectionData("Frozen Palace Spike Bridge", 0x1d4, (
			BFMConnection(0x1824b0, 0x3061, 0x5, "640", ""),
			BFMConnection(0x1824d4, 0x3062, 0x0, "641", ""),
		)),
	0x3065: BFMConnectionData("Frozen Palace Ramp to Dragon Church", 0x1d4, (
			BFMConnection(0x182500, 0x305c, 0x4, "650", ""),
			BFMConnection(0x182524, 0x3066, 0x0, "651", ""),
		)),
	0x3066: BFMConnectionData("Frozen Palace Dragon Church", 0x1d4, (
			BFMConnection(0x181bac, 0x3067, 0x0, "66", ""),
			BFMConnection(0x181b88, 0x3065, 0x1, "660", ""),
		)),
	0x3067: BFMConnectionData("Frost Dragon Arena", 0x1d8, (
			BFMConnection(0x194270, 0x305c, 0x8, "67", ""),
		)),
	0x3068: BFMConnectionData("Frozen Palace Courtyard", 0x1d4, (
			BFMConnection(0x181fec, 0x3014, 0x2, "68", ""),
			BFMConnection(0x182034, 0x30a6, 0x3, "68", ""),
			BFMConnection(0x182010, 0x305c, 0x0, "681", ""),
		)),
	0x3069: BFMConnectionData("Chapter 4 Village on Fire", 0x1bc, (
			BFMConnection(0x1882cc, 0x1077, 0x11, "69", "", other=0x4),
		)),
	0x306a: BFMConnectionData("Cutscene Chapter 4 Start", 0x1d4, (
			BFMConnection(0x183a0c, 0x1077, 0x7, "6a", ""),
		), is_cutscene = True),
	0x306b: BFMConnectionData("Upper Mine Entrance", 0x1d4, (
			BFMConnection(0x181cd4, 0x1011, 0x4, "6b", ""),
			BFMConnection(0x181c8c, 0x3049, 0x1, "6b0", ""),
			BFMConnection(0x181cb0, 0x306c, 0x0, "6b1", ""),
			BFMConnection(0x181d4c, 0x1095, 0x4, "6b2", ""),
			BFMConnection(0x181d04, 0x1053, 0x4, "6b2", ""),
			BFMConnection(0x181d28, 0x1078, 0x4, "6b2", ""),
		)),
	0x306c: BFMConnectionData("Upper Mine Rock Slide Bridges", 0x138, (
			BFMConnection(0x1895ec, 0x306b, 0x1, "6c0", ""),
			BFMConnection(0x189610, 0x306d, 0x0, "6c1", ""),
		)),
	0x306d: BFMConnectionData("Upper Mine Poison Elevators", 0x1d4, (
			BFMConnection(0x18403c, 0x306c, 0x1, "6d0", ""),
			BFMConnection(0x184060, 0x3072, 0x0, "6d1", ""),
			BFMConnection(0x184084, 0x306e, 0x0, "6d2", ""),
		)),
	0x306e: BFMConnectionData("Upper Mine Windy Path", 0x148, (
			BFMConnection(0x186374, 0x306d, 0x2, "6e0", ""),
			BFMConnection(0x186398, 0x306f, 0x0, "6e1", ""),
		)),
	0x306f: BFMConnectionData("Upper Mine Big Fan", 0x1d4, (
			BFMConnection(0x185364, 0x306e, 0x1, "6f0", ""),
			BFMConnection(0x185388, 0x3070, 0x0, "6f1", ""),
		)),
	0x3070: BFMConnectionData("Upper Mine Ant Parade", 0x1d4, (
			BFMConnection(0x185fc4, 0x306f, 0x1, "700", ""),
			BFMConnection(0x185fe8, 0x3071, 0x0, "701", ""),
		)),
	0x3071: BFMConnectionData("Upper Mine Dig Area Near KnightD", 0x1d4, (
			BFMConnection(0x183008, 0x306d, 0x3, "71", ""),
			BFMConnection(0x182fe4, 0x3070, 0x1, "710", ""),
		)),
	0x3072: BFMConnectionData("Upper Mine Gondola Station", 0x138, (
			BFMConnection(0x18446c, 0x3073, 0x0, "72", ""),
			BFMConnection(0x184448, 0x306d, 0x1, "720", ""),
		)),
	0x3073: BFMConnectionData("Upper Mine Gondola Minigame", 0x1d4, (
			BFMConnection(0x1863c4, 0x3074, 0x0, "73", ""),
		)),
	0x3074: BFMConnectionData("Upper Mine Above Queen Ant", 0x1d4, (
			BFMConnection(0x1824f8, 0x3075, 0x0, "74", ""),
		)),
	0x3075: BFMConnectionData("Queen Ant Arena", 0x1d8, (
			BFMConnection(0x19222c, 0x3014, 0x5, "75", ""),
		)),
	0x3076: BFMConnectionData("Cutscene Chapter 5 Start", 0x1d4, (
			BFMConnection(0x181728, 0x1094, 0x2, "76", ""),
		), is_cutscene = True),
	0x1077: BFMConnectionData("Chapter 4 Grillin Village", 0x1f0, (
			BFMConnection(0x190fd0, 0x3051, 0x0, "77", "", other=0x2),
			BFMConnection(0x190db4, 0x1078, 0x1, "771", "", other=0x2),
			BFMConnection(0x190dd8, 0x301c, 0x1, "772", "", other=0x2),
			BFMConnection(0x190dfc, 0x3000, 0x0, "773", "", other=0x6),
			BFMConnection(0x190e20, 0x207b, 0x0, "774", "", other=0x2),
			BFMConnection(0x190e68, 0x3014, 0x0, "776", "", other=0x2),
			BFMConnection(0x190e44, 0x3014, 0x1, "776", "", other=0x2),
			BFMConnection(0x190e8c, 0x2080, 0x0, "777", "", other=0x2),
			BFMConnection(0x190eb0, 0x207c, 0x0, "778", "", other=0x2),
			BFMConnection(0x190ed4, 0x207a, 0x0, "779", "", other=0x2),
			BFMConnection(0x190ef8, 0x207d, 0x0, "77a", "", other=0x6),
			BFMConnection(0x18f7b8, 0x3079, 0x0, "77a", ""),
			BFMConnection(0x190f1c, 0x207e, 0x0, "77b", "", other=0x2),
			BFMConnection(0x190f40, 0x207f, 0x0, "77c", "", other=0x2),
			BFMConnection(0x190f88, 0x304e, 0x2, "77e", ""),
			BFMConnection(0x190fac, 0x3043, 0x0, "77f", "", other=0x2),
		)),
	0x1078: BFMConnectionData("Chapter 4 Upper Village", 0x1d4, (
			BFMConnection(0x187140, 0x1077, 0x1, "781", "", other=0x2),
			BFMConnection(0x187164, 0x3025, 0x0, "782", "", other=0x2),
			BFMConnection(0x187188, 0x301e, 0x2, "783", "", other=0x2),
			BFMConnection(0x1871ac, 0x306b, 0x2, "784", "", other=0x4),
		)),
	0x3079: BFMConnectionData("Chapter 4 Nightmare", 0x1d4, (
			BFMConnection(0x182cbc, 0x1077, 0xa, "790", ""),
		)),
	0x207a: BFMConnectionData("Chapter 4 Toy Shop", -0x338, (
			BFMConnection(0x1e85b4, 0x1077, 0x9, "7a0", ""),
		)),
	0x207b: BFMConnectionData("Chapter 4 Bakery", -0x354, (
			BFMConnection(0x1e8664, 0x1077, 0x4, "7b0", ""),
		)),
	0x207c: BFMConnectionData("Chapter 4 Grocery", -0x338, (
			BFMConnection(0x1e8b2c, 0x1077, 0x8, "7c0", ""),
		)),
	0x207d: BFMConnectionData("Chapter 4 Inn", -0x1b4, (
			BFMConnection(0x1ebbac, 0x1077, 0xa, "7d0", ""),
		)),
	0x207e: BFMConnectionData("Chapter 4 Conner", -0x338, (
			BFMConnection(0x1e8798, 0x1077, 0xb, "7e0", ""),
		)),
	0x207f: BFMConnectionData("Chapter 4 Church", -0x338, (
			BFMConnection(0x1e850c, 0x1077, 0xc, "7f0", ""),
		)),
	0x2080: BFMConnectionData("Chapter 4 Restaurant", -0x338, (
			BFMConnection(0xd39cc, 0x3034, 0x0, "80", ""),
			BFMConnection(0x1e8630, 0x1077, 0x7, "800", ""),
		)),
	0x3081: BFMConnectionData("Sky Island", 0x1d4, (
			BFMConnection(0x18bff0, 0x3093, 0x0, "81", ""),
		)),
	0x3082: BFMConnectionData("Soda Fountain Electric Walls", 0x1d4, (
			BFMConnection(0x189270, 0x3083, 0x0, "82", ""),
		)),
	0x3083: BFMConnectionData("Soda Fountain Tumble Dryer", 0x1d4, (
			BFMConnection(0x18a520, 0x3090, 0x0, "83", ""),
		)),
	0x3084: BFMConnectionData("Soda Fountain Calendar Maze Entrance", 0x1d4, (
			BFMConnection(0x184010, 0x3084, 0x0, "84", ""),
			BFMConnection(0x183e84, 0x3084, 0x6, "84", ""),
			BFMConnection(0x183f80, 0x3085, 0x0, "84", ""),
			BFMConnection(0x184058, 0x3084, 0x5, "84", ""),
			BFMConnection(0x183ecc, 0x3087, 0x0, "84", ""),
		)),
	0x3085: BFMConnectionData("Soda Fountain Calendar Maze Middle", 0x1d4, (
			BFMConnection(0x182600, 0x3085, 0x3, "85", ""),
			BFMConnection(0x182648, 0x3086, 0x0, "85", ""),
		)),
	0x3086: BFMConnectionData("Soda Fountain Calendar Maze Torches", 0x1d4, (
			BFMConnection(0x183968, 0x3086, 0x4, "86", ""),
			BFMConnection(0x1839f8, 0x3084, 0xe, "86", ""),
		)),
	0x3087: BFMConnectionData("Soda Fountain Calendar Maze End", 0x1d4, (
			BFMConnection(0x182508, 0x3088, 0x0, "87", ""),
		)),
	0x3088: BFMConnectionData("Soda Fountain Ed Fight", 0x1d8, (
			BFMConnection(0x188904, 0x3089, 0x0, "88", ""),
		)),
	0x3089: BFMConnectionData("Soda Fountain Garden", 0x1dc, (
			BFMConnection(0x19701c, 0x308a, 0x0, "89", ""),
		)),
	0x308a: BFMConnectionData("Soda Fountain Garden 2 Hedge Maze", 0x1d4, (
			BFMConnection(0x188aa4, 0x3091, 0x0, "8a", ""),
		)),
	0x308b: BFMConnectionData("Soda Fountain Factory Entrance", 0x1d4, (
			BFMConnection(0x190d28, 0x308b, 0x2, "8b", ""),
			BFMConnection(0x190d70, 0x308c, 0x0, "8b", ""),
		)),
	0x308c: BFMConnectionData("Soda Fountain Factory Steam Knight Head", 0x1d4, (
			BFMConnection(0x193200, 0x308c, 0x2, "8c", ""),
			BFMConnection(0x193248, 0x308d, 0x0, "8c", ""),
		)),
	0x308d: BFMConnectionData("Soda Fountain Topo Dance Battle", 0x1c4, (
			BFMConnection(0x1886a4, 0x308d, 0x2, "8d", ""),
			BFMConnection(0x1886ec, 0x308e, 0x0, "8d", ""),
		)),
	0x308e: BFMConnectionData("Soda Fountain Spiral to ToD", 0x1d4, (
			BFMConnection(0x1819e4, 0x308f, 0x0, "8e", ""),
		)),
	0x308f: BFMConnectionData("Soda Fountain ToD", 0x0, (
			BFMConnection(0x0, 0x0, 0x0, "8f", ""),
		)),
	0x3090: BFMConnectionData("Soda Fountain Ben Fight", 0x178, (
			BFMConnection(0x1858c4, 0x3084, 0xd, "90", ""),
		)),
	0x3091: BFMConnectionData("Soda Fountain Garden 3 More Gates", 0x1dc, (
			BFMConnection(0x196d6c, 0x3092, 0x0, "91", ""),
		)),
	0x3092: BFMConnectionData("Soda Fountain Garden 4 Climb", 0x1dc, (
			BFMConnection(0x195290, 0x308b, 0x0, "92", ""),
		)),
	0x3093: BFMConnectionData("Cutscene to Soda Fountain", 0x1b8, (
			BFMConnection(0x1857bc, 0x3082, 0x0, "93", ""),
		), is_cutscene = True),
	0x1094: BFMConnectionData("Chapter 5-6 Grillin Village", 0x1f0, (
			BFMConnection(0x190f94, 0x3051, 0x0, "94", "", other=0x2),
			BFMConnection(0x190d78, 0x1095, 0x1, "941", "", other=0x2),
			BFMConnection(0x190d9c, 0x301c, 0x1, "942", "", other=0x2),
			BFMConnection(0x190dc0, 0x3000, 0x0, "943", "", other=0x4),
			BFMConnection(0x190de4, 0x2098, 0x0, "944", "", other=0x2),
			BFMConnection(0x190e2c, 0x3014, 0x0, "946", "", other=0x2),
			BFMConnection(0x190e08, 0x3014, 0x1, "946", "", other=0x2),
			BFMConnection(0x190e50, 0x209d, 0x0, "947", "", other=0x2),
			BFMConnection(0x190e74, 0x2099, 0x0, "948", "", other=0x2),
			BFMConnection(0x190e98, 0x2097, 0x0, "949", "", other=0x2),
			BFMConnection(0x190ebc, 0x209a, 0x0, "94a", "", other=0x6),
			BFMConnection(0x18f7a0, 0x3096, 0x0, "94a", ""),
			BFMConnection(0x190ee0, 0x209b, 0x0, "94b", "", other=0x2),
			BFMConnection(0x190f04, 0x209c, 0x0, "94c", "", other=0x6),
			BFMConnection(0x190f4c, 0x304e, 0x2, "94e", ""),
			BFMConnection(0x190f70, 0x3043, 0x0, "94f", "", other=0x2),
		)),
	0x1095: BFMConnectionData("Chapter 5-6 Upper Village", 0x1d4, (
			BFMConnection(0x18a744, 0x1094, 0x1, "951", "", other=0x2),
			BFMConnection(0x18a768, 0x3025, 0x0, "952", "", other=0x2),
			BFMConnection(0x18a78c, 0x301e, 0x2, "953", "", other=0x2),
			BFMConnection(0x18a7b0, 0x306b, 0x2, "954", "", other=0x4),
			BFMConnection(0x18a7d4, 0x3004, 0x3, "955", "", other=0x8),
		)),
	0x3096: BFMConnectionData("Chapter 5-6 Nightmare", 0x1d4, (
			BFMConnection(0x181744, 0x1010, 0xa, "96", ""),
			BFMConnection(0x181768, 0x1052, 0xa, "96", ""),
			BFMConnection(0x18178c, 0x1077, 0xa, "96", ""),
			BFMConnection(0x182cbc, 0x1094, 0xa, "960", ""),
		)),
	0x2097: BFMConnectionData("Chapter 5-6 Toy Shop", -0x230, (
			BFMConnection(0x1ee444, 0x1094, 0x9, "970", ""),
		)),
	0x2098: BFMConnectionData("Chapter 5-6 Bakery", -0x24c, (
			BFMConnection(0x1ee4ec, 0x1094, 0x4, "980", ""),
		)),
	0x2099: BFMConnectionData("Chapter 5-6 Grocery", -0x230, (
			BFMConnection(0x1ee9b4, 0x1094, 0x8, "990", ""),
		)),
	0x209a: BFMConnectionData("Chapter 5-6 Inn", -0xac, (
			BFMConnection(0x1f1a34, 0x1094, 0xa, "9a0", ""),
		)),
	0x209b: BFMConnectionData("Chapter 5-6 Conner", -0x230, (
			BFMConnection(0x1ee620, 0x1094, 0xb, "9b0", ""),
		)),
	0x209c: BFMConnectionData("Chapter 5-6 Church", -0x230, (
			BFMConnection(0x1ee394, 0x1094, 0xc, "9c0", ""),
		)),
	0x209d: BFMConnectionData("Chapter 5-6 Restaurant", -0x230, (
			BFMConnection(0xd39cc, 0x3034, 0x0, "9d", ""),
			BFMConnection(0x1ee4b8, 0x1094, 0x7, "9d0", ""),
		)),
	0x309e: BFMConnectionData("Soda Fountain Dark Lumina 1", 0x0, (
			BFMConnection(0x0, 0x0, 0x0, "9e", ""),
		)),
	0x309f: BFMConnectionData("Soda Fountain Dark Lumina 2 Climb", 0x0, (
			BFMConnection(0x0, 0x0, 0x0, "9f", ""),
		)),
	0x30a0: BFMConnectionData("Soda Fountain Dark Lumina 2 Fight", 0x0, (
			BFMConnection(0x0, 0x0, 0x0, "a0", ""),
		)),
	0x30a1: BFMConnectionData("Soda Fountain Dark Lumina 3", 0x0, (
			BFMConnection(0x0, 0x0, 0x0, "a1", ""),
		)),
	0x30a2: BFMConnectionData("Ending Cutscene", 0x0, (
			BFMConnection(0x0, 0x0, 0x0, "a2", ""),
		), is_cutscene = True),
	0x30a6: BFMConnectionData("Cutscene Outside Soda Fountain", 0x1bc, (
			BFMConnection(0x1820b4, 0x306a, 0x0, "a6", ""),
			BFMConnection(0x182120, 0x1077, 0x7, "a6", ""),
			BFMConnection(0x1820d8, 0x3076, 0x0, "a6", ""),
			BFMConnection(0x182144, 0x1094, 0x2, "a6", ""),
			BFMConnection(0x182090, 0x304a, 0x0, "a6", ""),
			BFMConnection(0x1820fc, 0x1053, 0x2, "a6", ""),
		), is_cutscene = True),

}

