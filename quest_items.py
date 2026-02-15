from typing import Dict, NamedTuple, Set, Optional, List, ClassVar

MAIN_RAM: str = "MainRAM"

quest_item_locations=[[
    (0x078e80, 2, MAIN_RAM), #16 Progression State
    (0x0ae659, 24, MAIN_RAM),#17 Assorted Event Flags
    (0x0ba1c2, 2, MAIN_RAM), #18 Bell Status
    (0x0ba1e7, 12, MAIN_RAM),#19 Inventory
    (0x0ba228, 1, MAIN_RAM), #20 Vambee Solider Toy
    (0x0ba236, 1, MAIN_RAM), #21 Topo Toy (same time as profits)
    (0x0ba28a, 4, MAIN_RAM), #22 Tree Status
    (0x0ba296, 1, MAIN_RAM), #23 Gondola Gizmo Status
    (0x0ba316, 2, MAIN_RAM)  #24 Wid Status
],[
    (0x077fe0, 2, MAIN_RAM), #Progression State
    (0x0ad7b9, 24, MAIN_RAM),#Assorted Event Flags
    (0x0b9322, 2, MAIN_RAM), #Bell Status
    (0x0b9347, 12, MAIN_RAM),#Inventory
    (0x0b9388, 1, MAIN_RAM), #Vambee Solider Toy
    (0x0b93e5, 1, MAIN_RAM), #Steam Status/Steamwood completion
    (0x0b93ea, 4, MAIN_RAM), #Tree Status
    (0x0b93f6, 1, MAIN_RAM), #Gondola Gizmo Status
    (0x0b9476, 2, MAIN_RAM)  #Wid Status
]]

well_water_id = {
    0x1010: 0x1913e8, 
    0x1077: 0x1e06bc,
    0x1094: 0x1e697c, 
}