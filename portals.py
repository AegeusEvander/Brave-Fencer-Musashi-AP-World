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
			BFMConnection(0x0, 0x0, 0x0, "000", "Enter Castle Outside from Village or Gondola", connection_group = "Ignore"),
			BFMConnection(0x182c50, 0x3003, 0x0, "001", "Select Visit"),
			BFMConnection(0x182c2c, 0x3002, 0x1, "002", "Select Library"),
			BFMConnection(0x182c08, 0x3001, 0x1, "003", "Select Room"),
			BFMConnection(0x182d24, 0x1010, 0x3, "005", "Select Village"),
			BFMConnection(0x182d48, 0x1052, 0x3, "005", "Select Village", connection_group = "Ignore"),
			BFMConnection(0x182d6c, 0x1077, 0x3, "005", "Select Village", connection_group = "Ignore"),
			BFMConnection(0x182d90, 0x1094, 0x3, "005", "Select Village", connection_group = "Ignore"),
			BFMConnection(0x0, 0x0, 0x0, "004", "Enter Castle Outside from Castle", connection_group = "Ignore"),
			BFMConnection(0x182db4, 0x3069, 0x0, "006", "Select Village (On Fire)", can_be_disconnected = False),
			BFMConnection(0x182cbc, 0x3004, 0x1, "007", "Select Gondola"),
			BFMConnection(0x182c74, 0x3004, 0x0, "008", "Select Village (Zipline)", can_be_disconnected = False, connection_group = "Ignore"),
		)),
	0x3001: BFMConnectionData("Castle Bedroom", 0x1d4, (
			#BFMConnection(0x185e5c, 0x3002, 0x0, "01", "Intro Cutscene to Chapter 2"),
			BFMConnection(0x185e38, 0x3000, 0x4, "011", "Bedroom Door"),
		)),
	0x3002: BFMConnectionData("Castle Library", 0x1d4, (
			BFMConnection(0x18317c, 0x3000, 0x4, "021", "Library Door"),
		)),
	0x3003: BFMConnectionData("Castle Meeting Room", 0x1d4, (
			BFMConnection(0x186364, 0x3000, 0x4, "030", "Meeting Room Door"),
		)),
	0x3004: BFMConnectionData("Castle Gondola", 0x1d4, (
			BFMConnection(0x18202c, 0x1011, 0x5, "040", "Zipline", can_be_disconnected = False),
			#BFMConnection(0x182008, 0x1095, 0x5, "041", "Take Gondola to Upper Village"),
			BFMConnection(0x182074, 0x1095, 0x6, "041", "Take Gondola to Upper Village"),
			BFMConnection(0x182050, 0x3000, 0x0, "043", "Take Gondola to Castle"),
			#BFMConnection(0x1820a8, 0x1011, 0x0, ""),
			#BFMConnection(0x1820cc, 0x1053, 0x0, ""),
			#BFMConnection(0x1820f0, 0x1078, 0x0, ""),
			#BFMConnection(0x182114, 0x1095, 0x0, ""),
			#BFMConnection(0x182074, 0x1095, 0x6, "041", "Bug Squish"),
		)),
	0x3005: BFMConnectionData("Cutscene MOON", 0x1f0, (
			BFMConnection(0x182618, 0x3006, 0x0, "051", "End Moon Cutscene", can_be_disconnected = False),
			BFMConnection(0x18263c, 0x3008, 0x0, "052", "Skip Moon Cutscene", connection_group = "Ignore", can_be_disconnected = False),
		), is_cutscene = True),
	0x3006: BFMConnectionData("Cutscene Summon Crystal", 0x30c, (
			BFMConnection(0x187268, 0x3008, 0x0, "061", "End Summon Crystal Cutscene", can_be_disconnected = False),
		), is_cutscene = True),
	0x3008: BFMConnectionData("Starting Forest", 0x1d4, (
			BFMConnection(0x18a55c, 0x3009, 0x0, "081", "Behind Statue", connection_group = "CH1"),
		)),
	0x3009: BFMConnectionData("Spiral Tower Outside", 0x1d4, (
			BFMConnection(0x18948c, 0x300a, 0x0, "091", "Spiral Tower Outside Door", connection_group = "CH1"),
		)),
	0x300a: BFMConnectionData("Spiral Tower Inside", 0x1d4, (
			BFMConnection(0x18a2cc, 0x300b, 0x0, "0a1", "Top of Ramp Teleport", connection_group = "CH1"),
		)),
	0x300b: BFMConnectionData("Spiral Tower Roof", 0x1dc, (
			BFMConnection(0x18ea48, 0x300d, 0x0, "0b1", "End of Chase", connection_group = "CH1"),
		)),
	0x300d: BFMConnectionData("Cutscene Castle Outside Steam Knight", 0x1d4, (
			BFMConnection(0x1816ec, 0x300e, 0x0, "0d1", "Through Wall", connection_group = "CH1"),
		), is_cutscene = True),
	0x300e: BFMConnectionData("Castle Steam Knight Fight", 0x1d0, (
			BFMConnection(0x194370, 0x3001, 0x0, "0e1", "Wrecking Ball Throw", connection_group = "Ignore"),
			BFMConnection(0x0, 0x3004, 0x0, "0e1", "Wrecking Ball Throw", connection_group = "CH1"),
		)),
	0x1010: BFMConnectionData("Grillin Village", 0x22c, ( #Chapter 2 
			#"100" Conners again
			BFMConnection(0x19113c, 0x1011, 0x1, "101", "Village Ramp", other=0x2, can_be_disconnected = False),
			BFMConnection(0x191160, 0x301c, 0x1, "102", "Village Path by Windmill", other=0x2),
			BFMConnection(0x191184, 0x3000, 0x0, "103", "Village Through Portcullis", other=0x4),
			BFMConnection(0x1911a8, 0x2015, 0x0, "104", "Village Bakery", other=0x2, can_be_disconnected = False),
			BFMConnection(0x1911cc, 0x3014, 0x1, "105", "Village to Somnolent Forest", other=0x2),
			BFMConnection(0x1911f0, 0x3014, 0x0, "106", "Village to Deadend Somnolent Forest", other=0x2),
			BFMConnection(0x191214, 0x201a, 0x0, "107", "Village Restaurant", other=0x2, can_be_disconnected = False),
			BFMConnection(0x191238, 0x2016, 0x0, "108", "Village Grocery", other=0x2, can_be_disconnected = False),
			BFMConnection(0x19125c, 0x2013, 0x0, "109", "Village Toy Shop", other=0x2, can_be_disconnected = False),
			BFMConnection(0x191280, 0x2017, 0x0, "10a", "Village Inn", other=0x6, can_be_disconnected = False),
			BFMConnection(0x1912a4, 0x2018, 0x0, "10b", "Village Conner", other=0x2, can_be_disconnected = False),
			BFMConnection(0x1912c8, 0x2019, 0x0, "10c", "Village Church Door", other=0x6, can_be_disconnected = False),
			#"10d" is Windmill door
			#"10e" is Well
			BFMConnection(0x191334, 0x3043, 0x0, "10f", "Village Lower Mine Door", other=0x2),
		)),
	0x1011: BFMConnectionData("Chapter 2 Upper Village", 0x1f4, (
			BFMConnection(0x189694, 0x1010, 0x1, "111", "Upper Village Ramp", other=0x2, can_be_disconnected = False),
			BFMConnection(0x1896b8, 0x3025, 0x0, "112", "Upper Village Mountain Pass", other=0x2, can_be_disconnected = False),
			BFMConnection(0x1896dc, 0x301e, 0x2, "113", "Upper Village Steam Pipe", other=0x2),
			BFMConnection(0x189700, 0x306b, 0x2, "114", "Upper Village Upper Open Vent", other=0x4),
		)),
	0x3012: BFMConnectionData("Chapter 2 Nightmare", 0x1d4, (
			BFMConnection(0x182d08, 0x1010, 0xa, "121", "Bed", connection_group = "Ignore"),
		)),
	0x2013: BFMConnectionData("Chapter 2 Toy Shop", -0x248, (
			BFMConnection(0x1efeec, 0x1010, 0x9, "130", "Toy Store Door", can_be_disconnected = False),
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
			BFMConnection(0x190614, 0x301b, 0x0, "142", "Somnolent Forest to Meandering", can_be_disconnected = False),
			BFMConnection(0x1906a4, 0x301b, 0x21, "142", "Somnolent Forest to Meandering", connection_group = "Ignore", can_be_disconnected = False),
			BFMConnection(0x190638, 0x301c, 0x0, "143", "Somnolent Forest Large Pipe"),
			BFMConnection(0x19065c, 0x3021, 0x0, "144", "Somnolent Forest to Island of Dragons"),
			BFMConnection(0x0, 0x0, 0x0, "145", "Somnolent Forest Deadend Fall From Sky"),
		)),
	0x2015: BFMConnectionData("Chapter 2 Bakery", -0x264, (
			BFMConnection(0x1eff94, 0x1010, 0x4, "150", "Bakery Door", can_be_disconnected = False),
		)),
	0x2016: BFMConnectionData("Chapter 2 Grocery", -0x248, (
			BFMConnection(0x1f045c, 0x1010, 0x8, "160", "Grocery Door", can_be_disconnected = False),
		)),
	0x2017: BFMConnectionData("Chapter 2 Inn", -0xc4, (
			BFMConnection(0x1f34dc, 0x1010, 0xa, "170", "Inn Door", can_be_disconnected = False),
		)),
	0x2018: BFMConnectionData("Chapter 2 Conner", -0x248, (
			BFMConnection(0x1f00e8, 0x1010, 0xb, "180", "Conner Door", can_be_disconnected = False),
		)),
	0x2019: BFMConnectionData("Chapter 2 Church", -0x248, (
			BFMConnection(0x1efe3c, 0x1010, 0xc, "190", "Church Door", can_be_disconnected = False),
		)),
	0x201a: BFMConnectionData("Chapter 2 Restaurant", -0x248, (
			BFMConnection(0x1eff60, 0x1010, 0x7, "1a0", "Restaurant Door", can_be_disconnected = False),
			BFMConnection(0x0d39cc, 0x3034, 0x0, "1a1", "Restaurant Hidden Exit Behind Counter"),
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
			BFMConnection(0x184dcc, 0x301d, 0x0, "1e1", "Outside Steamwood Enter Steamwood", can_be_disconnected = False),
			BFMConnection(0x184e8c, 0x3020, 0x0, "1e1", "Outside Steamwood Enter Steamwood", can_be_disconnected = False),
			BFMConnection(0x184df0, 0x1011, 0x3, "1e2", "Outside Steamwood Pipe"),
			BFMConnection(0x184e20, 0x1053, 0x3, "1e2", "Outside Steamwood Pipe", connection_group = "Ignore"),
			BFMConnection(0x184e44, 0x1078, 0x3, "1e2", "Outside Steamwood Pipe", connection_group = "Ignore"),
			BFMConnection(0x184e68, 0x1095, 0x3, "1e2", "Outside Steamwood Pipe", connection_group = "Ignore"),
		)),
	0x301f: BFMConnectionData("Cutscene Steamwood Success", 0x1d4, (
			BFMConnection(0x181b58, 0x301e, 0x1, "1f1", "Steamwood Cutscene", can_be_disconnected = False),
		), is_cutscene = True),
	0x3020: BFMConnectionData("Steamwood 2", 0x1c8, (
			BFMConnection(0x184a94, 0x301f, 0x0, "201", "Steamwood 2 Success", can_be_disconnected = False),
		)),
	0x3021: BFMConnectionData("Island of Dragons", 0x1d8, (
			BFMConnection(0x18f7d8, 0x3003, 0x0, "211", "Rescue Princess", connection_group = "Ignore", can_be_disconnected = False),
			BFMConnection(0x18f7b4, 0x3014, 0x4, "210", "Island of Dragons Exit"),
		)),
	0x3022: BFMConnectionData("Graveyard", 0x1d4, (
			BFMConnection(0x1828d4, 0x3014, 0x2, "221", "Graveyard Exit", can_be_disconnected = False),
		)),
	0x3023: BFMConnectionData("Grillin Volcano", 0x1d4, (
			BFMConnection(0x18aefc, 0x304d, 0x1, "230", "Volcano Caldera"),
			BFMConnection(0x18af20, 0x3014, 0x2, "231", "Exit Meandering Forest"),
		)),
	0x3024: BFMConnectionData("Skullpion Arena", 0x1d8, (
			BFMConnection(0x18f7c8, 0x302b, 0x1, "240", "Skullpion Arena Entrance"),
			BFMConnection(0x18f7ec, 0x30a6, 0x1, "241", "Defeat Skullpion", can_be_disconnected = False),
		)),
	0x3025: BFMConnectionData("Twinpeak Entrance", 0x1d4, (
			BFMConnection(0x18b3bc, 0x1011, 0x2, "250", "Twinpeak Entrance South Path", can_be_disconnected = False),
			BFMConnection(0x18b4fc, 0x1053, 0x2, "250", "Twinpeak Entrance South Path", connection_group = "Ignore", can_be_disconnected = False),
			BFMConnection(0x18b520, 0x1078, 0x2, "250", "Twinpeak Entrance South Path", connection_group = "Ignore", can_be_disconnected = False),
			BFMConnection(0x18b544, 0x1095, 0x2, "250", "Twinpeak Entrance South Path", connection_group = "Ignore", can_be_disconnected = False),
			BFMConnection(0x18b3e0, 0x302b, 0x0, "251", "Twinpeak Entrance East Path"),
			BFMConnection(0x0, 0x0, 0x0, "252", "Twinpeak Entrance Rafting Exit"),#"252" Rafting End
			BFMConnection(0x18b428, 0x3026, 0x1, "253", "Twinpeak Entrance West Path"),
			BFMConnection(0x18b470, 0x302b, 0x2, "255", "Twinpeak Entrance Cliff Upper East Path"),
			BFMConnection(0x18b4b8, 0x3029, 0x2, "257", "Twinpeak Entrance Dock"),
		)),
	0x3026: BFMConnectionData("Twinpeak Around the Bend", 0x184, (
			BFMConnection(0x194f28, 0x3025, 0x3, "261", "Twinpeak Around the Bend Along River East"),
			BFMConnection(0x0, 0x0, 0x0, "262", "Twinpeak Around the Bend Rafting Shortcut Exit"),#"262" Rafting shortcut waterfall exit
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
			#"2a0" Rafting Start
			BFMConnection(0x185884, 0x3026, 0x2, "2a1", "Rafting Shortcut"),
			BFMConnection(0x1858a8, 0x3025, 0x2, "2a2", "Rafting End"),
			#BFMConnection(0x78e50, 0x302a, 0x0, "2a", ""),
		)),
	0x302b: BFMConnectionData("Twinpeak Path to Skullpion", 0x1c4, (
			BFMConnection(0x185f00, 0x3025, 0x1, "2b0", "Path to Skullpion South"),
			BFMConnection(0x185f24, 0x3024, 0x0, "2b1", "Path to Skullpion North"),
			BFMConnection(0x185f48, 0x3025, 0x5, "2b2", "Path to Skullpion Upper Cliff South"),
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
			BFMConnection(0x18ef08, 0x302f, 0xb, "2f9", "Bowling 1 MercenA Room Upper"),
			BFMConnection(0x18ef2c, 0x302f, 0x8, "2fa", "Bowling 1 Odd Hat Room West"),
			BFMConnection(0x18ef50, 0x302f, 0x9, "2fb", "Fire Totem Room West"),
			BFMConnection(0x0, 0x0, 0x0, "2fc", "Fire Totem Room Elevator"),#"2fc" fire totem elevator 
			BFMConnection(0x18ef98, 0x302f, 0xe, "2fd", "Fire Totem Room East"),
			BFMConnection(0x18efbc, 0x302f, 0xd, "2fe", "Wall Crush Trap Room North"),
			BFMConnection(0x18efe0, 0x3030, 0x0, "2ff", "Wall Crush Trap Room East"),
		)),
	0x3030: BFMConnectionData("Restaurant Basement Bowling 2", 0x1d4, (
			BFMConnection(0x0, 0x0, 0x0, "300", "Bowling 2 Piston Trap West"),#"300" Bowling 2 Piston Trap West
			BFMConnection(0x18efec, 0x3030, 0x2, "301", "Bowling 2 Piston Trap North"),
			BFMConnection(0x18f010, 0x3030, 0x1, "302", "Bowling 2 Plant Room South"),
			BFMConnection(0x18f034, 0x3030, 0x4, "303", "Bowling 2 Plant Room West"),
			BFMConnection(0x18f058, 0x3030, 0x3, "304", "Bowling 2 East"),
			BFMConnection(0x18f07c, 0x3030, 0x7, "305", "Bowling 2 North"),
			BFMConnection(0x18f0a0, 0x3030, 0x8, "306", "Bowling 2 Elevator"),
			BFMConnection(0x18f0c4, 0x3030, 0x5, "307", "Bowling 2 MercenB Room South"),
			BFMConnection(0x0, 0x0, 0x0, "308", "Bowling 2 Top of Elevator"),#"308" bowling 2 elevator 
			BFMConnection(0x18f10c, 0x3030, 0xa, "309", "Bowling 2 Top of Elevator North"),
			BFMConnection(0x18f130, 0x3030, 0x9, "30a", "Bowling End Eye Room South"),
			BFMConnection(0x18f154, 0x3034, 0x6, "30b", "Bowling End Eye Room Teleport Back"),
		)),
	0x3031: BFMConnectionData("Restaurant Basement Teleport Maze Entrance", 0x1d4, (
			BFMConnection(0x18d0ac, 0x3034, 0x2, "310", "Teleport Maze Start Room South"),
			BFMConnection(0x18d0d0, 0x3031, 0x2, "311", "Teleport Maze Start Room North"),
			BFMConnection(0x18d0f4, 0x3031, 0x1, "312", "Teleport Maze Sliding Platform Room South"),
			BFMConnection(0x18d118, 0x3031, 0x7, "313", "Teleport Maze Sliding Platform Room Lower North"),
			BFMConnection(0x18d13c, 0x3031, 0x8, "314", "Teleport Maze Sliding Platform Room Upper North"),
			BFMConnection(0x18d160, 0x3032, 0x0, "315", "Teleport Maze Sliding Platform Room West"),
			BFMConnection(0x18d184, 0x3033, 0x0, "316", "Teleport Maze Sliding Platform Room East"),
			BFMConnection(0x18d1a8, 0x3031, 0x3, "317", "Teleport Maze Return Teleport South"),
			BFMConnection(0x18d1cc, 0x3031, 0x4, "318", "Teleport Maze Two Tiered Platforms Lower South"),
			BFMConnection(0x18d1f0, 0x303f, 0x0, "319", "Teleport Maze Two Tiered Platforms Upper North"),
			BFMConnection(0x0, 0x0, 0x0, "31a", "Teleport Maze Starting Room Return Pad"),#"31a" starting room return pad
			BFMConnection(0x0, 0x0, 0x0, "31b", "Teleport Maze Two Tiered Platforms Lower Pad"),#"31b" two tiered room lower pad
			BFMConnection(0x0, 0x0, 0x0, "31c", "Teleport Maze Two Tiered Platforms Upper Pad"),#"31c" two tiered room upper pad
			BFMConnection(0x18d280, 0x3031, 0xa, "31d", "Teleport Maze Return Teleport Pad"),
		)),
	0x3032: BFMConnectionData("Restaurant Basement Teleport Maze", 0x1d4, (
			BFMConnection(0x18f4d0, 0x3031, 0x5, "320", "Teleport Maze Left Dark Hallway East"),
			BFMConnection(0x18f4f4, 0x3032, 0x3, "321", "Teleport Maze Left Dark Hallway West"),
			BFMConnection(0x18f518, 0x3032, 0x6, "322", "Teleport Maze Left Dark Hallway Upper North"),
			BFMConnection(0x18f53c, 0x3032, 0x1, "323", "Teleport Maze Left Dark L Spike Hallway East"),
			BFMConnection(0x18f560, 0x3032, 0x5, "324", "Teleport Maze Left Dark L Spike Hallway North"),
			BFMConnection(0x18f584, 0x3032, 0x4, "325", "Teleport Maze First Teleport Choice South"),
			BFMConnection(0x18f5a8, 0x3032, 0x2, "326", "Teleport Maze Left Dark L Hallway South"),
			BFMConnection(0x18f5cc, 0x3032, 0x8, "327", "Teleport Maze Left Dark L Hallway East"),
			BFMConnection(0x18f5f0, 0x3032, 0x7, "328", "Teleport Maze Third Teleport Choice West"),
			BFMConnection(0x0, 0x0, 0x0, "329", "Teleport Maze Left Dark Hallway Upper Pad"),#"329" upper pad
			BFMConnection(0x18f638, 0x3031, 0xa, "32a", "Teleport Maze First Teleport Choice Left Pad"),
			BFMConnection(0x18f65c, 0x3033, 0x9, "32b", "Teleport Maze First Teleport Choice Right Pad"),
			BFMConnection(0x18f6a4, 0x3031, 0xc, "32c", "Teleport Maze Third Teleport Choice Left Pad"),
			BFMConnection(0x18f680, 0x3031, 0xb, "32d", "Teleport Maze Third Teleport Choice Right Pad"),
		)),
	0x3033: BFMConnectionData("Restaurant Basement Teleport Maze Side Area", 0x1d4, (
			BFMConnection(0x1904b4, 0x3031, 0x6, "330", "Teleport Maze Right Dark Hallway West"),
			BFMConnection(0x1904d8, 0x3033, 0x3, "331", "Teleport Maze Right Dark Hallway East"),
			BFMConnection(0x1904fc, 0x3033, 0x6, "332", "Teleport Maze Right Dark Hallway Upper North"),
			BFMConnection(0x190520, 0x3033, 0x1, "333", "Teleport Maze Right Dark J Spike Hallway West"),
			BFMConnection(0x190544, 0x3033, 0x5, "334", "Teleport Maze Right Dark J Spike Hallway North"),
			BFMConnection(0x190568, 0x3033, 0x4, "335", "Teleport Maze Bailiff Room South"),
			BFMConnection(0x19058c, 0x3033, 0x2, "336", "Teleport Maze Right J Hallway South"),
			BFMConnection(0x1905b0, 0x3033, 0x8, "337", "Teleport Maze Right J Hallway West"),
			BFMConnection(0x1905d4, 0x3033, 0x7, "338", "Teleport Maze Second Teleport Choice East"),
			BFMConnection(0x0, 0x0, 0x0, "339", "Teleport Maze Right Dark Hallway Upper Pad"),#"339" upper pad
			BFMConnection(0x190640, 0x3032, 0x9, "33a", "Teleport Maze Second Teleport Choice Left Pad"),
			BFMConnection(0x19061c, 0x3031, 0xb, "33b", "Teleport Maze Second Teleport Choice Right Pad"),
		)),
	0x3034: BFMConnectionData("Restaurant Basement Entrance", 0x1d4, (
			BFMConnection(0x188794, 0x1010, 0x7, "340", "Basement Exit (Upper South)"),
			BFMConnection(0x188890, 0x1052, 0x7, "340", "Basement Exit (Upper South)", connection_group = "Ignore"),
			BFMConnection(0x1888b4, 0x1077, 0x7, "340", "Basement Exit (Upper South)", connection_group = "Ignore"),
			BFMConnection(0x1888d8, 0x1094, 0x7, "340", "Basement Exit (Upper South)", connection_group = "Ignore"),
			BFMConnection(0x1887b8, 0x302e, 0x0, "341", "Basement South West Door (Bowling)"),
			BFMConnection(0x1887dc, 0x3031, 0x0, "342", "Basement North West Door (Teleport Maze)"),
			BFMConnection(0x188800, 0x3035, 0x0, "343", "Basement South East Door (Dark Maze)"),
			BFMConnection(0x188824, 0x303a, 0x0, "344", "Basement North East Door (Rotating Platforms)"),
			BFMConnection(0x188848, 0x3040, 0x0, "345", "Basement Lower Angel Statue Door"),
			BFMConnection(0x0, 0x0, 0x0, "346", "Basement Return Pad Center Crossroad"),#"346" return Pad center crossroad
		)),
	0x3035: BFMConnectionData("Restaurant Basement Dark Maze Entrance", 0x1d4, (
			BFMConnection(0x189a5c, 0x3034, 0x3, "350", "Dark Maze Vambees on Pillars South West"),
			BFMConnection(0x189a80, 0x3035, 0x2, "351", "Dark Maze Vambees on Pillars North East"),
			BFMConnection(0x189aa4, 0x3035, 0x1, "352", "Dark Maze Crossroads with Sliding Blocks South West"),
			BFMConnection(0x189ac8, 0x3036, 0x0, "353", "Dark Maze Crossroads with Sliding Blocks North East"),
			BFMConnection(0x189aec, 0x3037, 0x3, "354", "Dark Maze Crossroads with Sliding Blocks South East"),
			BFMConnection(0x189b10, 0x3035, 0x6, "355", "Dark Maze Crossroads with Sliding Blocks North West"),
			BFMConnection(0x189b34, 0x3035, 0x5, "356", "Dark Maze 2 East"),
			BFMConnection(0x189b58, 0x3038, 0x0, "357", "Dark Maze 2 West"),
		)),
	0x3036: BFMConnectionData("Restaurant Basement Dark Maze Sliding Block Puzzle", 0x1d4, (
			BFMConnection(0x18b2c0, 0x3035, 0x3, "360", "Dark Maze Crushing Blocks South West"),
			BFMConnection(0x18b2e4, 0x3036, 0x4, "361", "Dark Maze Crushing Blocks North West"),
			BFMConnection(0x18b308, 0x3036, 0x9, "362", "Dark Maze Crushing Blocks North East"),
			BFMConnection(0x18b32c, 0x3037, 0x0, "363", "Dark Maze Crushing Blocks South East"),
			BFMConnection(0x18b350, 0x3036, 0x1, "364", "Dark Maze Sliding Block Puzzle 1 Block East"),
			BFMConnection(0x18b374, 0x3036, 0x6, "365", "Dark Maze Sliding Block Puzzle 1 Block North"),
			BFMConnection(0x18b398, 0x3036, 0x5, "366", "Dark Maze Sliding Block Puzzle 3 Blocks South"),
			BFMConnection(0x18b3bc, 0x3036, 0x8, "367", "Dark Maze Sliding Block Puzzle 3 Blocks North"),
			BFMConnection(0x18b3e0, 0x3036, 0x7, "368", "Dark Maze Two Large Floating Platforms Left South West"),
			BFMConnection(0x18b404, 0x3036, 0x2, "369", "Dark Maze Two Large Floating Platforms Right South West"),
		)),
	0x3037: BFMConnectionData("Restaurant Basement Dark Maze", 0x1d4, (
			BFMConnection(0x184920, 0x3036, 0x3, "370", "Dark Maze Slow Elevating Platform North West"),
			BFMConnection(0x184944, 0x3037, 0x2, "371", "Dark Maze Slow Elevating Platform South West"),
			BFMConnection(0x184968, 0x3037, 0x1, "372", "Dark Maze 1 North"),
			BFMConnection(0x18498c, 0x3035, 0x4, "373", "Dark Maze 1 West"),
		)),
	0x3038: BFMConnectionData("Restaurant Basement Dark Maze Vertical Maze", 0x1d4, (
			BFMConnection(0x1844a0, 0x3035, 0x7, "380", "Dark Maze Vertical Maze Upper East"),
			BFMConnection(0x1844c4, 0x3039, 0x0, "381", "Dark Maze Vertical Maze Lower West"),
		)),
	0x3039: BFMConnectionData("Restaurant Basement Dark Maze End", 0x1d4, (
			BFMConnection(0x189a18, 0x3038, 0x1, "390", "Dark Maze 3 East"),
			BFMConnection(0x189a3c, 0x3039, 0x3, "391", "Dark Maze 3 West"),
			BFMConnection(0x189a60, 0x3039, 0x4, "392", "Dark Maze 3 Lower North"),
			BFMConnection(0x189a84, 0x3039, 0x1, "393", "Dark Maze End Eye Room South"),
			BFMConnection(0x189aa8, 0x3039, 0x2, "394", "Dark Maze KnightC Room South"),
			BFMConnection(0x0, 0x0, 0x0, "395", "Dark Maze 3 Teleport Pad"),#"395" Dark Maze 3 pad
			BFMConnection(0x189af0, 0x3039, 0x5, "396", "Dark Maze KnightC Room Teleport"),
			BFMConnection(0x189acc, 0x3034, 0x6, "397", "Dark Maze End Eye Room Teleport Back"),
		)),
	0x303a: BFMConnectionData("Restaurant Basement Rotating Platforms Entrance", 0x1d4, (
			BFMConnection(0x188ea4, 0x3034, 0x4, "3a0", "Rotating Platforms Entrance South West"),
			BFMConnection(0x188ec8, 0x303a, 0x2, "3a1", "Rotating Platforms Entrance North East"),
			BFMConnection(0x188eec, 0x303a, 0x1, "3a2", "Rotating Platforms Entrance Librarian South West"),
			BFMConnection(0x188f10, 0x303b, 0x0, "3a3", "Rotating Platforms Entrance Librarian North East"),
		)),
	0x303b: BFMConnectionData("Restaurant Basement Rotating Platforms Long Platforms", 0x1d4, (
			BFMConnection(0x187ebc, 0x303a, 0x3, "3b0", "Rotating Platforms Long Platforms South West"),
			BFMConnection(0x187ee0, 0x303c, 0x0, "3b1", "Rotating Platforms Long Platforms North West"),
		)),
	0x303c: BFMConnectionData("Restaurant Basement Rotating Platforms First Lava Area", 0x1d4, (
			BFMConnection(0x186e0c, 0x303b, 0x1, "3c0", "Rotating Platforms Small Lava Room Spiked Rotating Walls Lower South East"),
			BFMConnection(0x186e30, 0x303c, 0x2, "3c1", "Rotating Platforms Small Lava Room Spiked Rotating Walls Upper South East"),
			BFMConnection(0x186e54, 0x303c, 0x1, "3c2", "Rotating Platforms Orbiting Platforms North West"),
			BFMConnection(0x186e78, 0x303d, 0x0, "3c3", "Rotating Platforms Orbiting Platforms North East"),
		)),
	0x303d: BFMConnectionData("Restaurant Basement Rotating Platforms Lava and Pendulums", 0x1d4, (
			BFMConnection(0x188470, 0x303c, 0x3, "3d0", "Rotating Platforms Small Lava Room Swinging Pendulums South West"),
			BFMConnection(0x188494, 0x303d, 0x2, "3d1", "Rotating Platforms Small Lava Room Swinging Pendulums South East"),
			BFMConnection(0x1884b8, 0x303d, 0x1, "3d2", "Rotating Platforms Large Lava Room Spiked Rotating Walls Wooden Planks North West"),
			BFMConnection(0x1884dc, 0x303e, 0x0, "3d3", "Rotating Platforms Large Lava Room Spiked Rotating Walls Wooden Planks South West"),
		)),
	0x303e: BFMConnectionData("Restaurant Basement Rotating Platforms Final Pendulum Room", 0x1d4, (
			BFMConnection(0x187310, 0x303d, 0x3, "3e0", "Rotating Platforms Large Lava Room Swinging Pendulums North East"),
			BFMConnection(0x187334, 0x303e, 0x2, "3e1", "Rotating Platforms Large Lava Room Swinging Pendulums South West"),
			BFMConnection(0x187358, 0x303e, 0x1, "3e2", "Rotating Platforms End Eye Room South"),
			BFMConnection(0x18737c, 0x3034, 0x6, "3e3", "Rotating Platforms End Eye Room Teleport Back"),
		)),
	0x303f: BFMConnectionData("Restaurant Basement Teleport Maze Arrow Traps", 0x1d4, (
			BFMConnection(0x189b6c, 0x3031, 0x9, "3f0", "Teleport Maze Arrow Trap Upper West"),
			BFMConnection(0x189b90, 0x3041, 0x0, "3f1", "Teleport Maze Arrow Trap Lower West"),
		)),
	0x3040: BFMConnectionData("Restaurant Basement Moat and Platforming Over Lava", 0x1d4, (
			BFMConnection(0x187f44, 0x3034, 0x5, "400", "Basement Water Moat South"),
			BFMConnection(0x187f68, 0x3040, 0x2, "401", "Basement Water Moat North"),
			BFMConnection(0x187f8c, 0x3040, 0x1, "402", "Basement Platforming Over Lava South West"),
			BFMConnection(0x187fb0, 0x302d, 0x0, "403", "Basement Platforming Over Lava North East"),
		)),
	0x3041: BFMConnectionData("Restaurant Basement Teleport Maze End", 0x1d4, (
			BFMConnection(0x18e708, 0x303f, 0x1, "410", "Teleport Maze End Spike Hallway South"),
			BFMConnection(0x18e72c, 0x3041, 0x2, "411", "Teleport Maze End Spike Hallway North"),
			BFMConnection(0x18e750, 0x3041, 0x1, "412", "Teleport Maze End Eye Room South"),
			BFMConnection(0x18e774, 0x3034, 0x6, "413", "Teleport Maze End Eye Room Teleport Back"),
		)),
	0x3042: BFMConnectionData("Relic Keeper Arena", 0x1d8, (
			BFMConnection(0x18ddb8, 0x304c, 0x1, "420", "Relic Keeper Arena Entrance"),
			BFMConnection(0x18de00, 0x30a6, 0x2, "421", "Defeat Relic Keeper", can_be_disconnected = False),
		)),
	0x3043: BFMConnectionData("Lower Mine Entrance", 0xe0, (
			BFMConnection(0x185e94, 0x1010, 0xf, "430", "Lower Mine Entrance Towards Village"),
			BFMConnection(0x185f34, 0x1052, 0xf, "430", "Lower Mine Entrance Towards Village", connection_group = "Ignore"),
			BFMConnection(0x185f58, 0x1077, 0xf, "430", "Lower Mine Entrance Towards Village", connection_group = "Ignore"),
			BFMConnection(0x185f7c, 0x1094, 0xf, "430", "Lower Mine Entrance Towards Village", connection_group = "Ignore"),
			BFMConnection(0x185eb8, 0x3044, 0x0, "431", "Lower Mine Entrance Towards Mine (Upper Exit near Toadstool)"),
			BFMConnection(0x185edc, 0x3049, 0x2, "432", "Lower Mine Entrance Towards Mine Return (Upper Exit Inaccessible From Below)"),
			BFMConnection(0x185f00, 0x304e, 0x0, "433", "Lower Mine Entrance Towards Reservoir"),
		)),
	0x3044: BFMConnectionData("Lower Mine Ferris Wheel 1", 0x1d4, (
			BFMConnection(0x18468c, 0x3043, 0x1, "440", "Lower Mine Ferris Wheel 1 West"),
			BFMConnection(0x1846b0, 0x3045, 0x0, "441", "Lower Mine Ferris Wheel 1 East"),
		)),
	0x3045: BFMConnectionData("Lower Mine Large Fan", 0x1d4, (
			BFMConnection(0x181d70, 0x3044, 0x1, "450", "Lower Mine Large Fan Upper West"),
			BFMConnection(0x181d94, 0x3046, 0x0, "451", "Lower Mine Large Fan Lower West"),
			BFMConnection(0x181db8, 0x3050, 0x0, "452", "Lower Mine Large Fan Upper East"),
			BFMConnection(0x181ddc, 0x3048, 0x0, "453", "Lower Mine Large Fan Lower East"),
		)),
	0x3046: BFMConnectionData("Lower Mine Conveyor Belts", 0x1d4, (
			BFMConnection(0x1858f0, 0x3045, 0x1, "460", "Lower Mine Conveyor Belts East"),
			BFMConnection(0x185914, 0x3047, 0x0, "461", "Lower Mine Conveyor Belts West"),
		)),
	0x3047: BFMConnectionData("Misteria Underground Lake", 0x1d4, (
			BFMConnection(0x1889c4, 0x3046, 0x1, "470", "Misteria Underground Lake Entrance"),
		)),
	0x3048: BFMConnectionData("Lower Mine Poison Ferris Wheel", 0x138, (
			BFMConnection(0x18953c, 0x3045, 0x3, "480", "Lower Mine Poison Ferris Wheel West"),
			BFMConnection(0x189560, 0x304b, 0x0, "481", "Lower Mine Poison Ferris Wheel East"),
		)),
	0x3049: BFMConnectionData("Lower Mine Poison Elevators", 0x1d4, (
			BFMConnection(0x186ee4, 0x3050, 0x1, "490", "Lower Mine Poison Elevators Lower West"),
			BFMConnection(0x186f08, 0x306b, 0x0, "491", "Lower Mine Poison Elevators Upper East (Inaccessible From Below)"),
			BFMConnection(0x186f2c, 0x3043, 0x2, "492", "Lower Mine Poison Elevators Upper West"),
		)),
	0x304a: BFMConnectionData("Cutscene Chapter 3 Start", 0x1d4, (
			#"4a0" Start of Cutscene
			BFMConnection(0x182450, 0x1053, 0x2, "4a1", "Soda Fountain Vambee Cutscene", connection_group = "Ignore", can_be_disconnected = False),
		), is_cutscene = True),
	0x304b: BFMConnectionData("Lower Mine Scrap Depository", 0x138, (
			BFMConnection(0x183e98, 0x3048, 0x1, "4b0", "Lower Mine Scrap Depository Entrance"),
		)),
	0x304c: BFMConnectionData("Restaurant Basement Outside Relic Keeper", 0x1d8, (
			BFMConnection(0x18629c, 0x302d, 0x1, "4c0", "Basement Extinguishing Flaming Pedestals South West"),
			BFMConnection(0x1862c0, 0x3042, 0x0, "4c1", "Basement Extinguishing Flaming Pedestals North East"),
		)),
	0x304d: BFMConnectionData("Grillin Reservoir Tunnel", 0x1d4, (
			BFMConnection(0x18842c, 0x304e, 0x1, "4d0", "Grillin Reservoir Tunnel West"),
			BFMConnection(0x188450, 0x3023, 0x0, "4d1", "Grillin Reservoir Tunnel Upper East Climb"),
		)),
	0x304e: BFMConnectionData("Grillin Reservoir", 0x1d4, (
			BFMConnection(0x18dcb4, 0x3043, 0x3, "4e0", "Grillin Reservoir Eastern Mine Exit"),
			BFMConnection(0x18dcd8, 0x304d, 0x0, "4e1", "Grillin Reservoir Submerged Tunnel"),
			BFMConnection(0x18dcfc, 0x1010, 0xe, "4e2", "Grillin Reservoir Climb Rope", connection_group = "Ignore"),
			BFMConnection(0x18dd2c, 0x1052, 0xe, "4e2", "Grillin Reservoir Climb Rope"),
			BFMConnection(0x18dd50, 0x1077, 0xe, "4e2", "Grillin Reservoir Climb Rope", connection_group = "Ignore"),
			BFMConnection(0x18dd74, 0x1094, 0xe, "4e2", "Grillin Reservoir Climb Rope", connection_group = "Ignore"),
		)),
	0x3050: BFMConnectionData("Lower Mine Ferris Wheel 2", 0x1d4, (
			BFMConnection(0x182ae8, 0x3045, 0x2, "500", "Lower Mine Ferris Wheel 2 West"),
			BFMConnection(0x182b0c, 0x3049, 0x0, "501", "Lower Mine Ferris Wheel 2 East"),
		)),
	0x3051: BFMConnectionData("Chapter 3 Church Vambee Fight", 0x1d4, (
			BFMConnection(0x185bdc, 0x1052, 0xc, "511", "Chapter 3 Church Survive Vambee Fight", can_be_disconnected = False),
		)),
	0x1052: BFMConnectionData("Chapter 3 Grillin Village", 0x1f0, (
			#"520" Conners again
			BFMConnection(0x18e6c0, 0x1053, 0x1, "521", "Village Ramp", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x18e6e4, 0x301c, 0x1, "522", "Village Path by Windmill", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x18e708, 0x3000, 0x0, "523", "Village Through Portcullis", other=0x6, connection_group = "Ignore"),
			BFMConnection(0x18e72c, 0x2056, 0x0, "524", "Village Bakery", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x18e750, 0x3014, 0x1, "525", "Village to Somnolent Forest", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x18e774, 0x3014, 0x0, "526", "Village to Deadend Somnolent Forest", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x18e798, 0x205b, 0x0, "527", "Village Restaurant", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x18e7bc, 0x2057, 0x0, "528", "Village Grocery", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x18e7e0, 0x2055, 0x0, "529", "Village Toy Shop", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x18e804, 0x2058, 0x0, "52a", "Village Inn", other=0x6, connection_group = "Ignore"),
			#BFMConnection(0x18d130, 0x3054, 0x0, "52a", "Died in Village"),
			BFMConnection(0x18e828, 0x2059, 0x0, "52b", "Village Conner", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x0, 0x0, 0x0, "52c", "Village Church Door", connection_group = "Ignore"),#"52c" Village Church Door
			#"52d" is Windmill door (unused)
			BFMConnection(0x18e8dc, 0x3051, 0x0, "52d", "Village Church Roof", other=0x2, can_be_disconnected = False),
			BFMConnection(0x18e894, 0x304e, 0x2, "52e", "Village Climb Down Well Rope"),
			BFMConnection(0x18e8b8, 0x3043, 0x0, "52f", "Village Lower Mine Door", other=0x2, connection_group = "Ignore"),
		)),
	0x1053: BFMConnectionData("Chapter 3 Upper Village", 0x1d4, (
			BFMConnection(0x187b74, 0x1052, 0x1, "531", "Upper Village Ramp", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x187b98, 0x3025, 0x0, "532", "Upper Village Mountain Pass", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x187bbc, 0x301e, 0x2, "533", "Upper Village Steam Pipe", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x187be0, 0x306b, 0x2, "534", "Upper Village Upper Open Vent", other=0x4, connection_group = "Ignore"),
			#"535" Gondola
			BFMConnection(0x187c04, 0x2057, 0x3, "536", "Upper Village Save Tim", other=0x2, connection_group = "Ignore"),
		)),
	0x3054: BFMConnectionData("Chapter 3 Nightmare", 0x1d4, (
			BFMConnection(0x181744, 0x1010, 0xa, "540", "Revive", connection_group = "Ignore"),
			BFMConnection(0x18178c, 0x1077, 0xa, "541", "Revive", connection_group = "Ignore"),
			BFMConnection(0x1817b0, 0x1094, 0xa, "542", "Revive", connection_group = "Ignore"),
			BFMConnection(0x182cbc, 0x1052, 0xa, "543", "Revive", connection_group = "Ignore"),
		)),
	0x2055: BFMConnectionData("Chapter 3 Toy Shop", -0x4b0, (
			BFMConnection(0x1e304c, 0x1052, 0x9, "550", "Toy Store Door", connection_group = "Ignore"),
		)),
	0x2056: BFMConnectionData("Chapter 3 Bakery", -0x4cc, (
			BFMConnection(0x1e30fc, 0x1052, 0x4, "560", "Bakery Door", connection_group = "Ignore"),
		)),
	0x2057: BFMConnectionData("Chapter 3 Grocery", -0x4b0, (
			BFMConnection(0x1e35c4, 0x1052, 0x8, "570", "Grocery Door", connection_group = "Ignore"),
		)),
	0x2058: BFMConnectionData("Chapter 3 Inn", -0x32c, (
			BFMConnection(0x1e6644, 0x1052, 0xa, "580", "Inn Door", connection_group = "Ignore"),
		)),
	0x2059: BFMConnectionData("Chapter 3 Conner", -0x4b0, (
			BFMConnection(0x1e3230, 0x1052, 0xb, "590", "Conner Door", connection_group = "Ignore"),
		)),
	0x205b: BFMConnectionData("Chapter 3 Restaurant", -0x4b0, (
			BFMConnection(0x1e334c, 0x1052, 0x7, "5b0", "Restaurant Door", connection_group = "Ignore"),
			BFMConnection(0x0d39cc, 0x3034, 0x0, "5b1", "Restaurant Hidden Exit Behind Counter", connection_group = "Ignore"),
		)),
	0x305c: BFMConnectionData("Frozen Palace Lobby", 0x1d4, (
			BFMConnection(0x186e2c, 0x3068, 0x1, "5c0", "Frozen Palace Lobby Main Entrance"),
			BFMConnection(0x186e50, 0x3063, 0x2, "5c1", "Frozen Palace Lobby Red Eye Door"),
			BFMConnection(0x186e74, 0x305d, 0x0, "5c2", "Frozen Palace Lobby North West Doorway"),
			BFMConnection(0x186e98, 0x305d, 0x1, "5c3", "Frozen Palace Lobby Left Balcony Door"),
			BFMConnection(0x186ebc, 0x3065, 0x0, "5c4", "Frozen Palace Lobby Frozen Three Eye Door"),
			BFMConnection(0x186ee0, 0x3061, 0x1, "5c5", "Frozen Palace Lobby Right Balcony Door"),
			BFMConnection(0x186f04, 0x305f, 0x0, "5c6", "Frozen Palace Lobby North East Doorway"),
			BFMConnection(0x186f28, 0x3061, 0x0, "5c7", "Frozen Palace Lobby East Doorway"),
			BFMConnection(0x0, 0x0, 0x0, "5c8", "Frozen Palace Lobby Painting"),#"5c8" Frozen Palace Lobby Painting
		)),
	0x305d: BFMConnectionData("Frozen Palace Blue Eye Door Hallway", 0x1b4, (
			BFMConnection(0x18c33c, 0x305c, 0x2, "5d0", "Blue Eye Door Hallway Lower South East"),
			BFMConnection(0x18c360, 0x305c, 0x3, "5d1", "Blue Eye Door Hallway Upper South East"),
			BFMConnection(0x18c384, 0x305e, 0x0, "5d2", "Blue Eye Door Hallway North East"),
			BFMConnection(0x18c3a8, 0x305d, 0x5, "5d3", "Blue Eye Door Hallway Blue Eye Door"),
			BFMConnection(0x18c3cc, 0x305d, 0x6, "5d4", "Blue Eye Door Hallway Upper North West"),
			BFMConnection(0x18c3f0, 0x305d, 0x3, "5d5", "Blue Eye Door Stairwell Blue Eye Door"),
			BFMConnection(0x18c414, 0x305d, 0x4, "5d6", "Blue Eye Door Stairwell Upper Level Doorway"),
		)),
	0x305e: BFMConnectionData("Frozen Palace Ice Block and Red Eye Room", 0x1d4, (
			BFMConnection(0x185b78, 0x305d, 0x2, "5e0", "Sliding Ice Block Room South West"),
			BFMConnection(0x185b9c, 0x305e, 0x3, "5e1", "Sliding Ice Block Room North East"),
			BFMConnection(0x185bc0, 0x305f, 0x2, "5e2", "Sliding Ice Block Room South East"),
			BFMConnection(0x185be4, 0x305e, 0x1, "5e3", "Red Eye Room Doorway"),
		)),
	0x305f: BFMConnectionData("Frozen Palace Wolf Room", 0x1d4, (
			BFMConnection(0x188244, 0x305c, 0x6, "5f0", "Wolf Room South"),
			BFMConnection(0x188268, 0x305f, 0x3, "5f1", "Wolf Room Infront of Crates North East"),
			BFMConnection(0x18828c, 0x305e, 0x2, "5f2", "Wolf Room Behind Crates North West"),
			BFMConnection(0x1882b0, 0x305f, 0x1, "5f3", "Penguin Room With Broken Stairs Lower South West"),
			BFMConnection(0x1882d4, 0x3060, 0x0, "5f4", "Penguin Room With Broken Stairs Green Eye Door (Inaccessible From Below)"),
		)),
	0x3060: BFMConnectionData("Frozen Palace Green Eye Maze and Green Eye Room", 0x1d4, (
			BFMConnection(0x18b71c, 0x305f, 0x4, "600", "Green Eye Maze Green Eye Door"),
			BFMConnection(0x18b740, 0x3061, 0x3, "601", "Green Eye Maze Middle Doorway South West"),
			BFMConnection(0x18b764, 0x3060, 0x3, "602", "Green Eye Maze Right Doorway South West"),
			BFMConnection(0x18b788, 0x3060, 0x2, "603", "Green Eye Room Doorway"),
		)),
	0x3061: BFMConnectionData("Frozen Palace Ramp Hallway", 0x1d4, (
			BFMConnection(0x1835c0, 0x305c, 0x7, "610", "Ramp Hallway Lower North West"),
			BFMConnection(0x1835e4, 0x305c, 0x5, "611", "Ramp Hallway Upper Balcony North West"),
			BFMConnection(0x183608, 0x3061, 0x4, "612", "Ramp Hallway Upper Balcony South West"),
			BFMConnection(0x18362c, 0x3060, 0x1, "613", "Ramp Hallway End of Ramps East"),
			BFMConnection(0x183650, 0x3061, 0x2, "614", "Frozen Palace Tiny Room with Mapper Flower North East"),
			BFMConnection(0x183674, 0x3064, 0x0, "615", "Frozen Palace Tiny Room with Mapper Flower North West"),
		)),
	0x3062: BFMConnectionData("Frozen Palace Blue Eye Maze and Blue Eye Room", 0x1d4, (
			BFMConnection(0x189710, 0x3064, 0x1, "620", "Blue Eye Maze South East"),
			BFMConnection(0x189734, 0x3062, 0x3, "621", "Blue Eye Maze North West"),
			BFMConnection(0x189758, 0x3063, 0x0, "622", "Blue Eye Maze North East"),
			BFMConnection(0x18977c, 0x3062, 0x1, "623", "Blue Eye Room Doorway"),
		)),
	0x3063: BFMConnectionData("Frozen Palace Red Eye Hallway to Blue Eye Maze", 0x1d4, (
			BFMConnection(0x188b80, 0x3062, 0x2, "630", "Slow Guy and Cool Plant Room With Broken Stairs Upper South East"),
			BFMConnection(0x188ba4, 0x3063, 0x3, "631", "Slow Guy and Cool Plant Room With Broken Stairs Lower North West"),
			BFMConnection(0x188bc8, 0x305c, 0x1, "632", "Red Eye Hallway North East"),
			BFMConnection(0x188bec, 0x3063, 0x1, "633", "Red Eye Hallway Near Fallen Pillars South East"),
		)),
	0x3064: BFMConnectionData("Frozen Palace Spike Bridge", 0x1d4, (
			BFMConnection(0x1824b0, 0x3061, 0x5, "640", "Spike Bridge East"),
			BFMConnection(0x1824d4, 0x3062, 0x0, "641", "Spike Bridge West"),
		)),
	0x3065: BFMConnectionData("Frozen Palace Ramp to Dragon Church", 0x1d4, (
			BFMConnection(0x182500, 0x305c, 0x4, "650", "Ramp to Dragon Church Three Eye Door Lower South West"),
			BFMConnection(0x182524, 0x3066, 0x0, "651", "Ramp to Dragon Church Top of Ramp North East"),
		)),
	0x3066: BFMConnectionData("Frozen Palace Dragon Church", 0x1d4, (
			BFMConnection(0x181b88, 0x3065, 0x1, "660", "Dragon Church West"),
			BFMConnection(0x181bac, 0x3067, 0x0, "661", "Dragon Church Trap Door"),
		)),
	0x3067: BFMConnectionData("Frost Dragon Arena", 0x1d8, (
			BFMConnection(0x0, 0x0, 0x0, "670", "Frost Dragon Arena Entrance"),#"670" Frost Dragon Arena Entrance
			BFMConnection(0x194270, 0x305c, 0x8, "671", "Defeat Frost Dragon"),
		)),
	0x3068: BFMConnectionData("Frozen Palace Courtyard", 0x1d4, (
			BFMConnection(0x181fec, 0x3014, 0x2, "680", "Frozen Palace Courtyard Return to Village", can_be_disconnected = False),
			BFMConnection(0x182010, 0x305c, 0x0, "681", "Frozen Palace Courtyard Enter Frozen Palace"),
			BFMConnection(0x182034, 0x30a6, 0x3, "682", "Frozen Palace Courtyard Return to Village after Defeating Frost Dragon", connection_group = "Ignore", can_be_disconnected = False),
		)),
	0x3069: BFMConnectionData("Chapter 4 Village on Fire", 0x1bc, (
			#"690" Enter Burning Village
			BFMConnection(0x1882cc, 0x1077, 0x11, "691", "Extinguish Village", other=0x4, can_be_disconnected = False),
		)),
	0x306a: BFMConnectionData("Cutscene Chapter 4 Start", 0x1d4, (
			#"6a0" Start Summon Kojiro Cutscene
			BFMConnection(0x183a0c, 0x1077, 0x7, "6a1", "Summon Kojiro Cutscene", connection_group = "Ignore"),
		), is_cutscene = True),
	0x306b: BFMConnectionData("Upper Mine Entrance", 0x1d4, (
			BFMConnection(0x181c8c, 0x3049, 0x1, "6b0", "Upper Mine Entrance West"),
			BFMConnection(0x181cb0, 0x306c, 0x0, "6b1", "Upper Mine Entrance Poison Covered Path East"),
			BFMConnection(0x181cd4, 0x1011, 0x4, "6b2", "Upper Mine Entrance Climb"),
			BFMConnection(0x181d04, 0x1053, 0x4, "6b2", "Upper Mine Entrance Climb", connection_group = "Ignore"),
			BFMConnection(0x181d28, 0x1078, 0x4, "6b2", "Upper Mine Entrance Climb", connection_group = "Ignore"),
			BFMConnection(0x181d4c, 0x1095, 0x4, "6b2", "Upper Mine Entrance Climb", connection_group = "Ignore"),
		)),
	0x306c: BFMConnectionData("Upper Mine Rock Slide Bridges", 0x138, (
			BFMConnection(0x1895ec, 0x306b, 0x1, "6c0", "Upper Mine Rock Slide Bridges West"),
			BFMConnection(0x189610, 0x306d, 0x0, "6c1", "Upper Mine Rock Slide Bridges East"),
		)),
	0x306d: BFMConnectionData("Upper Mine Poison Elevators", 0x1d4, (
			BFMConnection(0x18403c, 0x306c, 0x1, "6d0", "Upper Mine Poison Elevators Upper West"),
			BFMConnection(0x184060, 0x3072, 0x0, "6d1", "Upper Mine Poison Elevators Lower East"),
			BFMConnection(0x184084, 0x306e, 0x0, "6d2", "Upper Mine Poison Elevators Upper East"),
			BFMConnection(0x0, 0x0, 0x0, "6d3", "Upper Mine Poison Elevators Fall From Above"),#"6d3" Upper Mine Poison Elevators Fall From Above
		)),
	0x306e: BFMConnectionData("Upper Mine Windy Path", 0x148, (
			BFMConnection(0x186374, 0x306d, 0x2, "6e0", "Windy Path Wind West"),
			BFMConnection(0x186398, 0x306f, 0x0, "6e1", "Windy Path Top of Ramp East"),
		)),
	0x306f: BFMConnectionData("Upper Mine Large Fan", 0x1d4, (
			BFMConnection(0x185364, 0x306e, 0x1, "6f0", "Upper Mine Large Fan Lower West"),
			BFMConnection(0x185388, 0x3070, 0x0, "6f1", "Upper Mine Large Fan Near Switch Upper West"),
		)),
	0x3070: BFMConnectionData("Upper Mine Ant Parade", 0x1d4, (
			BFMConnection(0x185fc4, 0x306f, 0x1, "700", "Upper Mine Ant Parade East"),
			BFMConnection(0x185fe8, 0x3071, 0x0, "701", "Upper Mine Ant Parade West"),
		)),
	0x3071: BFMConnectionData("Upper Mine Dig Area Near KnightD", 0x1d4, (
			BFMConnection(0x182fe4, 0x3070, 0x1, "710", "Upper Mine Dig Area Near KnightD East"),
			BFMConnection(0x183008, 0x306d, 0x3, "711", "Upper Mine Dig Area Near KnightD Dig Down"),
		)),
	0x3072: BFMConnectionData("Upper Mine Gondola Station", 0x138, (
			BFMConnection(0x184448, 0x306d, 0x1, "720", "Upper Mine Gondola Station West"),
			BFMConnection(0x18446c, 0x3073, 0x0, "721", "Upper Mine Gondola Station Take the Lift"),
		)),
	0x3073: BFMConnectionData("Upper Mine Gondola Minigame", 0x1d4, (
			#"730" Start of Mine Gondola Minigame
			BFMConnection(0x1863c4, 0x3074, 0x0, "731", "Gondola Minigame End"),
		)),
	0x3074: BFMConnectionData("Upper Mine Above Queen Ant", 0x1d4, (
			#"740" Above Queen Ant Arrive on Lift
			BFMConnection(0x1824f8, 0x3075, 0x0, "741", "Upper Mine Above Queen Ant Dig Down"),
		)),
	0x3075: BFMConnectionData("Queen Ant Arena", 0x1d8, (
			BFMConnection(0x0, 0x0, 0x0, "750", "Queen Ant Arena Entrance"),#"750" Fall onto Queen Ant
			BFMConnection(0x19222c, 0x3014, 0x5, "751", "Defeat Queen Ant"),
		)),
	0x3076: BFMConnectionData("Cutscene Chapter 5 Start", 0x1d4, (
			#"760" Start Soda Fountain Storehouse Cutscene
			BFMConnection(0x181728, 0x1094, 0x2, "761", "Soda Fountain Storehouse Cutscene", connection_group = "Ignore"),
		), is_cutscene = True),
	0x1077: BFMConnectionData("Chapter 4 Grillin Village", 0x1f0, (
			#"770" Conners again
			BFMConnection(0x190db4, 0x1078, 0x1, "771", "Village Ramp", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x190dd8, 0x301c, 0x1, "772", "Village Path by Windmill", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x190dfc, 0x3000, 0x0, "773", "Village Through Portcullis", other=0x6, connection_group = "Ignore"),
			BFMConnection(0x190e20, 0x207b, 0x0, "774", "Village Bakery", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x190e44, 0x3014, 0x1, "775", "Village to Somnolent Forest", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x190e68, 0x3014, 0x0, "776", "Village to Deadend Somnolent Forest", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x190e8c, 0x2080, 0x0, "777", "Village Restaurant", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x190eb0, 0x207c, 0x0, "778", "Village Grocery", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x190ed4, 0x207a, 0x0, "779", "Village Toy Shop", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x190ef8, 0x207d, 0x0, "77a", "Village Inn", other=0x6, connection_group = "Ignore"),
			#BFMConnection(0x18f7b8, 0x3079, 0x0, "77a", "Died in Village"),
			BFMConnection(0x190f1c, 0x207e, 0x0, "77b", "Village Conner", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x190f40, 0x207f, 0x0, "77c", "Village Church Door", other=0x2, connection_group = "Ignore"),
			#"77d" is Windmill door (unused)
			BFMConnection(0x190fd0, 0x3051, 0x0, "77d", "Village Church Roof", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x190f88, 0x304e, 0x2, "77e", "Village Climb Down Well Rope", connection_group = "Ignore"),
			BFMConnection(0x190fac, 0x3043, 0x0, "77f", "Village Lower Mine Door", other=0x2, connection_group = "Ignore"),
		)),
	0x1078: BFMConnectionData("Chapter 4 Upper Village", 0x1d4, (
			BFMConnection(0x187140, 0x1077, 0x1, "781", "Upper Village Ramp", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x187164, 0x3025, 0x0, "782", "Upper Village Mountain Pass", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x187188, 0x301e, 0x2, "783", "Upper Village Steam Pipe", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x1871ac, 0x306b, 0x2, "784", "Upper Village Upper Open Vent", other=0x4, connection_group = "Ignore"),
		)),
	0x3079: BFMConnectionData("Chapter 4 Nightmare", 0x1d4, (
			BFMConnection(0x182cbc, 0x1077, 0xa, "790", "Revive", connection_group = "Ignore"),
		)),
	0x207a: BFMConnectionData("Chapter 4 Toy Shop", -0x338, (
			BFMConnection(0x1e85b4, 0x1077, 0x9, "7a0", "Toy Store Door", connection_group = "Ignore"),
		)),
	0x207b: BFMConnectionData("Chapter 4 Bakery", -0x354, (
			BFMConnection(0x1e8664, 0x1077, 0x4, "7b0", "Bakery Door", connection_group = "Ignore"),
		)),
	0x207c: BFMConnectionData("Chapter 4 Grocery", -0x338, (
			BFMConnection(0x1e8b2c, 0x1077, 0x8, "7c0", "Grocery Door", connection_group = "Ignore"),
		)),
	0x207d: BFMConnectionData("Chapter 4 Inn", -0x1b4, (
			BFMConnection(0x1ebbac, 0x1077, 0xa, "7d0", "Inn Door", connection_group = "Ignore"),
		)),
	0x207e: BFMConnectionData("Chapter 4 Conner", -0x338, (
			BFMConnection(0x1e8798, 0x1077, 0xb, "7e0", "Conner Door", connection_group = "Ignore"),
		)),
	0x207f: BFMConnectionData("Chapter 4 Church", -0x338, (
			BFMConnection(0x1e850c, 0x1077, 0xc, "7f0", "Church Door", connection_group = "Ignore"),
		)),
	0x2080: BFMConnectionData("Chapter 4 Restaurant", -0x338, (
			BFMConnection(0x1e8630, 0x1077, 0x7, "800", "Restaurant Door", connection_group = "Ignore"),
			BFMConnection(0xd39cc, 0x3034, 0x0, "801", "Restaurant Hidden Exit Behind Counter", connection_group = "Ignore"),
		)),
	0x3081: BFMConnectionData("Sky Island", 0x1d4, (
			#"810" Arrive at Sky Island
			BFMConnection(0x18bff0, 0x3093, 0x0, "811", "Free Sky Scroll"),
		)),
	0x3082: BFMConnectionData("Soda Fountain Electric Walls", 0x1d4, (
			#"820" Eletric Walls South
			BFMConnection(0x189270, 0x3083, 0x0, "821", "Electric Walls North"),
		)),
	0x3083: BFMConnectionData("Soda Fountain Tumble Dryer", 0x1d4, (
			#"830" Tumble Dryer South
			BFMConnection(0x18a520, 0x3090, 0x0, "831", "Tumble Dryer North"),
		)),
	0x3084: BFMConnectionData("Soda Fountain Calendar Maze Entrance", 0x1d4, (
			BFMConnection(0x0, 0x0, 0x0, "840", "Calendar Maze Start Lower Door Under Fan"),#"840" start of Calendar Maze lower door under Fan
			BFMConnection(0x183e60, 0x3084, 0xc, "841", "Calendar Maze Start Fake Fire Door (Under Fan)"), #door 1?
			BFMConnection(0x183e84, 0x3084, 0x6, "842", "Calendar Maze Start Earth Door"),
			BFMConnection(0x0, 0x0, 0x0, "843", "Calendar Maze Start Upper Door Left of Fan"),#"843" start of Calendar Maze upper door left of Fan
			BFMConnection(0x183ecc, 0x3087, 0x0, "844", "Calendar Maze Start Sky Door Near Fan Foreground"),
			BFMConnection(0x183ef0, 0x3084, 0xf, "845", "Calendar Maze Start Doorway at Wind Scroll Jump Background"),
			BFMConnection(0x183f14, 0x3084, 0x2, "846", "Calendar Maze Earth Scroll Puzzle Room Earth Door West Foreground"),
			BFMConnection(0x183f38, 0x3084, 0xa, "847", "Calendar Maze Earth Scroll Puzzle Room Fake Water Door Under Extendable Platform Foreground"), #door 7?
			BFMConnection(0x183f5c, 0x3084, 0xc, "848", "Calendar Maze Earth Scroll Puzzle Room Fake Wind Door Near 4X Button Background"), #door 8?
			BFMConnection(0x183f80, 0x3085, 0x0, "849", "Calendar Maze Earth Scroll Puzzle Room Sun Door Background"),
			BFMConnection(0x0, 0x0, 0x0, "84a", "Calendar Maze Reset Room (From a Foreground Door)"),#"84a" took wrong path from foreground door
			BFMConnection(0x0, 0x0, 0x0, "84c", "Calendar Maze Reset Room (From a Background Door)"),#"84c" took wrong path from background door, blank door -> (reset) -> fire door
			BFMConnection(0x0, 0x0, 0x0, "84d", "Calendar Maze Initial Reset Room (From Ben Fight)"),#"84d" start of maze from Ben Fight
			BFMConnection(0x184034, 0x3086, 0x5, "84e", "Calendar Maze Small Room Wind Scroll Door Background"),
			BFMConnection(0x184058, 0x3084, 0x5, "84f", "Calendar Maze Small Room Doorway To Wind Scroll Jump Foreground"),
			BFMConnection(0x183fec, 0x3084, 0x3, "8410", "Reset Fire Door (No Blank Door Along Back Wall)"), #door 0x10?
			BFMConnection(0x183fc8, 0x3084, 0x3, "8411", "Reset Fire Door (Blank Door Along Back Wall)"), #door 0x11?
			BFMConnection(0x184010, 0x3084, 0x0, "8412", "Initial Fire Door (After walking into reset wall)"), #door 0x12?
		)),
	0x3085: BFMConnectionData("Soda Fountain Calendar Maze Middle", 0x1d4, (
			BFMConnection(0x1825b8, 0x3084, 0x9, "850", "Calendar Maze Sky Scroll Over Spikes and Retracting Panel Sun Door Foreground"),
			BFMConnection(0x1825dc, 0x3084, 0xc, "851", "Calendar Maze Sky Scroll Over Spikes and Retracting Panel Fake Sky Door Background"), #door 1?
			BFMConnection(0x182600, 0x3085, 0x3, "852", "Calendar Maze Sky Scroll Over Spikes and Retracting Panel Backwards C with a Line Door Foreground"),
			BFMConnection(0x182624, 0x3085, 0x2, "853", "Calendar Maze Washing Pole Room Backwards C With a Line Door Background"),
			BFMConnection(0x182648, 0x3086, 0x0, "854", "Calendar Maze Washing Pole Room Fire Door Foreground"),
			BFMConnection(0x18266c, 0x3084, 0xc, "855", "Calendar Maze Washing Pole Room Backwards Fake Earth Door Background"),
		)),
	0x3086: BFMConnectionData("Soda Fountain Calendar Maze Torches", 0x1d4, (
			BFMConnection(0x183944, 0x3085, 0x4, "860", "Calendar Maze Torches and Smashing Block Fire Door Background"),
			BFMConnection(0x183968, 0x3086, 0x4, "861", "Calendar Maze Torches and Smashing Block Water Door Foreground"),
			BFMConnection(0x18398c, 0x3084, 0xc, "862", "Calendar Maze Torches and Smashing Block Fake Wind Door Background"),
			BFMConnection(0x1839b0, 0x3084, 0xa, "863", "Calendar Maze Torches and Smashing Block Fake Sun Door Foreground"),
			BFMConnection(0x1839d4, 0x3086, 0x1, "864", "Calendar Maze Extinguish Torches Water Door Background"),
			BFMConnection(0x1839f8, 0x3084, 0xe, "865", "Calendar Maze Extinguish Torches Wind Door Foreground"),
			BFMConnection(0x183a1c, 0x3084, 0xa, "866", "Calendar Maze Extinguish Torches Fake Backwards C With a Line Door Foreground"),
			BFMConnection(0x183a40, 0x3084, 0xc, "867", "Calendar Maze Extinguish Torches Fake Sky Door Background"),
		)),
	0x3087: BFMConnectionData("Soda Fountain Calendar Maze End", 0x1d4, (
			BFMConnection(0x18249C, 0x3084, 0x4, "870", "Calendar Maze End Sky Scroll Over Spikes and Descend Shafts Sky Scroll Door Background"),
			BFMConnection(0x1824c0, 0x3084, 0xa, "871", "Calendar Maze End Sky Scroll Over Spikes and Descend Shafts Fake Fire Door Foreground"), #upper left
			BFMConnection(0x1824e4, 0x3084, 0xc, "872", "Calendar Maze End Sky Scroll Over Spikes and Descend Shafts Fake Water Door Background"), #Lower Left
			BFMConnection(0x182508, 0x3088, 0x0, "873", "Calendar Maze End Sky Scroll Over Spikes and Descend Shafts Blank Door Background"),
		)),
	0x3088: BFMConnectionData("Soda Fountain Ed Fight", 0x1d8, (
			#"880" Ed Fight start
			BFMConnection(0x188904, 0x3089, 0x0, "881", "Defeat Ed"),
		)),
	0x3089: BFMConnectionData("Soda Fountain Garden", 0x1dc, (
			#"890" Garden start
			BFMConnection(0x19701c, 0x308a, 0x0, "891", "Garden 1 Upsidedown J Daytime North Gate"),
		)),
	0x308a: BFMConnectionData("Soda Fountain Garden 2 Hedge Maze", 0x1d4, (
			#"8a0" Garden start
			BFMConnection(0x188aa4, 0x3091, 0x0, "8a1", "Garden 2 Hedge Maze North"),
		)),
	0x308b: BFMConnectionData("Soda Fountain Factory Entrance", 0x1d4, (
			BFMConnection(0x0, 0x0, 0x0, "8b0", "Factory Entrance"),#"8b0" start of factory
			BFMConnection(0x190d28, 0x308b, 0x2, "8b1", "Factory Entrance Over Large Gap Past Gate North"),
			BFMConnection(0x0, 0x0, 0x0, "8b2", "Green Vats"),#"8b2" Green Vats
			BFMConnection(0x190d70, 0x308c, 0x0, "8b3", "Factory Green Vats and Servers Past Gate North"),
		)),
	0x308c: BFMConnectionData("Soda Fountain Factory Steam Knight Head", 0x1d4, (
			BFMConnection(0x0, 0x0, 0x0, "8c0", "Factory Steam Knight Head Entrance"),#"8c0" Steam Knight Head Entrance
			BFMConnection(0x193200, 0x308c, 0x2, "8c1", "Factory Steam Knight Head Top of Elevator Past Gate North"),
			BFMConnection(0x0, 0x0, 0x0, "8c2", "Factory Elevator Door"),#"8c2" Factory Elevator entrance
			BFMConnection(0x193248, 0x308d, 0x0, "8c3", "Factory Elevator Up Elevator"),
		)),
	0x308d: BFMConnectionData("Soda Fountain Topo Dance Battle", 0x1c4, (
			BFMConnection(0x0, 0x0, 0x0, "8d0", "Factory Elevator Topo Room"),#"8d0" Enter Topo Dance Battle
			BFMConnection(0x1886a4, 0x308d, 0x2, "8d1", "Defeat Topo"),
			BFMConnection(0x0, 0x0, 0x0, "8d2", "Topo Elevator Loot Room"),#"8d2" Loot Room After Topo
			BFMConnection(0x1886ec, 0x308e, 0x0, "8d3", "Loot Room After Topo North"),
		)),
	0x308e: BFMConnectionData("Soda Fountain Spiral to ToD", 0x1d4, (
			#"8e0" Enter Soda Fountain Spiral
			BFMConnection(0x1819e4, 0x308f, 0x0, "8e1", "Soda Fountain Spiral to ToD Upper Door", can_be_disconnected = False),
		)),
	0x308f: BFMConnectionData("Soda Fountain ToD", 0x0, (
			#"8f0" Enter ToD
			BFMConnection(0x18fffc, 0x309e, 0x0, "8f1", "Defeat ToD"),
		)),
	0x3090: BFMConnectionData("Soda Fountain Ben Fight", 0x178, (
			#"900" Start Ben FIght
			BFMConnection(0x1858c4, 0x3084, 0xd, "901", "Defeat Ben Blank Door"),
		)),
	0x3091: BFMConnectionData("Soda Fountain Garden 3 More Gates", 0x1dc, (
			#"910" Garden start
			BFMConnection(0x196d6c, 0x3092, 0x0, "911", "Garden 3 More Gates L Evening North Gate"),
		)),
	0x3092: BFMConnectionData("Soda Fountain Garden 4 Climb", 0x1dc, (
			#"920" Garden start
			BFMConnection(0x195290, 0x308b, 0x0, "921", "Garden 4 Climb Fountain Elevator"),
		)),
	0x3093: BFMConnectionData("Cutscene to Soda Fountain", 0x1b8, (
			#"930" Cutscene start
			BFMConnection(0x1857bc, 0x3082, 0x0, "931", "Hop Onto Soda Fountain"),
		), is_cutscene = True),
	0x1094: BFMConnectionData("Chapter 5-6 Grillin Village", 0x1f0, (
			BFMConnection(0x190d78, 0x1095, 0x1, "941", "Village Ramp", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x190d9c, 0x301c, 0x1, "942", "Village Path by Windmill", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x190dc0, 0x3000, 0x0, "943", "Village Through Portcullis", other=0x4, connection_group = "Ignore"),
			BFMConnection(0x190de4, 0x2098, 0x0, "944", "Village Bakery", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x190e08, 0x3014, 0x1, "945", "Village to Somnolent Forest", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x190e2c, 0x3014, 0x0, "946", "Village to Deadend Somnolent Forest", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x190e50, 0x209d, 0x0, "947", "Village Restaurant", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x190e74, 0x2099, 0x0, "948", "Village Grocery", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x190e98, 0x2097, 0x0, "949", "Village Toy Shop", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x190ebc, 0x209a, 0x0, "94a", "Village Inn", other=0x6, connection_group = "Ignore"),
			#BFMConnection(0x18f7a0, 0x3096, 0x0, "94a", "Died in Village"),
			BFMConnection(0x190ee0, 0x209b, 0x0, "94b", "Village Conner", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x190f04, 0x209c, 0x0, "94c", "Village Church Door", other=0x6, connection_group = "Ignore"),
			#"77d" is Windmill door (unused)
			BFMConnection(0x190f94, 0x3051, 0x0, "94d", "Village Church Roof", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x190f4c, 0x304e, 0x2, "94e", "Village Climb Down Well Rope", connection_group = "Ignore"),
			BFMConnection(0x190f70, 0x3043, 0x0, "94f", "Village Lower Mine Door", other=0x2, connection_group = "Ignore"),
		)),
	0x1095: BFMConnectionData("Chapter 5-6 Upper Village", 0x1d4, (
			BFMConnection(0x18a744, 0x1094, 0x1, "951", "Upper Village Ramp", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x18a768, 0x3025, 0x0, "952", "Upper Village Mountain Pass", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x18a78c, 0x301e, 0x2, "953", "Upper Village Steam Pipe", other=0x2, connection_group = "Ignore"),
			BFMConnection(0x18a7b0, 0x306b, 0x2, "954", "Upper Village Upper Open Vent", other=0x4, connection_group = "Ignore"),
			BFMConnection(0x18a7d4, 0x3004, 0x3, "955", "Upper Village Take Gondola", other=0x8),
			BFMConnection(0x0, 0x0, 0x0, "956", "Squish Ant"),
		)),
	0x3096: BFMConnectionData("Chapter 5-6 Nightmare", 0x1d4, (
			BFMConnection(0x181744, 0x1010, 0xa, "960", "Revive", connection_group = "Ignore"),
			BFMConnection(0x181768, 0x1052, 0xa, "960", "Revive", connection_group = "Ignore"),
			BFMConnection(0x18178c, 0x1077, 0xa, "960", "Revive", connection_group = "Ignore"),
			BFMConnection(0x182cbc, 0x1094, 0xa, "960", "Revive", connection_group = "Ignore"),
		)),
	0x2097: BFMConnectionData("Chapter 5-6 Toy Shop", -0x230, (
			BFMConnection(0x1ee444, 0x1094, 0x9, "970", "Toy Store Door", connection_group = "Ignore"),
		)),
	0x2098: BFMConnectionData("Chapter 5-6 Bakery", -0x24c, (
			BFMConnection(0x1ee4ec, 0x1094, 0x4, "980", "Bakery Door", connection_group = "Ignore"),
		)),
	0x2099: BFMConnectionData("Chapter 5-6 Grocery", -0x230, (
			BFMConnection(0x1ee9b4, 0x1094, 0x8, "990", "Grocery Door", connection_group = "Ignore"),
		)),
	0x209a: BFMConnectionData("Chapter 5-6 Inn", -0xac, (
			BFMConnection(0x1f1a34, 0x1094, 0xa, "9a0", "Inn Door", connection_group = "Ignore"),
		)),
	0x209b: BFMConnectionData("Chapter 5-6 Conner", -0x230, (
			BFMConnection(0x1ee620, 0x1094, 0xb, "9b0", "Conner Door", connection_group = "Ignore"),
		)),
	0x209c: BFMConnectionData("Chapter 5-6 Church", -0x230, (
			BFMConnection(0x1ee394, 0x1094, 0xc, "9c0", "Church Door", connection_group = "Ignore"),
		)),
	0x209d: BFMConnectionData("Chapter 5-6 Restaurant", -0x230, (
			BFMConnection(0x1ee4b8, 0x1094, 0x7, "9d0", "Restaurant Door", connection_group = "Ignore"),
			BFMConnection(0xd39cc, 0x3034, 0x0, "9d1", "Restaurant Hidden Exit Behind Counter", connection_group = "Ignore"),
		)),
	0x309e: BFMConnectionData("Soda Fountain Dark Lumina 1", 0x0, (
			#"9e0" Start DL1 Chase
			BFMConnection(0x18608c, 0x30a1, 0x0, "9e1", "Finish DL1 Chase"),
		)),
	0x309f: BFMConnectionData("Soda Fountain Dark Lumina 2 Climb", 0x0, (
			#"9f0" Start DL2 Climb
			BFMConnection(0x184f3c, 0x30a0, 0x0, "9f1", "Reach the Princess"),
		)),
	0x30a0: BFMConnectionData("Soda Fountain Dark Lumina 2-3 Fight", 0x0, (
			#"a00" Reach Lumina 2 Arena
			BFMConnection(0x18a27c, 0x30a4, 0x0, "a01", "Defeat DL3", can_be_disconnected = False),
		)),
	0x30a1: BFMConnectionData("Soda Fountain Dark Lumina 2 Transform", 0x0, (
			#"a10" Lumina 1 Absorbs Kojiro
			BFMConnection(0x18de1c, 0x309f, 0x0, "a11", "Lizard Arrives"),
		), is_cutscene = True),
	0x30a2: BFMConnectionData("Ending Cutscene at Castle and Credits", 0x0, (
			#"a20" Start Castle End Cutscene
			BFMConnection(0x186940, 0x30a5, 0x0, "a21", "Finish Credits", can_be_disconnected = False),
		), is_cutscene = True),
	0x30a4: BFMConnectionData("Ending Cinematic 1 (after killing DL3)", 0x0, (
			#"a40" Start DL3 Ending Cutscene
			BFMConnection(0x1817b4, 0x30a2, 0x0, "a41", "End Cinematic 1", can_be_disconnected = False),
		), is_cutscene = True),
	0x30a5: BFMConnectionData("Ending Cinematic 2 (Returning Lumina)", 0x0, (
			#"a50" Start Cutscene to Return Lumina
			#BFMConnection(0x1859d0, 0x30a5, 0x0, "a51", "SquareEnix Logo", connection_group = "Ignore", can_be_disconnected = False),
			BFMConnection(0x0, 0x0, 0x0, "a51", "SquareEnix Logo", can_be_disconnected = False),
		), is_cutscene = True),
	0x30a6: BFMConnectionData("Cutscene Outside Soda Fountain", 0x1bc, (
			#"a61" End of Chapter 2
			#"a62" End of Chapter 3
			#"a63" End of Chapter 4
			BFMConnection(0x182090, 0x304a, 0x0, "a64", "Zoom in on Castle to Chapter 3 Cutscene", connection_group = "Ignore", can_be_disconnected = False),
			BFMConnection(0x1820fc, 0x1053, 0x2, "a65", "Skip Cutscene to Chapter 3 Town", can_be_disconnected = False),
			BFMConnection(0x1820b4, 0x306a, 0x0, "a66", "Zoom in on Castle to Chapter 4 Cutscene", connection_group = "Ignore", can_be_disconnected = False),
			BFMConnection(0x182120, 0x1077, 0x7, "a67", "Skip Cutscene to Chapter 4 Town", connection_group = "Ignore", can_be_disconnected = False),
			BFMConnection(0x1820d8, 0x3076, 0x0, "a68", "Zoom in on Castle to Chapter 5 Cutscene", connection_group = "Ignore", can_be_disconnected = False),
			BFMConnection(0x182144, 0x1094, 0x2, "a69", "Skip Cutscene to Chapter 5 Town", connection_group = "Ignore", can_be_disconnected = False),
		), is_cutscene = True),

}


