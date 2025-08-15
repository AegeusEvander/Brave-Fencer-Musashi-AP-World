from typing import Dict, TYPE_CHECKING

from worlds.generic.Rules import set_rule, forbid_item, add_rule
from BaseClasses import CollectionState
from .locations import location_name_groups
if TYPE_CHECKING:
    from . import BFMWorld


def can_fight_skullpion(state: CollectionState, world: "BFMWorld") -> bool:
    return state.has_all({"SoldierA", "MercenC", "CarpentA", "KnightB", "Bracelet"}, world.player) and has_lumina(state, world) and has_earth_scroll(state, world)

def can_fight_frost_dragon(state: CollectionState, world: "BFMWorld") -> bool:
    return state.has_all({"Red Eye", "Blue Eye", "Green Eye", "Red Shoes"}, world.player) and has_fire_scroll(state, world)

def can_enter_frozen_palace(state: CollectionState, world: "BFMWorld") -> bool:
    return state.has_all({"MercenA", "MercenB", "MercenC"}, world.player)

def can_identify_gondola_gizmo(state: CollectionState, world: "BFMWorld") -> bool:
    return state.has_all({"CarpentA", "CarpentB", "CarpentC"}, world.player) and has_water_scroll(state, world)

def saved_everyone(state: CollectionState, world: "BFMWorld") -> bool:
    return state.has_all({"Guard", "Seer", "Hawker", "Maid", "MusicianB", "SoldierA", "MercenC", "CarpentA", "KnightB", "Shepherd", "Bailiff", "Taster", "CarpentB", "Weaver", "SoldierB", "KnightA", "CookA", "Acrobat", "MercenB", "Janitor", "Artisan", "CarpentC", "MusicianC", "Knitter", "Chef", "MercenA", "Chief", "CookB", "Conductor", "Butcher", "KnightC", "Doctor", "KnightD", "Alchemist", "Librarian"}, world.player)

def has_lumina(state: CollectionState, world: "BFMWorld") -> bool:
    return (not world.options.lumina_randomzied) or state.has("Lumina", world.player)

def has_rice(state: CollectionState, world: "BFMWorld") -> bool:
    return state.has_all({"Bailiff", "CookA"}, world.player)

def has_orange(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.grocery_sanity.value == True):
        return state.has("Orange", world.player) and can_fight_skullpion(state, world)
    else:
        return can_fight_skullpion(state, world)

def has_bread(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.bakery_sanity.value == True):
        return state.has("Progressive Bread", world.player) 
    return True

def has_earth_scroll(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.scroll_sanity.value == True):
        return state.has("Earth Scroll", world.player)
    else:
        return state.has("Bracelet", world.player) and has_lumina(state, world)

def has_water_scroll(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.scroll_sanity.value == True):
        return state.has("Water Scroll", world.player)
    else:
        return can_fight_skullpion(state, world)

def has_fire_scroll(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.scroll_sanity.value == True):
        return state.has("Fire Scroll", world.player)
    else:
        return can_identify_gondola_gizmo(state, world) and can_fight_skullpion(state, world)

def has_wind_scroll(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.scroll_sanity.value == True):
        return state.has("Wind Scroll", world.player)
    else:
        return can_enter_frozen_palace(state, world) and can_identify_gondola_gizmo(state, world) and can_fight_skullpion(state, world) and can_fight_frost_dragon(state, world)

def has_sky_scroll(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.scroll_sanity.value == True):
        if(world.options.sky_scroll_logic.value == 1):
            return False
        return state.has("Sky Scroll", world.player)
    else:
        return False

def has_sky_scroll_complex(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.scroll_sanity.value == True):
        if(world.options.sky_scroll_logic.value != 3):
            return False
        return state.has("Sky Scroll", world.player)
    else:
        return False

def has_wind_crest(state: CollectionState, world: "BFMWorld") -> bool:
    return can_enter_frozen_palace(state, world) and can_identify_gondola_gizmo(state, world) and can_fight_skullpion(state, world) and can_fight_frost_dragon(state, world) and has_wind_scroll(state,world)

