from typing import Dict, TYPE_CHECKING

from worlds.generic.Rules import set_rule, forbid_item, add_rule
from BaseClasses import CollectionState
if TYPE_CHECKING:
    from . import BFMWorld

def saved_everyone(state: CollectionState, world: "BFMWorld") -> bool:
    return state.has_all({"Guard", "Seer", "Hawker", "MusicianB", "SoldierA", "Acrobat"}, world.player)