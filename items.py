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
    "CarpentB": BFMItemData(IC.progression, 1, 0x4c, "NPC"),
    "Weaver": BFMItemData(IC.progression, 1, 0x4d, "NPC"),
    "SoldierB": BFMItemData(IC.progression, 1, 0x4e, "NPC"),
    "KnightA": BFMItemData(IC.progression, 1, 0x4f, "NPC"),
    "CookA": BFMItemData(IC.progression, 1, 0x50, "NPC"),
    "Acrobat": BFMItemData(IC.progression, 1, 0x51, "NPC"),
    "MercenB": BFMItemData(IC.progression, 1, 0x52, "NPC"),
    "CarpentC": BFMItemData(IC.progression, 1, 0x55, "NPC"),
    "Knitter": BFMItemData(IC.progression, 1, 0x57, "NPC"),
    "MercenA": BFMItemData(IC.progression, 1, 0x59, "NPC"),
    "Chief": BFMItemData(IC.progression, 1, 0x5a, "NPC"),
    "KnightC": BFMItemData(IC.progression, 1, 0x5e, "NPC"),
    "Doctor": BFMItemData(IC.progression, 1, 0x5f, "NPC"),
    "Librarian": BFMItemData(IC.progression, 1, 0x62, "NPC"),
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

item_name_to_id: Dict[str, int] = {name: item_base_id + data.item_id_offset for name, data in item_table.items()}

filler_items: List[str] = [name for name, data in item_table.items() if data.classification == IC.filler and name != "Grass"]


def get_item_group(item_name: str) -> str:
    return item_table[item_name].item_group


item_name_groups: Dict[str, Set[str]] = {
    group: set(item_names) for group, item_names in groupby(sorted(item_table, key=get_item_group), get_item_group) if group != ""
}