def set_region_rules(world: "BFMWorld") -> None:
    player = world.player
    options = world.options

    world.get_entrance("Grillin Village -> Mine Entrance").access_rule = \
        lambda state: can_fight_skullpion(state, world)
    world.get_entrance("Grillin Village -> Restaurant Basement").access_rule = \
        lambda state: can_fight_skullpion(state, world)
    if(options.toy_sanity.value == True):
        world.get_entrance("Toy Shop Series 1 -> Toy Shop Series 3").access_rule = \
            lambda state: can_fight_skullpion(state, world)
        world.get_entrance("Toy Shop Series 1 -> Toy Shop Series 4").access_rule = \
            lambda state: can_enter_frozen_palace(state, world) and can_identify_gondola_gizmo(state, world) and can_fight_skullpion(state, world)
        world.get_entrance("Toy Shop Series 1 -> Toy Shop Series 5").access_rule = \
            lambda state: can_enter_frozen_palace(state, world) and can_identify_gondola_gizmo(state, world) and can_fight_skullpion(state, world) and can_fight_frost_dragon(state, world)
    world.get_entrance("Twinpeak Entrance -> Twinpeak Path to Skullpion").access_rule = \
        lambda state: has_earth_scroll(state, world) or has_sky_scroll(state, world)
    world.get_entrance("Twinpeak Entrance -> Twinpeak Around the Bend").access_rule = \
        lambda state: has_bread(state,world) or state.has("Bracelet", player) or has_water_scroll(state, world) or has_sky_scroll(state, world)
    world.get_entrance("Twinpeak Path to Skullpion -> Skullpion Arena").access_rule = \
        lambda state: can_fight_skullpion(state, world)
    world.get_entrance("Restaurant Basement -> Restaurant Basement Path to Crest Guardian").access_rule = \
        lambda state: has_water_scroll(state, world) or has_sky_scroll_complex(state, world)
    world.get_entrance("Somnolent Forest -> Island of Dragons").access_rule = \
        lambda state: can_identify_gondola_gizmo(state, world) and can_fight_skullpion(state, world) and has_water_scroll(state,world)
    world.get_entrance("Somnolent Forest -> Somnolent Forest Behind Steam").access_rule = \
        lambda state: state.has("Bracelet", player)
    world.get_entrance("Grillin Village -> Grillin Reservoir").access_rule = \
        lambda state: can_fight_skullpion(state, world)
    world.get_entrance("Reservoir Tunnel -> Wind Scroll").access_rule = \
        lambda state: can_enter_frozen_palace(state, world) and can_identify_gondola_gizmo(state, world) and can_fight_skullpion(state, world) and can_fight_frost_dragon(state, world)
    world.get_entrance("Meandering Forest -> Frozen Palace Entrance").access_rule = \
        lambda state: can_enter_frozen_palace(state, world) and can_identify_gondola_gizmo(state, world) and can_fight_skullpion(state, world)
    world.get_entrance("Frozen Palace Entrance -> Frozen Palace Red Eye Door").access_rule = \
        lambda state: state.has("Red Eye", player) or has_sky_scroll_complex(state, world)
    world.get_entrance("Frozen Palace Entrance -> Frozen Palace Blue Eye Door").access_rule = \
        lambda state: state.has("Blue Eye", player) or has_sky_scroll_complex(state, world)
    world.get_entrance("Frozen Palace Entrance -> Frozen Palace Green Eye Maze").access_rule = \
        lambda state: state.has("Red Shoes", player) or has_sky_scroll_complex(state, world)
    world.get_entrance("Frozen Palace Green Eye Maze -> Frozen Palace Atrium Right Balcony").access_rule = \
        lambda state: state.has("Green Eye", player) or has_sky_scroll_complex(state, world)
    world.get_entrance("Frozen Palace Entrance -> Frost Dragon Door").access_rule = \
        lambda state: can_fight_frost_dragon(state, world)
    world.get_entrance("Upper Grillin Village -> Upper Mines").access_rule = \
        lambda state: can_enter_frozen_palace(state, world) and can_identify_gondola_gizmo(state, world) and can_fight_skullpion(state, world) and can_fight_frost_dragon(state, world) #add wind scroll / double jump logic
    world.get_entrance("Upper Mines -> Upper Mines Behind Posion").access_rule = \
        lambda state: has_wind_scroll(state, world)
    world.get_entrance("Steamwood Forest -> Sky Island").access_rule = \
        lambda state: has_earth_scroll(state, world) and has_water_scroll(state, world) and has_fire_scroll(state, world) and has_wind_crest(state, world)

