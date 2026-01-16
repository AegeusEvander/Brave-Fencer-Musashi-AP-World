from typing import Dict, TYPE_CHECKING

from worlds.generic.Rules import set_rule, forbid_item, add_rule
from BaseClasses import CollectionState
from .locations import location_name_groups, location_table
from .items import item_table
if TYPE_CHECKING:
    from . import BFMWorld
import math


def check_location_name(name: str, lang: bool) -> str:
    if(lang == False):
        return name
    return location_table[name].jp_name

def check_item_name(name: str, world: "BFMWorld") -> str:
    if(world.options.set_lang.value == 1 or world.using_ut == True or world.options.spoiler_items_in_english.value == True):
        return name
    return item_table[name].jp_name

def can_fight_skullpion(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.playthrough_method.value == 2):
        return state.has_all({check_item_name("SoldierA", world), check_item_name("MercenC", world), check_item_name("CarpentA", world), check_item_name("KnightB", world)}, world.player) and (has_lumina(state, world) or can_wind_scroll_jump_complex(state, world)) and has_earth_scroll(state, world) and has_healing(state, world) 
    return state.has_all({check_item_name("SoldierA", world), check_item_name("MercenC", world), check_item_name("CarpentA", world), check_item_name("KnightB", world), check_item_name("Bracelet", world)}, world.player) and has_lumina(state, world) and has_earth_scroll(state, world) and has_healing(state, world) and has_freed_jon(state, world) and has_raft(state, world) and can_complete_steamwood_1(state, world)

def has_defeated_skullpion(state: CollectionState, world: "BFMWorld") -> bool:
    return can_fight_skullpion(state, world)

def has_completed_chapter_2(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.playthrough_method.value == 2):
        return True
    return has_defeated_skullpion(state, world) and has_freed_jon(state, world) and has_raft(state, world) and can_complete_steamwood_1(state, world)

def has_defeated_relic_keeper(state: CollectionState, world: "BFMWorld") -> bool:
    return has_angel_statue(state,world)and has_healing(state, world) and can_double_jump(state, world) and has_water_scroll(state, world) and has_rescued_tim(state, world) and has_lumina(state, world)

def has_completed_chapter_3(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.playthrough_method.value == 2):
        return True
    return has_completed_chapter_2(state, world) and has_rescued_tim(state, world) and has_defeated_relic_keeper(state,world) and can_double_jump(state, world)

def can_fight_frost_dragon(state: CollectionState, world: "BFMWorld") -> bool:
    return state.has_all({check_item_name("Red Eye", world), check_item_name("Blue Eye", world), check_item_name("Green Eye", world), check_item_name("Red Shoes", world)}, world.player) and has_fire_scroll(state, world) and has_lumina(state, world) and (can_double_jump(state, world) or can_wind_scroll_jump_simple(state, world)) and has_healing(state, world)

def can_enter_frozen_palace(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.playthrough_method.value == 2):
        return state.has_all({check_item_name("MercenA", world), check_item_name("MercenB", world), check_item_name("MercenC", world)}, world.player)
    return state.has_all({check_item_name("MercenA", world), check_item_name("MercenB", world), check_item_name("MercenC", world)}, world.player) and can_rescue_princess(state, world)

def can_identify_gondola_gizmo(state: CollectionState, world: "BFMWorld") -> bool:
    return state.has_all({check_item_name("CarpentA", world), check_item_name("CarpentB", world), check_item_name("CarpentC", world)}, world.player)

def has_saved_princess(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.playthrough_method.value == 2):
        return True
    return has_completed_chapter_3(state, world) and can_rescue_princess(state, world) and has_fixed_well(state, world) and has_fixed_gondola(state, world)

def has_completed_chapter_4(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.playthrough_method.value == 2):
        return True
    return has_completed_chapter_3(state, world) and can_rescue_princess(state, world) and can_enter_frozen_palace(state,world) and can_fight_frost_dragon(state,world) and has_fixed_well(state, world) and has_fixed_gondola(state, world)

def has_completed_chapter_5(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.playthrough_method.value == 2):
        return has_wind_scroll(state,world) and has_fixed_well(state, world) and has_fire_boss_core(state, world) and has_fire_scroll(state, world) and has_fixed_gondola(state, world) and can_double_jump(state, world)
    return has_completed_chapter_4(state, world) and has_wind_scroll(state,world) and has_fixed_well(state, world) and has_fire_boss_core(state, world)

