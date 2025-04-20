from typing import Dict, TYPE_CHECKING

from worlds.generic.Rules import set_rule, forbid_item, add_rule
from BaseClasses import CollectionState
if TYPE_CHECKING:
    from . import BFMWorld


def can_fight_skullpion(state: CollectionState, world: "BFMWorld") -> bool:
    return state.has_all({"SoldierA", "MercenC", "CarpentA", "KnightB"}, world.player)

def saved_everyone(state: CollectionState, world: "BFMWorld") -> bool:
    return state.has_all({"Guard", "Seer", "Hawker", "Maid", "MusicianB", "SoldierA", "MercenC", "CarpentA", "KnightB", "Shepherd", "Bailiff", "CarpentB", "Weaver", "SoldierB", "KnightA", "CookA", "Acrobat", "MercenB", "CarpentC", "Knitter", "MercenA", "Chief", "KnightC", "Doctor", "Librarian"}, world.player)


def set_region_rules(world: "BFMWorld") -> None:
    player = world.player
    options = world.options

    world.get_entrance("Grillin Village -> Mine Entrance").access_rule = \
        lambda state: can_fight_skullpion(state, world)
    world.get_entrance("Grillin Village -> Restaurant Basement").access_rule = \
        lambda state: can_fight_skullpion(state, world)

def set_location_rules(world: "BFMWorld") -> None:
    player = world.player

    set_rule(world.get_location("Knitter Bincho - Twinpeak Path to Skullpion"),
             lambda state: can_fight_skullpion(state, world))