from itertools import groupby
from typing import Dict, List, Set, NamedTuple, Optional
from BaseClasses import ItemClassification as IC


class BFMItemData(NamedTuple):
    classification: IC
    quantity_in_item_pool: int
    item_id_offset: int
    item_group: str = ""


item_base_id = 0x0ba1b8

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
    "Longevity Berry": BFMItemData(IC.useful, 13, 0x63 + item_base_id, "Stat Up"),
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
    "1000 Drans": BFMItemData(IC.filler, 6, 0x78, "Chest Reward"),
    "Lumina": BFMItemData(IC.progression, 1, 0x79, "Equipment"),
    "Progressive Bread": BFMItemData(IC.progression, 7, 0x80, "Bakery"),
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

