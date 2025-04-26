from typing import Dict, TYPE_CHECKING

from worlds.generic.Rules import set_rule, forbid_item, add_rule
from BaseClasses import CollectionState
if TYPE_CHECKING:
    from . import BFMWorld


def can_fight_skullpion(state: CollectionState, world: "BFMWorld") -> bool:
    return state.has_all({"SoldierA", "MercenC", "CarpentA", "KnightB"}, world.player)

def can_enter_frozen_palace(state: CollectionState, world: "BFMWorld") -> bool:
    return state.has_all({"MercenA", "MercenB", "MercenC"}, world.player)

def can_identify_gondola_gizmo(state: CollectionState, world: "BFMWorld") -> bool:
    return state.has_all({"CarpentA", "CarpentB", "CarpentC"}, world.player)

def saved_everyone(state: CollectionState, world: "BFMWorld") -> bool:
    return state.has_all({"Guard", "Seer", "Hawker", "Maid", "MusicianB", "SoldierA", "MercenC", "CarpentA", "KnightB", "Shepherd", "Bailiff", "Taster", "CarpentB", "Weaver", "SoldierB", "KnightA", "CookA", "Acrobat", "MercenB", "Janitor", "Artisan", "CarpentC", "MusicianC", "Knitter", "Chef", "MercenA", "Chief", "CookB", "Conductor", "Butcher", "KnightC", "Doctor", "KnightD", "Alchemist", "Librarian"}, world.player)


def set_region_rules(world: "BFMWorld") -> None:
    player = world.player
    options = world.options

    world.get_entrance("Grillin Village -> Mine Entrance").access_rule = \
        lambda state: can_fight_skullpion(state, world)
    world.get_entrance("Grillin Village -> Restaurant Basement").access_rule = \
        lambda state: can_fight_skullpion(state, world)
    world.get_entrance("Meandering Forest -> Frozen Palace Entrance").access_rule = \
        lambda state: can_enter_frozen_palace(state, world) and can_identify_gondola_gizmo(state, world) and can_fight_skullpion(state, world)
    world.get_entrance("Upper Grillin Village -> Upper Mines").access_rule = \
        lambda state: can_enter_frozen_palace(state, world) and can_identify_gondola_gizmo(state, world) and can_fight_skullpion(state, world)

def set_location_rules(world: "BFMWorld") -> None:
    player = world.player

    set_rule(world.get_location("Knitter Bincho - Twinpeak Path to Skullpion"),
             lambda state: can_fight_skullpion(state, world))