from typing import Dict, List, Any, Tuple, TypedDict, ClassVar, Union, Set, TextIO
from logging import warning
from BaseClasses import Region, Location, Item, Tutorial, ItemClassification, MultiWorld, CollectionState
from .items import item_name_to_id, item_table, item_name_groups, slot_data_item_names, jp_id_offset, item_base_id, item_id_to_name
from .locations import location_table, location_name_groups, standard_location_name_to_id, sphere_one, en_standard_location_name_to_id
from .rules import saved_everyone, set_region_rules, set_location_rules, can_fight_skullpion, has_all_scrolls, has_ex_drink, has_water_scroll, can_identify_gondola_gizmo, can_fight_frost_dragon, has_wind_scroll, can_enter_frozen_palace, has_earth_boss_core, has_wind_boss_core, has_fire_boss_core
from .regions import bfm_regions
from .options import BFMOptions
from worlds.AutoWorld import WebWorld, World
from Options import PlandoConnection, OptionError
from settings import Group, Bool
from .hair_color import hair_color_options, new_hair_color
from .utils import Constants
# This registers the client. The comment ignores "unused import" linter messages
from .client import BFMClient  # type: ignore  # noqa
from .version import __version__
from . import ut_stuff
import string

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
    required_client_version = (0, 2, 5)
    web = BFMWeb()
    hair_selection: str = hair_color_options[2]

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

    #taken from Tunic for UT
    using_ut: bool = False  # so we can check if we're using UT only once
    passthrough: Dict[str, Any]
    ut_can_gen_without_yaml = True  # class var that tells it to ignore the player yaml
    #tracker_world: ClassVar = ut_stuff.tracker_world

    def generate_early(self) -> None:
        ut_stuff.setup_options_from_slot_data(self)

        self.player_location_table = en_standard_location_name_to_id.copy()
        """
        if(self.using_ut == True):
            item_id_to_name: Dict[int, str] = {(item_base_id * (data.item_group == "NPC") + data.item_id_offset): name for name, data in item_table.items()}
            jp_item_id_to_name: Dict[int, str] = {(item_base_id * (data.item_group == "NPC") + data.item_id_offset + jp_id_offset): name for name, data in item_table.items()}
            item_id_to_name.update(jp_item_id_to_name)

            item_name_to_id: Dict[str, int] = {name: item_base_id * (data.item_group == "NPC") + data.item_id_offset for name, data in item_table.items()}
            jp_item_name_to_id: Dict[str, int] = {data.jp_name: item_base_id * (data.item_group == "NPC") + data.item_id_offset for name, data in item_table.items()}
            item_name_to_id.update(jp_item_name_to_id)
            self.item_name_to_id = item_name_to_id"""

        if(self.options.lumina_randomzied.value == False):
            del self.player_location_table["Lumina - Spiral Tower"]
        if(self.options.bakery_sanity.value == False):
            for name in location_name_groups["Bakery"]:
                del self.player_location_table[name]
        if(self.options.restaurant_sanity.value == False):
            for name in location_name_groups["Restaurant"]:
                del self.player_location_table[name]
        if(self.options.grocery_sanity.value == False):
            for name in location_name_groups["Grocery"]:
                del self.player_location_table[name]
        if(self.options.toy_sanity.value == False):
            for name in location_name_groups["Toy Shop"]:
                del self.player_location_table[name]
        if(self.options.tech_sanity.value == False):
            for name in location_name_groups["Tech"]:
                del self.player_location_table[name]
        if(self.options.scroll_sanity.value == False):
            for name in location_name_groups["Scroll"]:
                del self.player_location_table[name]
        if(self.options.core_sanity.value == False):
            for name in location_name_groups["Core"]:
                del self.player_location_table[name]
        if(self.options.level_sanity.value == False or self.options.xp_gain.value == 1):
            self.options.level_sanity.value = False
            for name in location_name_groups["Level"]:
                del self.player_location_table[name]
        
        if self.options.hair_color_selection == 1:
            if len(self.options.custom_hair_color_selection.value) == 6:
                if(all(s in string.hexdigits for s in self.options.custom_hair_color_selection.value)):
                    self.hair_selection = self.options.custom_hair_color_selection.value.upper()
                else:
                    self.hair_selection = hair_color_options[2]
            else:
                self.hair_selection = hair_color_options[2]
        else:
            self.hair_selection = hair_color_options[self.options.hair_color_selection]

        if(self.options.starting_hp.value == 1):
            self.options.death_link.value = False
        #if(self.options.set_lang.value == 2):
            #temp_locations: Dict[str, int] = {location_table[location_name].jp_name: location_id for location_name, location_id in self.player_location_table.items()}
            #self.player_location_table = temp_locations
        
    def create_regions(self) -> None:
        
        for region_name in bfm_regions:
                region = Region(region_name, self.player, self.multiworld)
                self.multiworld.regions.append(region)

        for region_name, exits in bfm_regions.items():
            region = self.get_region(region_name)
            region.add_exits(exits)

        for location_name, location_id in self.player_location_table.items():
            region = self.get_region(location_table[location_name].region)
            final_location_name = location_name
            #if(self.options.set_lang.value == 2):
            #    if(self.options.spoiler_items_in_english.value == True):
            #        return BFMItem(self.item_id_to_name[item_name_to_id[name]-jp_id_offset], itemclass, self.item_name_to_id[name], self.player)
            #return BFMItem(name, itemclass, self.item_name_to_id[name], self.player)
            if(self.options.set_lang.value == 2):
                if(self.options.spoiler_items_in_english.value == False or self.using_ut == True):
                    final_location_name = location_table[location_name].jp_name
            location = BFMLocation(self.player, final_location_name, location_id + ((self.options.set_lang.value == 2) * jp_id_offset), region)
            region.locations.append(location)

        if(self.options.goal.value == 1): #save all NPCs
            self.multiworld.completion_condition[self.player] = lambda state: state.has_group("NPC", self.player, 35)
        elif(self.options.goal.value == 2): #save x NPCs
            self.multiworld.completion_condition[self.player] = lambda state: state.has_group("NPC", self.player, self.options.npc_goal.value)
        elif(self.options.goal.value == 3): #defeat earth crest guardian
            self.multiworld.completion_condition[self.player] = lambda state: can_fight_skullpion(state, self)
        elif(self.options.goal.value == 4): #defeat water crest guardian
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_region("Relic Keeper Arena", self.player)
            #self.multiworld.completion_condition[self.player] = lambda state: can_fight_skullpion(state, self) and has_water_scroll(state, self)
        elif(self.options.goal.value == 5): #defeat fire crest guardian
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_region("Frost Dragon Arena", self.player)
            #self.multiworld.completion_condition[self.player] = lambda state: can_enter_frozen_palace(state, self) and can_identify_gondola_gizmo(state, self) and can_fight_skullpion(state, self) and can_fight_frost_dragon(state, self)
        elif(self.options.goal.value == 6): #defeat wind crest guardian
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_region("Queen Ant Arena", self.player)
            #self.multiworld.completion_condition[self.player] = lambda state: can_enter_frozen_palace(state, self) and can_identify_gondola_gizmo(state, self) and can_fight_skullpion(state, self) and can_fight_frost_dragon(state, self) and has_wind_scroll(state, self) and has_fire_boss_core(state, self)
        elif(self.options.goal.value == 7 or self.options.goal.value == 8): #defeat sky crest guardian or final boss
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_region("Soda Fountain", self.player)
            
            #self.multiworld.completion_condition[self.player] = lambda state: has_all_scrolls(state, self) and has_earth_boss_core(state, self) and has_wind_boss_core(state, self) and has_ex_drink(state, self) and state.has_all({"Lumina", "Bracelet"}, self.player)
        #self.multiworld.completion_condition[self.player] = lambda state: state.has_all({"Guard", "Seer", "Hawker", "Maid", "MusicianB", "SoldierA", "MercenC", "CarpentA", "KnightB", "Shepherd", "Bailiff", "Taster", "CarpentB", "Weaver", "SoldierB", "KnightA", "CookA", "Acrobat", "MercenB", "Janitor", "Artisan", "CarpentC", "MusicianC", "Knitter", "Chef", "MercenA", "Chief", "CookB", "Conductor", "Butcher", "KnightC", "Doctor", "KnightD", "Alchemist", "Librarian"}, self.player)
        #self.multiworld.completion_condition[self.player] = lambda state: saved_everyone(state, self.world)

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = {
            "version": __version__,
            "set_lang": self.options.set_lang.value,
            "goal": self.options.goal.value,
            "npc_goal": self.options.npc_goal.value,
            "starting_hp": self.options.starting_hp.value,
            "max_hp_logic": self.options.max_hp_logic.value,
            "deathlink": self.options.death_link.value,
            "hair_color": self.hair_selection,
            "lumina_randomzied": self.options.lumina_randomzied.value,
            "bakery_sanity": self.options.bakery_sanity.value,
            "restaurant_sanity": self.options.restaurant_sanity.value,
            "grocery_sanity": self.options.grocery_sanity.value,
            "grocery_s_revive": self.options.grocery_s_revive.value,
            "grocery_sanity_heal_logic": self.options.grocery_sanity_heal_logic.value,
            "toy_sanity": self.options.toy_sanity.value,
            "tech_sanity": self.options.tech_sanity.value,
            "scroll_sanity": self.options.scroll_sanity.value,
            "sky_scroll_logic": self.options.sky_scroll_logic.value,
            "core_sanity": self.options.core_sanity.value,
            "level_sanity": self.options.level_sanity.value,
            "level_bundles": self.options.level_bundles.value,
            "stat_gain_modifier": self.options.stat_gain_modifier.value,
            "xp_gain": self.options.xp_gain.value,
            "xp_gain_mind": self.options.xp_gain_mind.value,
            "early_skullpion": self.options.early_skullpion.value,
            "boulder_chase_zoom": self.options.boulder_chase_zoom.value,
            "leno_sniff_modifier": self.options.leno_sniff_modifier.value,
            "skip_minigame_follow_leno": self.options.skip_minigame_follow_leno.value,
            "raft_hp": self.options.raft_hp.value,
            "raft_difficulty": self.options.raft_difficulty.value,
            "raft_regrow": self.options.raft_regrow.value,
            "steamwood_timer": self.options.steamwood_timer.value,
            "steamwood_valve_timer": self.options.steamwood_valve_timer.value,
            "steamwood_disable_countdown": self.options.steamwood_disable_countdown.value,
            "steamwood_number_valves": self.options.steamwood_number_valves.value,
            "steamwood_random_valves": self.options.steamwood_random_valves.value,
            "steamwood_pressure_rise_rate": self.options.steamwood_pressure_rise_rate.value,
            "steamwood_progress_lost": self.options.steamwood_progress_lost.value,
            "steamwood_width_of_ok_pressure": self.options.steamwood_width_of_ok_pressure.value,
            "steamwood_valve_progress_modifier": self.options.steamwood_valve_progress_modifier.value,
            "steamwood_no_fail_over_pressure": self.options.steamwood_no_fail_over_pressure.value,
            "steamwood_elevator_logic": self.options.steamwood_elevator_logic.value,
            "aqualin_timer": self.options.aqualin_timer.value,
            "restaurant_teleport_maze_no_fail": self.options.restaurant_teleport_maze_no_fail.value,
            "church_fight_time_modifier": self.options.church_fight_time_modifier.value,
            "skip_minigame_town_on_fire": self.options.skip_minigame_town_on_fire.value,
            "skip_to_frost_palace": self.options.skip_to_frost_palace.value,
            "skip_minigame_ant_gondola": self.options.skip_minigame_ant_gondola.value,
            "skip_over_calendar_maze": self.options.skip_over_calendar_maze.value,
            "topo_dance_battle_logic": self.options.topo_dance_battle_logic.value,
            "soda_fountain_boss_rush": self.options.soda_fountain_boss_rush.value,
            "fast_walk": self.options.fast_walk.value
        }
        return slot_data

    def create_item(self, name: str, classification: ItemClassification = None) -> BFMItem:
        if(not name in item_table):
            item_data = item_table[self.item_id_to_name[self.item_name_to_id[name]-jp_id_offset]]
        else:
            item_data = item_table[name]
        # evaluate alternate classifications based on options
        # it'll choose whichever classification isn't None first in this if else tree
        itemclass: ItemClassification = item_data.classification
        #if(self.using_ut == True):
        #    return BFMItem(name, itemclass, self.item_name_to_id[name], self.player)
        #if(self.options.set_lang.value == 2):
        #    print(item_data.jp_name)
        #    return BFMItem(item_data.jp_name, itemclass, self.item_name_to_id[item_data.jp_name], self.player)
        #print(name)
        if(self.using_ut == True):
            if(not name in item_table):
                return BFMItem(self.item_id_to_name[item_name_to_id[name]-jp_id_offset], itemclass, self.item_name_to_id[name]-jp_id_offset, self.player)
        if(self.options.set_lang.value == 2):
            if(self.options.spoiler_items_in_english.value == True):
                return BFMItem(self.item_id_to_name[item_name_to_id[name]-jp_id_offset], itemclass, self.item_name_to_id[name], self.player)
        return BFMItem(name, itemclass, self.item_name_to_id[name], self.player)
        #return BFMItem(item_data.jp_name, itemclass, self.item_name_to_id[name], self.player)

    def create_items(self) -> None:
        bfm_items: List[BFMItem] = []
        self.slot_data_items = []

        items_to_create: Dict[str, int] = {item: data.quantity_in_item_pool for item, data in item_table.items()}
        if(self.options.lumina_randomzied.value == False):
            del items_to_create["Lumina"]
        if(self.options.bakery_sanity.value == False):
            del items_to_create["Progressive Bread"]
        #print(item_name_groups)
        if(self.options.restaurant_sanity.value == False):
            for name in item_name_groups["Restaurant"]:
                if(name in item_table):
                    del items_to_create[name] 
        if(self.options.grocery_sanity.value == False):
            for name in item_name_groups["Grocery"]:
                if(name in item_table):
                    del items_to_create[name] 
        if(self.options.toy_sanity.value == False):
            for name in item_name_groups["Toy Shop"]:
                if(name in item_table):
                    del items_to_create[name] 
        if(self.options.tech_sanity.value == False):
            for name in item_name_groups["Tech"]:
                if(name in item_table):
                    del items_to_create[name] 
        if(self.options.scroll_sanity.value == False):
            for name in item_name_groups["Scroll"]:
                if(name in item_table):
                    del items_to_create[name] 
        if(self.options.core_sanity.value == False):
            for name in item_name_groups["Core"]:
                if(name in item_table):
                    del items_to_create[name] 
        if(self.options.level_sanity.value == False or self.options.xp_gain.value == 1):
            for name in item_name_groups["Level"]:
                if(name in item_table):
                    del items_to_create[name] 

        if(self.options.level_sanity.value == True and self.options.xp_gain.value != 1 and self.options.level_bundles.value != 29):
            for name in item_name_groups["Level"]:
                if(name in item_table):
                    items_to_create[name] = self.options.level_bundles.value

        if(self.options.starting_hp.value == 1):
            items_to_create["Longevity Berry"] = 0

        for item, quantity in items_to_create.items():
            for _ in range(quantity):
                if(self.options.set_lang.value == 2):
                    bfm_items.append(self.create_item(item_table[item].jp_name))
                else:
                    bfm_items.append(self.create_item(item))

        total_locations = len(self.multiworld.get_unfilled_locations(self.player))

        for _ in range(total_locations - len(bfm_items)):
            bfm_items.append(self.create_filler())

        for bfm_item in bfm_items:
            if bfm_item.name in slot_data_item_names:
                self.slot_data_items.append(bfm_item)

        self.multiworld.itempool += bfm_items

        if (self.options.early_skullpion.value == True):
            if(self.options.set_lang.value == 2 and self.options.spoiler_items_in_english.value == False):
                self.multiworld.early_items[self.player][item_table["SoldierA"].jp_name] = 1
                self.multiworld.early_items[self.player][item_table["MercenC"].jp_name] = 1
                self.multiworld.early_items[self.player][item_table["CarpentA"].jp_name] = 1
                self.multiworld.early_items[self.player][item_table["KnightB"].jp_name] = 1
                if(self.options.lumina_randomzied.value == True):
                    self.multiworld.early_items[self.player][item_table["Lumina"].jp_name] = 1
            else:
                self.multiworld.early_items[self.player]["SoldierA"] = 1
                self.multiworld.early_items[self.player]["MercenC"] = 1
                self.multiworld.early_items[self.player]["CarpentA"] = 1
                self.multiworld.early_items[self.player]["KnightB"] = 1
                if(self.options.lumina_randomzied.value == True):
                    self.multiworld.early_items[self.player]["Lumina"] = 1

    def get_filler_item_name(self) -> str:
        return "1000 Drans"

    def create_filler(self) -> "Item":
        if(self.options.set_lang.value == 2):
            return self.create_item(item_table[self.get_filler_item_name()].jp_name)
        return self.create_item(self.get_filler_item_name())

    def set_rules(self) -> None:
        print(self.options.set_lang.value)
        set_region_rules(self)
        set_location_rules(self, self.options.set_lang.value == 2 and (self.options.spoiler_items_in_english.value == False or self.using_ut == True))

    # Taken from Tunic APWorld https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/tunic/__init__.py#L713
    # for the universal tracker, doesn't get called in standard gen
    # docs: https://github.com/FarisTheAncient/Archipelago/blob/tracker/worlds/tracker/docs/re-gen-passthrough.md
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        # returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
        # we are using re_gen_passthrough over modifying the world here due to complexities with ER
        return slot_data
        
