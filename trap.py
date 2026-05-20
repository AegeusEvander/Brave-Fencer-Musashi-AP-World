from typing import Dict, NamedTuple, Set, Optional, List

trap_weight: Dict[str, int] = {
    "Activate Ability Trap": 50, #queue
    #"Activate Scroll Trap": 50, #queue
    "Bald Trap": 10, #instant 0x0afb0c 0x5800 no upper top hair no torso no legs
    "Camera Manipulation Trap": 50, #short queue
    "Depression Trap": 50, #queue
    #"Disarm Trap": 50, #instant 0x0afb0c 0x5300 no bracelet no sheath
    #"Dismember Trap": 50, #instant 0x0afb0c 0x1108 crashes game when assimilating
    "Sinking Trap": 50, #queue other
    "Ghost Trap": 50, #queue
    "Instant Death Trap": 0, #instant
    "Jump Trap": 0, #queue
    "Pea Soup Trap": 50, #queue
    "Poison Trap": 50, #queue
    "Random Ability Trap": 50, #queue
    "Sleepy Trap": 50, #queue
    "Stinky Trap": 50, #queue
    "Toxin Trap": 50, #queue
    "Use S-Revive Trap": 20, #queue
}

"""
To add
mini
giant 
wide
disable weapon
Ice
money loss?
set on fire
shock
time skip
rot
"""
trap_conversion: Dict[str, str] = {
    "Bee Trap": "Stinky Trap",
    "Camera Rotate Trap": "Camera Manipulation Trap",
    "Damage Trap": "Sinking Trap",
    "Depletion Trap": "Use S-Revive Trap",
    "Egg Trap": "Pea Soup Trap",
    "Gadget Shuffle Trap": "Random Ability Trap",
    "Ghost": "Ghost Trap",
    "Poison Mushroom": "Toxin Trap",
    "Posession Trap": "Ghost Trap",
    "Random Status Trap": "Random Ability Trap",
    "Sleep Trap": "Sleepy Trap",
    "Slow Trap": "Depression Trap",
    "Slowness Trap": "Depression Trap",
    "Spooky Time": "Ghost Trap",
    "Underwater Trap": "Sinking Trap",
    "Whirlpool Trap": "Sinking Trap",
    "Zoom In Trap": "Camera Manipulation Trap",
    "Zoom Out Trap": "Camera Manipulation Trap",
    "Zoom Trap": "Camera Manipulation Trap",
}

trap_send_conversion: Dict[str, str] = {
    "Camera Manipulation Trap": "Camera Rotate Trap",
    "Sleepy Trap": "Sleep Trap",
}

regions_with_water: List[int] = [
    0x3008, #starting forest
    0x1010, #chapter 2 town
    0x3014, #somnolent forest
    0x3021, #island of dragons
    0x3025, #Twinpeak entrance
    0x3026, #twinpeak around the bend
    0x3027, #twinpeak cave 1
    0x3028, #twinpeak rope bridge
    0x3029, #twinpeak second peak
    #0x302a, #raft minigame
    0x302c, #twinpeak waterfall cave
    #0x3040, #basement moat
    0x3047, #Misteria underground lake
    0x304e, #grillin reservoir
    0x1052, #chapter 3 town
    #0x3069, chapter 4 on fire
    0x1077, #chapter 4 town
    0x3081, #sky island
    0x1094, #chapter 5 town
    0x3082, #electric wall rooms
    #0x3086, calendar maze only some rooms
]


trap_names_long_queue: List[str] = [
    "Activate Ability Trap",
    "Activate Scroll Trap",
    "Depression Trap",
    "Ghost Trap",
    "Jump Trap",
    "Poison Trap",
    "Random Ability Trap",
    "Sleepy Trap",
    "Stinky Trap",
    "Toxin Trap",
]

trap_names_short_queue: List[str] = [
    "Camera Manipulation Trap",
    "Pea Soup Trap",
    "Use S-Revive Trap",
]

assimilation_value: Dict[str, int] = {
    "Depression Trap": 0x1,
    "Ghost Trap": 0x18,
    "Sleepy Trap": 0x11,
    "Stinky Trap": 0x15,
    "Toxin Trap": 0x13,
}

item_swap_whitelist: Set[int] = {
    0x0,
    0x1,
    0x2,
    0x3,
    0x4,
    0x5,
    0x6,
    0x7,
    0x8,
    0x9,
    0xa,
    0xb,
    0xc,
    0xd,
    0xe,
    0xf,
    0x10,
    0x11,
    0x12,
    0x4c,
    0x53,
    0x54,
    0x55,
    0x68,
    0x69,
    0x6a,
    0x6d,
}


regions_indoors: Set[int] = {
    0x3000, 
    0x3001,
    0x3002,
    0x3003,
    0x3004,
    0x300b,
    0x300e,
    0x2013,
    0x2015,
    0x2016,
    0x2017,
    0x2018,
    0x2019,
    0x201a,
    0x301d,
    0x3020,
    0x302a,
    0x2055,
    0x2056,
    0x2057,
    0x2058,
    0x2059,
    0x205b,
    0x3073,
    0x207a,
    0x207b,
    0x207c,
    0x207d,
    0x207e,
    0x207f,
    0x2080,
    0x2097,
    0x2098,
    0x2099,
    0x209a,
    0x209b,
    0x209c,
    0x209d,
}