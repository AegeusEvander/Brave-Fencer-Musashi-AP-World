from itertools import groupby
from typing import Dict, List, Set, NamedTuple, Optional
from BaseClasses import ItemClassification as IC


class BFMItemData(NamedTuple):
    classification: IC
    quantity_in_item_pool: int
    item_id_offset: int
    item_group: str = ""


item_base_id = 0x06dc00

item_table: Dict[str, BFMItemData] = {
    "Guard": BFMItemData(IC.progression, 1, 0x40, "NPC"),
    "Seer": BFMItemData(IC.progression, 1, 0x41, "NPC"),
    "Hawker": BFMItemData(IC.progression, 1, 0x42, "NPC"),
    "MusicianB": BFMItemData(IC.progression, 1, 0x43, "NPC"),
    "SoldierA": BFMItemData(IC.progression, 1, 0x44, "NPC"),
    "Acrobat": BFMItemData(IC.progression, 1, 0x51, "NPC"),
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

