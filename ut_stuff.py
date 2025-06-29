#taken from Tunic 
from typing import Any, TYPE_CHECKING

#from .options import 

if TYPE_CHECKING:
    from . import BFMWorld


def setup_options_from_slot_data(world: "BFMWorld") -> None:
    if hasattr(world.multiworld, "re_gen_passthrough"):
        if "BFM" in world.multiworld.re_gen_passthrough:
            world.using_ut = True
            world.passthrough = world.multiworld.re_gen_passthrough["BFM"]
            #world.options.start_with_sword.value = world.passthrough["start_with_sword"]
        else:
            world.using_ut = False
    else:
        world.using_ut = False