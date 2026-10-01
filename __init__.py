from typing import Dict, List, Any, Tuple, TypedDict, ClassVar, Union, Set, TextIO
from logging import warning
from BaseClasses import Region, Location, Item, Tutorial, ItemClassification, MultiWorld, CollectionState, EntranceType
from .items import item_name_to_id, item_table, item_name_groups, jp_id_offset, item_base_id, item_id_to_name
from .locations import location_table, location_name_groups, standard_location_name_to_id, en_standard_location_name_to_id
from .rulebuilder import set_rules
from .rulebuilder_er import set_er_rules
from .rules import set_region_rules, set_location_rules
from .regions import bfm_regions, bfm_er_static_regions, region_alias, bfm_er_static_one_way_connections,short_name_substitute,expand_region_id,region_alias_reverse
from .options import BFMOptions
from worlds.AutoWorld import WebWorld, World
from Options import PlandoConnection, OptionError
from settings import Group, Bool
from .hair_color import hair_color_options, new_hair_color, default_hair_color
from .utils import Constants
#import Utils
from Utils import visualize_regions, is_windows, messagebox, open_file, tuplize_version, async_start
# This registers the client. The comment ignores "unused import" linter messages
from .client import BFMClient  # type: ignore  # noqa
from .version import __version__
from .trap import trap_weight
#from . import ut_stuff
from .tracker import UTMxin, setup_options_from_slot_data
import string
import math
from worlds.LauncherComponents import Component, Type, components
from .launch import run_client
from .settings import BFMSettings
from .portals import bfm_portals, BFMConnection, bfm_portals_short_to_door_names, bfm_portals_door_names_to_short,bfm_portals_short_to_door_names_no_ignore
from entrance_rando import randomize_entrances, disconnect_entrance_for_randomization, ERPlacementState, EntranceRandomizationError


components.append(
    Component(
        "BFM Client",
        func=run_client,
        game_name=Constants.GAME_NAME,
        component_type=Type.CLIENT,
        supports_uri=True,
    )
)

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

