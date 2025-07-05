from typing import Dict, NamedTuple, Set, Optional, List

bakery_locations: List[int] = [
    0x2015, #Chapter 2
    0x2056, #Chapter 3
    0x207b, #Chapter 4
    0x2098  #Chapter 5 and 6
]

class StoreData(NamedTuple):
    inventory_id: int
    inventory_pointer_upper_pointer: int
    inventory_pointer_upper: List[int]
    inventory_pointer_lower_pointer: int
    inventory_pointer_lower: List[int]
    inventory_length_id: int
    inventory_length_id_expanded: Optional[int] = None

store_table: Dict[int, StoreData] = {
    0x2015: StoreData(0x1fab10, 0x189ab4, [0x20, 0x80], 0x189ab8, [0x10, 0xab], 0x189aa0, inventory_length_id_expanded = 0x189ab0),
    0x2056: StoreData(0x1fab10, 0x18671c, [0x20, 0x80], 0x186720, [0x10, 0xab], 0x186718, inventory_length_id_expanded = 0x186708),
    0x207b: StoreData(0x1fab10, 0x186ff4, [0x20, 0x80], 0x186ff8, [0x10, 0xab], 0x186fe0, inventory_length_id_expanded = 0x186ff0),
    0x2098: StoreData(0x1fab10, 0x186cf4, [0x20, 0x80], 0x186cf8, [0x10, 0xab], 0x186cf0, inventory_length_id_expanded = 0x186ce0),
}