def set_location_rules(world: "BFMWorld") -> None:
    player = world.player
    options = world.options

    for index, name in enumerate(location_name_groups["Bincho"]):
        set_rule(world.get_location(name), lambda state: has_lumina(state, world)) 

    add_rule(world.get_location("Weaver Bincho - Twinpeak Second Peak"),
        lambda state: can_fight_skullpion(state, world) or has_sky_scroll(state, world)) 
    set_rule(world.get_location("Minku - Twinpeak End of Stream"),
        lambda state: can_fight_skullpion(state, world) or has_water_scroll(state, world) or has_sky_scroll(state, world))
    set_rule(world.get_location("Minku - Steamwood Forest"),
        lambda state: can_fight_skullpion(state, world))
    set_rule(world.get_location("Minku - Somnolent Forest"),
        lambda state: can_fight_skullpion(state, world) or has_water_scroll(state, world) or has_sky_scroll(state, world))
    if(options.bakery_sanity.value == True):
        set_rule(world.get_location("Item 6 - Bakery"),
            lambda state: can_fight_skullpion(state, world))
        set_rule(world.get_location("Item 7 - Bakery"),
            lambda state: can_fight_skullpion(state, world))
    if(options.grocery_sanity.value == True):
        set_rule(world.get_location("Item 8 - Grocery"), #orange, save Tim
            lambda state: can_fight_skullpion(state, world))
        set_rule(world.get_location("Item 9 - Grocery"), #Chapter 4 EX-Drink
            lambda state: can_fight_skullpion(state, world))
        set_rule(world.get_location("Item 10 - Grocery"), #Chapter 4 H-Mint
            lambda state: can_fight_skullpion(state, world))
        set_rule(world.get_location("Item 11 - Grocery"), #rice ball
            lambda state: has_rice(state, world) and state.has("Chef", player))
        set_rule(world.get_location("Item 12 - Grocery"), #neatball
            lambda state: has_rice(state, world) and state.has_all({"CookB", "Butcher"}, player))
    set_rule(world.get_location("Minku - Grillin Village Above Gondola"),
        lambda state: state.has("Bracelet", player))
    set_rule(world.get_location("Aged Coin Chest - Steamwood Forest"),
        lambda state: state.has("Bracelet", player))
    if(options.scroll_sanity.value == True):
        set_rule(world.get_location("Earth Scroll - Twinpeak First Peak"),
            lambda state: state.has("Bracelet", player) and has_lumina(state, world))
    set_rule(world.get_location("Rock Chest - Twinpeak Second Peak"),
        lambda state: has_earth_scroll(state, world)) #add sky scroll + double jump stuff here
    set_rule(world.get_location("Bracelet Chest - Twinpeak Entrance"),
        lambda state: has_lumina(state, world) and (has_bread(state, world) or state.has("Bracelet", player)) or has_water_scroll(state, world) or has_sky_scroll(state, world))
    set_rule(world.get_location("200 Drans Chest - Twinpeak Path to Skullpion"),
        lambda state: ((has_water_scroll(state, world) or has_sky_scroll(state, world)) and has_earth_scroll(state, world)) or has_sky_scroll_complex(state, world))
    set_rule(world.get_location("Glasses Chest - Somnolent Forest"),
        lambda state: can_fight_skullpion(state, world) and has_water_scroll(state, world))
    set_rule(world.get_location("Minku - Grillin Reservoir"),
        lambda state: has_water_scroll(state, world) or has_sky_scroll(state, world))     
    set_rule(world.get_location("Old Shirt Chest - Grillin Reservoir"),
        lambda state: has_water_scroll(state, world) or has_sky_scroll(state, world))    
    set_rule(world.get_location("Used Boot Chest - Grillin Reservoir"),
        lambda state: has_water_scroll(state, world))       
    set_rule(world.get_location("Armor Chest - Reservoir Tunnel"),
        lambda state: has_water_scroll(state, world))       
    if(options.toy_sanity.value == True):
        set_rule(world.get_location("Skullpion - Toy Shop"),
            lambda state: can_fight_skullpion(state, world))
        set_rule(world.get_location("Frost Dragon - Toy Shop"),
            lambda state: can_fight_frost_dragon(state, world))
        set_rule(world.get_location("Slow Guy - Toy Shop"),
            lambda state: state.has_any({"Red Eye", "Blue Eye", "Red Shoes"}, player) or has_sky_scroll_complex(state, world))
        set_rule(world.get_location("Steel Golem - Toy Shop"),
            lambda state: state.has_any({"Red Eye", "Red Shoes"}, player) or has_sky_scroll_complex(state, world))
        set_rule(world.get_location("GiAnt - Toy Shop"),
            lambda state: has_wind_scroll(state, world))
        set_rule(world.get_location("Queen Ant - Toy Shop"),
            lambda state: has_wind_scroll(state, world))
    if(options.tech_sanity.value == True):
        set_rule(world.get_location("Improved Fusion - Allucaneet Castle"),
            lambda state: state.has("Artisan", player))
        set_rule(world.get_location("Dashing Pierce - Allucaneet Castle"),
            lambda state: state.has("Maid", player))
        set_rule(world.get_location("Shish Kebab - Allucaneet Castle"),
            lambda state: state.has("Acrobat", player) and has_orange(state, world))
        set_rule(world.get_location("Crosswise Cut - Allucaneet Castle"),
            lambda state: can_fight_skullpion(state, world))
        set_rule(world.get_location("Tenderize - Allucaneet Castle"),
            lambda state: state.has("KnightA", player))
        set_rule(world.get_location("Desperado Attack - Allucaneet Castle"),
            lambda state: state.has("KnightC", player) and state.has("Crosswise Cut", player))
        set_rule(world.get_location("Rumparoni Special - Allucaneet Castle"),
            lambda state: state.has("KnightD", player))
    


             