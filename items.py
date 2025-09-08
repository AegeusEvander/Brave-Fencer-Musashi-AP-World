from itertools import groupby
from typing import Dict, List, Set, NamedTuple, Optional
from BaseClasses import ItemClassification as IC


class BFMItemData(NamedTuple):
    classification: IC
    quantity_in_item_pool: int
    item_id_offset: int
    item_group: str = ""


item_base_id = 0x0ba1b8
item_action_figure_id = 0x100
scroll_base_id = 0x200
core_base_id = 0x300

item_table: Dict[str, BFMItemData] = {
    "Guard": BFMItemData(IC.progression, 1, 0x40, "NPC"),
    "Seer": BFMItemData(IC.progression, 1, 0x41, "NPC"),
    "Hawker": BFMItemData(IC.progression, 1, 0x42, "NPC"),
    "Maid": BFMItemData(IC.progression, 1, 0x43, "NPC"),
    "MusicianB": BFMItemData(IC.progression, 1, 0x44, "NPC"),
    "SoldierA": BFMItemData(IC.progression, 1, 0x45, "NPC"),
    "MercenC": BFMItemData(IC.progression, 1, 0x46, "NPC"),
    "CarpentA": BFMItemData(IC.progression, 1, 0x47, "NPC"),
    "KnightB": BFMItemData(IC.progression, 1, 0x48, "NPC"),
    "Shepherd": BFMItemData(IC.progression, 1, 0x49, "NPC"),
    "Bailiff": BFMItemData(IC.progression, 1, 0x4a, "NPC"),
    "Taster": BFMItemData(IC.progression, 1, 0x4b, "NPC"),
    "CarpentB": BFMItemData(IC.progression, 1, 0x4c, "NPC"),
    "Weaver": BFMItemData(IC.progression, 1, 0x4d, "NPC"),
    "SoldierB": BFMItemData(IC.progression, 1, 0x4e, "NPC"),
    "KnightA": BFMItemData(IC.progression, 1, 0x4f, "NPC"),
    "CookA": BFMItemData(IC.progression, 1, 0x50, "NPC"),
    "Acrobat": BFMItemData(IC.progression, 1, 0x51, "NPC"),
    "MercenB": BFMItemData(IC.progression, 1, 0x52, "NPC"),
    "Janitor": BFMItemData(IC.progression, 1, 0x53, "NPC"),
    "Artisan": BFMItemData(IC.progression, 1, 0x54, "NPC"),
    "CarpentC": BFMItemData(IC.progression, 1, 0x55, "NPC"),
    "MusicianC": BFMItemData(IC.progression, 1, 0x56, "NPC"),
    "Knitter": BFMItemData(IC.progression, 1, 0x57, "NPC"),
    "Chef": BFMItemData(IC.progression, 1, 0x58, "NPC"),
    "MercenA": BFMItemData(IC.progression, 1, 0x59, "NPC"),
    "Chief": BFMItemData(IC.progression, 1, 0x5a, "NPC"),
    "CookB": BFMItemData(IC.progression, 1, 0x5b, "NPC"),
    "Conductor": BFMItemData(IC.progression, 1, 0x5c, "NPC"),
    "Butcher": BFMItemData(IC.progression, 1, 0x5d, "NPC"),
    "KnightC": BFMItemData(IC.progression, 1, 0x5e, "NPC"),
    "Doctor": BFMItemData(IC.progression, 1, 0x5f, "NPC"),
    "KnightD": BFMItemData(IC.progression, 1, 0x60, "NPC"),
    "Alchemist": BFMItemData(IC.progression, 1, 0x61, "NPC"),
    "Librarian": BFMItemData(IC.progression, 1, 0x62, "NPC"),
    "Longevity Berry": BFMItemData(IC.progression, 13, 0x63 + item_base_id, "Stat Up"),
    "Rock": BFMItemData(IC.useful, 1, 0x13, "Chest Reward"),
    "Old Sword": BFMItemData(IC.filler, 1, 0x15, "Chest Reward"),
    "Shield": BFMItemData(IC.filler, 1, 0x17, "Chest Reward"),
    "Old Book": BFMItemData(IC.filler, 1, 0x19, "Chest Reward"),
    "Aged Coin": BFMItemData(IC.filler, 1, 0x1b, "Chest Reward"),
    "Old Crown": BFMItemData(IC.filler, 1, 0x1d, "Chest Reward"),
    "Old Pipe": BFMItemData(IC.filler, 1, 0x1f, "Chest Reward"),
    "Odd Hat": BFMItemData(IC.filler, 1, 0x21, "Chest Reward"),
    "Dagger": BFMItemData(IC.filler, 1, 0x23, "Chest Reward"),
    "Powder": BFMItemData(IC.filler, 1, 0x25, "Chest Reward"),
    "Cloth": BFMItemData(IC.useful, 1, 0x27, "Chest Reward"),
    "Helmet": BFMItemData(IC.filler, 1, 0x29, "Chest Reward"),
    "Used Boot": BFMItemData(IC.filler, 1, 0x2b, "Chest Reward"),
    "Old Glove": BFMItemData(IC.filler, 1, 0x2d, "Chest Reward"),
    "Armor": BFMItemData(IC.filler, 1, 0x2f, "Chest Reward"),
    "Long Tube": BFMItemData(IC.useful, 1, 0x31, "Chest Reward"),
    "Red Cloth": BFMItemData(IC.filler, 1, 0x33, "Chest Reward"),
    "White Cloth": BFMItemData(IC.filler, 1, 0x35, "Chest Reward"),
    "Black Cloth": BFMItemData(IC.filler, 1, 0x37, "Chest Reward"),
    "Large Tool": BFMItemData(IC.filler, 1, 0x39, "Chest Reward"),
    "Odd Bone": BFMItemData(IC.filler, 1, 0x3b, "Chest Reward"),
    "Bracelet": BFMItemData(IC.progression, 1, 0x49, "Chest Reward"),
    "Old Shirt": BFMItemData(IC.useful, 1, 0x4a, "Chest Reward"),
    "Red Shoes": BFMItemData(IC.progression, 1, 0x4b, "Chest Reward"),
    "Red Eye": BFMItemData(IC.progression, 1, 0x60, "Chest Reward"),
    "Blue Eye": BFMItemData(IC.progression, 1, 0x61, "Chest Reward"),
    "Green Eye": BFMItemData(IC.progression, 1, 0x62, "Chest Reward"),
    "1000 Drans": BFMItemData(IC.filler, 0, 0x78, "Chest Reward"), # moving 6 to 0 to allow for dynamic filler levels
    "Lumina": BFMItemData(IC.progression | IC.useful, 1, 0x79, "Equipment"),
    "Progressive Bread": BFMItemData(IC.progression, 7, 0x80, "Bakery"),
    "Juice": BFMItemData(IC.filler, 1, 0x71, "Restaurant"),
    "Pea Soup": BFMItemData(IC.filler, 1, 0x72, "Restaurant"),
    "Cake": BFMItemData(IC.filler, 1, 0x73, "Restaurant"),
    "Gravy": BFMItemData(IC.filler, 1, 0x74, "Restaurant"),
    "Salad": BFMItemData(IC.filler, 1, 0x75, "Restaurant"),
    "Lasagna": BFMItemData(IC.filler, 1, 0x76, "Restaurant"),
    "Pork Chop": BFMItemData(IC.filler, 1, 0x77, "Restaurant"),
    "Rice Ball": BFMItemData(IC.filler, 1, 0x01, "Grocery"),
    "Gel": BFMItemData(IC.filler, 1, 0x04, "Grocery"),
    "W-Gel": BFMItemData(IC.progression, 1, 0x05, "Grocery"),
    "Progressive Drink": BFMItemData(IC.progression, 2, 0x06, "Grocery"),
    #"EX-Drink": BFMItemData(IC.useful, 1, 0x07, "Grocery"),
    "Progressive Mint": BFMItemData(IC.useful, 2, 0x08, "Grocery"),
    "Antidote": BFMItemData(IC.useful, 1, 0x09, "Grocery"),
    "S-Revive": BFMItemData(IC.useful, 1, 0x0a, "Grocery"),
    "Orange": BFMItemData(IC.progression, 1, 0x0b, "Grocery"),
    "Neatball": BFMItemData(IC.useful, 1, 0x6a, "Grocery"),
    "Cheese": BFMItemData(IC.useful, 1, 0x6b, "Grocery"),
    #"H-Mint": BFMItemData(IC.useful, 1, 0x6d, "Grocery"),
    "Musashi Action Figure": BFMItemData(IC.filler, 1, 0x0 + item_action_figure_id, "Toy Shop"),
    "Bee Plant": BFMItemData(IC.filler, 1, 0x1 + item_action_figure_id, "Toy Shop"),
    "Soldier1": BFMItemData(IC.filler, 1, 0x2 + item_action_figure_id, "Toy Shop"),
    "Soldier2": BFMItemData(IC.filler, 1, 0x3 + item_action_figure_id, "Toy Shop"),
    "Rootrick": BFMItemData(IC.filler, 1, 0x4 + item_action_figure_id, "Toy Shop"),
    "Steam Knight": BFMItemData(IC.filler, 1, 0x5 + item_action_figure_id, "Toy Shop"),
    "Soldier3": BFMItemData(IC.filler, 1, 0x6 + item_action_figure_id, "Toy Shop"),
    "Herb Plant": BFMItemData(IC.filler, 1, 0x7 + item_action_figure_id, "Toy Shop"),
    "Killer Man Eater": BFMItemData(IC.filler, 1, 0x8 + item_action_figure_id, "Toy Shop"),
    "Magician": BFMItemData(IC.filler, 1, 0x9 + item_action_figure_id, "Toy Shop"),
    "Sleepie": BFMItemData(IC.filler, 1, 0xa + item_action_figure_id, "Toy Shop"),
    "Skullpion": BFMItemData(IC.filler, 1, 0xb + item_action_figure_id, "Toy Shop"),
    "Relic Vambee": BFMItemData(IC.filler, 1, 0xc + item_action_figure_id, "Toy Shop"),
    "Vambee Soldier": BFMItemData(IC.filler, 1, 0xd + item_action_figure_id, "Toy Shop"),
    "Bowler": BFMItemData(IC.filler, 1, 0xe + item_action_figure_id, "Toy Shop"),
    "Cure Worm": BFMItemData(IC.filler, 1, 0xf + item_action_figure_id, "Toy Shop"),
    "Bubbles": BFMItemData(IC.filler, 1, 0x10 + item_action_figure_id, "Toy Shop"),
    "Relic Keeper": BFMItemData(IC.filler, 1, 0x11 + item_action_figure_id, "Toy Shop"),
    "Penguin": BFMItemData(IC.filler, 1, 0x12 + item_action_figure_id, "Toy Shop"),
    "Haya Wolf": BFMItemData(IC.filler, 1, 0x13 + item_action_figure_id, "Toy Shop"),
    "Slow Guy": BFMItemData(IC.filler, 1, 0x14 + item_action_figure_id, "Toy Shop"),
    "Steel Golem": BFMItemData(IC.filler, 1, 0x15 + item_action_figure_id, "Toy Shop"),
    "Gingerelle": BFMItemData(IC.filler, 1, 0x16 + item_action_figure_id, "Toy Shop"),
    "Frost Dragon": BFMItemData(IC.filler, 1, 0x17 + item_action_figure_id, "Toy Shop"),
    "GiAnt": BFMItemData(IC.filler, 1, 0x18 + item_action_figure_id, "Toy Shop"),
    "Toad Stool": BFMItemData(IC.filler, 1, 0x19 + item_action_figure_id, "Toy Shop"),
    "Ed & Ben": BFMItemData(IC.filler, 1, 0x1a + item_action_figure_id, "Toy Shop"),
    "Topo": BFMItemData(IC.filler, 1, 0x1b + item_action_figure_id, "Toy Shop"),
    "Colonel Capricola": BFMItemData(IC.filler, 1, 0x1c + item_action_figure_id, "Toy Shop"),
    "Queen Ant": BFMItemData(IC.filler, 1, 0x1d + item_action_figure_id, "Toy Shop"),
    "Improved Fusion": BFMItemData(IC.useful, 1, 0x81, "Tech"),
    "Dashing Pierce": BFMItemData(IC.useful, 1, 0x82, "Tech"),
    "Shish Kebab": BFMItemData(IC.useful, 1, 0x83, "Tech"),
    "Crosswise Cut": BFMItemData(IC.progression, 1, 0x84, "Tech"),
    "Tenderize": BFMItemData(IC.useful, 1, 0x85, "Tech"),
    "Desperado Attack": BFMItemData(IC.useful, 1, 0x86, "Tech"),
    "Rumparoni Special": BFMItemData(IC.useful, 1, 0x87, "Tech"),
    "Earth Scroll": BFMItemData(IC.progression | IC.useful, 1, 0x16 + scroll_base_id, "Scroll"),
    "Water Scroll": BFMItemData(IC.progression | IC.useful, 1, 0x17 + scroll_base_id, "Scroll"),
    "Fire Scroll": BFMItemData(IC.progression | IC.useful, 1, 0x18 + scroll_base_id, "Scroll"),
    "Wind Scroll": BFMItemData(IC.progression | IC.useful, 1, 0x19 + scroll_base_id, "Scroll"),
    "Sky Scroll": BFMItemData(IC.progression | IC.useful, 1, 0x1a + scroll_base_id, "Scroll"),
    "Earth Boss Core": BFMItemData(IC.progression, 1, 0x8a + scroll_base_id, "Core"),
    "Water Boss Core": BFMItemData(IC.progression, 1, 0x8b + scroll_base_id, "Core"),
    "Fire Boss Core": BFMItemData(IC.progression, 1, 0x8c + scroll_base_id, "Core"),
    "Wind Boss Core": BFMItemData(IC.progression, 1, 0x8d + scroll_base_id, "Core"),
}

# items we'll want the location of in slot data, for generating in-game hints
slot_data_item_names = [
    "Guard",
    "Seer",
    "Hawker",
    "MusicianB",
    "SoldierA",
    "Acrobat",
]

item_name_to_id: Dict[str, int] = {name: item_base_id * (data.item_group == "NPC") + data.item_id_offset for name, data in item_table.items()}

item_id_to_name: Dict[int, str] = {(item_base_id * (data.item_group == "NPC") + data.item_id_offset): name for name, data in item_table.items()}

filler_items: List[str] = [name for name, data in item_table.items() if data.classification == IC.filler and name != "Grass"]

npc_ids: List[int] = [item_base_id + data.item_id_offset for name, data in item_table.items() if data.item_group == "NPC"]

def get_item_group(item_name: str) -> str:
    return item_table[item_name].item_group


item_name_groups: Dict[str, Set[str]] = {
    group: set(item_names) for group, item_names in groupby(sorted(item_table, key=get_item_group), get_item_group) if group != ""
}

