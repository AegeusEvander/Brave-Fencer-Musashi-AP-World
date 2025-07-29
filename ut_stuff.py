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
            world.options.lumina_randomzied.value = world.passthrough["lumina_randomzied"]
            world.options.bakery_sanity.value = world.passthrough["bakery_sanity"]
            world.options.restaurant_sanity.value = world.passthrough["restaurant_sanity"]
            world.options.grocery_sanity.value = world.passthrough["grocery_sanity"]
            world.options.toy_sanity.value = world.passthrough["toy_sanity"]
            world.options.tech_sanity.value = world.passthrough["tech_sanity"]
        else:
            world.using_ut = False
    else:
        world.using_ut = False