class BFMWorld(UTMxin, World):
    """Brave Fencer Musashi is a PlayStation RPG where you must rescue the Allucaneat Kingdom from the tyranny of the Thirstquencher Empire."""
    game: str = Constants.GAME_NAME
    options_dataclass =  BFMOptions
    options: BFMOptions
    settings_key = "brave_fencer_musashi_settings"
    settings: ClassVar[BFMSettings]
    required_client_version = (0, 6, 7)
    web = BFMWeb()
    hair_selection: str = hair_color_options[2]
    scalp_selection: str = hair_color_options[2]

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

    entrance_ids_connected: List[Tuple[str,str]] = []
    er_pairings: Dict[str,str] = {}

    def generate_early(self) -> None:
        tracker.setup_options_from_slot_data(self)
        if(getattr(self.multiworld, "generation_is_fake", False)):
            warning("Fake GEN")
        if(self.using_ut == True):
            warning(" >UT Gen<")

        self.player_location_table = en_standard_location_name_to_id.copy()


        if(self.options.entrance_rando.value):
            if(self.options.sky_scroll_logic.value == 1):
                self.options.sky_scroll_logic.value = 2
            self.options.toy_sanity.value = False
            self.options.playthrough_method.value = 2
            #self.options.time_sanity.value = False
            #self.options.level_sanity.value = False
            #self.options.scroll_sanity.value = True
            self.options.skip_over_calendar_maze.value = False
            self.options.skip_minigame_ant_gondola.value = False
            self.options.soda_fountain_boss_rush.value = False
            self.options.force_soda_fountain_last.value = False
            self.options.restaurant_teleport_maze_no_fail.value = False
            self.options.fast_walk.value = True
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
        if(self.options.quest_item_sanity.value == False):
            for name in location_name_groups["Quest"]:
                del self.player_location_table[name]
        if(self.options.bp_sanity.value == False):
            for name in location_name_groups["BP"]:
                del self.player_location_table[name]
        if(self.options.time_sanity.value == False):
            for name in location_name_groups["Time"]:
                del self.player_location_table[name]
            for name in location_name_groups["Time Combined"]:
                del self.player_location_table[name]
        else:
            if(self.options.time_sanity_settings.value == 2):
                for name in location_name_groups["Time"]:
                    del self.player_location_table[name]
            else:
                for name in location_name_groups["Time Combined"]:
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

        if self.options.scalp_color_selection == 1:
            if len(self.options.custom_scalp_color_selection.value) == 6:
                if(all(s in string.hexdigits for s in self.options.custom_scalp_color_selection.value)):
                    self.scalp_selection = self.options.custom_scalp_color_selection.value.upper()
                else:
                    self.scalp_selection = self.hair_selection
            else:
                self.scalp_selection = self.hair_selection
        elif self.options.scalp_color_selection == 2:
            self.scalp_selection = self.hair_selection
        elif self.options.scalp_color_selection == 3:
            self.scalp_selection = default_hair_color
        else:
            self.scalp_selection = hair_color_options[self.options.scalp_color_selection - 2]

        if(self.options.starting_hp.value == 1):
            self.options.death_link.value = False

        if(self.options.early_skullpion.value == True):
            if(self.options.time_sanity.value == True and self.options.lumina_randomzied.value == True and self.options.bakery_sanity.value == False):
                warning("extremely restrictive settings are turned on with early skullpion, turning off early_skullpion")
                self.options.early_skullpion.value = False

        #if(self.options.set_lang.value == 2):
            #temp_locations: Dict[str, int] = {location_table[location_name].jp_name: location_id for location_name, location_id in self.player_location_table.items()}
            #self.player_location_table = temp_locations
        
    def create_regions(self) -> None:
        if(self.options.entrance_rando.value == False):
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
        else:
            #for short_name, door_name in bfm_portals_short_to_door_names.items():
            #    region = Region(door_name, self.player, self.multiworld)
            #    self.multiworld.regions.append(region)
            #region = Region("Menu", self.player, self.multiworld)
            #self.multiworld.regions.append(region)
            region_names = []
            self.entrance_ids_connected = []
            for id, connection_data in bfm_portals.items():
                num_not_ignore = 0
                for connection in connection_data.connections:
                    if(connection.connection_group != "Ignore" and not connection.door_name in region_names):
                        region_names.append(connection.door_name)
                        num_not_ignore = num_not_ignore + 1
                        region = Region(connection.door_name, self.player, self.multiworld)
                        self.multiworld.regions.append(region)
                if(not id in bfm_er_static_regions and num_not_ignore > 0):
                    if(connection_data.region in region_alias):
                        if(not region_alias[connection_data.region] in region_names):
                            region_names.append(region_alias[connection_data.region])
                            region = Region(region_alias[connection_data.region], self.player, self.multiworld)
                            self.multiworld.regions.append(region)
                    elif(not connection_data.region in region_names):
                        region_names.append(connection_data.region)
                        region = Region(connection_data.region, self.player, self.multiworld)
                        self.multiworld.regions.append(region)


            for id, connection_data in bfm_er_static_regions.items():
                for region_name, connections in connection_data.items():
                    if(not region_name in region_names):
                        region_names.append(region_name)
                        region = Region(region_name, self.player, self.multiworld)
                        self.multiworld.regions.append(region)

            for id, connection_data in bfm_portals.items():
                if(not "Nightmare" in connection_data.region):
                    #try:

                        num_not_ignore = 0
                        for connection in connection_data.connections:
                            if(connection.connection_group != "Ignore"):
                                num_not_ignore = num_not_ignore + 1
                                break
                        if(num_not_ignore > 0):
                            if(connection_data.region in region_alias):
                                origin_region = self.get_region(region_alias[connection_data.region])
                            else:
                                origin_region = self.get_region(connection_data.region)

                            regions = []
                            if(not id in bfm_er_static_regions):
                                for connection in connection_data.connections:
                                    if(connection.connection_group != "Ignore"):
                                        regions.append(connection.door_name)
                                        region = self.get_region(connection.door_name)
                                        region.connect(origin_region)
                                origin_region.add_exits(regions)
                            else:
                                for region_name, connections in bfm_er_static_regions[id].items():
                                    origin_region = self.get_region(region_name)
                                    origin_region.add_exits(connections)
                                    for connection in connections:
                                        region = self.get_region(connection)
                                        region.connect(origin_region)
                            for connection in connection_data.connections:
                                if(connection.connection_group != "Ignore"):
                                    short_name = hex(connection.destination)[4:] + hex(connection.door)[2:]
                                    origin_region = self.get_region(connection.door_name)
                                    if(short_name in ["000", "004", "107"] and id in short_name_substitute):
                                        short_name = short_name_substitute[id]
                                    if(short_name in bfm_portals_short_to_door_names):
                                        if(bfm_portals_short_to_door_names[short_name] in region_alias):
                                            region = self.get_region(region_alias[bfm_portals_short_to_door_names[short_name]])
                                        else:
                                            region = self.get_region(bfm_portals_short_to_door_names[short_name])
                                        self.entrance_ids_connected.append((connection.short_name,short_name))
                                        #if(not (short_name,connection.short_name) in self.entrance_ids_connected): #TODO is this needed?
                                        origin_region.connect(region)
                                    else:
                                        if(connection.destination in bfm_portals):
                                            if(bfm_portals[connection.destination].region in region_alias):
                                                region = self.get_region(region_alias[bfm_portals[connection.destination].region])
                                            else:
                                                region = self.get_region(bfm_portals[connection.destination].region)
                                            origin_region.connect(region)
                    #except KeyError:
                    #    warning("Missing %s", connection_data.region)
                    #    warning("Missing %s", region_name)
            warning("connected : %s", self.entrance_ids_connected)
            for origin_region_name, region_name in bfm_er_static_one_way_connections.items():
                origin_region = self.get_region(origin_region_name)
                region = self.get_region(region_name)
                origin_region.connect(region)
            origin_region = self.get_region("Menu")
            #region = self.get_region("Upper Village")
            #region = self.get_region("Zipline")
            region = self.get_region("Cutscene MOON")
            origin_region.connect(region)
            #self.get_entrance("Menu -> Cutscene MOON").randomization_type = EntranceType.TWO_WAY


                        
            #for region_name, exits in bfm_regions.items():
            #    region = self.get_region(region_name)
            #    region.add_exits(exits)
            #visualize_regions(self.multiworld.get_region("Castle Bedroom", self.player), "my_world.puml")
            #visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")
            is_er = self.options.entrance_rando.value

            for location_name, location_id in self.player_location_table.items():
                if(is_er):
                    region = self.get_region(location_table[location_name].er_region)
                else:
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
            self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_region("Skullpion Arena", self.player)
            #self.multiworld.completion_condition[self.player] = lambda state: can_fight_skullpion(state, self)
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
            if(self.options.entrance_rando.value):
                if(self.options.goal.value == 7):
                    self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_region("Defeat ToD", self.player)
                else:
                    self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_region("Defeat DL3", self.player)
            else:
                self.multiworld.completion_condition[self.player] = lambda state: state.can_reach_region("Soda Fountain", self.player)
        elif(self.options.goal.value == 9): #defeat x crest guardian
            self.multiworld.completion_condition[self.player] = lambda state: state.has("Boss killed", self.player, self.options.guardian_goal.value) or (state.has("Boss killed", self.player, self.options.guardian_goal.value - 1) and state.has("ToD killed", self.player))
            
        visualize_regions(self.multiworld.get_region("Menu", self.player), "bfm_with_locations.puml")
            #self.multiworld.completion_condition[self.player] = lambda state: has_all_scrolls(state, self) and has_earth_boss_core(state, self) and has_wind_boss_core(state, self) and has_ex_drink(state, self) and state.has_all({"Lumina", "Bracelet"}, self.player)
        #self.multiworld.completion_condition[self.player] = lambda state: state.has_all({"Guard", "Seer", "Hawker", "Maid", "MusicianB", "SoldierA", "MercenC", "CarpentA", "KnightB", "Shepherd", "Bailiff", "Taster", "CarpentB", "Weaver", "SoldierB", "KnightA", "CookA", "Acrobat", "MercenB", "Janitor", "Artisan", "CarpentC", "MusicianC", "Knitter", "Chef", "MercenA", "Chief", "CookB", "Conductor", "Butcher", "KnightC", "Doctor", "KnightD", "Alchemist", "Librarian"}, self.player)
        #self.multiworld.completion_condition[self.player] = lambda state: saved_everyone(state, self.world)

    def fill_slot_data(self) -> Dict[str, Any]:
        slot_data: Dict[str, Any] = {
            "version": __version__,
            "set_lang": self.options.set_lang.value,
            "playthrough_method": self.options.playthrough_method.value,
            "starting_location": self.options.starting_location.value,
            "skip_over_bosses": self.options.skip_over_bosses.value,
            "goal": self.options.goal.value,
            "npc_goal": self.options.npc_goal.value,
            "guardian_goal": self.options.guardian_goal.value,
            "force_soda_fountain_last": self.options.force_soda_fountain_last.value,
            "starting_hp": self.options.starting_hp.value,
            "starting_bp": self.options.starting_bp.value,
            "max_hp_logic": self.options.max_hp_logic.value,
            "deathlink": self.options.death_link.value,
            "trap_link": self.options.trap_link.value,
            "hair_color": self.hair_selection,
            "scalp_color": self.scalp_selection,
            "lumina_randomzied": self.options.lumina_randomzied.value,
            "bakery_sanity": self.options.bakery_sanity.value,
            "restaurant_sanity": self.options.restaurant_sanity.value,
            "grocery_sanity": self.options.grocery_sanity.value,
            "grocery_s_revive": self.options.grocery_s_revive.value,
            "grocery_sanity_heal_logic": self.options.grocery_sanity_heal_logic.value,
            "toy_sanity": self.options.toy_sanity.value,
            "tech_sanity": self.options.tech_sanity.value,
            "scroll_sanity": self.options.scroll_sanity.value,
            "wind_scroll_logic": self.options.wind_scroll_logic.value,
            "sky_scroll_logic": self.options.sky_scroll_logic.value,
            "rumparoni_logic": self.options.rumparoni_logic.value,
            "double_jump_logic": self.options.double_jump_logic.value,
            "core_sanity": self.options.core_sanity.value,
            "level_sanity": self.options.level_sanity.value,
            "level_bundles": self.options.level_bundles.value,
            "stat_gain_modifier": self.options.stat_gain_modifier.value,
            "xp_gain": self.options.xp_gain.value,
            "xp_gain_mind": self.options.xp_gain_mind.value,
            "quest_item_sanity": self.options.quest_item_sanity.value,
            "bp_sanity": self.options.bp_sanity.value,
            "bp_bundles": self.options.bp_bundles.value,
            "time_sanity": self.options.time_sanity.value,
            "time_sanity_settings": self.options.time_sanity_settings.value,
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
            "steamwood_color_accessibility": self.options.steamwood_color_accessibility.value,
            "aqualin_timer": self.options.aqualin_timer.value,
            "restaurant_teleport_maze_no_fail": self.options.restaurant_teleport_maze_no_fail.value,
            "church_fight_time_modifier": self.options.church_fight_time_modifier.value,
            "skip_minigame_town_on_fire": self.options.skip_minigame_town_on_fire.value,
            "skip_to_frozen_palace": self.options.skip_to_frozen_palace.value,
            "skip_minigame_ant_gondola": self.options.skip_minigame_ant_gondola.value,
            "skip_over_calendar_maze": self.options.skip_over_calendar_maze.value,
            "topo_dance_battle_logic": self.options.topo_dance_battle_logic.value,
            "soda_fountain_boss_rush": self.options.soda_fountain_boss_rush.value,
            "message_level": self.options.message_level.value,
            "fast_walk": self.options.fast_walk.value,
            "er_pairings": self.er_pairings,
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
                if(not name in item_table):
                    return BFMItem(self.item_id_to_name[item_name_to_id[name]-jp_id_offset], itemclass, self.item_name_to_id[name], self.player)
        return BFMItem(name, itemclass, self.item_name_to_id[name], self.player)
        #return BFMItem(item_data.jp_name, itemclass, self.item_name_to_id[name], self.player)

    def create_items(self) -> None:
        bfm_items: List[BFMItem] = []
        self.slot_data_items = []

        items_to_create: Dict[str, int] = {item: data.quantity_in_item_pool for item, data in item_table.items()}
        if(self.options.lumina_randomzied.value == False):
            del items_to_create["Lumina"]
            if(self.options.entrance_rando.value):
                self.get_region("Spiral Tower Roof").add_event("Can Grab Lumina", "Has Lumina", location_type = BFMLocation, item_type = BFMItem)
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
            if(self.options.entrance_rando.value):
                self.get_region("Twinpeak Around the Bend").add_event("Can Free Earth Scroll", "Has Earth Scroll", location_type = BFMLocation, item_type = BFMItem)
                self.get_region("Grillin Reservoir").add_event("Can Free Water Scroll", "Has Water Scroll", location_type = BFMLocation, item_type = BFMItem)
                self.get_region("Island of Dragons").add_event("Can Free Fire Scroll", "Has Fire Scroll", location_type = BFMLocation, item_type = BFMItem)
                self.get_region("Grillin Volcano").add_event("Can Free Wind Scroll", "Has Wind Scroll", location_type = BFMLocation, item_type = BFMItem)
                self.get_region("Free Sky Scroll").add_event("Can Free Sky Scroll", "Has Sky Scroll", location_type = BFMLocation, item_type = BFMItem)
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
        if(self.options.quest_item_sanity.value == False):
            for name in item_name_groups["Quest"]:
                if(name in item_table):
                    del items_to_create[name] 
        if(self.options.bp_sanity.value == False):
            for name in item_name_groups["BP"]:
                if(name in item_table):
                    del items_to_create[name] 
        else:
            if(self.options.bp_bundles.value < 13):
                items_to_create["BP Up"] = self.options.bp_bundles.value
                items_to_create["Large BP Up"] = 0
            else:
                items_to_create["BP Up"] = self.options.bp_bundles.value - 6
        if(self.options.time_sanity.value == False):
            for name in item_name_groups["Time"]:
                if(name in item_table):
                    del items_to_create[name] 
            for name in item_name_groups["Time Combined"]:
                if(name in item_table):
                    del items_to_create[name] 
        else:
            if(self.options.time_sanity_settings.value == 2):
                for name in item_name_groups["Time"]:
                    if(name in item_table):
                        del items_to_create[name] 
            else:
                for name in item_name_groups["Time Combined"]:
                    if(name in item_table):
                        del items_to_create[name] 
            


        if(self.options.quest_item_sanity.value == True):
            items_to_create["Longevity Berry"] = items_to_create["Longevity Berry"] + 1 #mayor berry
        if(self.options.starting_hp.value == 1):
            items_to_create["Longevity Berry"] = 0

        for item, quantity in items_to_create.items():
            for _ in range(quantity):
                if(self.options.set_lang.value == 2):
                    bfm_items.append(self.create_item(item_table[item].jp_name))
                else:
                    bfm_items.append(self.create_item(item))

        total_locations = len(self.multiworld.get_unfilled_locations(self.player))
        if self.options.trap_percent.value > 0 and total_locations > len(bfm_items):
            trap_count = math.floor((total_locations - len(bfm_items)) * (self.options.trap_percent / 100))
            trap_names = sorted(list(set(self.options.trap_weights.keys()) & set(trap_weight.keys())))
            trap_weights = {k:self.options.trap_weights[k] for k in trap_names}
            if len(trap_names) == 0:
                trap_names = ["Random Ability Trap"]
                trap_weights = {"Random Ability Trap": 50}
            trap_values = [trap_weights[k] for k in trap_names]
            max_trap_weight = sum(trap_values)
            if len(trap_values) > 1:
                trap_ranges = trap_values
                for i in range(1, len(trap_ranges)):
                    trap_ranges[i] = trap_ranges[i] + trap_ranges[i - 1] 
                for _ in range(trap_count):
                    random_trap = self.random.randint(0, max_trap_weight - 1)
                    for i in range(len(trap_ranges)):
                        if random_trap < trap_ranges[i]:
                            bfm_items.append(self.create_item(trap_names[i]))
                            break
            else:
                for _ in range(trap_count):
                    bfm_items.append(self.create_item(trap_names[0]))


        for _ in range(total_locations - len(bfm_items)):
            bfm_items.append(self.create_filler())

        #for bfm_item in bfm_items:
        #    if bfm_item.name in slot_data_item_names:
        #        self.slot_data_items.append(bfm_item)

        self.multiworld.itempool += bfm_items

        if(self.options.early_skullpion.value == True):
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
        #warning("adding boss killed events")
        self.get_region("Twinpeak Around the Bend").add_event("Can Reach Twinpeak Around the Bend", "Can Cross Stream", location_type = BFMLocation, item_type = BFMItem)
        self.get_region("Twinpeak Second Peak").add_event("Can Reach Twinpeak Second Peak", "Can Reach Second Peak", location_type = BFMLocation, item_type = BFMItem)
        self.get_region("Skullpion Arena").add_event("Earth Crest Guardian Defeated", "Boss killed", location_type = BFMLocation, item_type = BFMItem)
        self.get_region("Relic Keeper Arena").add_event("Water Crest Guardian Defeated", "Boss killed", location_type = BFMLocation, item_type = BFMItem)
        self.get_region("Frost Dragon Arena").add_event("Fire Crest Guardian Defeated", "Boss killed", location_type = BFMLocation, item_type = BFMItem)
        self.get_region("Queen Ant Arena").add_event("Wind Crest Guardian Defeated", "Boss killed", location_type = BFMLocation, item_type = BFMItem)
        self.get_region("Skullpion Arena").add_event("Earth Crest Guardian", "Skullpion killed", location_type = BFMLocation, item_type = BFMItem)
        self.get_region("Relic Keeper Arena").add_event("Water Crest Guardian", "Relic Keeper killed", location_type = BFMLocation, item_type = BFMItem)
        self.get_region("Frost Dragon Arena").add_event("Fire Crest Guardian", "Frost Dragon killed", location_type = BFMLocation, item_type = BFMItem)
        self.get_region("Queen Ant Arena").add_event("Wind Crest Guardian", "Queen Ant killed", location_type = BFMLocation, item_type = BFMItem)
        if(self.options.playthrough_method.value == 2):
            if(self.options.entrance_rando.value):
                self.get_region("Defeat ToD").add_event("Sky Crest Guardian Defeated", "Boss killed", location_type = BFMLocation, item_type = BFMItem)
            else:
                self.get_region("Soda Fountain").add_event("Sky Crest Guardian Defeated", "Boss killed", location_type = BFMLocation, item_type = BFMItem)
        else:
            if(self.options.entrance_rando.value):
                self.get_region("Defeat ToD").add_event("Sky Crest Guardian Defeated", "ToD killed", location_type = BFMLocation, item_type = BFMItem)
            else:
                self.get_region("Soda Fountain").add_event("Sky Crest Guardian Defeated", "ToD killed", location_type = BFMLocation, item_type = BFMItem)

        if(self.options.entrance_rando.value):
            self.get_region("Twinpeak Entrance").add_event("Can Reach Twinpeak Entrance", "Can Reach Twinpeak Entrance", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Graveyard").add_event("Can Reach Graveyard", "Can Reach Graveyard", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Twinpeak Second Peak Aqualin").add_event("Can Reach Aqualin", "Can Reach Aqualin", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Restaurant Basement Entrance Behind 4 Eye Door").add_event("Can Reach Ugly Belt Chest", "Can Reach Ugly Belt Chest", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Castle Meeting Room").add_event("Can Reach Castle Meeting Room", "Can Reach Castle Meeting Room", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Misteria Underground Lake").add_event("Can Reach Misteria", "Can Reach Misteria", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Waterfall Cave West").add_event("Can Reach Waterfall Cave", "Can Reach Hotelo", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Lower Mine Scrap Depository").add_event("Can Reach Scrap Depository", "Can Reach Gondola Gizmo", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Chapter 3 Church Vambee Fight").add_event("Can Reach Chapter 3 Church Vambee Fight", "Church Vambee Fight", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Grillin Reservoir").add_event("Can Reach Grillin Reservoir", "Can Reach Water Crest", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Restaurant Basement Bowling Entrance").add_event("Can Reach Restaurant Basement Bowling Entrance", "Can Bowl", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Bowling 1 Plant Room").add_event("Can Reach Bowling 1 Plant Room", "Can Bowl", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Bowling 2 Plant Room").add_event("Can Reach Bowling 2 Plant Room", "Can Bowl", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Green Eye Maze").add_event("Green Eye Maze Clone", "Has Clone", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Blue Eye Door Hallway Upper Path").add_event("Blue Eye Door Hallway Upper Path Clone", "Has Clone", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Red Eye Hallway").add_event("Red Eye Hallway Clone", "Has Clone", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Red Eye Hallway Near Fallen Pillars South East").add_event("Red Eye Hallway Near Fallen Pillars South East Clone", "Has Clone", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Green Eye Maze").add_event("Green Eye Maze Steel", "Has Steel", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Blue Eye Maze").add_event("Blue Eye Maze Steel", "Has Steel", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Teleport Maze End Eye Room").add_event("Can Reach Teleport Maze End Eye Room", "Eye Switch", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Bowling End Eye Room").add_event("Can Reach Bowling End Eye Room", "Eye Switch", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Dark Maze End Eye Room").add_event("Can Reach Dark Maze End Eye Room", "Eye Switch", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Rotating Platforms End Eye Room").add_event("Can Reach Rotating Platforms End Eye Room", "Eye Switch", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Upper Mine Large Fan Near Switch Upper West").add_event("Can Reach Upper Mine Large Fan Near Switch Upper West", "Mine Power Switch On", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Squish Ant").add_event("Can Reach Squish Ant Cutscene", "Squish Ant Cutscene", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Grillin Reservoir Tunnel").add_event("Can Reach Grillin Reservoir Tunnel", "Can Reach Fire Crest", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Lower Mine Entrance").add_event("Can Reach Lower Mine Entrance", "Can Reach Lower Mine Entrance", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Island of Dragons").add_event("Can Reach Island of Dragons", "Can Reach Island of Dragons", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Steamwood Outside").add_event("Can Reach Steamwood Outside", "Can Reach Steamwood Outside", location_type = BFMLocation, item_type = BFMItem)
            self.get_region("Upper Village Steam Pipe").add_event("Can Reach Upper Village Steam Pipe", "Can Reach Fores", location_type = BFMLocation, item_type = BFMItem)
        #final_boss_room.add_event(
        #"Final Boss Defeated", "Victory", location_type=APQuestLocation, item_type=items.APQuestItem)

    def get_filler_item_name(self) -> str:
        return "1000 Drans"

    def create_filler(self) -> "Item":
        if(self.options.set_lang.value == 2):
            return self.create_item(item_table[self.get_filler_item_name()].jp_name)
        return self.create_item(self.get_filler_item_name())

    def set_rules(self) -> None:
        #print(self.options.set_lang.value)
        
        if(self.options.entrance_rando.value):
            set_er_rules(self)
            warning("ran ER Rules")
        else:
            set_rules(self)
        #if(self.using_ut == False):
        #    set_rules(self)
        #else:
        #    set_region_rules(self)
        #    set_location_rules(self, self.options.set_lang.value == 2 and (self.options.spoiler_items_in_english.value == False or self.using_ut == True))
        #if(self.options.quest_item_sanity.value == True):
            #warning(" quest sanity is on !?!?!")
        #warning("registering indirect connections")
        #self.explicit_indirect_conditions = False
        #self.multiworld.register_indirect_condition(self.get_region("Twinpeak Second Peak"), self.get_entrance("Twinpeak Waterfall Cave 2 -> Twinpeak Second Peak"))
        #self.multiworld.register_indirect_condition(self.get_region("Grillin Reservoir"), self.get_entrance("Grillin Village -> Grillin Reservoir"))
        #self.multiworld.register_indirect_condition(self.get_region("Skullpion Arena"), self.get_entrance("Twinpeak Path to Skullpion -> Skullpion Arena"))
        #self.multiworld.register_indirect_condition(self.get_region("Relic Keeper Arena"), self.get_entrance("Restaurant Basement Path to Crest Guardian -> Relic Keeper Arena"))
        #self.multiworld.register_indirect_condition(self.get_region("Frost Dragon Arena"), self.get_entrance("Frost Dragon Door -> Frost Dragon Arena"))
        #self.multiworld.register_indirect_condition(self.get_region("Queen Ant Arena"), self.get_entrance("Upper Mines Poison Elevators -> Queen Ant Arena"))
        #visualize_regions(self.multiworld.get_region("Menu", self.player), "my_world.puml")
    
    def connect_entrances(self) -> None:
        if(self.options.entrance_rando.value == False):
            return
        groups_to_remain_connected: List[str] = []
        if(self.options.starting_location.value == 1):
            groups_to_remain_connected.append("CH1")
        entrance_ids_disconnected: List[Tuple[str,str]] = []
        for id, connection_data in bfm_portals.items():
            if(not "Nightmare" in connection_data.region):
                #try:
                for connection in connection_data.connections:
                    if(connection.connection_group != "Ignore" and connection.can_be_disconnected and not connection.connection_group in groups_to_remain_connected):
                        short_name = hex(connection.destination)[4:] + hex(connection.door)[2:]
                        #origin_region = self.get_region(connection.door_name)
                        if(short_name in bfm_portals_short_to_door_names):
                            if(short_name in ["000", "004", "107"] and id in short_name_substitute):
                                short_name = short_name_substitute[id]
                            #if(not (short_name,connection.short_name) in entrance_ids_disconnected):
                            entrance_ids_disconnected.append((connection.short_name,short_name))
                            entrance = self.get_entrance(f"{connection.door_name} -> {bfm_portals_short_to_door_names[short_name]}")
                            if((short_name,connection.short_name) in self.entrance_ids_connected):
                                #warning("is two way : %s", entrance.name)
                                #pass
                                entrance.randomization_type = EntranceType.TWO_WAY
                            if(self.using_ut == False):
                                entrance.randomization_group = 1
                                disconnect_entrance_for_randomization(entrance,1,bfm_portals_short_to_door_names[short_name])
                            else:
                                entrance.connected_region.entrances.remove(entrance)
                                entrance.connected_region = None
                                entrance.parent_region.exits.remove(entrance)
                                entrance.parent_region = None

                            #region = self.get_region(bfm_portals_short_to_door_names[short_name])
                            #origin_region.connect(region)
                        else:
                            if(connection.destination in bfm_portals):
                                if(bfm_portals[connection.destination].region in region_alias):
                                    child_name = region_alias[bfm_portals[connection.destination].region]
                                    #region = self.get_region(region_alias[bfm_portals[connection.destination].region])
                                else:
                                    child_name = bfm_portals[connection.destination].region
                                    #region = self.get_region(bfm_portals[connection.destination].region)
                                #entrance_ids_disconnected.append((connection.short_name,short_name))
                                entrance = self.get_entrance(f"{connection.door_name} -> {child_name}")
                                if(self.using_ut == False):
                                    entrance.randomization_group = 1
                                    disconnect_entrance_for_randomization(entrance,1,child_name)
                                else:
                                    entrance.connected_region.entrances.remove(entrance)
                                    entrance.connected_region = None
                                    entrance.parent_region.exits.remove(entrance)
                                    entrance.parent_region = None
                                #origin_region.connect(region)
        #warning("connected : %s", self.entrance_ids_connected)
        """
        warning("disconnected : %s", entrance_ids_disconnected)
        warning("disconnected num : %s", len(entrance_ids_disconnected))
        warning("connected num : %s", len(self.entrance_ids_connected))
        warning("if equal : %s", set(self.entrance_ids_connected) - set(entrance_ids_disconnected))
        for conn in entrance_ids_disconnected:
            if(not (conn[1], conn[0]) in entrance_ids_disconnected):
                warning("is oneway? : %s", conn)
            if(entrance_ids_disconnected.count(conn) != 1):
                warning("too many or few? %s : count : %s",conn,entrance_ids_disconnected.count(conn))
        """
        if(self.options.starting_location.value == 2):
            entrance = self.get_entrance("End Summon Crystal Cutscene -> Starting Forest")
            disconnect_entrance_for_randomization(entrance,None,"Starting Forest")
            #child_region = entrance.connected_region
            #child_region.entrances.remove(entrance)
            entrance.connected_region = None
            entrance.parent_region.exits.remove(entrance)
            entrance.parent_region = None
                
            if(self.using_ut == True):
                region = self.get_region("Starting Forest")
                #entrance = self.get_entrance("Starting Forest -> Starting Forest")
                entrance = region.entrances[1]
                region.entrances.remove(entrance)
                #region.exits.remove(entrance)
                entrance.connected_region = None
            #warning("summon %s",self.get_region("End Summon Crystal Cutscene").exits)
            #warning("forest %s",self.get_region("Starting Forest").entrances)
            origin_region = self.get_region("End Summon Crystal Cutscene")
            region = self.get_region("Zipline")
            origin_region.connect(region)
                
            if(self.using_ut == False):
                #warning("zip %s",self.get_region("Zipline").entrances[0])
                entrance = self.get_region("Zipline").entrances[0]
                region.entrances.remove(entrance)
                #region.exits.remove(entrance)
                entrance.connected_region = None
                #entrance.parent_region = None

        #visualize_regions(self.multiworld.get_region("Menu", self.player), "er_puml/just_before_bfm_er.puml")

        #visualize_regions(self.multiworld.get_region("Menu", self.player), "just_before_bfm_er.puml")
        if(self.using_ut == False):
            import traceback
            attempts: int = 0
            #mess_with_rng = 0
            er_info: ERPlacementState = None
            max_attempts = 1
            while(attempts < max_attempts and er_info is None):
                attempts = attempts + 1
                try:
                    er_info: ERPlacementState = randomize_entrances(self,True,{0: [0,1],1: [0,1]})
                except EntranceRandomizationError as er_error:
                    warning("Attempt to ER for BFM # %s failed", attempts)
                    if(attempts >= max_attempts):
                        warning("Reached max attempts to ER for BFM for player: %s (player #%s)",self.player_name,self.player)
                        #warning(traceback.format_exc())
                        warning("Ask Player '%s' to report this issue to the Brave Fencer Musashi Dev and perhaps try tweaking yaml settings before genning again",self.player_name)
                        raise er_error
                    #taken from https://github.com/Ars-Ignis/Archipelago/blob/4a94e83ec86977c9c1eb4663133d0a6ea340fd08/worlds/crystalis/regions.py#L678
                    for region in self.get_regions():
                        for entrance in region.get_exits():
                            if (entrance.randomization_group == 1 and entrance.parent_region and entrance.connected_region):
                                #warning("disconnected : %s -> %s", entrance.parent_region, entrance.connected_region)
                                if(entrance.connected_region.name == "Restaurant Hidden Exit Behind Counter"):
                                    warning("Parent of region that shouldn't be disconnected %s",entrance.parent_region.name)
                                if(entrance.parent_region.name == "Restaurant Hidden Exit Behind Counter"):
                                    warning("should only be one of these, restaurant connected to %s", entrance.connected_region)
                                    warning("entrance type %s", entrance.randomization_type)
                                disconnect_entrance_for_randomization(entrance, entrance.randomization_group, region.name)
            visualize_regions(self.multiworld.get_region("Menu", self.player), "bfm_er.puml")
            warning("er info pairings : %s",er_info.pairings)

            for pair in er_info.pairings:
                origin = pair[0].split(" -> ")[0]
                dest = pair[1].split(" -> ")[0]
                if(origin in bfm_portals_door_names_to_short):
                    origin = bfm_portals_door_names_to_short[origin]
                #elif(origin in region_alias_reverse):
                #    origin = region_alias_reverse[origin]
                #    if(origin in bfm_portals_door_names_to_short):
                #        origin = bfm_portals_door_names_to_short[origin]
                if(dest in bfm_portals_door_names_to_short):
                    dest = bfm_portals_door_names_to_short[dest]
                elif(dest in region_alias_reverse):
                    dest = region_alias_reverse[dest]
                    if(dest in bfm_portals_door_names_to_short):
                        dest = bfm_portals_door_names_to_short[dest]
                if(dest in ["001","002","003"]):
                    dest = "004"
                if(dest in ["005","006","007"]):
                    dest = "000"
                if(dest in ["10"]):
                    dest = "107"
                if(origin == "9d1"):
                    origin = "1a1"
                self.er_pairings[origin] = dest
                #if(dest in self.er_pairings):
                #    if(self.er_pairings[dest] != origin or True):
                #        self.er_pairings[origin] = dest
                #else:
                #    self.er_pairings[origin] = dest
            if(self.options.starting_location.value == 2):
                self.er_pairings["052"] = "040"
                self.er_pairings["061"] = "040"
            warning("short_name_pairs : %s",self.er_pairings)
        else:
            warning("pairings list %s",self.er_pairings)
            for origin, dest in self.er_pairings.items():
                if(origin in bfm_portals_short_to_door_names_no_ignore):
                    long_name_origin = bfm_portals_short_to_door_names_no_ignore[origin]
                else:
                    warning("not in list %s",origin)
                    continue
                    #num: int = expand_region_id(int(origin,16))
                    #if(num in bfm_portals):
                    #    long_name_origin = bfm_portals[num].region
                if(long_name_origin in region_alias):
                    long_name_origin = region_alias[long_name_origin]
                if(dest in ["000", "004"]):
                    long_name_region = "Castle Outside"
                elif(dest == "107"):
                    long_name_region = "Grillin Village"
                elif(dest in bfm_portals_short_to_door_names_no_ignore):
                    long_name_region = bfm_portals_short_to_door_names_no_ignore[dest]
                else:
                    warning("not in list %s",dest)
                    continue
                    #num: int = expand_region_id(int(dest,16))
                    #if(num in bfm_portals):
                    #    long_name_region = bfm_portals[num].region
                if(long_name_region in region_alias):
                    long_name_region = region_alias[long_name_region]
                    #else:
                    #    warning("no name found for %s, %s",dest,num)
                origin_region = self.get_region(long_name_origin)
                region = self.get_region(long_name_region)
                origin_region.connect(region, name = long_name_origin)
            visualize_regions(self.multiworld.get_region("Menu", self.player), "bfm_UT_er.puml")

        #warning("er info placements : %s",er_info.placements)
    # Taken from Tunic APWorld https://github.com/ArchipelagoMW/Archipelago/blob/main/worlds/tunic/__init__.py#L713
    # for the universal tracker, doesn't get called in standard gen
    # docs: https://github.com/FarisTheAncient/Archipelago/blob/tracker/worlds/tracker/docs/re-gen-passthrough.md
    @staticmethod
    def interpret_slot_data(slot_data: Dict[str, Any]) -> Dict[str, Any]:
        # returning slot_data so it regens, giving it back in multiworld.re_gen_passthrough
        return slot_data
        