bfm_portals_short_to_door_names: dict[str, str] = {connection.short_name: connection.door_name for id, portal in bfm_portals.items() for connection in portal.connections} | {hex(id)[4:]: portal.region for id, portal in bfm_portals.items()}
bfm_portals_door_names_to_short: dict[str, str] = {v: k for k, v in bfm_portals_short_to_door_names.items()} #| {portal.region: hex(id)[4:] for id, portal in bfm_portals.items()}

bfm_portals_connection_info: dict[str, List[int]] = {(hex(connection.destination)[4:] + hex(connection.door)[2:]): [connection.destination & 0xff, connection.destination >> 8, connection.door, connection.other] for id, portal in bfm_portals.items() for connection in portal.connections} | {(hex(id)[4:]): [id & 0xff, id >> 8, 0, 0] for id, portal in bfm_portals.items()}
#ids_to_ignore_during_generation: tuple(int) = (0x)
bfm_portals_short_to_door_names_no_ignore: dict[str, str] = {connection.short_name: connection.door_name for id, portal in bfm_portals.items() for connection in portal.connections if (connection.connection_group != "Ignore" or "Village" in portal.region)} | {hex(id)[4:]: portal.region for id, portal in bfm_portals.items()}
del bfm_portals_short_to_door_names_no_ignore["040"]