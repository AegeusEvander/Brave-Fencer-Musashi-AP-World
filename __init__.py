from typing import Dict, List, Any, Tuple, TypedDict, ClassVar, Union, Set, TextIO
from logging import warning
from BaseClasses import Region, Location, Item, Tutorial, ItemClassification, MultiWorld, CollectionState
from .items import item_name_to_id, item_table, item_name_groups, slot_data_item_names
from .locations import location_table, location_name_groups, standard_location_name_to_id, sphere_one
from .rules import saved_everyone, set_region_rules, set_location_rules
from .regions import bfm_regions
from .options import BFMOptions, LuminaRandomized
from worlds.AutoWorld import WebWorld, World
from Options import PlandoConnection, OptionError
from settings import Group, Bool
from .utils import Constants
# This registers the client. The comment ignores "unused import" linter messages
from .client import BFMClient  # type: ignore  # noqa
from .version import __version__

class BFMWeb(WebWorld):
    theme = "grass"

    setup_en = Tutorial(
        "Multiworld Setup Guide",
        f"A guide to playing {Constants.GAME_NAME} with Archipelago.",
        "English",
        "setup_en.md",
        "setup/en",
        ["AegeusEvander"]
    )

    tutorials = [setup_en]


class BFMItem(Item):
    game: str = Constants.GAME_NAME


class BFMLocation(Location):
    game: str = Constants.GAME_NAME

class BFMWorld(World):
    """Brave Fencer Musashi is a PlayStation RPG where you must rescue the Allucaneat Kingdom from the tyranny of the Thirstquencher Empire."""
    game: str = Constants.GAME_NAME
    options_dataclass =  BFMOptions
    options: BFMOptions
    required_client_version = (0, 0, 1)
    web = BFMWeb()


    item_name_groups = item_name_groups
    location_name_groups = location_name_groups

    item_name_to_id = item_name_to_id
    location_name_to_id = standard_location_name_to_id.copy()
    
    player_location_table: Dict[str, int]
    slot_data_items: List[BFMItem]

    # for the local_fill option
    fill_items: List[BFMItem]
    fill_locations: List[Location]
    amount_to_local_fill: int

    # so we only loop the multiworld locations once
    # if these are locations instead of their info, it gives a memory leak error
    item_link_locations: Dict[int, Dict[str, List[Tuple[int, str]]]] = {}
    player_item_link_locations: Dict[str, List[Location]]

    def generate_early(self) -> None:
        self.player_location_table = standard_location_name_to_id.copy()

    def create_regions(self) -> None:
        
        for region_name in bfm_regions:
                region = Region(region_name, self.player, self.multiworld)
                self.multiworld.regions.append(region)

        for region_name, exits in bfm_regions.items():
            region = self.get_region(region_name)
            region.add_exits(exits)

        for location_name, location_id in self.player_location_table.items():
            region = self.get_region(location_table[location_name].region)
            location = BFMLocation(self.player, location_name, location_id, region)
            region.locations.append(location)

        self.multiworld.completion_condition[self.player] = lambda state: state.has_all({"Guard", "Seer", "Hawker", "Maid", "MusicianB", "SoldierA", "MercenC", "CarpentA", "KnightB", "Shepherd", "Bailiff", "CarpentB", "Weaver", "SoldierB", "KnightA", "CookA", "Acrobat", "MercenB", "CarpentC", "Knitter", "MercenA", "Chief", "KnightC", "Doctor", "Librarian"}, self.player)

    def fill_slot_data(self) -> Dict[str, Any]:
        return {
            Constants.GENERATED_WITH_KEY: __version__,
            #Constants.GAME_OPTIONS_KEY: self.options.serialize(),
            Constants.DEATHLINK_OPTION_KEY: self.options.death_link.value
        }

    def create_item(self, name: str, classification: ItemClassification = None) -> BFMItem:
        item_data = item_table[name]
        # evaluate alternate classifications based on options
        # it'll choose whichever classification isn't None first in this if else tree
        itemclass: ItemClassification = item_data.classification
        return BFMItem(name, itemclass, self.item_name_to_id[name], self.player)

    def create_items(self) -> None:
        bfm_items: List[BFMItem] = []
        self.slot_data_items = []

        items_to_create: Dict[str, int] = {item: data.quantity_in_item_pool for item, data in item_table.items()}
        for item, quantity in items_to_create.items():
            for _ in range(quantity):
                bfm_items.append(self.create_item(item))

        for bfm_item in bfm_items:
            if bfm_item.name in slot_data_item_names:
                self.slot_data_items.append(bfm_item)

        self.multiworld.itempool += bfm_items
    
    def set_rules(self) -> None:
        set_region_rules(self)
        set_location_rules(self)


        