def saved_everyone(state: CollectionState, world: "BFMWorld") -> bool:
    return state.has_all({"Guard", "Seer", "Hawker", "Maid", "MusicianB", "SoldierA", "MercenC", "CarpentA", "KnightB", "Shepherd", "Bailiff", "Taster", "CarpentB", "Weaver", "SoldierB", "KnightA", "CookA", "Acrobat", "MercenB", "Janitor", "Artisan", "CarpentC", "MusicianC", "Knitter", "Chef", "MercenA", "Chief", "CookB", "Conductor", "Butcher", "KnightC", "Doctor", "KnightD", "Alchemist", "Librarian"}, world.player)

def has_lumina(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.lumina_randomzied.value == True):
        return state.has(check_item_name("Lumina", world), world.player)
    return True

def has_rice(state: CollectionState, world: "BFMWorld") -> bool:
    return state.has_all({check_item_name("Bailiff", world), check_item_name("CookA", world)}, world.player)

def has_orange(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.grocery_sanity.value == True):
        return state.has(check_item_name("Orange", world), world.player) and can_fight_skullpion(state, world)
    else:
        return can_fight_skullpion(state, world)

def has_bread(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.quest_item_sanity.value == True and world.options.bakery_sanity.value == True):
        return state.has(check_item_name("Progressive Bread", world), world.player) and state.has(check_item_name("Well H20", world), world.player)
    if(world.options.quest_item_sanity.value == True):
        return state.has(check_item_name("Well H20", world), world.player) 
    if(world.options.bakery_sanity.value == True):
        return state.has(check_item_name("Progressive Bread", world), world.player) 
    return True

def has_healing(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.grocery_sanity_heal_logic.value == True and world.options.grocery_sanity.value == True):
        return state.has(check_item_name("W-Gel", world), world.player) or state.has(check_item_name("Progressive Drink", world), world.player)
    return True

def has_ex_drink(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.grocery_sanity.value == True):
        return state.has(check_item_name("Progressive Drink", world), world.player, 2)
    return True

def has_raft(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.quest_item_sanity.value == True):
        return state.has(check_item_name("Log", world), world.player, 4) and state.can_reach_region("Twinpeak Second Peak", world.player)
    else:
        return has_lumina(state, world) and has_bread(state, world) 

def has_jon_key(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.quest_item_sanity.value == True):
        return state.has(check_item_name("Jon's Key", world), world.player)
    return True

def has_freed_jon(state: CollectionState, world: "BFMWorld") -> bool:
    return has_bread(state, world) and has_jon_key(state, world)

def has_misteria(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.quest_item_sanity.value == True):
        return state.has(check_item_name("Misteria", world), world.player)
    return True

def has_aqualin(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.quest_item_sanity.value == True):
        return state.has(check_item_name("Aqualin", world), world.player)
    return True

def has_rescued_tim(state: CollectionState, world: "BFMWorld") -> bool:
    return (has_earth_scroll(state, world) and (has_lumina(state, world) or has_sky_scroll_complex(state, world)) or (can_double_jump(state, world) and has_sky_scroll_complex(state, world))) and has_completed_chapter_2(state, world) and has_misteria(state, world) and has_aqualin(state, world) and state.can_reach_region("Twinpeak Second Peak", world.player)

def can_complete_steamwood_1(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.quest_item_sanity.value == True):
        return state.has_all({check_item_name("Bracelet", world), check_item_name("Manual", world)}, world.player)
    return state.has(check_item_name("Bracelet", world), world.player)

def can_enter_mine(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.quest_item_sanity.value == True):
        return state.has(check_item_name("Key", world), world.player) and has_completed_chapter_2(state, world)
    return has_completed_chapter_2(state, world)

def has_rope(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.quest_item_sanity.value == True):
        return state.has(check_item_name("Rope", world), world.player) and has_completed_chapter_2(state, world)
    return has_completed_chapter_2(state, world) and has_rescued_tim(state, world) and can_double_jump(state, world)

def has_angel_statue(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.quest_item_sanity.value == True):
        return state.has(check_item_name("Angel Statue", world), world.player) and has_completed_chapter_2(state, world) and has_rescued_tim(state, world) and can_double_jump(state, world)
    return has_completed_chapter_2(state, world) and (has_water_scroll(state, world) or has_sky_scroll_simple(state, world))

def has_fixed_well(state: CollectionState, world: "BFMWorld") -> bool:
    return has_water_scroll(state, world) and has_water_boss_core(state, world) and can_enter_mine(state, world)

def has_fixed_gondola(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.quest_item_sanity.value == True):
        return state.has(check_item_name("Gondola Gizmo", world), world.player) and has_completed_chapter_2(state, world) and can_identify_gondola_gizmo(state, world) and has_fixed_well(state, world)
    return has_completed_chapter_2(state, world) and can_identify_gondola_gizmo(state, world) and has_fixed_well(state, world)

