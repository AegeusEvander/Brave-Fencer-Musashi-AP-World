#taken from Tunic 
from typing import Any, TYPE_CHECKING
#from .options import 
#from .options import BFMOptions, LuminaRandomized

if TYPE_CHECKING:
    from . import BFMWorld


def setup_options_from_slot_data(world: "BFMWorld") -> None:
    if hasattr(world.multiworld, "re_gen_passthrough"):
        if "Brave Fencer Musashi" in world.multiworld.re_gen_passthrough:
            world.using_ut = True
            world.passthrough = world.multiworld.re_gen_passthrough["Brave Fencer Musashi"]
            world.options.goal.value = world.passthrough["goal"]
            world.options.npc_goal.value = world.passthrough["npc_goal"]
            world.options.starting_hp.value = world.passthrough["starting_hp"]
            world.options.max_hp_logic.value = world.passthrough["max_hp_logic"]
            world.options.lumina_randomzied.value = world.passthrough["lumina_randomzied"]
            world.options.bakery_sanity.value = world.passthrough["bakery_sanity"]
            world.options.restaurant_sanity.value = world.passthrough["restaurant_sanity"]
            world.options.grocery_sanity.value = world.passthrough["grocery_sanity"]
            world.options.grocery_sanity_heal_logic.value = world.passthrough["grocery_sanity_heal_logic"]
            world.options.toy_sanity.value = world.passthrough["toy_sanity"]
            world.options.tech_sanity.value = world.passthrough["tech_sanity"]
            world.options.scroll_sanity.value = world.passthrough["scroll_sanity"]
            world.options.sky_scroll_logic.value = world.passthrough["sky_scroll_logic"]
            world.options.core_sanity.value = world.passthrough["core_sanity"]
            world.options.level_sanity.value = world.passthrough["level_sanity"]
            world.options.xp_gain.value = world.passthrough["xp_gain"]
            world.options.early_skullpion.value = world.passthrough["early_skullpion"]
        else:
            world.using_ut = False
    else:
        world.using_ut = False