def can_rescue_princess(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.quest_item_sanity.value == True):
        if(world.options.playthrough_method.value == 2):
            return state.has(check_item_name("Rock Salt", world), world.player) and has_water_boss_core(state, world) and has_water_scroll(state, world) and has_lumina(state, world)
        else:
            return state.has(check_item_name("Rock Salt", world), world.player) and has_fixed_gondola(state, world)
    return has_fixed_gondola(state, world)

def has_salt(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.quest_item_sanity.value == True):
        return state.has(check_item_name("Rock Salt", world), world.player) and has_completed_chapter_3(state, world)
    return has_fixed_gondola(state, world) and has_completed_chapter_3(state, world)

def has_hp_for_soda_fountain(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.starting_hp.value == 1):
        return True
    berries_needed = math.ceil((world.options.max_hp_logic.value - world.options.starting_hp) / 25.0)
    if(berries_needed > 1):
        berries_needed = berries_needed - 1 #account for free mayor berry
    berries_needed = max(min(13, berries_needed), 0)
    return state.has(check_item_name("Longevity Berry", world), world.player, berries_needed)

def has_earth_scroll(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.scroll_sanity.value == True):
        return state.has(check_item_name("Earth Scroll", world), world.player)
    else:
        return state.has(check_item_name("Bracelet", world), world.player) and has_lumina(state, world) and state.can_reach_region("Twinpeak Around the Bend", world.player) and can_complete_steamwood_1(state, world)

def has_water_scroll(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.scroll_sanity.value == True):
        return state.has(check_item_name("Water Scroll", world), world.player)
    else:
        return has_completed_chapter_2(state, world) and state.can_reach_region("Grillin Reservoir", world.player)

def has_fire_scroll(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.scroll_sanity.value == True):
        return state.has(check_item_name("Fire Scroll", world), world.player)
    else:
        return can_rescue_princess(state, world)

def has_wind_scroll(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.scroll_sanity.value == True):
        return state.has(check_item_name("Wind Scroll", world), world.player)
    else:
        return has_completed_chapter_4(state, world) and can_enter_mine(state, world) and has_water_scroll(state, world) and has_water_boss_core(state, world) and has_fire_scroll(state, world) and has_fire_boss_core(state, world) and has_lumina(state, world)

def has_sky_scroll(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.scroll_sanity.value == True):
        return state.has(check_item_name("Sky Scroll", world), world.player)
    else:
        return False

def has_sky_scroll_simple(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.scroll_sanity.value == True):
        if(world.options.sky_scroll_logic.value == 1):
            return False
        return state.has(check_item_name("Sky Scroll", world), world.player)
    else:
        return False

def has_sky_scroll_complex(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.scroll_sanity.value == True):
        if(world.options.sky_scroll_logic.value != 3):
            return False
        return state.has(check_item_name("Sky Scroll", world), world.player)
    else:
        return False

def has_earth_boss_core(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.core_sanity.value == True):
        return state.has(check_item_name("Earth Boss Core", world), world.player)
    return has_defeated_skullpion(state, world)

def has_water_boss_core(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.core_sanity.value == True):
        return state.has(check_item_name("Water Boss Core", world), world.player)
    return has_defeated_relic_keeper(state, world)

def has_fire_boss_core(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.core_sanity.value == True):
        return state.has(check_item_name("Fire Boss Core", world), world.player)
    return has_completed_chapter_4(state, world) and can_enter_frozen_palace(state, world) and can_fight_frost_dragon(state, world)

def has_wind_boss_core(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.core_sanity.value == True):
        return state.has(check_item_name("Wind Boss Core", world), world.player)
    return has_completed_chapter_5(state, world)

def has_all_scrolls(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.scroll_sanity.value == True):
        return has_earth_scroll(state, world) and has_water_scroll(state, world) and has_fire_scroll(state, world) and has_wind_scroll(state, world) and has_sky_scroll(state, world)
    return has_earth_scroll(state, world) and has_water_scroll(state, world) and has_fire_scroll(state, world) and has_wind_scroll(state, world)

def can_double_jump(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.quest_item_sanity.value == True):
        return state.has(check_item_name("Ugly Belt", world), world.player)
    return has_completed_chapter_2(state, world)

def can_wind_scroll_jump_simple(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.wind_scroll_logic.value == 1):
        return False
    return has_wind_scroll(state, world)

def can_wind_scroll_jump_complex(state: CollectionState, world: "BFMWorld") -> bool:
    if(world.options.wind_scroll_logic.value == 3):
        return has_wind_scroll(state, world)
    return False

def set_region_rules(world: "BFMWorld") -> None:
    player = world.player
    options = world.options

    world.get_entrance("Grillin Village -> Defeat First Boss").access_rule = \
        lambda state: state.has("Boss killed", player)
    world.get_entrance("Defeat First Boss -> Defeat Second Boss").access_rule = \
        lambda state: state.has("Boss killed", player, 2)
    world.get_entrance("Defeat Second Boss -> Defeat Third Boss").access_rule = \
        lambda state: state.has("Boss killed", player, 3) 
    world.get_entrance("Defeat Third Boss -> Defeat Fourth Boss").access_rule = \
        lambda state: state.has("Boss killed", player, 4)
    world.get_entrance("Grillin Village -> Mine Entrance").access_rule = \
        lambda state: can_enter_mine(state, world)
    world.get_entrance("Grillin Village -> Restaurant Basement").access_rule = \
        lambda state: has_rescued_tim(state, world)
    world.get_entrance("Restaurant Basement Bowling 1 -> Restaurant Basement Bowling 2").access_rule = \
        lambda state: has_lumina(state, world)
    if(options.quest_item_sanity.value == True):
        world.get_entrance("Meandering Forest -> Graveyard").access_rule = \
            lambda state: has_bread(state, world)
        world.get_entrance("Steamwood Forest -> Steamwood 2").access_rule = \
            lambda state: has_completed_chapter_4(state, world) and can_double_jump(state, world) and state.has_all({check_item_name("Manual", world), check_item_name("Bracelet", world), check_item_name("Handle #0", world), check_item_name("Handle #1", world), check_item_name("Handle #4", world), check_item_name("Handle #8", world), check_item_name("Profits", world)}, player)
    if(options.toy_sanity.value == True):
        world.get_entrance("Toy Shop Series 1 -> Toy Shop Series 3").access_rule = \
            lambda state: has_completed_chapter_2(state, world)
        world.get_entrance("Toy Shop Series 1 -> Toy Shop Series 4").access_rule = \
            lambda state: can_enter_frozen_palace(state, world) and has_fixed_gondola(state, world) and has_completed_chapter_3(state, world) and can_rescue_princess(state, world)
        world.get_entrance("Toy Shop Series 1 -> Toy Shop Series 5").access_rule = \
            lambda state: has_completed_chapter_4(state, world)
    world.get_entrance("Twinpeak Entrance -> Twinpeak Path to Skullpion").access_rule = \
        lambda state: has_earth_scroll(state, world) or has_sky_scroll_simple(state, world)
    world.get_entrance("Twinpeak Entrance -> Twinpeak Around the Bend").access_rule = \
        lambda state: has_bread(state,world) and has_jon_key(state, world) or has_water_scroll(state, world) or has_sky_scroll_simple(state, world) or can_double_jump(state, world)
    world.get_entrance("Twinpeak Path to Skullpion -> Skullpion Arena").access_rule = \
        lambda state: can_fight_skullpion(state, world)
    world.get_entrance("Restaurant Basement -> Restaurant Basement Path to Crest Guardian").access_rule = \
        lambda state: (has_angel_statue(state, world) or has_sky_scroll_complex(state, world)) and can_double_jump(state, world)
    world.get_entrance("Restaurant Basement Path to Crest Guardian -> Relic Keeper Arena").access_rule = \
        lambda state: has_water_scroll(state, world) and has_healing(state, world)
    world.get_entrance("Somnolent Forest -> Island of Dragons").access_rule = \
        lambda state: has_salt(state, world)
    world.get_entrance("Somnolent Forest -> Somnolent Forest Behind Steam").access_rule = \
        lambda state: can_complete_steamwood_1(state, world)
    world.get_entrance("Grillin Village -> Grillin Reservoir").access_rule = \
        lambda state: has_completed_chapter_2(state, world) and has_rope(state, world)
    world.get_entrance("Mine Entrance -> Grillin Reservoir").access_rule = \
        lambda state: has_water_scroll(state, world) or has_sky_scroll_simple(state, world)
    world.get_entrance("Mine Entrance -> Scrap Depository").access_rule = \
        lambda state: can_identify_gondola_gizmo(state, world) and (can_double_jump(state, world) or has_sky_scroll_complex(state, world)) and has_completed_chapter_3(state, world) and has_fixed_well(state, world)
    world.get_entrance("Grillin Reservoir -> Reservoir Tunnel").access_rule = \
        lambda state: has_water_scroll(state, world) and has_water_boss_core(state, world)
    world.get_entrance("Reservoir Tunnel -> Wind Scroll").access_rule = \
        lambda state: has_fire_boss_core(state, world) and has_fire_scroll(state, world)
    world.get_entrance("Meandering Forest -> Frozen Palace Entrance").access_rule = \
        lambda state: can_enter_frozen_palace(state, world) and has_saved_princess(state, world)
    world.get_entrance("Frozen Palace Entrance -> Frozen Palace Red Eye Room").access_rule = \
        lambda state: can_double_jump(state, world) or can_wind_scroll_jump_complex(state, world) or has_sky_scroll_simple(state, world)
    world.get_entrance("Frozen Palace Entrance -> Frozen Palace Red Eye Door").access_rule = \
        lambda state: (state.has(check_item_name("Red Eye", world), player) and (can_double_jump(state, world) or can_wind_scroll_jump_simple(state, world))) or has_sky_scroll_complex(state, world)
    world.get_entrance("Frozen Palace Entrance -> Frozen Palace Blue Eye Door").access_rule = \
        lambda state: state.has(check_item_name("Blue Eye", world), player) or has_sky_scroll_complex(state, world)
    world.get_entrance("Frozen Palace Blue Eye Door -> Frozen Palace Atrium Left Balcony").access_rule = \
        lambda state: can_double_jump(state, world) or can_wind_scroll_jump_simple(state, world) 
    world.get_entrance("Frozen Palace Entrance -> Frozen Palace Green Eye Maze").access_rule = \
        lambda state: state.has(check_item_name("Red Shoes", world), player) or has_sky_scroll_complex(state, world)
    world.get_entrance("Frozen Palace Green Eye Maze -> Frozen Palace Atrium Right Balcony").access_rule = \
        lambda state: has_sky_scroll_complex(state, world)
    world.get_entrance("Frozen Palace Entrance -> Frost Dragon Door").access_rule = \
        lambda state: can_fight_frost_dragon(state, world)
    world.get_entrance("Upper Grillin Village -> Upper Mines").access_rule = \
        lambda state: has_completed_chapter_4(state, world) and state.has(check_item_name("Bracelet", world), player) and has_fire_boss_core(state, world) and has_fire_scroll(state, world) and has_fixed_well(state, world) and (can_wind_scroll_jump_simple(state, world) or can_double_jump(state, world) or has_sky_scroll_simple(state, world)) and has_fixed_gondola(state, world)
    world.get_entrance("Upper Mines -> Upper Mines Behind Poison").access_rule = \
        lambda state: has_wind_scroll(state, world)
    world.get_entrance("Upper Mines Behind Poison -> Upper Mines Poison Elevators").access_rule = \
        lambda state: (has_earth_scroll(state, world) or has_sky_scroll_complex(state, world)) and can_double_jump(state, world)
    world.get_entrance("Upper Mines Poison Elevators -> Queen Ant Arena").access_rule = \
        lambda state: has_lumina(state, world) and has_healing(state, world)
    world.get_entrance("Steamwood Forest -> Sky Island").access_rule = \
        lambda state: has_earth_scroll(state, world) and has_water_scroll(state, world) and has_fire_scroll(state, world) and has_wind_scroll(state, world) and has_wind_boss_core(state, world) and has_earth_boss_core(state, world) and has_lumina(state, world) and state.has(check_item_name("Bracelet", world), player) and (can_double_jump(state, world) or has_sky_scroll(state, world))
    world.get_entrance("Sky Island -> Soda Fountain").access_rule = \
        lambda state: has_all_scrolls(state, world) and can_double_jump(state, world) and has_lumina(state, world) and state.has(check_item_name("Bracelet", world), player) and has_hp_for_soda_fountain(state, world) and has_ex_drink(state, world)         

def set_location_rules(world: "BFMWorld", lang: bool) -> None:
    player = world.player
    options = world.options

    for index, name in enumerate(location_name_groups["Bincho"]):
        set_rule(world.get_location(check_location_name(name, lang)), lambda state: has_lumina(state, world))

    if(options.level_sanity.value == True and options.starting_hp.value != 1):
        for index, name in enumerate(location_name_groups["Level"]):
            if("Lum" in name):
                set_rule(world.get_location(check_location_name(name, lang)), lambda state: has_lumina(state, world)) 

    if(options.quest_item_sanity.value == True):
        add_rule(world.get_location(check_location_name("Doctor Bincho - Twinpeak Around the Bend", lang)),
            lambda state: has_raft(state, world) or has_water_scroll(state,world) or has_sky_scroll_simple(state, world)) 
        set_rule(world.get_location(check_location_name("First Log - Twinpeak Second Peak", lang)),
            lambda state: has_lumina(state, world))
        set_rule(world.get_location(check_location_name("Second Log - Twinpeak Second Peak", lang)),
            lambda state: has_lumina(state, world))
        set_rule(world.get_location(check_location_name("Third Log - Twinpeak Second Peak", lang)),
            lambda state: has_lumina(state, world))
        set_rule(world.get_location(check_location_name("Fourth Log - Twinpeak Second Peak", lang)),
            lambda state: has_lumina(state, world))
        set_rule(world.get_location(check_location_name("Manual from Mayor - Grillin Village", lang)),
            lambda state: state.has(check_item_name("Bracelet", world), player))
        set_rule(world.get_location(check_location_name("Mayor Berry - Grillin Village", lang)),
            lambda state: state.has_all({check_item_name("Bracelet", world), check_item_name("Manual", world)}, player))
        set_rule(world.get_location(check_location_name("Key from Wid - Grillin Village", lang)),
            lambda state: has_completed_chapter_2(state, world))
        set_rule(world.get_location(check_location_name("Aqualin - Twinpeak Second Peak", lang)),
            lambda state: (has_earth_scroll(state, world) and (has_lumina(state, world) or has_sky_scroll_complex(state, world)) or (can_double_jump(state, world) and has_sky_scroll_complex(state, world))) and has_completed_chapter_2(state, world) and state.has(check_item_name("Misteria", world), player) and has_aqualin(state, world))
        set_rule(world.get_location(check_location_name("Rescue Tim - Grillin Village", lang)),
            lambda state: has_rescued_tim(state, world))
        set_rule(world.get_location(check_location_name("Defeat Vambee Soldiers - Grillin Village", lang)),
            lambda state: has_rescued_tim(state, world) and can_double_jump(state, world))
        set_rule(world.get_location(check_location_name("Return Bell - Grillin Village", lang)),
            lambda state: has_rescued_tim(state, world) and can_double_jump(state, world) and can_enter_mine(state, world) and (has_water_scroll(state, world) or has_sky_scroll_simple(state, world)))
        set_rule(world.get_location(check_location_name("Mrs Govern's Pie - Grillin Village", lang)),
            lambda state: has_completed_chapter_3(state, world) and has_water_boss_core(state, world))
        set_rule(world.get_location(check_location_name("Reward #1 After Extinguishing Village - Grillin Village", lang)),
            lambda state: has_completed_chapter_3(state, world) and has_fixed_gondola(state, world))
        set_rule(world.get_location(check_location_name("Reward #2 After Extinguishing Village - Grillin Village", lang)),
            lambda state: has_completed_chapter_3(state, world) and has_fixed_gondola(state, world))
        set_rule(world.get_location(check_location_name("Jon's Note - Somnolent Forest Deadend", lang)),
            lambda state: state.can_reach_region("Queen Ant Arena", player) and has_wind_boss_core(state, world))
    add_rule(world.get_location(check_location_name("Weaver Bincho - Twinpeak Second Peak", lang)),
        lambda state: can_double_jump(state, world) or has_sky_scroll_simple(state, world)) 
    set_rule(world.get_location(check_location_name("Minku - Twinpeak End of Stream", lang)),
        lambda state: has_water_scroll(state, world) or has_sky_scroll_simple(state, world))
    set_rule(world.get_location(check_location_name("Minku - Steamwood Forest", lang)),
        lambda state: has_earth_boss_core(state, world) and has_earth_scroll(state, world) and state.has(check_item_name("Bracelet", world), player))
    set_rule(world.get_location(check_location_name("Minku - Somnolent Forest", lang)),
        lambda state: has_water_scroll(state, world) or has_sky_scroll_simple(state, world))
    if(options.bakery_sanity.value == True):
        set_rule(world.get_location(check_location_name("Item 6 (JamBread) - Bakery", lang)),
            lambda state: has_completed_chapter_3(state, world) and state.has("Boss killed", player, 2))
        set_rule(world.get_location(check_location_name("Item 7 (Biscuit) - Bakery", lang)),
            lambda state: has_completed_chapter_3(state, world) and state.has("Boss killed", player, 2))
    if(options.grocery_sanity.value == True):
        set_rule(world.get_location(check_location_name("Item 8 (Orange) - Grocery", lang)), #orange, save Tim
            lambda state: has_completed_chapter_2(state, world) and has_rescued_tim(state, world))
        set_rule(world.get_location(check_location_name("Item 9 (EX-Drink) - Grocery", lang)), #Chapter 4 EX-Drink
            lambda state: has_completed_chapter_3(state, world) and state.has("Boss killed", player, 2))
        set_rule(world.get_location(check_location_name("Item 10 (H-Mint) - Grocery", lang)), #Chapter 4 H-Mint
            lambda state: has_completed_chapter_3(state, world) and state.has("Boss killed", player, 2))
        set_rule(world.get_location(check_location_name("Item 11 (Riceball) - Grocery", lang)), #rice ball
            lambda state: has_rice(state, world) and state.has(check_item_name("Chef", world), player))
        set_rule(world.get_location(check_location_name("Item 12 (Neat Ball) - Grocery", lang)), #neatball
            lambda state: has_rice(state, world) and state.has_all({check_item_name("CookB", world), check_item_name("Butcher", world)}, player))
    set_rule(world.get_location(check_location_name("Minku - Grillin Village Above Gondola", lang)),
        lambda state: state.has(check_item_name("Bracelet", world), player))
    set_rule(world.get_location(check_location_name("Aged Coin Chest - Steamwood Forest", lang)),
        lambda state: state.has(check_item_name("Bracelet", world), player))
    if(options.scroll_sanity.value == True):
        set_rule(world.get_location(check_location_name("Earth Scroll - Twinpeak First Peak", lang)),
            lambda state: state.has(check_item_name("Bracelet", world), player) and has_lumina(state, world) and can_complete_steamwood_1(state, world))
        set_rule(world.get_location(check_location_name("Water Scroll - Grillin Reservoir", lang)),
            lambda state: has_lumina(state, world))
        set_rule(world.get_location(check_location_name("Fire Scroll - Island of Dragons", lang)),
            lambda state: can_rescue_princess(state, world) and has_lumina(state, world))
        set_rule(world.get_location(check_location_name("Wind Scroll - Grillin Volcano", lang)),
            lambda state: has_lumina(state, world))
    set_rule(world.get_location(check_location_name("Rock Chest - Twinpeak Second Peak", lang)),
        lambda state: has_earth_scroll(state, world) and (has_lumina(state, world) or has_sky_scroll_complex(state, world)) or (can_double_jump(state, world) and has_sky_scroll_complex(state, world))) #add sky scroll + double jump stuff here
    set_rule(world.get_location(check_location_name("Bracelet Chest - Twinpeak Entrance", lang)),
        lambda state: has_raft(state, world) or has_water_scroll(state, world) or has_sky_scroll_simple(state, world))
    set_rule(world.get_location(check_location_name("200 Drans Chest - Twinpeak Path to Skullpion", lang)),
        lambda state: ((has_water_scroll(state, world) or has_sky_scroll_simple(state, world)) and has_earth_scroll(state, world)) or has_sky_scroll_complex(state, world) or (has_raft(state, world) and has_earth_scroll(state,world)))
    set_rule(world.get_location(check_location_name("Glasses Chest - Somnolent Forest", lang)),
        lambda state: has_water_scroll(state, world) and has_water_boss_core(state, world))
    set_rule(world.get_location(check_location_name("Ugly Belt - Restaurant Basement", lang)),
        lambda state: has_lumina(state, world))#eventually will need to add requirements for four eyes
    set_rule(world.get_location(check_location_name("Minku - Grillin Reservoir", lang)),
        lambda state: (has_water_scroll(state, world) and has_water_boss_core(state, world)) or has_sky_scroll_simple(state, world))     
    set_rule(world.get_location(check_location_name("Old Shirt Chest - Grillin Reservoir", lang)),
        lambda state: (has_water_scroll(state, world) and has_water_boss_core(state, world)) or has_sky_scroll_simple(state, world))    
    set_rule(world.get_location(check_location_name("Used Boot Chest - Grillin Reservoir", lang)),
        lambda state: has_water_scroll(state, world) and has_water_boss_core(state, world))
    set_rule(world.get_location(check_location_name("White Cloth Chest - Frozen Palace Green Eye Maze", lang)),
        lambda state: can_double_jump(state, world) or can_wind_scroll_jump_complex(state, world))
    add_rule(world.get_location(check_location_name("MusicianC Bincho - Frozen Palace Green Eye Maze", lang)),
        lambda state: can_double_jump(state, world) or can_wind_scroll_jump_complex(state, world))
    if(options.toy_sanity.value == True):
        set_rule(world.get_location(check_location_name("Skullpion - Toy Shop", lang)),
            lambda state: can_fight_skullpion(state, world))
        set_rule(world.get_location(check_location_name("Ed & Ben - Toy Shop", lang)),
            lambda state: has_water_scroll(state, world) and has_water_boss_core(state, world) and can_enter_mine(state, world))
        set_rule(world.get_location(check_location_name("Relic Keeper - Toy Shop", lang)),
            lambda state: state.can_reach_region("Relic Keeper Arena", player))
        set_rule(world.get_location(check_location_name("Frost Dragon - Toy Shop", lang)),
            lambda state: state.can_reach_region("Frost Dragon Arena", player))
        set_rule(world.get_location(check_location_name("Slow Guy - Toy Shop", lang)),
            lambda state: state.has_any({check_item_name("Red Eye", world), check_item_name("Blue Eye", world), check_item_name("Red Shoes", world)}, player) or has_sky_scroll_complex(state, world))
        set_rule(world.get_location(check_location_name("Stomp Golem - Toy Shop", lang)),
            lambda state: state.has_any({check_item_name("Red Eye", world), check_item_name("Red Shoes", world)}, player) or has_sky_scroll_complex(state, world))
        set_rule(world.get_location(check_location_name("GiAnt - Toy Shop", lang)),
            lambda state: has_wind_scroll(state, world) and has_fire_boss_core(state, world))
        set_rule(world.get_location(check_location_name("Queen Ant - Toy Shop", lang)),
            lambda state: state.can_reach_region("Queen Ant Arena", player))
            #lambda state: has_wind_scroll(state, world) and has_fire_boss_core(state, world) and has_wind_boss_core(state, world))
        set_rule(world.get_location(check_location_name("GiAnt - Toy Shop", lang)),
            lambda state: state.can_reach_region("Upper Mines Ant Parade", player))
        set_rule(world.get_location(check_location_name("Toad Stool - Toy Shop", lang)),
            lambda state: can_enter_mine(state, world) or state.can_reach_region("Upper Mines", player))
        set_rule(world.get_location(check_location_name("Colonel Capricola - Toy Shop", lang)),
            lambda state: state.can_reach_region("Frost Dragon Arena", player))
        if(options.quest_item_sanity.value == True):
            set_rule(world.get_location(check_location_name("Relic Vambee - Toy Shop", lang)),
                lambda state: state.can_reach_region("Restaurant Basement", player))
            set_rule(world.get_location(check_location_name("Bowler - Toy Shop", lang)),
                lambda state: state.can_reach_region("Restaurant Basement Bowling 1", player))
            set_rule(world.get_location(check_location_name("Cure Worm - Toy Shop", lang)),
                lambda state: state.can_reach_region("Mine Entrance", player))
            set_rule(world.get_location(check_location_name("Topo - Toy Shop", lang)),
                lambda state: state.can_reach_region("Steamwood 2", player))
            set_rule(world.get_location(check_location_name("Vambee Soldier - Toy Shop", lang)),
                lambda state: has_rescued_tim(state, world) and can_double_jump(state, world))
            set_rule(world.get_location(check_location_name("Bubbles - Toy Shop", lang)),
                lambda state: has_rescued_tim(state, world) and can_double_jump(state, world))
    if(options.tech_sanity.value == True):
        set_rule(world.get_location(check_location_name("Improved Fusion (Artisan) - Allucaneet Castle", lang)),
            lambda state: state.has(check_item_name("Artisan", world), player))
        set_rule(world.get_location(check_location_name("Dashing Pierce (Maid) - Allucaneet Castle", lang)),
            lambda state: state.has(check_item_name("Maid", world), player))
        set_rule(world.get_location(check_location_name("Shish Kebab (Clown) - Allucaneet Castle", lang)),
            lambda state: state.has(check_item_name("Acrobat", world), player) and has_orange(state, world))
        set_rule(world.get_location(check_location_name("Crosswise Cut (KnightB) - Allucaneet Castle", lang)),
            lambda state: can_fight_skullpion(state, world))
        set_rule(world.get_location(check_location_name("Tenderize (KnightA) - Allucaneet Castle", lang)),
            lambda state: state.has(check_item_name("KnightA", world), player))
        set_rule(world.get_location(check_location_name("Desperado Attack (KnightC) - Allucaneet Castle", lang)),
            lambda state: state.has(check_item_name("KnightC", world), player) and state.has(check_item_name("Crosswise Cut", world), player))
        set_rule(world.get_location(check_location_name("Rumparoni Special (KnightD) - Allucaneet Castle", lang)),
            lambda state: state.has(check_item_name("KnightD", world), player))
    


             