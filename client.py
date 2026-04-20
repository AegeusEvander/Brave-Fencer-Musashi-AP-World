"""
A module containing the BizHawkClient base class and metaclass
"""

from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Any, ClassVar, List

from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch as launch_component

from .locations import location_table, location_name_groups, standard_location_name_to_id, sphere_one, location_base_id, en_table_ids_to_hint, jp_table_ids_to_hint
from .dialog_locations import dialog_location_table, short_text_boxes, castle_dialog, scroll_dialog, boss_core_update, boss_core_dialog, boss_locations, quest_item_dialog
#if TYPE_CHECKING:
#    from .context import BizHawkClientContext
from .utils import Constants
from .version import __version__
from .hair_color import hair_color_addresses, default_hair_color, new_hair_color
from .items import npc_ids, item_id_to_name, item_name_to_id, item_name_groups, jp_id_offset
from .store_info import bakery_locations, store_table, restaurant_pointers, restaurant_pointers_pointers, restaurant_locations, grocery_locations, toy_shop_locations, toy_shop_fix, toy_shop_dialog, toy_shop_dialog_length, tech_fix, tech_check_locations, appraisal_items_buy_cost, appraisal_l_armor_buy_cost, key_item_buy_cost, store_sanity_buy_cost, quest_item_buy_cost
from .stats import body_xp, mind_xp, lumina_xp, fusion_xp, body_stat, mind_stat, lumina_stat, fusion_stat, level_memory_ids
from .jp_encoding import jp_encoding
from .quest_items import quest_item_locations, well_water_id, gate_angles
from .portals import bfm_portals, BFMConnection
from .progression_state import calc_completed_progression_state, calc_progression_state, progression_state_table
import math
import random
from NetUtils import ClientStatus, NetworkItem
from collections import Counter
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient
from pathlib import Path
import os
import Utils
import zipfile
from BaseClasses import ItemClassification as IC

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext, BizHawkClientCommandProcessor
    from NetUtils import JSONMessagePart


def cmd_debug_dump(self: "BizHawkClientCommandProcessor") -> None:
    """If something goes wrong, run this command and send the results to the dev"""
    from CommonClient import logger
    from worlds._bizhawk.context import BizHawkClientContext
    if self.ctx.game != "Brave Fencer Musashi":
        logger.warning("This command can only be used when playing Brave Fencer Musashi.")
        return
    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return

    ctx = self.ctx
    assert isinstance(ctx, BizHawkClientContext)
    client = ctx.client_handler
    assert isinstance(client, BFMClient)
    
    logger.info("%s\n%s\n%s\n%s\n%s",client.debug_text[not client.debug_index], client.debug_text[client.debug_index], ctx.slot_data, client.old_game_state, [item_id_to_name[received_item[0] - ((ctx.slot_data["set_lang"] - 1) * jp_id_offset)] for received_item in ctx.items_received])

def cmd_message_level(self: "BizHawkClientCommandProcessor", status = "") -> None:
    """Change Bizhawk Client Message Level"""
    from CommonClient import logger
    from worlds._bizhawk.context import BizHawkClientContext
    if self.ctx.game != "Brave Fencer Musashi":
        logger.warning("This command can only be used when playing Brave Fencer Musashi.")
        return
    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return

    ctx = self.ctx
    assert isinstance(ctx, BizHawkClientContext)
    client = ctx.client_handler
    assert isinstance(client, BFMClient)
    if status == "":
        if client.message_level == 1:
            msg = "ON"
        elif client.message_level == 2:
            msg = "HINT"
        elif client.message_level == 3:
            msg = "DEV"
        else:
            msg = "OFF"
        logger.info(f"Message Level: {msg}\n"
                    f"    To change the status, use the command: /message_level [off/on/hint/dev]\n"
                    f"    OFF  : Nearly no messages\n"
                    f"    ON   : Messages acknowledging a receieved item, reconnection sync messages, some warnings \n"
                    f"    HINT : Notes what action is expected of the player for the current game state in town and all the messages from ON")
        return
    elif status.lower() == "on":
        msg = "ON"
        client.message_level = 1
    elif status.lower() == "off":
        msg = "OFF"
        client.message_level = 0
    elif status.lower() == "hint":
        msg = "HINT"
        client.message_level = 2
    elif status.lower() == "dev":
        msg = "DEV"
        client.message_level = 3
    else:
        logger.info(f"Invalid argument for function ""message_level""\n")
        return
    logger.info(f"Message Level is now {msg}")

#command taken from Ape Escape AP World
def cmd_deathlink(self: "BizHawkClientCommandProcessor", status = "") -> None:
    """Toggle Deathlink on and off"""
    from CommonClient import logger
    from worlds._bizhawk.context import BizHawkClientContext
    if self.ctx.game != "Brave Fencer Musashi":
        logger.warning("This command can only be used when playing Brave Fencer Musashi.")
        return
    if not self.ctx.server or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return

    ctx = self.ctx
    assert isinstance(ctx, BizHawkClientContext)
    client = ctx.client_handler
    assert isinstance(client, BFMClient)
    if status == "":
        if client.deathlink == 1 or (client.deathlink == -1 and ctx.slot_data["deathlink"]):
            msg = "ON"
        else:
            msg = "OFF"
        logger.info(f"Deathlink: {msg}\n"
                    f"    To change the status, use the command: /deathlink [on/off]")
        return
    elif status.lower() == "on":
        client.previous_death_link = ctx.last_death_link
        client.deathlink = 1
    elif status.lower() == "off":
        client.deathlink = 0
    else:
        logger.info(f"Invalid argument for function ""deathlink""\n")
        return
    
    if client.deathlink == 1:
        Utils.async_start(ctx.update_death_link(True))
        msg = "ON"
    else:
        Utils.async_start(ctx.update_death_link(False))
        msg = "OFF"

    logger.info(f"Deathlink is now {msg}\n")

def cmd_goal(self: "BizHawkClientCommandProcessor") -> None:
    """check Goal"""
    from CommonClient import logger
    from worlds._bizhawk.context import BizHawkClientContext
    if self.ctx.game != "Brave Fencer Musashi":
        logger.warning("This command can only be used when playing Brave Fencer Musashi.")
        return
    if not self.ctx.server or self.ctx.server.socket.closed or not self.ctx.slot:
        logger.warning("You must be connected to a server to use this command.")
        return

    ctx = self.ctx
    assert isinstance(ctx, BizHawkClientContext)
    client = ctx.client_handler
    assert isinstance(client, BFMClient)
    npc_num = ctx.slot_data["npc_goal"]
    crest_guardian_num = ctx.slot_data["guardian_goal"]
    goal_names = [
        "rescue all npcs",
        f'rescue {npc_num} npcs',
        "defeat earth crest guardian",
        "defeat water crest guardian",
        "defeat fire crest guardian",
        "defeat wind crest guardian",
        "defeat sky crest guardian",
        "defeat final boss",
        f'defeat {crest_guardian_num} crest guardians'
    ]
    string_message = f"Your current goal: {goal_names[ctx.slot_data["goal"] - 1]}"
    logger.info(string_message)
    Utils.async_start(bizhawk.display_message(ctx.bizhawk_ctx, string_message))


MAIN_RAM: typing.Final[str] = "MainRAM"
PLAYER_CURR_HP_MEMORY: typing.Final[int] = 0x078EB4

class BFMClient(BizHawkClient):
    system: ClassVar[str | tuple[str, ...]] = "PSX"
    """The system(s) that the game this client is for runs on"""

    game: ClassVar[str] = Constants.GAME_NAME
    """The game this client is for"""

    patch_suffix: ClassVar[str | tuple[str, ...] | None] = ".apbfm"
    """The file extension(s) this client is meant to open and patch (e.g. ".apz3")"""
    bincho_checks = [False] * 35
    minku_checks = [False] * 13
    chest_checks = [False] * 33
    bakery_checks = [False] * 7
    grocery_checks = [False] * 12
    restaurant_checks = [False] * 7
    toy_checks = [False] * 30
    tech_checks = [False] * 7
    scroll_checks = [False] * 5
    core_checks = [False] * 4
    quest_item_checks = [False] * 29
    chest_indices_to_skip = [0, 1, 2, 3, 4, 25]
    bakery_inventory_default = [0xd,0xe,0xf,0x10,0x53]
    bakery_inventory_sanity = [0x3e,0x3e,0x3e,0x3e,0x3e]
    bakery_inventory_expansion = []
    bakery_inventory = []
    bakery_dialog: List[str] = [] 
    restaurant_inventory_default = [0x71,0x72,0x73,0x74,0x75,0x76,0x77]
    restaurant_inventory_sanity = [0x40,0x40,0x40,0x40,0x40,0x40,0x40]
    restaurant_inventory = []
    restaurant_dialog: List[str] = [] 
    grocery_inventory_default = [0x04,0x05,0x06,0x0a,0x08,0x09,0x6b]
    grocery_inventory_sanity = [0x42,0x42,0x42,0x42,0x42,0x42,0x42]
    grocery_inventory = []
    grocery_dialog: List[str] = [] 
    toy_inventory = [False] * 30
    toy_dialog: List[bytearray] = [bytearray()] * 30 
    tech_dialog: List[bytearray] = [bytearray()] * 7 
    core_dialog: List[bytearray] = [bytearray()] * 4 
    found_wind_scroll = False
    progression_state = 0
    received_count = 0
    old_location = 0
    old_step_count = 0
    level_transition = 0
    request_hints = 0
    hair_color_updated = 0
    has_died = 0
    death_link_timer = 240
    previous_death_link: float = 0
    legendary_armor = [False] * 7
    curr_inventory = [0] * 12
    counter_for_delayed_check = 0
    check_for_logs = 0
    list_of_received_items: List[int] = []
    check_if_lumina_was_found = 1
    check_if_lumina_needs_removed = 1
    cursor_pos = 0
    checked_cores = False
    max_hp_updated = False
    xp_gain_updated = False
    curr_body_lvl = 0
    curr_mind_lvl = 0
    curr_fus_lvl = 0
    curr_lum_lvl = 0
    curr_body_stat = 4
    curr_mind_stat = 6
    curr_fus_stat = 4
    curr_lum_stat = 8
    raft_regrow_timer = 0
    raft_hp = 4
    elevator_active = True
    jp_version = False
    table_ids_to_hint = []
    deathlink = -1
    num_bosses_killed = -1
    completed_progression: set[int] = set()
    manually_checked_progression: set[int] = set()
    manually_checked_progression_states: List[int] = [0xd2, 0x136, 0x186, 0x280, 0x294, 0x2b2, 0x2bc, 0x2c6, 0x2e4, 0x3ac, 0x3b6, 0x3c0, 0x47e, 0x488, 0x492]
    save_manual_progression = False
    try_to_update_connections = False
    old_inventory = set()
    chapter3_items = []
    chapter4_items = []
    chapter5_items = []
    message_level = 2
    debug_text: List[str] = ["", ""]
    debug_index = 0
    old_game_state = []
    messagequeue = []
    messagetimer = 0
    musashi_old_floor = 1
    old_closest_gizmo = 0
    last_displayed_hint: str = ""
    hint_dictionary: Dict[int, str] = {}
    Commands_Dict = {
        "deathlink": "cmd_deathlink",
        "message_level": "cmd_message_level",
        "debug_dump": "cmd_debug_dump",
        "goal": "cmd_goal",
    }


    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        """Should return whether the currently loaded ROM should be handled by this client. You might read the game name
        from the ROM header, for example. This function will only be asked to validate ROMs from the system set by the
        client class, so you do not need to check the system yourself.

        Once this function has determined that the ROM should be handled by this client, it should also modify `ctx`
        as necessary (such as setting `ctx.game = self.game`, modifying `ctx.items_handling`, etc...)."""
        from CommonClient import logger
        logger.info("Attempting to validate rom")
        bfm_identifier_ram_address: int = 0x00ba94

        self.jp_version = False
        # = SLUS-00726MUSASHI in ASCII, code taken from AP Forbidden Memories
        bytes_expected: bytes = bytes.fromhex("534C55532D30303732364D555341534849")
        Commands_List = list(self.Commands_Dict.keys())
        try:
            bytes_actual: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                bfm_identifier_ram_address, len(bytes_expected), MAIN_RAM
            )]))[0]
            if bytes_actual != bytes_expected:
                bytes_actual = (await bizhawk.read(ctx.bizhawk_ctx, [(
                    0x009f9a, len(bytes_expected), MAIN_RAM
                )]))[0]
                if bytes_actual != bytes_expected:
                    bytes_actual = (await bizhawk.read(ctx.bizhawk_ctx, [(
                        0x072e02, len(bytes_expected), MAIN_RAM
                    )]))[0]
                    if bytes_actual != bytes_expected:
                        #SLUS_007.26;1 in ASCII
                        bytes_expected = bytes.fromhex("534C55535F3030372E32363B31")
                        bytes_actual = (await bizhawk.read(ctx.bizhawk_ctx, [(
                            0x0093c4, len(bytes_expected), MAIN_RAM
                        )]))[0]
                        if bytes_actual != bytes_expected:
                            bytes_actual = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                0x009e19, len(bytes_expected), MAIN_RAM
                            )]))[0]
                            if bytes_actual != bytes_expected:
                                bytes_actual = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                    0x00b8b7, len(bytes_expected), MAIN_RAM
                                )]))[0]
                                if bytes_actual != bytes_expected:
                                    bytes_actual = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                        0x008c5c, len(bytes_expected), MAIN_RAM
                                    )]))[0]
                                    if bytes_actual != bytes_expected:
                                        bytes_actual = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                            0x009699, len(bytes_expected), MAIN_RAM
                                        )]))[0]
                                        if bytes_actual != bytes_expected:
                                            bytes_actual = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                                0x00b117, len(bytes_expected), MAIN_RAM
                                            )]))[0]
                                            if bytes_actual != bytes_expected:
                                                bytes_actual = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                                    0x0765ec, len(bytes_expected), MAIN_RAM
                                                )]))[0]
                                                if bytes_actual != bytes_expected:
                                                    bytes_actual = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                                        0x078485, len(bytes_expected), MAIN_RAM
                                                    )]))[0]
                                                    if bytes_actual != bytes_expected:
                                                        #SLPS_014.90;1 in ASCII
                                                        bytes_expected = bytes.fromhex("534C50535F3031342E39303B31")
                                                        bytes_actual = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                                            0x075730, len(bytes_expected), MAIN_RAM
                                                        )]))[0]
                                                        if bytes_actual != bytes_expected:
                                                            bytes_actual = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                                                0x0775a7, len(bytes_expected), MAIN_RAM
                                                            )]))[0]
                                                            if bytes_actual != bytes_expected:
                                                                for command in Commands_List:
                                                                    if command in ctx.command_processor.commands:
                                                                        ctx.command_processor.commands.pop(command)
                                                                return False
                                                        self.jp_version = True
                                                        logger.info("JP Version Detected")
        except Exception:
            for command in Commands_List:
                if command in ctx.command_processor.commands:
                    ctx.command_processor.commands.pop(command)
            return False

        ctx.game = self.game
        ctx.items_handling = 0b011
        ctx.want_slot_data = True
        #ctx.watcher_timeout = 0.125  # value taken from Forbiden Memories, taken from Pokemon Emerald's client
        ctx.watcher_timeout = 0.25  
        for command in Commands_List:
            if command not in ctx.command_processor.commands:
                functionName = self.Commands_Dict[command]
                linkedfunction = globals()[functionName]
                ctx.command_processor.commands[command] = linkedfunction
        logger.info(f"Brave Fencer Musashi Client v{__version__}. For updates:")
        logger.info("https://github.com/AegeusEvander/Brave-Fencer-Musashi-AP-World/releases")
        #logger.info("test: %s",bfm_portals[0x3000].region)
        #logger.info("test: %s",bfm_portals[0x3000].connections[0].door)
        #logger.info(f"This Archipelago slot was generated with v{ctx.slot_data["version"]}")
        return True
    
    async def kill_player(self, ctx: "BizHawkClientContext") -> None:
        """sets player HP to 0"""
        # # Player HP at 078EB4 2 Bytes MAINRAM
        #     await bizhawk.write
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(PLAYER_CURR_HP_MEMORY + (self.jp_version * -0xea0), (0).to_bytes(2, "little"), MAIN_RAM)]
        )
        return

    async def set_auth(self, ctx: "BizHawkClientContext") -> None:
        """Should set ctx.auth in anticipation of sending a `Connected` packet. You may override this if you store slot
        name in your patched ROM. If ctx.auth is not set after calling, the player will be prompted to enter their
        username."""
        pass

    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        """Runs on a loop with the approximate interval `ctx.watcher_timeout`. The currently loaded ROM is guaranteed
        to have passed your validator when this function is called, and the emulator is very likely to be connected."""
        if ctx.server is None or ctx.server.socket.closed or ctx.slot_data is None:
            return
        try:
            check_game_state: bytes = bytes.fromhex("0b")
            #game_state: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
            #    0x0b99de + (self.jp_version * -0xea0) , 1, MAIN_RAM
            #)]))[0]
            game_state: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [
                (0x0b99de + (self.jp_version * -0xea0), 1, MAIN_RAM), #is in main menu
                (0x0ae671 + (self.jp_version * -0xea0), 9, MAIN_RAM), #bincho sanity
                (0x0ae650 + (self.jp_version * -0xea0), 2, MAIN_RAM), #minku sanity
                (0x0ae651 + (self.jp_version * -0xea0), 5, MAIN_RAM), #chest sanity
                (0x0ba21b + (self.jp_version * -0xea0), 43, MAIN_RAM), #toy sanity
            ] + tech_check_locations[self.jp_version] + level_memory_ids[self.jp_version] + quest_item_locations[self.jp_version] +
            [(0x0b9a08 + (self.jp_version * -0xea0), 2, MAIN_RAM),#25 current location
            (0x0ae64a + (self.jp_version * -0xea0), 3, MAIN_RAM), #26 Scrolls and LArmor
            (0x0ba1f3 + (self.jp_version * -0xea0), 1, MAIN_RAM), #27 Geezer   
            (0x0ba285 + (self.jp_version * -0xea0), 1, MAIN_RAM), #28 Steamwood Status
            (0x075400 + (self.jp_version * -0xe70), 1, MAIN_RAM)] #29 Zone Loaded   
            ))
            if check_game_state != game_state[0]:
                self.received_count = 0
                self.hair_color_updated = 0
                self.old_step_count = 0
                self.check_if_lumina_needs_removed = 1
                self.max_hp_updated = False
                self.xp_gain_updated = False
                self.num_bosses_killed = -1
                return
            self.old_game_state = game_state
            #global bincho_checks
            from CommonClient import logger
            #logger.info("data dump %s", game_state)
            received_list: List[int] = [received_item[0] - ((ctx.slot_data["set_lang"] - 1) * jp_id_offset) for received_item in ctx.items_received]


            curr_location_data: bytes = game_state[25]
            curr_location = int.from_bytes(curr_location_data,byteorder='little')
            old_progression_state = self.progression_state
            self.progression_state = int.from_bytes(game_state[16], byteorder='little')
            if(old_progression_state != self.progression_state): #TODO clear and resync on death
                if(self.progression_state in self.manually_checked_progression_states and not self.progression_state in self.manually_checked_progression):
                    if(self.progression_state == 0x2bc):
                        if(curr_location == 0x1077):
                            self.manually_checked_progression.add(0x2bc)
                            if(self.max_hp_updated == True):
                                self.save_manual_progression = True
                    else:
                        self.manually_checked_progression.add(self.progression_state)
                        if(self.max_hp_updated == True):
                            self.save_manual_progression = True
            if(game_state[29][0] == 0b1 or (old_progression_state != self.progression_state and self.level_transition == 0) or self.try_to_update_connections == True):
                self.try_to_update_connections = False
                self.completed_progression = calc_completed_progression_state(ctx, game_state)
                self.completed_progression.update(self.manually_checked_progression)
                s = "caclulating completed progression : %s" % list(map(hex,sorted(self.completed_progression)))
                if(self.message_level == 3):
                    logger.info(s)
                destinations = []
                progression_states = []#[0,0]
                fix_town_id = []
                if(curr_location in bfm_portals):
                    connection_data = bfm_portals[curr_location]
                    #logger.info("len %s", len(connection_data.connections))
                    s = s + ("\nconnections %s" % (connection_data,))
                    if(self.message_level == 3):
                        logger.info("connections %s", connection_data)
                    for connection in connection_data.connections:
                        #logger.info("con %s", connection)
                        dest = connection.destination
                        if(dest in bfm_portals):
                            calc_progression, hint_text = calc_progression_state(ctx, dest, self.progression_state, game_state, self.completed_progression, received_list)
                            if(curr_location in [0x3069, 0x3075] or connection_data.is_cutscene == True): #Chapter 4 town on fire, queen ant, thirstquencher cutscenes
                                calc_progression = 0
                            if(curr_location == 0x3021 and dest == 0x3003):
                                calc_progression = 0
                            if(curr_location in [0x2018, 0x2059, 0x207e, 0x209b]): #in conners
                                if(self.progression_state == 0x64): #appraised Bracelet
                                    calc_progression = 0
                                elif(self.progression_state == 0x181 and (ctx.slot_data["playthrough_method"] == 2 or game_state[17][13] & 0b1000 == 0b1000)): #appraised ugly belt
                                    calc_progression = 0
                            if(curr_location == 0x3051): #church fight
                                calc_progression = 0
                            if(curr_location == 0x2057 and self.progression_state in [0x118, 0x122]):#orange cutscene
                                calc_progression = 0
                            if(curr_location == 0x3029 and dest == 0x302c): #twinpeak second peak
                                #await self.update_progression(ctx)
                                if(self.progression_state == 0xf0 or calc_progression == 0xf0): #about to meet Hotelo at twinpeak
                                    fix_town_id = fix_town_id + [(0x18e096 + (self.jp_version * 0xe8), [0x0], MAIN_RAM)] #change entrance from 1 to 0 to prevent softlock
                                    if(self.message_level > 0):
                                        logger.info("applied shortcut to hotelo softlock fix")
                            if(dest in [0x1010, 0x1052, 0x1077, 0x1094]): #town
                                if(calc_progression == 0):
                                    if(self.progression_state < 0xc8):
                                        dest = 0x1010
                                    elif(self.progression_state < 0x258):
                                        dest = 0x1052
                                    elif(self.progression_state < 0x398):
                                        dest = 0x1077
                                    else:
                                        dest = 0x1094
                                elif(calc_progression < 0xc8):
                                    dest = 0x1010
                                elif(calc_progression < 0x258):
                                    dest = 0x1052
                                elif(calc_progression < 0x398):
                                    dest = 0x1077
                                else:
                                    dest = 0x1094
                            if(dest in [0x1011, 0x1053, 0x1078, 0x1095]): #upper town
                                if(calc_progression == 0):
                                    if(self.progression_state < 0xc8):
                                        dest = 0x1011
                                    elif(self.progression_state < 0x258):
                                        dest = 0x1053
                                    elif(self.progression_state < 0x398):
                                        dest = 0x1078
                                    else:
                                        dest = 0x1095
                                elif(calc_progression < 0xc8):
                                    dest = 0x1011
                                elif(calc_progression < 0x258):
                                    dest = 0x1053
                                elif(calc_progression < 0x398):
                                    dest = 0x1078
                                else:
                                    dest = 0x1095
                            if(dest == 0x3034 and curr_location in [0x201a, 0x205b, 0x2080, 0x209d] and not (game_state[17][14] & 0b100000 == 0b100000 or game_state[17][14] & 0b1000000 == 0b1000000)): #basement lobby
                                dest = 0x3000
                            if(dest == 0x3043 and curr_location in [0x1010, 0x1052, 0x1077, 0x1094]):#town to Mine
                                if(ctx.slot_data["quest_item_sanity"] == True and not item_name_to_id["Key"] in received_list):
                                    dest = 0x3000
                            if(dest == 0x304e and curr_location in [0x1010, 0x1052, 0x1077, 0x1094]):#town to Well
                                if(ctx.slot_data["quest_item_sanity"] == True and not item_name_to_id["Rope"] in received_list or game_state[17][6] & 0b1 == 0b1):
                                    dest = 0x3000
                                    fix_town_id = fix_town_id + [(connection.memory + 0x2 + (self.jp_version * connection_data.jp_offset), [0], MAIN_RAM)] #change door
                            #if(dest in [0x207b, 0x2098] and self.num_bosses_killed <2): #bakery chapter 4, 5/6
                            #    dest = 0x2056
                            #if(dest in [0x207c, 0x2099] and self.num_bosses_killed <2): #grocery chapter 4, 5/6
                            #    dest = 0x2057
                            if(dest in [0x2080, 0x209d] and not (game_state[17][14] & 0b100000 == 0b100000 or game_state[17][14] & 0b1000000 == 0b1000000)): #restaurant chapter 4, 5/6
                                dest = 0x201a
                            if(dest != connection.destination or dest in [0x3034, 0x3043, 0x304e] or (curr_location in [0x1011, 0x1053, 0x1078, 0x1095] and dest in [0x1010, 0x1052, 0x1077, 0x1094])):
                                fix_town_id = fix_town_id + [(connection.memory + (self.jp_version * connection_data.jp_offset), dest.to_bytes(2, 'little'), MAIN_RAM)]
                            if(len(hint_text) > 0):
                                #logger.info("destination %x, hint_text %s", dest, hint_text)
                                self.hint_dictionary[dest] = hint_text
                            if((dest + 1 & 0xff) in destinations):
                                continue
                            destinations = destinations + [(dest + 1) & 0xff] #need to offset by 1 due to 0x3000
                            calc_array = calc_progression.to_bytes(2, 'little')
                            progression_states = progression_states + [calc_array[0], calc_array[1]]#[calc_progression & 0xff, calc_progression >> 8]
                            
                            s = s + "\nconnection : %s : name : %s" % (hex(dest), bfm_portals[dest].region)
                            if(self.message_level == 3):
                                logger.info("connection : %s : name : %s", hex(dest), bfm_portals[dest].region)

                            if(calc_progression == 0):
                                s = s + "\nno change to game state"
                                if(self.message_level == 3):
                                    logger.info("no change to game state")
                                calc_progression = self.progression_state
                            if(calc_progression in progression_state_table):
                                s = s + "\ngame state : %s : name : %s" % (hex(calc_progression), progression_state_table[calc_progression])
                                if(self.message_level == 3):
                                    logger.info("game state : %s : name : %s", hex(calc_progression), progression_state_table[calc_progression])
                            else:
                                s = s + "\ngame state : %s " % hex(calc_progression)
                                if(self.message_level == 3):
                                    logger.info("game state : %s ", hex(calc_progression))
                    if(self.save_manual_progression == True):
                        self.save_manual_progression = False
                        if(self.message_level == 3):
                            logger.info("saving manually checked progression : %s", list(map(hex,sorted(self.manually_checked_progression))))
                        vals = sum([(1 << i) * (val in self.manually_checked_progression) for i, val in enumerate(self.manually_checked_progression_states)])
                        fix_town_id = fix_town_id + [(0x0ba247 + (self.jp_version * -0xea0), vals.to_bytes(2, 'little'), MAIN_RAM)]
                        if(self.message_level == 3):
                            logger.info("recording manual prog to RAM %s", vals.to_bytes(2, 'little'))
                    s = s + "\ndata: %s : %s : %s" % (destinations, progression_states, fix_town_id)
                    if(self.message_level == 3):
                        logger.info("data: %s : %s : %s", destinations, progression_states, fix_town_id)
                if(ctx.slot_data["fast_walk"] == True):
                    fix_town_id = fix_town_id + [(0x15a7e4 + (self.jp_version * 0x2a8), [0xa0, 0xff, 0x03, 0x3c, 0x2c, 0x00, 0x23, 0xae, 0x1e + (self.jp_version * 0xaa), 0x6a, 0x05, 0x08, 0x00, 0x00, 0x00, 0x00], MAIN_RAM)] #andi $v0 $s0 0x4000 to andi $v0 $s0 0x09 #jmp c8 6a 05 08 for jp version JP 8015ab20
                
                fix_town_id = fix_town_id + [(0x13f430 + (self.jp_version * 0x344), [0x06, 0x01, 0x02, 0x24], MAIN_RAM)] #fix scroll cursor
                await bizhawk.write(
                    ctx.bizhawk_ctx,
                    [(0x075400 + (self.jp_version * -0xe70), [2] + destinations + [0], MAIN_RAM),
                    (0x075422 + (self.jp_version * -0xe70), progression_states, MAIN_RAM)] + fix_town_id
                )

                self.debug_text[self.debug_index] = s
                self.debug_index = not self.debug_index



            save_data: bytes = game_state[1]
            #save_data: bytes = (await bizhawk.read(
            #    ctx.bizhawk_ctx,
            #    [(0x0ae671 + (self.jp_version * -0xea0), 9, MAIN_RAM)] #jp version 0x0ad7d1
            #))[0]
            holdint = [save_data[0],save_data[1],save_data[2],save_data[3]]
            new_bincho_checks = self.decode_booleans(int.from_bytes(holdint, byteorder='little'), 32)
            #logger.info("What was read 0 in 0aae671 %s",self.bincho_checks)
            holdint = [save_data[4],save_data[5]]
            new_bincho_checks.extend(self.decode_booleans(int.from_bytes(holdint, byteorder='little'), 3))
            if(ctx.slot_data["bakery_sanity"] == True):
                new_bakery_checks = self.decode_booleans_with_exclusions(int.from_bytes(holdint, byteorder='little'), 10, [0,1,2])
            else:
                new_bakery_checks = self.bakery_checks
            if(ctx.slot_data["restaurant_sanity"] == True):
                holdint = [save_data[5],save_data[6]]
                new_restaurant_checks = self.decode_booleans_with_exclusions(int.from_bytes(holdint, byteorder='little'), 9, [0,1])
            else:
                new_restaurant_checks = self.restaurant_checks
            if(ctx.slot_data["grocery_sanity"] == True):
                holdint = [save_data[6],save_data[7]]
                new_grocery_checks = self.decode_booleans_with_exclusions(int.from_bytes(holdint, byteorder='little'), 13, [0])
            else:
                new_grocery_checks = self.grocery_checks
            holdint = [save_data[7],save_data[8]]
            new_scroll_checks = self.decode_booleans_with_exclusions(int.from_bytes(holdint, byteorder='little'), 10, [0,1,2,3,4])
            save_data = game_state[2]
            #save_data = (await bizhawk.read(
            #    ctx.bizhawk_ctx,
            #    [(0x0ae650 + (self.jp_version * -0xea0), 2, MAIN_RAM)]
            #))[0]
            holdint = [save_data[0],save_data[1]]
            new_minku_checks = self.decode_booleans(int.from_bytes(holdint, byteorder='little'), 13)
            
            save_data = game_state[3]
            #save_data: bytes = (await bizhawk.read(
            #    ctx.bizhawk_ctx,
            #    [(0x0ae651 + (self.jp_version * -0xea0), 5, MAIN_RAM)]
            #))[0]
            holdint = [save_data[0],save_data[1],save_data[2],save_data[3]]
            new_chest_checks = self.decode_booleans_with_exclusions(int.from_bytes(holdint, byteorder='little'), 32, self.chest_indices_to_skip)
            #logger.info("What was read 0 in 0aae671 %s",self.bincho_checks)
            holdint = [save_data[4]]
            new_chest_checks.extend(self.decode_booleans(int.from_bytes(holdint, byteorder='little'), 7))

            save_data_toys: bytes = bytes()
            if(ctx.slot_data["toy_sanity"] == True or ctx.slot_data["core_sanity"] == True or ctx.slot_data["goal"] > 2):
                save_data_toys = game_state[4]
            #    save_data_toys = (await bizhawk.read(
            #        ctx.bizhawk_ctx,
            #        [(0x0ba21b + (self.jp_version * -0xea0), 43, MAIN_RAM)]
            #    ))[0]

            if(ctx.slot_data["toy_sanity"] == True):
                save_data: bytes = save_data_toys[:30]
                new_toy_checks: List[bool] = [val & 0b10000 == 0b10000 for val in save_data]
                new_toy_inventory: List[bool] = [val & 0b11110000 == 0b10000000 for val in save_data]
                new_toy_purchased_awaiting: List[bool] = [val & 0b11110000 == 0b10010000 for val in save_data]
                new_toy_in_storage: List[bool] = [val & 0b01000000 == 0b01000000 for val in save_data]
                new_toy_needs_fixed: List[bool] = [val & 0b11010000 == 0b11000000 for val in save_data]
                if(True in new_toy_needs_fixed):
                    for i in range(len(new_toy_needs_fixed)):
                        if(new_toy_needs_fixed[i]):
                            toy_data = save_data[i] | 0b10000
                            toy_data = toy_data & 0b10011111
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x0ba21b+i + (self.jp_version * -0xea0), [toy_data], MAIN_RAM)]
                            )
            else:
                new_toy_checks = self.toy_checks
                new_toy_inventory = self.toy_inventory

            
            save_data: bytes = bytes([save_data_toys[11], save_data_toys[17], save_data_toys[23], save_data_toys[29], save_data_toys[35]])
            if(ctx.slot_data["core_sanity"] == True):
                new_core_checks: List[bool] = [val & 0b10000000 == 0b10000000 for val in save_data] 
            else:
                new_core_checks = self.core_checks
            new_num_bosses_killed = sum(val & 0b10000000 == 0b10000000 for val in save_data)
            if(new_num_bosses_killed != self.num_bosses_killed):
                self.num_bosses_killed = new_num_bosses_killed
                limit_levels = [8, 16, 22, 27, 30, 30]
                await bizhawk.write(
                    ctx.bizhawk_ctx,
                    [(0x02aa90 + (self.jp_version * -0xdb0), [limit_levels[self.num_bosses_killed]], MAIN_RAM), #limit lvl 16
                    (0x02aa80 + (self.jp_version * -0xdb0), [limit_levels[self.num_bosses_killed]], MAIN_RAM), #limit lvl 22
                    (0x02aa70 + (self.jp_version * -0xdb0), [limit_levels[self.num_bosses_killed]], MAIN_RAM), #limit lvl 27
                    (0x02aa78 + (self.jp_version * -0xdb0), [0xa], MAIN_RAM), #limit lvl 16 progression state check, lower to 0xa
                    (0x02aa50 + (self.jp_version * -0xdb0), [0x4a, 0x6], MAIN_RAM)] #limit lvl 30 (chapter 6 check)
                )

            if(ctx.slot_data["tech_sanity"] == True):
                save_data = game_state[5:12]
            #    save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, tech_check_locations[self.jp_version]))
                new_tech_checks: List[bool] = []
                for i in range(len(save_data)):
                    new_tech_checks = new_tech_checks + [int.from_bytes(save_data[i], "little")>(2+(i==2))]
            else:
                new_tech_checks = self.tech_checks

            if(ctx.slot_data["level_sanity"] == True):
                save_data = game_state[12:16]
            #    save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, level_memory_ids[self.jp_version]))
                new_body_lvl: int = int.from_bytes(save_data[0], byteorder='little')
                new_mind_lvl: int = int.from_bytes(save_data[1], byteorder='little')
                new_fus_lvl: int = int.from_bytes(save_data[2], byteorder='little')
                new_lum_lvl: int = int.from_bytes(save_data[3], byteorder='little')
            else:
                new_body_lvl = self.curr_body_lvl
                new_mind_lvl = self.curr_mind_lvl
                new_fus_lvl = self.curr_fus_lvl
                new_lum_lvl = self.curr_lum_lvl

            #curr_location_data: bytes = (await bizhawk.read(
            #    ctx.bizhawk_ctx,
            #    [(0x0b9a08 + (self.jp_version * -0xea0), 2, MAIN_RAM)]
            #))[0]
            if(ctx.slot_data["quest_item_sanity"] == True):
                #save_data = game_state[17:25]
                new_quest_item_checks = [False] * 29
                if(self.quest_item_checks[0] == False): #Well water
                    well_H20 = 0x4c
                    if(well_H20 in game_state[19]):
                        #logger.info("well water found")
                        new_quest_item_checks[0] = True
                        if(not item_name_to_id["Well H20"] in received_list):
                            new_inventory: List[int] = [val * (well_H20 != val) for val in game_state[19]] 
                            #new_inventory: List[int] = [val for val in save_data[19]] 
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x0ba1e7 + (self.jp_version * -0xea0), new_inventory, MAIN_RAM),
                                (well_water_id[self.jp_version][curr_location], [0x0], MAIN_RAM)]
                            )
                else:
                    new_quest_item_checks[0] = True
                #Jon's Key
                new_quest_item_checks[1] = game_state[17][11] & 0b1000000 == 0b1000000
                #Logs
                num_logs = game_state[22].count(0b11)
                new_quest_item_checks[2] = num_logs > 0
                new_quest_item_checks[3] = num_logs > 1
                new_quest_item_checks[4] = num_logs > 2
                new_quest_item_checks[5] = num_logs > 3
                #Manual (moved to mayor cutscene)
                new_quest_item_checks[6] = game_state[17][12] & 0b10000 == 0b10000
                #Mayor Berry
                new_quest_item_checks[7] = game_state[17][12] & 0b10000000 == 0b10000000
                #Key from Wid
                new_quest_item_checks[8] = self.progression_state == 0xdc and curr_location == 0x1052
                #new_quest_item_checks[8] = int.from_bytes(game_state[24], byteorder='little') >= 0x47
                #Misteria
                new_quest_item_checks[9] = (self.progression_state == 0xe6 and curr_location == 0x3047)
                #Aqualin
                new_quest_item_checks[10] = self.progression_state == 0x10e or (game_state[17][14] & 0b10 == 0b10)
                #save tim/orange
                new_quest_item_checks[11] = game_state[17][14] & 0b1000 == 0b1000
                #Ugly Belt
                new_quest_item_checks[12] = self.progression_state == 0x17c
                #Rope
                new_quest_item_checks[13] = game_state[20][0] & 0b10000000 == 0b10000000 and curr_location == 0x1052
                #Angel Statue
                new_quest_item_checks[14] = int.from_bytes(game_state[18], byteorder='little') == 0x1052
                #Pie
                new_quest_item_checks[15] = self.progression_state == 0x280
                #Gondola Gizmo
                gizmo_state = int.from_bytes(game_state[23], byteorder='little')
                new_quest_item_checks[16] = gizmo_state == 4
                new_quest_item_checks[17] = gizmo_state == 3
                new_quest_item_checks[18] = gizmo_state == 2
                new_quest_item_checks[19] = gizmo_state == 1
                #Calendar/Rocksalt
                new_quest_item_checks[20] = self.progression_state == 0x2bc and curr_location == 0x1077 
                new_quest_item_checks[21] = self.progression_state == 0x2bc and curr_location == 0x1077
                #Handles
                new_quest_item_checks[22] = self.progression_state == 0x3ca or (game_state[17][6] & 0b100000 == 0b100000)
                new_quest_item_checks[23] = game_state[17][6] & 0b1000000 == 0b1000000
                new_quest_item_checks[24] = game_state[17][6] & 0b10000000 == 0b10000000
                new_quest_item_checks[25] = game_state[17][7] & 0b1 == 0b1
                #profits
                new_quest_item_checks[26] = game_state[21][0] & 0b10000000 == 0b10000000
                #Musashi's share of the profits
                new_quest_item_checks[27] = game_state[17][20] & 0b100000 == 0b100000
                #Jon's Note
                new_quest_item_checks[28] = game_state[17][22] & 0b1 == 0b1
            else:
                new_quest_item_checks = self.quest_item_checks

            locations_to_send_to_server = []
            #logger.info("What was read 1 in 0aae671 %s",new_bincho_checks)
            if(new_bincho_checks != self.bincho_checks):
                for i in range(len(new_bincho_checks)):
                    if(new_bincho_checks[i]):
                        locations_to_send_to_server.append(location_base_id + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                #logger.info("Sending Bincho checks")
                if(new_bincho_checks[0] == True and self.bincho_checks[0] == False):
                    #logger.info("Sending Guard bincho check")
                    self.update_list_of_received_items(ctx)
                    #logger.info("items receieved %s", self.list_of_received_items)
                    if(not item_name_to_id["Guard"] in received_list):
                        save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                            0x0ae666 + (self.jp_version * -0xea0), 1, MAIN_RAM
                        )]))[0]
                        guard_state = int.from_bytes(save_data, byteorder='little')
                        if(guard_state & 0x1 == 0x1):
                            if(self.message_level > 0):
                                logger.info("Sending Macho back to Twinpeak")
                            guard_state = guard_state & 0xfe
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x0ae666 + (self.jp_version * -0xea0), [guard_state], MAIN_RAM)]
                            )

                #logger.info("What was read in 0ae671 %s",save_data)
                #logger.info("Trying to send %s",locations_to_send_to_server)
                #await ctx.send_msgs([{
                #    "cmd": "LocationChecks",
                #    "locations": locations_to_send_to_server
                #}])
                #self.bincho_checks = new_bincho_checks
            #logger.info("items Received %s",ctx.items_received)

            if(new_minku_checks != self.minku_checks):
                for i in range(len(new_minku_checks)):
                    if(new_minku_checks[i]):
                        locations_to_send_to_server.append(location_base_id + i + 35 + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                #logger.info("What was read in 0ae671 %s",save_data)
                #logger.info("Trying to send %s",locations_to_send_to_server)

            if(new_chest_checks != self.chest_checks):
                for i in range(len(new_chest_checks)):
                    if(new_chest_checks[i]):
                        locations_to_send_to_server.append(location_base_id + i + 48 + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
            
            if(new_bakery_checks != self.bakery_checks):
                #logger.info("bakery checks %s", new_bakery_checks)
                for i in range(len(new_bakery_checks)):
                    if(new_bakery_checks[i]):
                        locations_to_send_to_server.append(location_base_id + i + 82 + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                        if(i*2 < len(self.bakery_dialog)):
                            if(not "Purchased" in self.bakery_dialog[i*2] and not "かいもの" in self.bakery_dialog[i*2]):
                                if(self.jp_version == False):
                                    self.bakery_dialog[i*2] = "Purchased"
                                else:
                                    self.bakery_dialog[i*2] = "かいもの"
                                self.fix_dialog(self.bakery_dialog)

            if(new_restaurant_checks != self.restaurant_checks):
                #logger.info("bakery checks %s", new_bakery_checks)
                for i in range(len(new_restaurant_checks)):
                    if(new_restaurant_checks[i]):
                        locations_to_send_to_server.append(location_base_id + i + 89 + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                        if(i*2 < len(self.restaurant_dialog)):
                            if(not "Purchased" in self.restaurant_dialog[i*2] and not "かいもの" in self.restaurant_dialog[i*2]):
                                if(self.jp_version == False):
                                    self.restaurant_dialog[i*2] = "Purchased"
                                else:
                                    self.restaurant_dialog[i*2] = "かいもの"
                                self.fix_dialog(self.restaurant_dialog)

            if(new_grocery_checks != self.grocery_checks):
                #logger.info("bakery checks %s", new_bakery_checks)
                for i in range(len(new_grocery_checks)):
                    if(new_grocery_checks[i]):
                        locations_to_send_to_server.append(standard_location_name_to_id["Item 1 - Grocery"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                        if(i*2 < len(self.grocery_dialog)):
                            if(not "Purchased" in self.grocery_dialog[i*2] and not "かいもの" in self.grocery_dialog[i*2]):
                                if(self.jp_version == False):
                                    self.grocery_dialog[i*2] = "Purchased"
                                else:
                                    self.grocery_dialog[i*2] = "かいもの"
                                self.fix_dialog(self.grocery_dialog)
            
            if(new_toy_checks != self.toy_checks):
                #logger.info("bakery checks %s", new_bakery_checks)
                for i in range(len(new_toy_checks)):
                    if(new_toy_checks[i]):
                        locations_to_send_to_server.append(standard_location_name_to_id["Musashi - Toy Shop"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                        if(new_toy_purchased_awaiting[i]):
                            if(item_name_to_id["Musashi Action Figure"] + i in received_list):
                                if(self.message_level > 0):
                                    logger.info("adding %s toy to storage", item_id_to_name[item_name_to_id["Musashi Action Figure"] + i])
                                save_data: bytes = (await bizhawk.read(
                                    ctx.bizhawk_ctx,
                                    [(0x0ba21b+i + (self.jp_version * -0xea0), 1, MAIN_RAM)]
                                ))[0]
                                toy_data = save_data[0] | 0b1000000
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x0ba21b+i + (self.jp_version * -0xea0), [toy_data], MAIN_RAM)]
                                )
                                new_toy_in_storage[i] = True
                                new_toy_purchased_awaiting[i] = False


            if(new_toy_inventory != self.toy_inventory):
                toys_for_sale = []
                for i in range(len(new_toy_inventory)):
                    if(new_toy_inventory[i] and not self.toy_inventory[i]):
                        toys_for_sale = toys_for_sale + [item_id_to_name[item_name_to_id["Musashi Action Figure"] + i]]
                if(len(toys_for_sale)>0):
                    if(self.message_level > 0):
                        logger.info("new toys for sale %s",toys_for_sale)
                self.toy_inventory = new_toy_inventory
            
            if(new_tech_checks != self.tech_checks):
                for i in range(len(new_tech_checks)):
                    if(new_tech_checks[i]):
                        locations_to_send_to_server.append(standard_location_name_to_id["Improved Fusion (Artisan) - Allucaneet Castle"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))

            if(new_core_checks != self.core_checks):
                for i in range(len(new_core_checks)):
                    if(new_core_checks[i]):
                        locations_to_send_to_server.append(standard_location_name_to_id["Defeat Earth Crest Guardian - Skullpion Arena"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
            

            if(new_scroll_checks != self.scroll_checks):
                for i in range(len(new_scroll_checks)):
                    if(new_scroll_checks[i]):
                        if(ctx.slot_data["scroll_sanity"] == True):
                            locations_to_send_to_server.append(standard_location_name_to_id["Earth Scroll - Twinpeak First Peak"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                            if(i == 3):
                                self.found_wind_scroll = True
                                if(curr_location == 0x3023):
                                    if(not item_name_to_id["Wind Scroll"] in received_list):
                                        if(self.message_level > 0):
                                            logger.info("digging hole")
                                        await bizhawk.write(
                                            ctx.bizhawk_ctx,
                                            [(0x1206da + (self.jp_version * 0xa70), [0x23, 0xfb], MAIN_RAM)]
                                        )
                        else:
                            if(i == 3):
                                self.found_wind_scroll = True
                            if(i < 2):
                                save_data: bytes = (await bizhawk.read(
                                    ctx.bizhawk_ctx,
                                    [(0x0ae64a + (self.jp_version * -0xea0), 1, MAIN_RAM)]
                                ))[0]
                                
                                scroll_data = save_data[0] | (0b1 << (i + 6))
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x0ae64a + (self.jp_version * -0xea0), [scroll_data], MAIN_RAM)]
                                )
                            else:
                                save_data: bytes = (await bizhawk.read(
                                    ctx.bizhawk_ctx,
                                    [(0x0ae64b + (self.jp_version * -0xea0), 1, MAIN_RAM)]
                                ))[0]
                                scroll_data = save_data[0] | (0b1 << (i - 2))
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x0ae64b + (self.jp_version * -0xea0), [scroll_data], MAIN_RAM)]
                                )

            if(self.curr_body_lvl != new_body_lvl):
                for i in range(new_body_lvl):
                    locations_to_send_to_server.append(standard_location_name_to_id["lvl 2 Body - Menu"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                stats_to_write = [(0x0638fa + (self.jp_version * -0xea4) + 16 * (new_body_lvl), self.curr_body_stat.to_bytes(2, 'little'), MAIN_RAM)]
                if(new_body_lvl < 29):
                    stats_to_write.append((0x0638fa + (self.jp_version * -0xea4) + 16 * (new_body_lvl + 1), self.curr_body_stat.to_bytes(2, 'little'), MAIN_RAM))
                await bizhawk.write(
                    ctx.bizhawk_ctx,
                    stats_to_write
                )
            
            if(self.curr_mind_lvl != new_mind_lvl):
                for i in range(new_mind_lvl):
                    locations_to_send_to_server.append(standard_location_name_to_id["lvl 2 Mind - Menu"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                stats_to_write = [(0x0638fe + (self.jp_version * -0xea4) + 16 * (new_mind_lvl), self.curr_mind_stat.to_bytes(2, 'little'), MAIN_RAM)]
                if(new_mind_lvl < 29):
                    stats_to_write.append((0x0638fe + (self.jp_version * -0xea4) + 16 * (new_mind_lvl + 1), self.curr_mind_stat.to_bytes(2, 'little'), MAIN_RAM))
                await bizhawk.write(
                    ctx.bizhawk_ctx,
                    stats_to_write
                )

            if(self.curr_fus_lvl != new_fus_lvl):
                for i in range(new_fus_lvl):
                    locations_to_send_to_server.append(standard_location_name_to_id["lvl 2 Fus - Menu"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                stats_to_write = [(0x063906 + (self.jp_version * -0xea4) + 16 * (new_fus_lvl), self.curr_fus_stat.to_bytes(2, 'little'), MAIN_RAM)]
                if(new_fus_lvl < 29):
                    stats_to_write.append((0x063906 + (self.jp_version * -0xea4) + 16 * (new_fus_lvl + 1), self.curr_fus_stat.to_bytes(2, 'little'), MAIN_RAM))
                await bizhawk.write(
                    ctx.bizhawk_ctx,
                    stats_to_write
                )

            if(self.curr_lum_lvl != new_lum_lvl):
                for i in range(new_lum_lvl):
                    locations_to_send_to_server.append(standard_location_name_to_id["lvl 2 Lum - Menu"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                stats_to_write = [(0x063902 + (self.jp_version * -0xea4) + 16 * (new_lum_lvl), self.curr_lum_stat.to_bytes(2, 'little'), MAIN_RAM)]
                if(new_lum_lvl < 29):
                    stats_to_write.append((0x063902 + (self.jp_version * -0xea4) + 16 * (new_lum_lvl + 1), self.curr_lum_stat.to_bytes(2, 'little'), MAIN_RAM))
                await bizhawk.write(
                    ctx.bizhawk_ctx,
                    stats_to_write
                )
            if(new_quest_item_checks != self.quest_item_checks):
                for i in range(len(new_quest_item_checks)):
                    if(new_quest_item_checks[i]):
                        locations_to_send_to_server.append(standard_location_name_to_id["Well H20 - Grillin Village"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))


            #if(new_bincho_checks != self.bincho_checks or new_minku_checks != self.minku_checks or new_chest_checks != self.chest_checks or new_bakery_checks != self.bakery_checks or new_restaurant_checks != self.restaurant_checks or new_grocery_checks != self.grocery_checks or new_toy_checks != self.toy_checks or new_tech_checks != self.tech_checks or new_scroll_checks != self.scroll_checks or new_core_checks != self.core_checks):
            if(len(locations_to_send_to_server) > 0):
                await ctx.check_locations(locations_to_send_to_server)
                #await ctx.send_msgs([{
                #    "cmd": "LocationChecks",
                #    "locations": locations_to_send_to_server
                #}])
                self.bincho_checks = new_bincho_checks
                self.minku_checks = new_minku_checks
                self.chest_checks = new_chest_checks
                self.bakery_checks = new_bakery_checks
                self.restaurant_checks = new_restaurant_checks
                self.grocery_checks = new_grocery_checks
                self.toy_checks = new_toy_checks
                self.tech_checks = new_tech_checks
                self.scroll_checks = new_scroll_checks
                self.core_checks = new_core_checks
                self.curr_body_lvl = new_body_lvl
                self.curr_mind_lvl = new_mind_lvl
                self.curr_fus_lvl = new_fus_lvl
                self.curr_lum_lvl = new_lum_lvl
                self.quest_item_checks = new_quest_item_checks

            
            if(curr_location == 0x3005): #main menu/first moon cutscene
                self.level_transition = 1
            if(curr_location in [0x3012, 0x3054, 0x3079, 0x3096]): #waking up from nightmare
                self.level_transition = 1
                self.received_count = 0
                self.old_step_count = 0
                self.death_link_timer = 240
                self.has_died = 0
                self.check_if_lumina_needs_removed = 1
                self.max_hp_updated = False
                curr_hp_bytes: bytes = (await bizhawk.read(
                    ctx.bizhawk_ctx,
                    [(0x078eb4 + (self.jp_version * -0xea0), 2, MAIN_RAM)]
                ))[0]
                curr_hp: int = int.from_bytes(curr_hp_bytes, byteorder='little')
                if curr_hp < 5:
                    new_hp = 150
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [(0x078eb4+ (self.jp_version * -0xea0), new_hp.to_bytes(2, 'little'), MAIN_RAM)]
                    )   

            #logger.info("curr_location %s",curr_location)
            #logger.info("in Town")
            #if(curr_location == 4112 or curr_location == 4178):
            #not save menu
            #if(curr_location != 12296):

            if(self.old_step_count != 0 and self.level_transition != 1):
                for _ in range(4):
                    if(self.received_count < len(ctx.items_received)):
                        #logger.info("list %s",ctx.items_received[self.received_count])
                        item_id = ctx.items_received[self.received_count][0]
                        if(item_id > jp_id_offset):
                            item_id = item_id - jp_id_offset
                        #logger.info("list %s",item_id)
                        if(item_id>0x0ba1f7 and item_id<0x0ba21b):
                            npc_state: bytes = (await bizhawk.read(
                                ctx.bizhawk_ctx,
                                [(item_id + (self.jp_version * -0xea0), 1, MAIN_RAM)]
                            ))[0]
                            if(npc_state[0] == 0b0):
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(item_id + (self.jp_version * -0xea0), [0b1], MAIN_RAM)]
                                )
                                if(self.message_level > 0):
                                    logger.info("adding to rescue list %s",item_id_to_name[item_id])
                                #logger.info("IDs of receieved items %s",set(received_list))
                                #logger.info("IDs of all NPCs %s",set(npc_ids))
                            else:
                                if(self.message_level > 0):
                                    logger.info("already in rescue list: %s",item_id_to_name[item_id])
                            if(item_id == item_name_to_id["Guard"]):
                                save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                    0x0ae666 + (self.jp_version * -0xea0), 1, MAIN_RAM
                                )]))[0]
                                guard_state = int.from_bytes(save_data, byteorder='little')
                                if(guard_state & 0x1 == 0x0):
                                    if(self.message_level > 0):
                                        logger.info("Sending Guard to Twinpeak")
                                    guard_state = guard_state | 0x1
                                    await bizhawk.write(
                                        ctx.bizhawk_ctx,
                                        [(0x0ae666 + (self.jp_version * -0xea0), [guard_state], MAIN_RAM)]
                                    )
                        elif(item_id==0x0ba21b): #found max health berry
                            await self.update_max_hp(ctx, self.received_count+1)
                            if(self.message_level > 0):
                                logger.info("Longevity Berry Found")
                            """curr_max_hp_bytes: bytes = (await bizhawk.read(
                                ctx.bizhawk_ctx,
                                [(0x078eb2, 2, MAIN_RAM)]
                            ))[0]
                            curr_max_hp: int = int.from_bytes(curr_max_hp_bytes, byteorder='little')
                            new_hp = ctx.slot_data["starting_hp"] + 25
                            for i in range(self.received_count+1):
                                if(ctx.items_received[i][0] == 0x0ba21b):
                                    new_hp += 25
                            if(curr_max_hp < new_hp):
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x078eb2, new_hp.to_bytes(2, 'little'), MAIN_RAM)]
                                )#max hp
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x078eb4, new_hp.to_bytes(2, 'little'), MAIN_RAM)]
                                )#current hp"""
                        elif(item_id == 0xa):
                            if(ctx.slot_data["grocery_s_revive"] == True):
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x10ee64 + (self.jp_version * 0x1d10), [0x1e, 0, 0x1e, 0], MAIN_RAM)]
                                )#lower s-revive price
                        elif((item_id < 0x68 and item_id > 0x12) or item_id == 0x6c or item_id == 0x6e):
                            if(ctx.slot_data["playthrough_method"] == 1 and item_id in [0x56, 0x58, 0x59, 0x5a] and not 0xc8 in self.completed_progression):
                                if(not item_id in self.chapter3_items):
                                    self.chapter3_items.append(item_id)
                                    if(self.message_level > 0):
                                        logger.info("Witholding %s until completing chapter 2", item_id_to_name[item_id])
                            elif(ctx.slot_data["playthrough_method"] == 1 and item_id in [0x5e, 0x5f, 0x63, 0x64, 0x65, 0x66] and not (0x258 in self.completed_progression and 0x1e0 in self.completed_progression and 0x1ae in self.completed_progression)):
                                if(not item_id in self.chapter4_items):
                                    self.chapter4_items.append(item_id)
                                    if(self.message_level > 0):
                                        logger.info("Witholding %s until completing chapter 3", item_id_to_name[item_id])
                            elif(ctx.slot_data["playthrough_method"] == 1 and item_id in [0x67, 0x5b, 0x5c, 0x5d, 0x6c, 0x6e] and not 0x384 in self.completed_progression):
                                if(not item_id in self.chapter5_items):
                                    self.chapter4_items.append(item_id)
                                    if(self.message_level > 0):
                                        logger.info("Witholding %s until completing chapter 4", item_id_to_name[item_id])
                            else:
                                if(not item_id in self.bakery_inventory_expansion):
                                    self.bakery_inventory_expansion.append(item_id)
                                    if(self.message_level > 0):
                                        logger.info("%s added to Bakery",item_id_to_name[item_id])
                            if(item_name_to_id["Key"] == item_id or ctx.slot_data["quest_item_sanity"] == False):
                                if(item_name_to_id["Water Boss Core"] in received_list or (ctx.slot_data["core_sanity"] == False and save_data_toys[17] & 0b10000000 == 0b10000000)):
                                    if(self.message_level > 0):
                                        logger.info("adding Water Boss Core")
                                    i = item_name_to_id["Water Boss Core"] - 0x28a + 2
                                    save_data: bytes = (await bizhawk.read(
                                        ctx.bizhawk_ctx,
                                        [(0x0ae659 + (self.jp_version * -0xea0), 1, MAIN_RAM)]
                                    ))[0]
                                    
                                    core_data = save_data[0] | (0b1 << i)
                                    await bizhawk.write(
                                        ctx.bizhawk_ctx,
                                        [(0x0ae659 + (self.jp_version * -0xea0), [core_data], MAIN_RAM)]
                                    )
                        elif(item_id == 0x78):
                            curr_money_bytes: bytes = (await bizhawk.read(
                                ctx.bizhawk_ctx,
                                [(0x078e8C + (self.jp_version * -0xea0), 4, MAIN_RAM)]
                            ))[0]
                            curr_money: int = int.from_bytes(curr_money_bytes, byteorder='little')
                            new_money = curr_money
                            num_boons_byte: bytes = (await bizhawk.read(
                                ctx.bizhawk_ctx,
                                [(0x0ba246 + (self.jp_version * -0xea0), 1, MAIN_RAM)]
                            ))[0]
                            num_boons: int = int.from_bytes(num_boons_byte, byteorder='little')
                            boon_count = 0
                            for i in range(self.received_count+1):
                                if(ctx.items_received[i][0] == 0x78 + ((ctx.slot_data["set_lang"] == 2) * jp_id_offset)):
                                    boon_count += 1
                                    if(boon_count > num_boons):
                                        new_money += 100
                            if(curr_money < new_money):
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x078e8C + (self.jp_version * -0xea0), new_money.to_bytes(4, 'little'), MAIN_RAM)]
                                )
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x0ba246 + (self.jp_version * -0xea0), boon_count.to_bytes(1, 'little'), MAIN_RAM)]  #0x0ba238 is queen ant toy, maybe 0x0ba246
                                )
                                if(self.message_level > 0):
                                    logger.info("added 1000 Drans to wallet")
                        elif(item_id == 0x79):
                            if(self.message_level > 0):
                                logger.info("Returning Lumina")
                            save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                0x0ae658 + (self.jp_version * -0xea0), 1, MAIN_RAM
                            )]))[0]
                            lumina_state = int.from_bytes(save_data, byteorder='little')
                            lumina_state = lumina_state | 0b1
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x0ae658 + (self.jp_version * -0xea0), [lumina_state], MAIN_RAM)]
                            )
                            """
                            save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                0x078ec0, 1, MAIN_RAM
                            )]))[0]
                            lumina_state = int.from_bytes(save_data, byteorder='little')
                            lumina_state = lumina_state | 0b1
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x078ec0, [lumina_state], MAIN_RAM)]
                            )"""
                        elif(item_id == 0x80):
                            if(self.message_level > 0):
                                logger.info("New stock added to Bakery")
                        elif(item_id < 0x78 and item_id > 0x70):
                            if(self.message_level > 0):
                                logger.info("%s added to Restaurant",item_id_to_name[item_id])
                        elif(item_id < 0xc or item_id == 0x6a or item_id == 0x6b or item_id== 0x6d):
                            if(self.message_level > 0):
                                logger.info("%s added to Grocery",item_id_to_name[item_id])
                        elif(item_id >= item_name_to_id["Musashi Action Figure"] and item_id < item_name_to_id["Musashi Action Figure"] + len(item_name_groups["Toy Shop"])):
                            if(ctx.slot_data["toy_sanity"] == True):
                                val = item_id - item_name_to_id["Musashi Action Figure"]
                                if(new_toy_purchased_awaiting[val] == False):
                                    if(new_toy_in_storage[val]):
                                        if(self.message_level > 0):
                                            logger.info("%s toy already in storage", item_id_to_name[item_id])
                                    else:
                                        if(self.message_level > 0):
                                            logger.info("received %s toy but was not yet purchased", item_id_to_name[item_id])
                                else:
                                    if(self.message_level > 0):
                                        logger.info("adding %s toy to storage", item_id_to_name[item_id])
                                    save_data: bytes = (await bizhawk.read(
                                        ctx.bizhawk_ctx,
                                        [(0x0ba21b+val + (self.jp_version * -0xea0), 1, MAIN_RAM)]
                                    ))[0]
                                    toy_data = save_data[0] | 0b1000000
                                    await bizhawk.write(
                                        ctx.bizhawk_ctx,
                                        [(0x0ba21b+val + (self.jp_version * -0xea0), [toy_data], MAIN_RAM)]
                                    )
                                    new_toy_in_storage[val] = True
                                    new_toy_purchased_awaiting[val] = False
                            else:
                                if(self.message_level > 0):
                                    logger.info("received toy when toysanity was disabled, something went wrong")
                        elif(item_id>0x80 and item_id<0x88):
                            if(self.message_level > 0):
                                logger.info("adding %s to Tech",item_id_to_name[item_id])
                            if(item_id == 0x87):
                                save_data: bytes = (await bizhawk.read(
                                    ctx.bizhawk_ctx,
                                    [(0x0ae659 + (self.jp_version * -0xea0), 1, MAIN_RAM)]
                                ))[0]
                                tech_data = save_data[0] | 0b10
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x0ae659 + (self.jp_version * -0xea0), [tech_data], MAIN_RAM)]
                                )
                            else:
                                save_data: bytes = (await bizhawk.read(
                                    ctx.bizhawk_ctx,
                                    [(0x0ae658 + (self.jp_version * -0xea0), 1, MAIN_RAM)]
                                ))[0]
                                tech_data = save_data[0] | (0b1 << (item_id - 0x80 + (item_id > 0x83)))
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x0ae658 + (self.jp_version * -0xea0), [tech_data], MAIN_RAM)]
                                )
                        elif(item_id > 0x215 and item_id < 0x21b):
                            if(self.message_level > 0):
                                logger.info("adding %s",item_id_to_name[item_id])
                            i = item_id - 0x216
                            if(i < 2):
                                save_data: bytes = (await bizhawk.read(
                                    ctx.bizhawk_ctx,
                                    [(0x0ae64a + (self.jp_version * -0xea0), 1, MAIN_RAM)]
                                ))[0]
                                
                                scroll_data = save_data[0] | (0b1 << (i + 6))
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x0ae64a + (self.jp_version * -0xea0), [scroll_data], MAIN_RAM)]
                                )
                            else:
                                save_data: bytes = (await bizhawk.read(
                                    ctx.bizhawk_ctx,
                                    [(0x0ae64b + (self.jp_version * -0xea0), 1, MAIN_RAM)]
                                ))[0]
                                scroll_data = save_data[0] | (0b1 << (i - 2))
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x0ae64b + (self.jp_version * -0xea0), [scroll_data], MAIN_RAM)]
                                )
                        elif(item_id > 0x289 and item_id < 0x28e): #boss cores
                            if(item_name_to_id["Water Boss Core"] == item_id and not item_name_to_id["Key"] in received_list and ctx.slot_data["quest_item_sanity"] == True):
                                if(self.message_level > 0):
                                    logger.info("witholding water boss core until Key is found to prevent softlocks")
                            else:
                                if(self.message_level > 0):
                                    logger.info("adding %s",item_id_to_name[item_id])
                                i = item_id - 0x28a + 2
                                save_data: bytes = (await bizhawk.read(
                                    ctx.bizhawk_ctx,
                                    [(0x0ae659 + (self.jp_version * -0xea0), 1, MAIN_RAM)]
                                ))[0]
                                
                                core_data = save_data[0] | (0b1 << i)
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x0ae659 + (self.jp_version * -0xea0), [core_data], MAIN_RAM)]
                                )
                        elif(item_id == 0x401): #body stat up
                            new_stat_value = 40
                            stat_up_found = 0
                            for i in range(len(ctx.items_received)):
                                if(ctx.items_received[i][0] == item_id + ((ctx.slot_data["set_lang"] == 2) * jp_id_offset)):
                                    stat_up_found = stat_up_found + 1
                            stat_up_found = min(stat_up_found, ctx.slot_data["level_bundles"])
                            if(ctx.slot_data["stat_gain_modifier"] == 1): #Early
                                new_stat_value = 4 + round(32 * math.sqrt(stat_up_found / ctx.slot_data["level_bundles"]))
                            elif(ctx.slot_data["stat_gain_modifier"] == 2): #Vanilla
                                new_stat_value = body_stat[round(29.0 * stat_up_found / ctx.slot_data["level_bundles"])]
                            else: #Enhanced
                                new_stat_value = body_stat[round(29.0 * stat_up_found / ctx.slot_data["level_bundles"])] + round(math.pow(stat_up_found / ctx.slot_data["level_bundles"], 10) * 100)
                            if(new_stat_value != self.curr_body_stat):
                                if(self.message_level > 0):
                                    logger.info("%s: %s -> %s",item_id_to_name[item_id], self.curr_body_stat, new_stat_value)
                                self.curr_body_stat = new_stat_value
                                stats_to_write = [(0x0638fa + (self.jp_version * -0xea4) + 16 * (self.curr_body_lvl), self.curr_body_stat.to_bytes(2, 'little'), MAIN_RAM)]
                                if(self.curr_body_lvl < 29):
                                    stats_to_write.append((0x0638fa + (self.jp_version * -0xea4) + 16 * (self.curr_body_lvl + 1), self.curr_body_stat.to_bytes(2, 'little'), MAIN_RAM))
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    stats_to_write
                                )
                        elif(item_id == 0x402): #mind stat up
                            new_stat_value = 40
                            stat_up_found = 0
                            for i in range(len(ctx.items_received)):
                                if(ctx.items_received[i][0] == item_id + ((ctx.slot_data["set_lang"] == 2) * jp_id_offset)):
                                    stat_up_found = stat_up_found + 1
                            stat_up_found = min(stat_up_found, ctx.slot_data["level_bundles"])
                            if(ctx.slot_data["stat_gain_modifier"] == 1): #Early
                                new_stat_value = 6 + round(38 * math.sqrt(stat_up_found / ctx.slot_data["level_bundles"]))
                            elif(ctx.slot_data["stat_gain_modifier"] == 2): #Vanilla
                                new_stat_value = mind_stat[round(29.0 * stat_up_found / ctx.slot_data["level_bundles"])]
                            else: #Enhanced
                                new_stat_value = mind_stat[round(29.0 * stat_up_found / ctx.slot_data["level_bundles"])] + round(math.pow(stat_up_found / ctx.slot_data["level_bundles"], 10) * 100)
                            if(new_stat_value != self.curr_mind_stat):
                                if(self.message_level > 0):
                                    logger.info("%s: %s -> %s",item_id_to_name[item_id], self.curr_mind_stat, new_stat_value)
                                self.curr_mind_stat = new_stat_value
                                stats_to_write = [(0x0638fe + (self.jp_version * -0xea4) + 16 * (self.curr_mind_lvl), self.curr_mind_stat.to_bytes(2, 'little'), MAIN_RAM)]
                                if(self.curr_mind_lvl < 29):
                                    stats_to_write.append((0x0638fe + (self.jp_version * -0xea4) + 16 * (self.curr_mind_lvl + 1), self.curr_mind_stat.to_bytes(2, 'little'), MAIN_RAM))
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    stats_to_write
                                )
                        elif(item_id == 0x403): #fusion stat up
                            new_stat_value = 40
                            stat_up_found = 0
                            for i in range(len(ctx.items_received)):
                                if(ctx.items_received[i][0] == item_id + ((ctx.slot_data["set_lang"] == 2) * jp_id_offset)):
                                    stat_up_found = stat_up_found + 1
                            stat_up_found = min(stat_up_found, ctx.slot_data["level_bundles"])
                            if(ctx.slot_data["stat_gain_modifier"] == 1): #Early
                                new_stat_value = 4 + round(34 * math.sqrt(stat_up_found / ctx.slot_data["level_bundles"]))
                            elif(ctx.slot_data["stat_gain_modifier"] == 2): #Vanilla
                                new_stat_value = fusion_stat[round(29.0 * stat_up_found / ctx.slot_data["level_bundles"])]
                            else: #Enhanced
                                new_stat_value = fusion_stat[round(29.0 * stat_up_found / ctx.slot_data["level_bundles"])] + round(math.pow(stat_up_found / ctx.slot_data["level_bundles"], 10) * 100)
                            if(new_stat_value != self.curr_fus_stat):
                                if(self.message_level > 0):
                                    logger.info("%s: %s -> %s",item_id_to_name[item_id], self.curr_fus_stat, new_stat_value)
                                self.curr_fus_stat = new_stat_value
                                stats_to_write = [(0x063906 + (self.jp_version * -0xea4) + 16 * (self.curr_fus_lvl), self.curr_fus_stat.to_bytes(2, 'little'), MAIN_RAM)]
                                if(self.curr_fus_lvl < 29):
                                    stats_to_write.append((0x063906 + (self.jp_version * -0xea4) + 16 * (self.curr_fus_lvl + 1), self.curr_fus_stat.to_bytes(2, 'little'), MAIN_RAM))
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    stats_to_write
                                )
                        elif(item_id == 0x404): #Lumina stat up
                            new_stat_value = 40
                            stat_up_found = 0
                            for i in range(len(ctx.items_received)):
                                if(ctx.items_received[i][0] == item_id + ((ctx.slot_data["set_lang"] == 2) * jp_id_offset)):
                                    stat_up_found = stat_up_found + 1
                            stat_up_found = min(stat_up_found, ctx.slot_data["level_bundles"])
                            if(ctx.slot_data["stat_gain_modifier"] == 1): #Early
                                new_stat_value = 8 + round(68 * math.sqrt(stat_up_found / ctx.slot_data["level_bundles"]))
                            elif(ctx.slot_data["stat_gain_modifier"] == 2): #Vanilla
                                new_stat_value = lumina_stat[round(29.0 * stat_up_found / ctx.slot_data["level_bundles"])]
                            else: #Enhanced
                                new_stat_value = lumina_stat[round(29.0 * stat_up_found / ctx.slot_data["level_bundles"])] + round(math.pow(stat_up_found / ctx.slot_data["level_bundles"], 10) * 1000)
                            if(new_stat_value != self.curr_lum_stat):
                                if(self.message_level > 0):
                                    logger.info("%s: %s -> %s",item_id_to_name[item_id], self.curr_lum_stat, new_stat_value)
                                self.curr_lum_stat = new_stat_value
                                stats_to_write = [(0x063902 + (self.jp_version * -0xea4) + 16 * (self.curr_lum_lvl), self.curr_lum_stat.to_bytes(2, 'little'), MAIN_RAM)]
                                if(self.curr_lum_lvl < 29):
                                    stats_to_write.append((0x063902 + (self.jp_version * -0xea4) + 16 * (self.curr_lum_lvl + 1), self.curr_lum_stat.to_bytes(2, 'little'), MAIN_RAM))
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    stats_to_write
                                )
                        elif(item_id == 0x500): #Well H20
                            if(self.message_level > 0):
                                logger.info("Well H20 returned to well")
                        elif(item_id == 0x501): #Log
                            log_ids = [0x4e, 0x50, 0x51, 0x52]
                            log_ids = log_ids[:received_list.count(item_name_to_id["Log"])]
                            for log_id in log_ids:
                                if(not log_id in self.bakery_inventory_expansion):
                                    self.bakery_inventory_expansion.append(log_id)
                                    if(self.message_level > 0):
                                        logger.info("%s added to Bakery",item_id_to_name[item_id])
                        elif(item_id == 0x502): #Aqualin
                            if(self.message_level > 0):
                                logger.info("Aqualin available during minigame")
                        elif(item_id == 0x503): #Manual
                            if(self.message_level > 0):
                                logger.info("Manual available during minigame")
                        else:
                            if(self.message_level > 0):
                                logger.info("unhandled item receieved %s",item_id_to_name[item_id])
                        self.received_count += 1
                if(self.checked_cores == False):
                    self.checked_cores = True
                    if(ctx.slot_data["core_sanity"] == True):
                        save_data: bytes = (await bizhawk.read(
                            ctx.bizhawk_ctx,
                            [(0x0ae659 + (self.jp_version * -0xea0), 1, MAIN_RAM)]
                        ))[0]
                        cores_collected: List[bool] = self.decode_booleans_with_exclusions(save_data[0], 6, [0,1])
                        need_to_update_cores = False
                        new_core_data: int = save_data[0]
                        for i in range(4):
                            if(cores_collected[i] == True):
                                if(not (item_name_to_id["Earth Boss Core"] + i in received_list)):
                                    new_core_data = new_core_data & (0b11111111 - (0b1 << (i+2)))
                                    need_to_update_cores = True
                        if(need_to_update_cores == True):
                            if(self.message_level > 0):
                                logger.info("Removing extra cores acquired") 
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x0ae659 + (self.jp_version * -0xea0), [new_core_data], MAIN_RAM)]
                            )
                if(self.max_hp_updated == False):
                    self.max_hp_updated = True
                    await self.update_max_hp(ctx, self.received_count)
                    bytes_to_update_progression: bytes = (await bizhawk.read(
                        ctx.bizhawk_ctx,
                        [(0x0ba247 + (self.jp_version * -0xea0), 2, MAIN_RAM)]
                    ))[0]
                    if(self.message_level == 3):
                        logger.info("bytes %s", bytes_to_update_progression)
                    vals_to_update_progression = int.from_bytes(bytes_to_update_progression,byteorder='little')
                    self.manually_checked_progression = set([val * (vals_to_update_progression & 1 << i == 1 << i) for i, val in enumerate(self.manually_checked_progression_states)])
                    self.manually_checked_progression.discard(0)
                    if(self.message_level == 3):
                        logger.info("resync progression %s", list(map(hex,sorted(self.manually_checked_progression))))
            if(self.xp_gain_updated == False):
                self.xp_gain_updated = True
                if(ctx.slot_data["xp_gain"] != 4):
                    if(ctx.slot_data["xp_gain"] != 1):
                        xp_factor: float = 1.0
                        if(ctx.slot_data["xp_gain"] == 2):
                            xp_factor = 0.25
                        elif(ctx.slot_data["xp_gain"] == 3):
                            xp_factor = 0.5
                        elif(ctx.slot_data["xp_gain"] == 5):
                            xp_factor = 2
                        elif(ctx.slot_data["xp_gain"] == 6):
                            xp_factor = 4
                        elif(ctx.slot_data["xp_gain"] == 7):
                            xp_factor = 10
                        elif(ctx.slot_data["xp_gain"] == 8):
                            xp_factor = 100
                        
                        xp_factor_mind: float = 1.0
                        if(ctx.slot_data["xp_gain_mind"] == 1):
                            xp_factor_mind = xp_factor
                        elif(ctx.slot_data["xp_gain_mind"] == 2):
                            xp_factor_mind = 0.5
                        elif(ctx.slot_data["xp_gain_mind"] == 4):
                            xp_factor_mind = 2
                        elif(ctx.slot_data["xp_gain_mind"] == 5):
                            xp_factor_mind = 4
                        elif(ctx.slot_data["xp_gain_mind"] == 6):
                            xp_factor_mind = 10
                        elif(ctx.slot_data["xp_gain_mind"] == 7):
                            xp_factor_mind = 100
                        write_instructions = []
                        for i in range(29):
                            write_instructions.append((0x0638f8 + (self.jp_version * -0xea4)+16*i, math.ceil(body_xp[i] / xp_factor).to_bytes(2, 'little'), MAIN_RAM))
                            write_instructions.append((0x0638fc + (self.jp_version * -0xea4)+16*i, math.ceil(mind_xp[i] / xp_factor_mind).to_bytes(2, 'little'), MAIN_RAM))
                            write_instructions.append((0x063900 + (self.jp_version * -0xea4)+16*i, math.ceil(lumina_xp[i] / xp_factor).to_bytes(2, 'little'), MAIN_RAM))
                            write_instructions.append((0x063904 + (self.jp_version * -0xea4)+16*i, math.ceil(fusion_xp[i] / xp_factor).to_bytes(2, 'little'), MAIN_RAM))
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            write_instructions
                        )
                    else:
                        write_instructions = [
                            (0x02aa98 + (self.jp_version * -0xdb0), [0, 0, 0x2, 0x24], MAIN_RAM), #limit lvl 8
                            (0x02aa90 + (self.jp_version * -0xdb0), [0], MAIN_RAM), #limit lvl 16
                            (0x02aa80 + (self.jp_version * -0xdb0), [0], MAIN_RAM), #limit lvl 22
                            (0x02aa70 + (self.jp_version * -0xdb0), [0], MAIN_RAM), #limit lvl 27
                            (0x02aa50 + (self.jp_version * -0xdb0), [0x4a, 0x6], MAIN_RAM), #limit lvl 30 (chapter 6 check)
                            (0x078ee4 + (self.jp_version * -0xdb0), [0] * 32, MAIN_RAM) #set lvl to 1 and xp to 0
                        ]
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            write_instructions
                        )
            if(self.hair_color_updated == 0):
                curr_hair_color: bytes = (await bizhawk.read(
                    ctx.bizhawk_ctx,
                    [(hair_color_addresses[0] + (self.jp_version * 0x1d10), 3, MAIN_RAM)]
                ))[0]
                if("message_level" in ctx.slot_data):
                    self.message_level = ctx.slot_data["message_level"]
                if(curr_hair_color == bytes.fromhex(ctx.slot_data["hair_color"])):
                    self.hair_color_updated = 1
                else:
                    logger.info(f"v{ctx.slot_data["version"]} Version of APWorld used to generate this slot")
                    logger.info(f"v{__version__} Currently installed APWorld version")
                    if(bytes.fromhex(default_hair_color) == curr_hair_color):
                        logger.info("This version of the game appears to be unpatched, attempting to patch")
                        if(self.jp_version == True):
                            curr_directory = str(Path(__file__).parent.parent) #directory of the apworld
                            write_instructions = []
                            archive = zipfile.ZipFile(curr_directory, 'r')
                            data = archive.read("bfm/patch/jp/fixBinchoIDc.bin")
                            write_instructions.append((0x06a2ec, data, MAIN_RAM))
                            data = archive.read("bfm/patch/jp/fixChestsc.bin")
                            write_instructions.append((0x062724, data, MAIN_RAM))
                            #data = archive.read("bfm/patch/jp/versionc.bin")
                            data = list(map(int,__version__.split(".")))
                            write_instructions.append((0x046f2c, data, MAIN_RAM))
                            data = archive.read("bfm/patch/jp/writeBinchoc.bin")
                            write_instructions.append((0x06cf9c, data, MAIN_RAM))
                            data = archive.read("bfm/patch/jp/updateProgressionc.bin")
                            write_instructions.append((0x073d90, data, MAIN_RAM))
                            data = archive.read("bfm/patch/jp/fixBinchoIDHooks.bin")
                            write_instructions.append((0x013a7c, data, MAIN_RAM))
                            data = archive.read("bfm/patch/jp/writeBinchoHooks.bin")
                            write_instructions.append((0x0283f0, data, MAIN_RAM))
                            data = archive.read("bfm/patch/jp/updateProgressionHooks.bin")
                            write_instructions.append((0x0d08cc, data, MAIN_RAM))
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                write_instructions
                            )
                        else:
                            curr_directory = str(Path(__file__).parent.parent) #directory of the apworld
                            write_instructions = []
                            archive = zipfile.ZipFile(curr_directory, 'r')
                            data = archive.read("bfm/patch/en/fixBinchoIDc.bin")
                            write_instructions.append((0x06b150, data, MAIN_RAM))
                            data = archive.read("bfm/patch/en/fixChestsc.bin")
                            write_instructions.append((0x063588, data, MAIN_RAM))
                            #data = archive.read("bfm/patch/en/versionc.bin")
                            data = list(map(int,__version__.split(".")))
                            write_instructions.append((0x047dc0, data, MAIN_RAM))
                            data = archive.read("bfm/patch/en/writeBinchoc.bin")
                            write_instructions.append((0x06de00, data, MAIN_RAM))
                            data = archive.read("bfm/patch/en/updateProgressionc.bin")
                            write_instructions.append((0x074bf0, data, MAIN_RAM))
                            data = archive.read("bfm/patch/en/fixBinchoIDHooks.bin")
                            write_instructions.append((0x0144e8, data, MAIN_RAM))
                            data = archive.read("bfm/patch/en/writeBinchoHooks.bin")
                            write_instructions.append((0x0291a0, data, MAIN_RAM))
                            data = archive.read("bfm/patch/en/updateProgressionHooks.bin")
                            write_instructions.append((0x0d17dc, data, MAIN_RAM))
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                write_instructions
                            )
                            #logger.info("This version of the game appears to be unpatched, this could result in unexpected behavior and maybe uncompletable. Please close and reopen this client after selecting the patched version of the game in bizhawk.")
                            #logger.info("For assistance in patching the game please view:")
                            #logger.info("https://github.com/AegeusEvander/Brave-Fencer-Musashi-AP-World/blob/main/docs/setup_en.md#patching-the-bin-file")
                            #logger.info("For further assistance please consider joining the Archipelago discord server (found on https://archipelago.gg/) going to future game design and then Brave Fencer Musashi")
                        logger.info("patching completed")
                    else:
                        save_data: bytes = (await bizhawk.read(
                            ctx.bizhawk_ctx,
                            [(0x047dc0 + (self.jp_version * -0xe94), 3, MAIN_RAM)]
                        ))[0]
                        s = str(save_data[0]) + "." + str(save_data[1]) + "." + str(save_data[2])
                        logger.info(f"v{s} Current game patch") 
                        logger.info("Try to have all version numbers match if possible for best compatibility")     
                    logger.info("Coloring Hair")
                    for address in hair_color_addresses:
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(address + (self.jp_version * 0x1d10), bytes.fromhex(ctx.slot_data["hair_color"]), MAIN_RAM)]
                        )
                    write_instructions = []
                    write_instructions.append((0x0d1490 + (self.jp_version * -0xe80), [0x0], MAIN_RAM))#set Minku healing to 0
                    for cost in appraisal_items_buy_cost:
                        write_instructions.append((cost + (self.jp_version * 0x1d10), [0xf6, 0xff], MAIN_RAM))
                    for cost in appraisal_l_armor_buy_cost:
                        write_instructions.append((cost + (self.jp_version * 0x1d10), [0xf5, 0xff], MAIN_RAM))
                    for cost in key_item_buy_cost:
                        write_instructions.append((cost + (self.jp_version * 0x1d10), [0x0a, 0x00], MAIN_RAM))
                    if(ctx.slot_data["quest_item_sanity"] == True):
                        for cost in quest_item_buy_cost:
                            write_instructions.append((cost + (self.jp_version * 0x1d10), [0x0a, 0x00], MAIN_RAM))
                    write_instructions.append((store_sanity_buy_cost[0] + (self.jp_version * 0x1d10), [0x1e, 0x00], MAIN_RAM))#bakery
                    write_instructions.append((store_sanity_buy_cost[1]  + (self.jp_version * 0x1d10), [0x64, 0x00], MAIN_RAM))#restaurant
                    write_instructions.append((store_sanity_buy_cost[2]  + (self.jp_version * 0x1d10), [0x32, 0x00], MAIN_RAM))#Grocery
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        write_instructions
                    )
                                
        
            if(curr_location != self.old_location):
                steps_bytes: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                    0x078E7C + (self.jp_version * -0xea0), 4, MAIN_RAM #replaced by timer (for steps0x078F08, 4, MAIN_RAM)
                )]))[0]
                step_count = int.from_bytes(steps_bytes,byteorder='little')
                if(self.level_transition == 0 or curr_location == 0x3005):
                    self.old_step_count = step_count
                    self.level_transition = 1
                elif(self.old_step_count != step_count):
                    self.old_location = curr_location
                    self.level_transition = 0
                    self.check_for_logs = 0
                    #if("Tracker" in ctx.tags):
                    if(True):
                        """self.completed_progression = calc_completed_progression_state(ctx, game_state)
                        logger.info("caclulating completed progression : %s", self.completed_progression)
                        connection_data = bfm_portals[curr_location]
                        #logger.info("len %s", len(connection_data.connections))
                        logger.info("connections %s", connection_data)
                        for connection in connection_data.connections:
                            #logger.info("con %s", connection)
                            calc_progression = calc_progression_state(ctx, connection.destination, self.progression_state, game_state, self.completed_progression, received_list)
                            logger.info("connection : %s : name : %s", hex(connection.destination), bfm_portals[connection.destination].region)
                            if(calc_progression == 0):
                                logger.info("no change to game state")
                                calc_progression = self.progression_state
                            logger.info("game state : %s : name : %s", hex(calc_progression), progression_state_table[calc_progression])"""
                        #{player}_{team}_bfm_area
                        #logger.info("tags : %s", ctx.tags)
                        #logger.info("auto tabbing to %x", curr_location)
                        await ctx.send_msgs([{
                            "cmd": "Set", 
                            "key": f"{ctx.slot}_{ctx.team}_bfm_area", 
                            "default": 0,
                            "want_reply": False,
                            "operations":
                                [{"operation": "replace", "value": curr_location}],
                        }])
                    if(curr_location in self.hint_dictionary and self.message_level > 1):
                        #logger.info("hint dict %s", self.hint_dictionary)
                        if(len(self.hint_dictionary[curr_location]) > 0 and self.hint_dictionary[curr_location] != self.last_displayed_hint):
                            logger.info(self.hint_dictionary[curr_location])
                            self.last_displayed_hint = self.hint_dictionary[curr_location]
                    if(curr_location in dialog_location_table): 
                        for loc_id, dialog_id in dialog_location_table[curr_location].items():
                            if(loc_id in ctx.locations_info or loc_id + jp_id_offset in ctx.locations_info):
                                if(loc_id in short_text_boxes):
                                    barray = await self.assemble_short_binary_array_for_textbox(ctx, loc_id + ((ctx.slot_data["set_lang"] == 2) * jp_id_offset))
                                else:
                                    barray = await self.assemble_binary_array_for_textbox(ctx, loc_id + ((ctx.slot_data["set_lang"] == 2) * jp_id_offset))
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(dialog_id[self.jp_version]+4, barray, MAIN_RAM)]
                                )
                            else:
                                logger.info("no scout information found try reentering area (after taking a couple steps)")
                                await ctx.send_msgs([{
                                    "cmd": "LocationScouts",
                                    "locations": self.table_ids_to_hint,
                                    "create_as_hint": 0
                                }])
                                break
                    if(ctx.slot_data["scroll_sanity"] == True):
                        #await bizhawk.write(
                        #    ctx.bizhawk_ctx,
                        #    [(0x13f430 + (self.jp_version * 0x344), [0x06, 0x01, 0x02, 0x24], MAIN_RAM)] #fix scroll cursor
                        #)    
                        save_data: bytes = (await bizhawk.read(
                            ctx.bizhawk_ctx,
                            [(0x0ae65b + (self.jp_version * -0xea0), 1, MAIN_RAM)]
                        ))[0]
                        if(save_data[0] & 0b10000000 == 0b00000000):
                            if(self.message_level > 0):
                                logger.info("Removing Rock on Twinpeak")
                            rock_data = save_data[0] | (0b10000000)
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x0ae65b + (self.jp_version * -0xea0), [rock_data], MAIN_RAM)]
                            )           
                        if(curr_location in scroll_dialog):
                            for loc_id, dialog_id in scroll_dialog[curr_location].items():
                                if(loc_id in ctx.locations_info or loc_id + jp_id_offset in ctx.locations_info):
                                    barray = await self.assemble_binary_array_for_textbox(ctx, loc_id + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                                    await bizhawk.write(
                                        ctx.bizhawk_ctx,
                                        [(dialog_id[self.jp_version]+4, barray, MAIN_RAM)]
                                    )
                                else:
                                    logger.info("no scout information found try reentering area (after taking a couple steps)")
                                    if(not standard_location_name_to_id["Earth Scroll - Twinpeak First Peak"] + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset) in self.table_ids_to_hint):
                                        for i in range(5):
                                            self.table_ids_to_hint.append(standard_location_name_to_id["Earth Scroll - Twinpeak First Peak"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                                    await ctx.send_msgs([{
                                        "cmd": "LocationScouts",
                                        "locations": self.table_ids_to_hint,
                                        "create_as_hint": 0
                                    }])
                                    break
                    if(curr_location in bakery_locations): # 0x2015chapter 2 Jam, also changes to 0x2056 chapter 3

                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x11514A + (self.jp_version * 0xa70), [0x0], MAIN_RAM)]
                        )
                        #if(curr_location == 0x207b or curr_location == 0x2098):
                        if(self.num_bosses_killed > 1):
                            if(not 0x68 in self.bakery_inventory_default):
                                self.bakery_inventory_default = self.bakery_inventory_default + [0x69,0x68]
                            if(len(self.bakery_inventory_sanity) < 7):
                                self.bakery_inventory_sanity = [0x3e,0x3e,0x3e,0x3e,0x3e,0x3e,0x3e]
                        self.bakery_inventory = [0x0d]
                        await self.remove_extra_legendary_armor_from_bakery(ctx)
                        #logger.info("bakery inventory %s",self.bakery_inventory)
                        #logger.info("bakery inventory bytes %s",bytes(self.bakery_inventory))
                        #logger.info("bakery inventory len %s",len(self.bakery_inventory))
                        #logger.info("bakery inventory len bytes %s",bytes(len(self.bakery_inventory)))
                        if(len(self.bakery_inventory_expansion)>1):
                            self.bakery_inventory_expansion.sort(reverse=True)
                        #await self.update_progression(ctx)
                        if(ctx.slot_data["bakery_sanity"] == True):
                            self.update_list_of_received_items(ctx)
                            self.bakery_dialog = []
                            self.cursor_pos = -1


                            for i in range(len(self.bakery_inventory_sanity)):
                                loc_id = standard_location_name_to_id["Item 1 - Bakery"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset)
                                if(loc_id in ctx.locations_info):
                                    if(self.bakery_checks[i]==True):
                                        if(self.jp_version == False):
                                            s = "Purchased"
                                        else:
                                            s = "かいもの"
                                    else:
                                        s = ctx.item_names.lookup_in_slot(ctx.locations_info[loc_id].item, ctx.locations_info[loc_id].player)
                                    self.bakery_dialog = self.bakery_dialog + [s]
                                    s = ctx.player_names[ctx.locations_info[loc_id].player]
                                    self.bakery_dialog = self.bakery_dialog + [s]
                                else:
                                    if(not standard_location_name_to_id["Item 1 - Bakery"] + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset) in self.table_ids_to_hint):
                                        for i in range(7):
                                            self.table_ids_to_hint.append(standard_location_name_to_id["Item 1 - Bakery"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                                    #logger.info("no scout information found try reentering area (after taking a couple steps) %s", self.table_ids_to_hint)
                                    #logger.info("item 7 id %s", standard_location_name_to_id["Item 7 - Bakery"])
                                    await ctx.send_msgs([{
                                        "cmd": "LocationScouts",
                                        "locations": self.table_ids_to_hint,
                                        "create_as_hint": 0
                                    }])
                                    break
                            self.fix_dialog(self.bakery_dialog)

                            #logger.info("bakery dialog %s", self.bakery_dialog)
                            self.bakery_inventory = self.bakery_inventory_sanity.copy()

                            for i in range(len(self.bakery_inventory)-1,-1,-1):
                                if(self.bakery_checks[i]==True):
                                    self.bakery_inventory.pop(i)
                                else:
                                    break

                            bread_to_add = []
                            if(item_name_to_id["Progressive Bread"] in self.list_of_received_items or (item_name_to_id["Progressive Bread"] + jp_id_offset) in self.list_of_received_items):
                                bread_to_add = self.bakery_inventory_default[:(self.list_of_received_items.count(item_name_to_id["Progressive Bread"]) + self.list_of_received_items.count(item_name_to_id["Progressive Bread"] + jp_id_offset))]
                            
                            if((curr_location == 0x2015 or curr_location == 0x2056) and ctx.slot_data["restaurant_sanity"] == True and self.progression_state > 0x63):
                                await self.fill_restaurant_dialog(ctx)
                                for i in range(len(self.bakery_inventory)):
                                    if(self.bakery_checks[i]==True and self.restaurant_checks[i]==False):
                                        self.bakery_inventory[i]=0x40
                                    elif(self.bakery_checks[i]==True):
                                        if(len(bread_to_add)>0):
                                            self.bakery_inventory[i]=bread_to_add.pop(0)
                                for i in range(6,len(self.bakery_inventory)-1,-1):
                                    if(self.restaurant_checks[i]==False):
                                        self.bakery_inventory = self.bakery_inventory + [0x40] * (i-len(self.bakery_inventory)+1)
                                        break
                            else:
                                for i in range(len(self.bakery_inventory)):
                                    if(self.bakery_checks[i]==True):
                                        if(len(bread_to_add)>0):
                                            #logger.info("bread to add %s", bread_to_add)
                                            #logger.info("bakery inventory %s", self.bakery_inventory)
                                            #logger.info("bakery inventory sanity %s", self.bakery_inventory_sanity)
                                            self.bakery_inventory[i]=bread_to_add.pop(0)
                                    
                            self.bakery_inventory = self.bakery_inventory + bread_to_add
                            self.bakery_inventory = self.bakery_inventory + self.bakery_inventory_expansion
                        elif((curr_location == 0x2015 or curr_location == 0x2056) and ctx.slot_data["restaurant_sanity"] == True and self.progression_state > 0x63):
                            self.bakery_inventory = []
                            self.cursor_pos = -1
                            await self.fill_restaurant_dialog(ctx)
                            for i in range(6,-1,-1):
                                if(self.restaurant_checks[i]==False):
                                    self.bakery_inventory = [0x40] * (i+1)
                                    break
                            bread_to_add = self.bakery_inventory_default.copy()
                            for i in range(len(self.bakery_inventory)):
                                if(self.bakery_checks[i]==True):
                                    if(len(bread_to_add)>0):
                                        self.bakery_inventory[i]=bread_to_add.pop(0)
                            self.bakery_inventory = self.bakery_inventory + bread_to_add + self.bakery_inventory_expansion
                        else:
                            self.bakery_inventory = self.bakery_inventory_default + self.bakery_inventory_expansion
                        self.bakery_inventory = self.bakery_inventory[:40]
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(store_table[curr_location][self.jp_version].inventory_id, self.bakery_inventory, MAIN_RAM)]
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(store_table[curr_location][self.jp_version].inventory_length_id, [len(self.bakery_inventory)], MAIN_RAM)]
                        )
                        if(store_table[curr_location][self.jp_version].inventory_length_id_expanded):
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(store_table[curr_location][self.jp_version].inventory_length_id_expanded, [len(self.bakery_inventory)], MAIN_RAM)]
                            )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(store_table[curr_location][self.jp_version].inventory_pointer_upper_pointer, store_table[curr_location][self.jp_version].inventory_pointer_upper, MAIN_RAM)] #somehow coresponds to 0x801f
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(store_table[curr_location][self.jp_version].inventory_pointer_lower_pointer, store_table[curr_location][self.jp_version].inventory_pointer_lower, MAIN_RAM)]
                        )
                    if(curr_location in restaurant_locations):
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x11514A + (self.jp_version * 0xa70), [0x0], MAIN_RAM)]
                        )
                        #logger.info("entered restaurant")
                        if(ctx.slot_data["restaurant_sanity"] == True):
                            if(False in self.restaurant_checks or not set(received_list).issuperset(set(self.restaurant_inventory_default))):
                                self.update_list_of_received_items(ctx)
                                self.restaurant_dialog = []
                                self.cursor_pos = -1

                                for i in range(7):
                                    loc_id = standard_location_name_to_id["Item 1 - Restaurant"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset)
                                    if(loc_id in ctx.locations_info):
                                        if(self.restaurant_checks[i]==True):
                                            if(self.jp_version == False):
                                                s = "Purchased"
                                            else:
                                                s = "かいもの"
                                        else:
                                            s = ctx.item_names.lookup_in_slot(ctx.locations_info[loc_id].item, ctx.locations_info[loc_id].player)
                                        self.restaurant_dialog = self.restaurant_dialog + [s]
                                        s = ctx.player_names[ctx.locations_info[loc_id].player]
                                        self.restaurant_dialog = self.restaurant_dialog + [s]
                                    else:
                                        if(not standard_location_name_to_id["Item 1 - Restaurant"] + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset) in self.table_ids_to_hint):
                                            for i in range(7):
                                                self.table_ids_to_hint.append(standard_location_name_to_id["Item 1 - Restaurant"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                                        await ctx.send_msgs([{
                                            "cmd": "LocationScouts",
                                            "locations": self.table_ids_to_hint,
                                            "create_as_hint": 0
                                        }])
                                        break
                                self.fix_dialog(self.restaurant_dialog)

                                #logger.info("bakery dialog %s", self.bakery_dialog)
                                self.restaurant_inventory = self.restaurant_inventory_sanity.copy()

                                for i in range(len(self.restaurant_inventory)-1,-1,-1):
                                    if(self.restaurant_checks[i]==True):
                                        self.restaurant_inventory.pop(i)
                                    else:
                                        break

                                restaurant_to_add = list(set(self.restaurant_inventory_default) & set(received_list))
                                for i in range(len(self.restaurant_inventory)):
                                    if(self.restaurant_checks[i]==True):
                                        if(len(restaurant_to_add)>0):
                                            self.restaurant_inventory[i]=restaurant_to_add.pop(0)
                                self.restaurant_inventory = self.restaurant_inventory + restaurant_to_add
                                self.restaurant_inventory = self.restaurant_inventory[:7]

                                restaurant_dialog_pointers = []
                                for i in range(len(self.restaurant_inventory)):
                                    restaurant_dialog_pointers = restaurant_dialog_pointers + restaurant_pointers[curr_location][self.jp_version][self.restaurant_inventory[i]]

                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(store_table[curr_location][self.jp_version].inventory_id, self.restaurant_inventory, MAIN_RAM)]
                                )
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(store_table[curr_location][self.jp_version].inventory_length_id, [len(self.restaurant_inventory)], MAIN_RAM)]
                                )
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(restaurant_pointers_pointers[curr_location][self.jp_version], restaurant_dialog_pointers, MAIN_RAM)]
                                )
                    if(curr_location in grocery_locations): # 0x2015chapter 2 Jam, also changes to 0x2056 chapter 3
                        if(ctx.slot_data["grocery_sanity"] == True):
                            #await self.update_progression(ctx)
                            self.update_list_of_received_items(ctx)
                            self.grocery_dialog = []
                            self.cursor_pos = -1
                            
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x11514A + (self.jp_version * 0xa70), [0x0], MAIN_RAM)] #set cursor to zero incase it is greater than the current index
                            )
                            if(len(self.grocery_inventory_sanity)<12 or 0 in self.grocery_inventory_sanity):
                                save_data: bytes = (await bizhawk.read(
                                    ctx.bizhawk_ctx,
                                    [(0x0BA202 + (self.jp_version * -0xea0), 1, MAIN_RAM)]
                                ))[0]
                                rice_ball = 0
                                rice_state = int.from_bytes(save_data, byteorder='little')
                                if(rice_state == 0x4):
                                    if(self.message_level > 0):
                                        logger.info("rice ball item available")
                                    rice_ball = 1
                                save_data: bytes = (await bizhawk.read(
                                    ctx.bizhawk_ctx,
                                    [(0x0BA213 + (self.jp_version * -0xea0), 1, MAIN_RAM)]
                                ))[0]
                                neatball = 0
                                neatball_state = int.from_bytes(save_data, byteorder='little')
                                if(neatball_state == 0x3):
                                    if(self.message_level > 0):
                                        logger.info("neatball item available")
                                    neatball = 1
                                if(neatball == 1 or rice_ball == 1):
                                    if(rice_ball == 1 and not 0x1 in self.grocery_inventory_default):
                                        self.grocery_inventory_default = self.grocery_inventory_default + [0x1]
                                    if(neatball == 1 and not 0x6a in self.grocery_inventory_default):
                                        self.grocery_inventory_default = self.grocery_inventory_default + [0x6a]
                                    if(len(self.grocery_inventory_sanity) < 11):
                                        if(neatball == 1 and rice_ball == 0):
                                            self.grocery_inventory_sanity = self.grocery_inventory_sanity + [0]*(11-len(self.grocery_inventory_sanity)) + [0x42]
                                        elif(neatball == 0 and rice_ball == 1):
                                            self.grocery_inventory_sanity = self.grocery_inventory_sanity + [0]*(10-len(self.grocery_inventory_sanity)) + [0x42] 
                                        else:
                                            self.grocery_inventory_sanity = self.grocery_inventory_sanity + [0]*(10-len(self.grocery_inventory_sanity)) + [0x42, 0x42]
                                    elif(len(self.grocery_inventory_sanity) == 11 and neatball == 1): 
                                        self.grocery_inventory_sanity = self.grocery_inventory_sanity + [0x42]
                                    elif(rice_ball == 1):
                                        self.grocery_inventory_sanity[10] = 0x42

                            if(not 0xb in self.grocery_inventory_default):
                                #if(self.progression_state >= 0x12c):
                                if(game_state[17][14] & 0b1000 == 0b1000): #tim is saved, add orange to inventory
                                    if(len(self.grocery_inventory_sanity) < 11): #no Riceball or Neatball yet
                                        self.grocery_inventory_sanity = self.grocery_inventory_sanity + [0x42]
                                        self.grocery_inventory_default = self.grocery_inventory_default + [0xb]
                                    else: #have either Riceball or Neatball
                                        self.grocery_inventory_sanity[7] = 0x42
                                        self.grocery_inventory_default = self.grocery_inventory_default[:7] + [0xb] + self.grocery_inventory_default[7:]

                            #if(curr_location == 0x207c or curr_location == 0x2099): #Chapter 4/5/6
                            if(self.num_bosses_killed > 1): #Chapter 4/5/6
                                if(not 0x7 in self.grocery_inventory_default):
                                    self.grocery_inventory_default = self.grocery_inventory_default[:3] + [0x7] + self.grocery_inventory_default[3:5] + [0x6d] + self.grocery_inventory_default[5:] #EX-Drink and H-Mint
                                    if(len(self.grocery_inventory_sanity) < 11): #no Riceball or Neatball yet
                                        self.grocery_inventory_sanity = self.grocery_inventory_sanity + [0x42,0x42]
                                    else:
                                        self.grocery_inventory_sanity[8] = 0x42
                                        self.grocery_inventory_sanity[9] = 0x42
                                    
                            self.grocery_inventory = [0x0a]
                            #logger.info("bakery inventory %s",self.bakery_inventory)
                            #logger.info("bakery inventory bytes %s",bytes(self.bakery_inventory))
                            #logger.info("bakery inventory len %s",len(self.bakery_inventory))
                            #logger.info("bakery inventory len bytes %s",bytes(len(self.bakery_inventory)))


                            for i in range(len(self.grocery_inventory_sanity)):
                                loc_id = standard_location_name_to_id["Item 1 - Grocery"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset)
                                if(loc_id in ctx.locations_info):
                                    if(self.grocery_checks[i]==True):
                                        if(self.jp_version == False):
                                            s = "Purchased"
                                        else:
                                            s = "かいもの"
                                    else:
                                        s = ctx.item_names.lookup_in_slot(ctx.locations_info[loc_id].item, ctx.locations_info[loc_id].player)
                                    self.grocery_dialog = self.grocery_dialog + [s]
                                    s = ctx.player_names[ctx.locations_info[loc_id].player]
                                    self.grocery_dialog = self.grocery_dialog + [s]
                                else:
                                    if(not standard_location_name_to_id["Item 1 - Grocery"] + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset) in self.table_ids_to_hint):
                                        for i in range(12):
                                            self.table_ids_to_hint.append(standard_location_name_to_id["Item 1 - Grocery"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                                    #logger.info("no scout information found try reentering area (after taking a couple steps) %s", self.table_ids_to_hint)
                                    #logger.info("item 7 id %s", standard_location_name_to_id["Item 7 - Bakery"])
                                    await ctx.send_msgs([{
                                        "cmd": "LocationScouts",
                                        "locations": self.table_ids_to_hint,
                                        "create_as_hint": 0
                                    }])
                                    break
                            self.fix_dialog(self.grocery_dialog)

                            #logger.info("bakery dialog %s", self.bakery_dialog)
                            self.grocery_inventory = self.grocery_inventory_sanity.copy()

                            for i in range(len(self.grocery_inventory)-1,-1,-1):
                                if(self.grocery_checks[i]==True or self.grocery_inventory[i]==0x0):
                                    self.grocery_inventory.pop(i)
                                else:
                                    break

                            #logger.info("starting inventory %s", self.grocery_inventory)
                            #logger.info("grocery default %s", self.grocery_inventory_default)
                            #grocery_to_add = list(set(self.grocery_inventory_default) & set(received_list))
                            grocery_to_add = []
                            for i in range(len(self.grocery_inventory_default)):
                                if(self.grocery_inventory_default[i] in received_list or (ctx.slot_data["grocery_s_revive"] == True and self.grocery_inventory_default[i] == 0xa)):
                                    grocery_to_add = grocery_to_add + [self.grocery_inventory_default[i]]
                                    #logger.info("grocery to add %s", grocery_to_add)
                            if(received_list.count(0x6) > 1 and 0x7 in self.grocery_inventory_default):
                                grocery_to_add = [0x7 if x==0x6 else x for x in grocery_to_add]
                            if(received_list.count(0x8) > 1 and 0x6d in self.grocery_inventory_default):
                                grocery_to_add = [0x6d if x==0x8 else x for x in grocery_to_add]
                            #logger.info("grocery to add %s", grocery_to_add)

                            if(len(self.grocery_inventory) >= 4 and 0xa in grocery_to_add):
                                if(self.grocery_checks[3]==True):
                                    self.grocery_inventory[3] = 0xa
                                    grocery_to_add.remove(0xa)
                            
                            for i in range(len(self.grocery_inventory)):
                                if(self.grocery_checks[i]==True or self.grocery_inventory[i]==0x0):
                                    if(self.grocery_inventory[i] != 0xa):
                                        if(len(grocery_to_add)>0):
                                            #logger.info("bread to add %s", bread_to_add)
                                            #logger.info("bakery inventory %s", self.bakery_inventory)
                                            #logger.info("bakery inventory sanity %s", self.bakery_inventory_sanity)
                                            self.grocery_inventory[i]=grocery_to_add.pop(0)
                            #logger.info("inventory after after grocery to add %s", self.grocery_inventory)
                                    
                            self.grocery_inventory = self.grocery_inventory + grocery_to_add

                            if(len(self.grocery_inventory) >= 4 and 0xa in self.grocery_inventory):
                                if(self.grocery_checks[3]==True):
                                    if(self.grocery_inventory[3] != 0xa):
                                        for i in range(len(self.grocery_inventory)):
                                            if(self.grocery_inventory[i] == 0xa):
                                                self.grocery_inventory[i] = self.grocery_inventory[3]
                                        self.grocery_inventory[3] = 0xa
                            #logger.info("inventory after after final adds grocery to add %s", self.grocery_inventory)
                        
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(store_table[curr_location][self.jp_version].inventory_id, self.grocery_inventory, MAIN_RAM)]
                            )
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(store_table[curr_location][self.jp_version].inventory_length_id, [len(self.grocery_inventory)]*8, MAIN_RAM)]
                            )
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(store_table[curr_location][self.jp_version].inventory_pointer_upper_pointer, store_table[curr_location][self.jp_version].inventory_pointer_upper, MAIN_RAM)] #somehow coresponds to 0x801f
                            )
                    
                    if(curr_location in toy_shop_locations): # 0x2015chapter 2 Jam, also changes to 0x2056 chapter 3
                        if(ctx.slot_data["toy_sanity"] == True):
                            
                            if(len(self.toy_dialog[29]) == 0):
                                for i in range(len(self.toy_checks)):
                                    loc_id = standard_location_name_to_id["Musashi - Toy Shop"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset)
                                    if(loc_id in ctx.locations_info):
                                        self.toy_dialog[i] = await self.assemble_binary_array_for_toyshop(ctx,loc_id,toy_shop_dialog_length[self.jp_version][i])
                                    else:
                                        if(not standard_location_name_to_id["Musashi - Toy Shop"] + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset) in self.table_ids_to_hint):
                                            for i in range(30):
                                                self.table_ids_to_hint.append(standard_location_name_to_id["Musashi - Toy Shop"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                                        logger.info("no scout information found try reentering area (after taking a couple steps)")
                                        #logger.info("item 7 id %s", standard_location_name_to_id["Item 7 - Bakery"])
                                        await ctx.send_msgs([{
                                            "cmd": "LocationScouts",
                                            "locations": self.table_ids_to_hint,
                                            "create_as_hint": 0
                                        }])
                                        break
                            
                            if(len(self.toy_dialog[29]) != 0):
                                if(self.message_level > 0):
                                    logger.info("writing toy dialog")
                                for i in range(len(self.toy_inventory)):
                                    if(self.toy_inventory[i]):
                                        await bizhawk.write(
                                            ctx.bizhawk_ctx,
                                            [(toy_shop_dialog[curr_location][self.jp_version][i], self.toy_dialog[i], MAIN_RAM)]
                                        )
                            
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(toy_shop_fix[curr_location][self.jp_version], [0x10], MAIN_RAM)]
                            )

                            save_data: bytes = (await bizhawk.read(
                                ctx.bizhawk_ctx,
                                [(0x0ba239 + (self.jp_version * -0xea0), 13, MAIN_RAM)]
                            ))[0]
                            new_toy_purchased_to_update: List[bool] = [val & 0b11110000 == 0b10010000 for val in save_data]
                            if(True in new_toy_purchased_to_update):
                                for i in range(len(new_toy_purchased_to_update)):
                                    if(new_toy_purchased_to_update[i]):
                                        if(self.message_level > 0):
                                            logger.info("adding yet to be randomized toy to storage")
                                        save_data: bytes = (await bizhawk.read(
                                            ctx.bizhawk_ctx,
                                            [(0x0ba239+i + (self.jp_version * -0xea0), 1, MAIN_RAM)]
                                        ))[0]
                                        toy_data = save_data[0] | 0b1000000
                                        toy_data = toy_data & 0b11101111
                                        await bizhawk.write(
                                            ctx.bizhawk_ctx,
                                            [(0x0ba239+i + (self.jp_version * -0xea0), [toy_data], MAIN_RAM)]
                                        )
                    if(curr_location == 0x3003): #At Geezer
                        if(ctx.slot_data["tech_sanity"] == True):
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                tech_fix[self.jp_version]
                            )
                            if(len(self.tech_dialog[6]) == 0):
                                for i in range(len(self.tech_checks)):
                                    loc_id = standard_location_name_to_id["Improved Fusion (Artisan) - Allucaneet Castle"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset)
                                    if(loc_id in ctx.locations_info):
                                        self.tech_dialog[i] = await self.assemble_binary_array_for_textbox(ctx,loc_id)
                                    else:
                                        if(not standard_location_name_to_id["Improved Fusion (Artisan) - Allucaneet Castle"] + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset) in self.table_ids_to_hint):
                                            for i in range(7):
                                                self.table_ids_to_hint.append(standard_location_name_to_id["Improved Fusion (Artisan) - Allucaneet Castle"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                                        logger.info("no scout information found try reentering area (after taking a couple steps)")
                                        #logger.info("item 7 id %s", standard_location_name_to_id["Item 7 - Bakery"])
                                        await ctx.send_msgs([{
                                            "cmd": "LocationScouts",
                                            "locations": self.table_ids_to_hint,
                                            "create_as_hint": 0
                                        }])
                                        break
                            
                            if(len(self.tech_dialog[6]) != 0):
                                if(self.message_level > 0):
                                    logger.info("writing tech dialog")
                                for i in range(len(self.tech_dialog)):
                                    if(self.tech_checks[i] == False):
                                        await bizhawk.write(
                                            ctx.bizhawk_ctx,
                                            [(castle_dialog[self.jp_version][i], self.tech_dialog[i], MAIN_RAM)]
                                        )
                        if(ctx.slot_data["skip_minigame_town_on_fire"] == True):
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x17f0e8 + (self.jp_version * 0x200), [0xb2], MAIN_RAM)]
                            )
                        if(self.progression_state == 0x28a): #Ask geezer about gondola gizmo and his state is too high
                            if(item_name_to_id["CarpentA"] in received_list and item_name_to_id["CarpentB"] in received_list and item_name_to_id["CarpentC"] in received_list):
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x0ba1f3 + (self.jp_version * -0xea0), [0x7], MAIN_RAM)]
                                )
                            elif(int.from_bytes(game_state[27], byteorder='little') > 7):
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x0ba1f3 + (self.jp_version * -0xea0), [0x1], MAIN_RAM)]
                                )
                        if(int.from_bytes(game_state[8], "little") in [1, 2]): #KnightB state
                            if(game_state[4][11] & 0b10000000 == 0b10000000): #skullpion killed
                                if(self.message_level > 0):
                                    logger.info("skullpion killed, can get crosswise cut")
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x18090c + (self.jp_version * 0x200), [0xa, 0x0], MAIN_RAM)]
                                )
                            else:
                                if(self.message_level > 0):
                                    logger.info("skullpion not killed, can't get crosswise cut")
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x18090c + (self.jp_version * 0x200), [0x40, 0x6], MAIN_RAM)]
                                )
                    if(curr_location == 0x1011): #chapter 2 upper town
                        if(self.progression_state == 0x14):
                            self.try_to_update_connections = True

                    if(curr_location in boss_core_dialog): #At a Boss
                        if(ctx.slot_data["core_sanity"] == False and curr_location == 0x3042 and ctx.slot_data["quest_item_sanity"] == True and not item_name_to_id["Key"] in received_list):
                            for jump_id in boss_core_update[curr_location][self.jp_version]:
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(jump_id, [0,0,0,0], MAIN_RAM)]
                                )
                            if(self.message_level > 0):    
                                logger.info("temporarily hiding water boss core until Key to mine is found to prevent soft locks")

                        if(ctx.slot_data["core_sanity"] == True):
                            for jump_id in boss_core_update[curr_location][self.jp_version]:
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(jump_id, [0,0,0,0], MAIN_RAM)]
                                )
                            for loc_id, dialog_id in boss_core_dialog[curr_location].items():
                                if(loc_id in ctx.locations_info or loc_id + jp_id_offset in ctx.locations_info):
                                #for i in range(len(self.core_checks)):
                                    #loc_id = standard_location_name_to_id["Defeat Earth Crest Guardian - Skullpion Arena"] + i
                                    #if(loc_id in ctx.locations_info):
                                        #logger.info("loop index %s", i)
                                        #logger.info("textbox length %s", boss_core_dialog[[boss_locations[i]][1])
                                        #logger.info("location id %s", loc_id)


                                    barray = await self.assemble_binary_array_for_boss_textbox(ctx,loc_id + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset),dialog_id[self.jp_version][1])
                                    if(self.message_level > 0):
                                        logger.info("writing boss core dialog")
                                    await bizhawk.write(
                                        ctx.bizhawk_ctx,
                                        [(dialog_id[self.jp_version][0]+4, barray, MAIN_RAM)]
                                    )
                                else:
                                    if(not standard_location_name_to_id["Defeat Earth Crest Guardian - Skullpion Arena"] + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset) in self.table_ids_to_hint):
                                        for i in range(4):
                                            self.table_ids_to_hint.append(standard_location_name_to_id["Defeat Earth Crest Guardian - Skullpion Arena"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                                    logger.info("no scout information found")
                                    #logger.info("item 7 id %s", standard_location_name_to_id["Item 7 - Bakery"])
                                    await ctx.send_msgs([{
                                        "cmd": "LocationScouts",
                                        "locations": self.table_ids_to_hint,
                                        "create_as_hint": 0
                                    }])
                                    break
                    if(curr_location == 0x3072):
                        if(ctx.slot_data["skip_minigame_ant_gondola"] == True):
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x18446c + (self.jp_version * 0x138), [0x74], MAIN_RAM)]
                            )
                    if(curr_location == 0x304e): #in well
                        #await self.update_progression(ctx)
                        if(ctx.slot_data["core_sanity"] == True or ctx.slot_data["scroll_sanity"] == True or ctx.slot_data["quest_item_sanity"] == True):
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x182e1c + (self.jp_version * 0x200), [0,0,0,0], MAIN_RAM)] #skip over water scroll updating progression state
                            )
                            if(self.progression_state < 0x19a): #before entering church
                                if(self.message_level > 0):
                                    logger.info("Hiding bell to prevent soft lock, return after Father White makes a request for the bell and learning how to enter the restaurant basement")
                                save_data: bytes = (await bizhawk.read(
                                    ctx.bizhawk_ctx,
                                    [(0x1207e6 + (self.jp_version * 0xa70), 2, MAIN_RAM)]
                                ))[0]
                                bell_z = int.from_bytes(save_data, byteorder='little')
                                if(bell_z == 0xfe6e):
                                    await bizhawk.write(
                                        ctx.bizhawk_ctx,
                                        [(0x1207e6 + (self.jp_version * 0xa70), [0xff,0xfe], MAIN_RAM)] #hide the bell in a wall
                                    )
                                else:
                                    save_data: bytes = (await bizhawk.read(
                                        ctx.bizhawk_ctx,
                                        [(0x1209fe + (self.jp_version * 0xa70), 2, MAIN_RAM)]
                                    ))[0]
                                    bell_z = int.from_bytes(save_data, byteorder='little')
                                    if(bell_z == 0xfe6e):
                                        await bizhawk.write(
                                            ctx.bizhawk_ctx,
                                            [(0x1209fe + (self.jp_version * 0xa70), [0xff,0xfe], MAIN_RAM)] #hide the bell in a wall
                                        )
                                    else:
                                        logger.info("Could not find bell in memory")

                            else:
                                save_data: bytes = (await bizhawk.read(
                                    ctx.bizhawk_ctx,
                                    [(0x0ba1c2 + (self.jp_version * -0xea0), 1, MAIN_RAM)]
                                ))[0]
                                bell_state: bool = save_data[0] == 0b1001110 #is in intial spawn position
                                if(bell_state):
                                    save_data: bytes = (await bizhawk.read(
                                        ctx.bizhawk_ctx,
                                        [(0x0ae65f + (self.jp_version * -0xea0), 1, MAIN_RAM)]
                                    ))[0]
                                    water_level_changed: bool = save_data[0] & 0b1 == 0b1
                                    if(water_level_changed):
                                        if(self.message_level > 0):
                                            logger.info("water level has risen, moving bell to prevent soft lock")

                                        save_data: bytes = (await bizhawk.read(
                                            ctx.bizhawk_ctx,
                                            [(0x1207e6 + (self.jp_version * 0xa70), 2, MAIN_RAM)]
                                        ))[0]
                                        bell_z = int.from_bytes(save_data, byteorder='little')
                                        if(bell_z == 0xfe6e):
                                            await bizhawk.write(
                                                ctx.bizhawk_ctx,
                                                [(0x1207e2 + (self.jp_version * 0xa70), [0x27,0x06, 0x0, 0x0, 0x7e, 0xfd, 0x0, 0x0, 0x80, 0xff], MAIN_RAM)] #water level has risen but bell has not been rescued, move bell to higher ground
                                            )
                                        else:
                                            save_data: bytes = (await bizhawk.read(
                                                ctx.bizhawk_ctx,
                                                [(0x1209fe + (self.jp_version * 0xa70), 2, MAIN_RAM)]
                                            ))[0]
                                            bell_z = int.from_bytes(save_data, byteorder='little')
                                            if(bell_z == 0xfe6e):
                                                await bizhawk.write(
                                                    ctx.bizhawk_ctx,
                                                    [(0x1209fa + (self.jp_version * 0xa70), [0x27,0x06, 0x0, 0x0, 0x7e, 0xfd, 0x0, 0x0, 0x80, 0xff], MAIN_RAM)] #water level has risen but bell has not been rescued, move bell to higher ground
                                                )
                                            else:
                                                logger.info("Could not find bell in memory")
                            
                        if(ctx.slot_data["core_sanity"] == True):
                            if(self.progression_state < 0x258 or self.progression_state > 0x276): #before killing Relic Keeper or after fixing well
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x1845f4 + (self.jp_version * 0x200), [0,0,0,0], MAIN_RAM)] #skip over water crest updating progression state
                                )
                    if(curr_location == 0x1052 or curr_location == 0x1077): #in chapter 3 and 4 town
                        if(ctx.slot_data["core_sanity"] == True):
                            save_data: bytes = (await bizhawk.read(
                                ctx.bizhawk_ctx,
                                [(0x0ae65f + (self.jp_version * -0xea0), 1, MAIN_RAM)]
                            ))[0]
                            water_level_changed: bool = save_data[0] & 0b1 == 0b1
                            if(water_level_changed):
                                #await self.update_progression(ctx)
                                if(self.progression_state >= 0x19a and self.progression_state < 0x1ae): #getting rope reward
                                    if(self.message_level > 0):
                                        logger.info("removing rope to prevent soft lock")
                                    await bizhawk.write(
                                        ctx.bizhawk_ctx,
                                        [(0x18f7b0 + (self.jp_version * 0x1f0), [0], MAIN_RAM)] #removing rope as a reward
                                    )
                                save_data: bytes = (await bizhawk.read(
                                    ctx.bizhawk_ctx,
                                    [(0x0ae668 + (self.jp_version * -0xea0), 1, MAIN_RAM)]
                                ))[0]
                                rope_into_well: bool = save_data[0] & 0b1000000 == 0b1000000
                                if(rope_into_well):
                                    if(self.message_level > 0):
                                        logger.info("removing rope to prevent soft lock")
                                    remove_rope = save_data[0] & 0b10111111
                                    await bizhawk.write(
                                        ctx.bizhawk_ctx,
                                        [(0x0ae668 + (self.jp_version * -0xea0), [remove_rope], MAIN_RAM)] #water level has risen remove rope from well
                                    )
                                if(self.progression_state == 0x258): #defeated relic keeper
                                    await bizhawk.write(
                                        ctx.bizhawk_ctx,
                                        [(0x078e80 + (self.jp_version * -0xea0), [0x76], MAIN_RAM)] #well was fixed move progression state
                                    )
                    if(curr_location == 0x3023): #at volcano near wind scroll
                        if(ctx.slot_data["core_sanity"] == True):
                            #await self.update_progression(ctx)
                            if(self.progression_state < 0x3d4): #before steamwood 2
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x182d38 + (self.jp_version * 0x200), [0,0,0,0], MAIN_RAM)] #dont update progression for wind scroll
                                )
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x18386c + (self.jp_version * 0x200), [0,0,0,0], MAIN_RAM)] #dont update progression for freed from bincho
                                )
                    #if(curr_location == 0x1094): #Chapter 5 town
                    #    if(ctx.slot_data["core_sanity"] == True):
                    #        #await self.update_progression(ctx)
                    #        if(self.progression_state > 0x3d4 and self.progression_state < 0x460): #after steamwood 2
                    #            if(self.found_wind_scroll): #already went to wind scroll
                    #                await bizhawk.write(
                    #                    ctx.bizhawk_ctx,
                    #                    [(0x078e80 + (self.jp_version * -0xea0), [0x60, 0x04], MAIN_RAM)] #update progression to freed from bincho
                    #                )
                    if(curr_location == 0x301b): #entering Meandering Forest
                        save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                            0x0ba284 + (self.jp_version * -0xea0), 1, MAIN_RAM
                        )]))[0]
                        leno_state = int.from_bytes(save_data, byteorder='little')
                        if(leno_state > 0 and leno_state < 0xf and ctx.slot_data["leno_sniff_modifier"] != 100):
                            snif_multiplier: float = 100.0
                            snif_multiplier = ctx.slot_data["leno_sniff_modifier"] / snif_multiplier 
                            write_instructions = []
                            write_instructions.append((0x181434 + (self.jp_version * 0x188), math.ceil(0xb4 * snif_multiplier).to_bytes(2, 'little'), MAIN_RAM))
                            write_instructions.append((0x180d40 + (self.jp_version * 0x188), math.ceil(0xb4 * snif_multiplier).to_bytes(2, 'little'), MAIN_RAM))
                            write_instructions.append((0x180d4c + (self.jp_version * 0x188), math.ceil(0xd2 * snif_multiplier).to_bytes(2, 'little'), MAIN_RAM))
                            write_instructions.append((0x181488 + (self.jp_version * 0x188), math.ceil(0xd2 * snif_multiplier).to_bytes(2, 'little'), MAIN_RAM))
                            write_instructions.append((0x180d68 + (self.jp_version * 0x188), math.ceil(0xf0 * snif_multiplier).to_bytes(2, 'little'), MAIN_RAM))
                            write_instructions.append((0x1814a0 + (self.jp_version * 0x188), math.ceil(0xf0 * snif_multiplier).to_bytes(2, 'little'), MAIN_RAM))
                            write_instructions.append((0x180d74 + (self.jp_version * 0x188), math.ceil(0x10e * snif_multiplier).to_bytes(2, 'little'), MAIN_RAM))
                            write_instructions.append((0x1814ac + (self.jp_version * 0x188), math.ceil(0x10e * snif_multiplier).to_bytes(2, 'little'), MAIN_RAM))
                            write_instructions.append((0x180d90 + (self.jp_version * 0x188), math.ceil(0x12c * snif_multiplier).to_bytes(2, 'little'), MAIN_RAM))
                            write_instructions.append((0x1814c4 + (self.jp_version * 0x188), math.ceil(0x12c * snif_multiplier).to_bytes(2, 'little'), MAIN_RAM))
                            write_instructions.append((0x180d9c + (self.jp_version * 0x188), math.ceil(0x14a * snif_multiplier).to_bytes(2, 'little'), MAIN_RAM))
                            write_instructions.append((0x1814d0 + (self.jp_version * 0x188), math.ceil(0x14a * snif_multiplier).to_bytes(2, 'little'), MAIN_RAM))
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                write_instructions
                            )
                    if(curr_location == 0x3014): #entering Somnolent Forest
                        if(ctx.slot_data["skip_minigame_follow_leno"] == True):
                            save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                0x0ba284 + (self.jp_version * -0xea0), 1, MAIN_RAM
                            )]))[0]
                            leno_state = int.from_bytes(save_data, byteorder='little')
                            if(leno_state > 0 and leno_state < 0x3):
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x0ba284 + (self.jp_version * -0xea0), [0x0e], MAIN_RAM), (0x190614 + (self.jp_version * 0x5c), [0x22, 0x30, 0x00, 0x04], MAIN_RAM)] #graveyard 0x04003022
                                )
                    if(curr_location == 0x302a): #rafting minigame
                        if(ctx.slot_data["raft_difficulty"] == 2):
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x17ece0 + (self.jp_version * -0xea0), [0x0, 0x0], MAIN_RAM)] #remove damage calculation for rafting #, [0x200]????
                            )
                    if(curr_location == 0x1010 or curr_location == 0x1011 or curr_location == 0x301c or curr_location == 0x301d or curr_location == 0x301e or curr_location == 0x3020):
                        if(ctx.slot_data["steamwood_timer"] != 100):
                            #await self.update_progression(ctx)
                            if((self.progression_state < 0x0082 and self.progression_state >= 0x0078) or (self.progression_state < 0x03d4 and self.progression_state >= 0x03ca)):
                                time_modifier = math.ceil(ctx.slot_data["steamwood_timer"] * 0x1555 / 100.0)
                                if(ctx.slot_data["steamwood_timer"] == 1):
                                    time_modifier = 0x25
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x14ae6c + (self.jp_version * 0x2d0), time_modifier.to_bytes(2, 'little'), MAIN_RAM)] #fix steamwood timer
                                )
                        gizmos_in_inventory = sum([val in [0x63, 0x64, 0x65, 0x66] for val in game_state[19]])
                        if(gizmos_in_inventory > 1): #gondola gizmos in inventory
                            #logger.info("gizmos in inventory %s", gizmos_in_inventory)
                            new_inventory: List[int] = [val for val in game_state[19]] 
                            for i in range(11,-1,-1):
                                if(new_inventory[i] in [0x63, 0x64, 0x65, 0x66] and gizmos_in_inventory > 1):
                                    new_inventory[i] = 0
                                    gizmos_in_inventory = gizmos_in_inventory - 1

                            #new_inventory: List[int] = [val for val in save_data[19]] 
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x0ba1e7 + (self.jp_version * -0xea0), new_inventory, MAIN_RAM)]
                            )
                            if(self.message_level > 0):
                                logger.info("removing extra gondola gizmos from inventory (They are very heavy)")

                    if(curr_location == 0x301d or curr_location == 0x3020): #steamwood
                        write_instructions = []
                        if(ctx.slot_data["steamwood_random_valves"] == True):
                            if(curr_location == 0x301d):#steamwood 1
                                write_instructions.append((0x183cf8 + (self.jp_version * 0x1c0), [0x99, 0xb] * 7, MAIN_RAM)) #fix steamwood 1 valve timer
                            else:
                                write_instructions.append((0x184ed0 + (self.jp_version * 0x1c0), [0x99, 0xb] * 7, MAIN_RAM)) #fix steamwood 2 valve timer
                        elif(ctx.slot_data["steamwood_valve_timer"] != 100):
                            valve_long_timer = math.ceil(0x708 * ctx.slot_data["steamwood_valve_timer"] / 100.0).to_bytes(2, 'little')
                            valve_short_timer = math.ceil(0x41a * ctx.slot_data["steamwood_valve_timer"] / 100.0).to_bytes(2, 'little')
                            valve_timers = [valve_long_timer[0], valve_long_timer[1]] * 3 + [valve_short_timer[0], valve_short_timer[1]] * 2 + [valve_long_timer[0], valve_long_timer[1]] + [valve_short_timer[0], valve_short_timer[1]]
                            if(curr_location == 0x301d):#steamwood 1
                                write_instructions.append((0x183cf8 + (self.jp_version * 0x1c0), valve_timers, MAIN_RAM)) #fix steamwood 1 valve timer
                            else:
                                write_instructions.append((0x184ed0 + (self.jp_version * 0x1c0), valve_timers, MAIN_RAM)) #fix steamwood 2 valve timer
                        if(ctx.slot_data["steamwood_disable_countdown"] == True):
                            if(curr_location == 0x301d):#steamwood 1
                                write_instructions.append((0x17ed0c + (self.jp_version * 0x200), [0x0, 0x0], MAIN_RAM)) #remove valve countdown
                            else:
                                write_instructions.append((0x17f4d8 + (self.jp_version * 0x200), [0x0, 0x0], MAIN_RAM)) #remove valve countdown
                        if(ctx.slot_data["steamwood_pressure_rise_rate"] == 2): #Faster
                            if(curr_location == 0x301d):
                                write_instructions.append((0x183a28 + (self.jp_version * 0x1c8), [0x4] * 4, MAIN_RAM)) #steamwood 1 pressure rise
                            else:
                                write_instructions.append((0x184a60 + (self.jp_version * 0x1c8), [0x4] * 4, MAIN_RAM)) #steamwood 2 pressure rise
                        elif(ctx.slot_data["steamwood_pressure_rise_rate"] == 3): #Slower
                            if(curr_location == 0x301d):
                                write_instructions.append((0x183a2c + (self.jp_version * 0x1c8), [0x3, 0x3, 0x4, 0x5], MAIN_RAM)) #steamwood 1 pressure rise
                            else:
                                write_instructions.append((0x184a64 + (self.jp_version * 0x1c8), [0x3, 0x3, 0x4, 0x5], MAIN_RAM)) #steamwood 2 pressure rise
                        elif(ctx.slot_data["steamwood_pressure_rise_rate"] == 4): #Even 
                            if(curr_location == 0x301d):
                                write_instructions.append((0x183a28 + (self.jp_version * 0x1c8), [0x3] * 8, MAIN_RAM)) #steamwood 1 pressure rise
                            else:
                                write_instructions.append((0x184a60 + (self.jp_version * 0x1c8), [0x3] * 8, MAIN_RAM)) #steamwood 2 pressure rise
                        if(ctx.slot_data["steamwood_progress_lost"] != -16):
                            write_instructions.append((0x17c598 + (self.jp_version * 0x200), ctx.slot_data["steamwood_progress_lost"].to_bytes(2, 'little', signed=True), MAIN_RAM))
                        top_edge = 17
                        bottom_edge = 68
                        if(ctx.slot_data["steamwood_width_of_ok_pressure"] != 12):
                            #mid_point = 74
                            half_width = round(ctx.slot_data["steamwood_width_of_ok_pressure"] / 2)
                            if(half_width > 16):
                                top_edge = 0
                            else:
                                top_edge = top_edge - half_width
                            bottom_edge = 96 - top_edge - ctx.slot_data["steamwood_width_of_ok_pressure"]
                            write_instructions.append((0x17c540 + (self.jp_version * 0x200), (bottom_edge * -1).to_bytes(2, 'little', signed=True), MAIN_RAM)) #steamwood bottom edge calculation
                            write_instructions.append((0x17c544 + (self.jp_version * 0x200), (ctx.slot_data["steamwood_width_of_ok_pressure"] + 1).to_bytes(2, 'little'), MAIN_RAM)) #steamwood top edge calculation
                            if(curr_location == 0x301d):
                                write_instructions.append((0x18397a + (self.jp_version * 0x1d4), [ctx.slot_data["steamwood_width_of_ok_pressure"]], MAIN_RAM)) #steamwood 1 ok bar thickness
                                write_instructions.append((0x183976 + (self.jp_version * 0x1d4), [top_edge+1], MAIN_RAM)) #steamwood 1 top edge
                            else:
                                write_instructions.append((0x1849b2 + (self.jp_version * 0x1d4), [ctx.slot_data["steamwood_width_of_ok_pressure"]], MAIN_RAM)) #steamwood 2 ok bar thickness
                                write_instructions.append((0x1849ae + (self.jp_version * 0x1d4), [top_edge+1], MAIN_RAM)) #steamwood 2 top edge
                        if(ctx.slot_data["steamwood_valve_progress_modifier"] != 100):
                            if(curr_location == 0x301d):
                                write_instructions.append((0x183a30 + (self.jp_version * 0x1c8), [
                                    math.ceil(0x30 * ctx.slot_data["steamwood_valve_progress_modifier"] / 100.0),
                                    math.ceil(0x28 * ctx.slot_data["steamwood_valve_progress_modifier"] / 100.0),
                                    math.ceil(0x20 * ctx.slot_data["steamwood_valve_progress_modifier"] / 100.0),
                                    math.ceil(0x18 * ctx.slot_data["steamwood_valve_progress_modifier"] / 100.0),
                                    math.ceil(0x10 * ctx.slot_data["steamwood_valve_progress_modifier"] / 100.0),
                                    math.ceil(0x10 * ctx.slot_data["steamwood_valve_progress_modifier"] / 100.0),
                                    math.ceil(0x10 * ctx.slot_data["steamwood_valve_progress_modifier"] / 100.0),
                                    math.ceil(0x10 * ctx.slot_data["steamwood_valve_progress_modifier"] / 100.0)
                                ], MAIN_RAM)) #steamwood 1 valve progress
                            else:
                                write_instructions.append((0x184a68 + (self.jp_version * 0x1c8), [
                                    math.ceil(0x30 * ctx.slot_data["steamwood_valve_progress_modifier"] / 100.0),
                                    math.ceil(0x28 * ctx.slot_data["steamwood_valve_progress_modifier"] / 100.0),
                                    math.ceil(0x20 * ctx.slot_data["steamwood_valve_progress_modifier"] / 100.0),
                                    math.ceil(0x18 * ctx.slot_data["steamwood_valve_progress_modifier"] / 100.0),
                                    math.ceil(0x10 * ctx.slot_data["steamwood_valve_progress_modifier"] / 100.0),
                                    math.ceil(0x10 * ctx.slot_data["steamwood_valve_progress_modifier"] / 100.0),
                                    math.ceil(0x10 * ctx.slot_data["steamwood_valve_progress_modifier"] / 100.0),
                                    math.ceil(0x10 * ctx.slot_data["steamwood_valve_progress_modifier"] / 100.0)
                                ], MAIN_RAM)) #steamwood 2 valve progress
                        if(ctx.slot_data["steamwood_no_fail_over_pressure"] == True):
                            write_instructions.append((0x17c6dc + (self.jp_version * 0x200), [97 - top_edge], MAIN_RAM)) #check if over pressure
                            write_instructions.append((0x17c6e4 + (self.jp_version * 0x200), [bottom_edge, 0x00, 0x02, 0x24, 0x0e, 0x02, 0x82], MAIN_RAM)) #set new pressure level
                        #li $v0, 0x0001
                        #noop
                        #addu $v0, $a0
                        #bne $v1, $v0, 0x8017dbf4
                        if(curr_location == 0x301d):
                            write_instructions.append((0x17dbc4 + (self.jp_version * 0x200), [0x01, 0x00 , 0x02, 0x24, 0x00, 0x00, 0x00, 0x00, 0x21, 0x10, 0x44, 0x00, 0x08, 0x00, 0x62, 0x14], MAIN_RAM)) #fix if the correct valve was completed
                        else:
                            write_instructions.append((0x17df00 + (self.jp_version * 0x200), [0x01, 0x00 , 0x02, 0x24, 0x00, 0x00, 0x00, 0x00, 0x21, 0x10, 0x44, 0x00, 0x08, 0x00, 0x62, 0x14], MAIN_RAM)) #fix if the correct valve was completed

                        if(curr_location == 0x301d):
                            write_instructions.append((0x17dbb0 + (self.jp_version * 0x200), [0x01, 0x00 , 0x02, 0x24], MAIN_RAM)) #fix check if current valve is less than next valve
                        else:
                            write_instructions.append((0x17deec + (self.jp_version * 0x200), [0x01, 0x00 , 0x02, 0x24], MAIN_RAM)) #fix check if current valve is less than next valve
                        write_instructions.append((0x17db40 + (self.jp_version * 0x200), [0x00, 0x00 , 0x00, 0x00, 0x02, 0x00, 0x63, 0x24], MAIN_RAM)) #fix check if current valve is less than active valve
                        valve_order = [2, 3, 4, 5, 6, 7]
                        if(ctx.slot_data["steamwood_number_valves"] == 1):
                            valve_order = [8]
                            write_instructions.append((0x0ba286 + (self.jp_version * -0xea0), [0x08], MAIN_RAM)) #fix active valve
                        elif(ctx.slot_data["steamwood_number_valves"] == 2):
                            valve_order = [1, 8]
                        else:
                            if(ctx.slot_data["steamwood_random_valves"] == True):
                                random.shuffle(valve_order)
                            while(len(valve_order) + 2 > ctx.slot_data["steamwood_number_valves"]):
                                valve_order.pop(random.randrange(len(valve_order))) 
                            valve_order = [1] + valve_order + [8]
                        valve_update = [8] * 7

                        for i in range(len(valve_order)-1):
                            # 1 7 2 5 3 4 6 8
                            # 1 2 3 4 5 6 8
                            valve_update[valve_order[i]-1] = valve_order[i+1]
                        #logger.info("valve order %s", valve_order)
                        #logger.info("valve update %s", valve_update)
                        if(curr_location == 0x301d):
                            write_instructions.append((0x183bc5 + (self.jp_version * 0x1c8), valve_update, MAIN_RAM)) #steamwood 1 valve order
                        else:
                            write_instructions.append((0x184c59 + (self.jp_version * 0x1c8), valve_update, MAIN_RAM)) #steamwood 2 valve order

                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            write_instructions
                        )
                    if(curr_location == 0x302c or curr_location == 0x3029):
                        if(ctx.slot_data["aqualin_timer"] != 100):
                            #await self.update_progression(ctx)
                            if(self.progression_state < 0x012c and self.progression_state >= 0x00f0):
                                time_modifier = math.ceil(ctx.slot_data["aqualin_timer"] * 0x1555 / 100.0)
                                if(ctx.slot_data["aqualin_timer"] == 1):
                                    time_modifier = 0x25
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x14ae6c + (self.jp_version * 0x2d0), time_modifier.to_bytes(2, 'little'), MAIN_RAM)] #fix aqualin timer
                                )
                    if(ctx.slot_data["restaurant_teleport_maze_no_fail"] == True):
                        if(curr_location == 0x3032):
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x18f638 + (self.jp_version * 0x1d4), [0x32, 0x30, 0x05, 0x00], MAIN_RAM)] #fix left teleporter first room
                            )
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x18f680 + (self.jp_version * 0x1d4), [0x32, 0x30, 0x08, 0x00], MAIN_RAM)] #fix left teleporter third room
                            )
                        if(curr_location == 0x3033):
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x19061c + (self.jp_version * 0x1d4), [0x33, 0x30, 0x08, 0x00], MAIN_RAM)] #fix right teleporter second room
                            )
                    if(curr_location == 0x3051):
                        if(ctx.slot_data["church_fight_time_modifier"] != 100):
                            time_modifier = math.ceil(ctx.slot_data["church_fight_time_modifier"] * 0x1555 / 100.0)
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x14ae6c + (self.jp_version * 0x2d0), time_modifier.to_bytes(2, 'little'), MAIN_RAM)] #fix steamwood timer
                            )
                    if(curr_location == 0x3000): #path to castle
                        if(ctx.slot_data["skip_minigame_town_on_fire"] == True):
                            #await self.update_progression(ctx)
                            if(self.progression_state < 0x2b2 and self.progression_state >= 0x294):
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x078e80 + (self.jp_version * -0xea0), [0xb2, 0x02], MAIN_RAM)]
                                )
                        if(not 0x294 in self.completed_progression):
                            if(item_name_to_id["CarpentA"] in received_list and item_name_to_id["CarpentB"] in received_list and item_name_to_id["CarpentC"] in received_list):
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x0ba1ff + (self.jp_version * -0xea0), [0x3], MAIN_RAM),
                                    (0x0ba204 + (self.jp_version * -0xea0), [0x3], MAIN_RAM),
                                    (0x0ba20d + (self.jp_version * -0xea0), [0x3], MAIN_RAM)]
                                )#update so you dont need to talk to carpenters to deliver gondola gizmo

                    if(curr_location == 0x301b): #meandering forest
                        if(ctx.slot_data["skip_to_frozen_palace"] == True):
                            #await self.update_progression(ctx)
                            if(self.progression_state >= 0x2f0 or 0x2f0 in self.completed_progression):
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x18adc4 + (self.jp_version * 0x118), [0x68, 0x30, 0x00, 0x04], MAIN_RAM)] #0x04003068 frost palace gates
                                )
                    if(curr_location == 0x3090): #Ben Fight
                        if(ctx.slot_data["skip_over_calendar_maze"] == True or ctx.slot_data["soda_fountain_boss_rush"] == True):
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x1858c4 + (self.jp_version * 0x178), [0x88, 0x30, 0x00, 0x00], MAIN_RAM)] #0x00003088 ed fight
                            )
                    if(curr_location == 0x3093): #sky island to soda fountain cutscene
                        if(ctx.slot_data["soda_fountain_boss_rush"] == True):
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x1857bc + (self.jp_version * 0x1b8), [0x90, 0x30, 0x00, 0x00], MAIN_RAM)] #0x00003090 ben fight
                            )
                    if(curr_location == 0x3088): #ed fight
                        if(ctx.slot_data["soda_fountain_boss_rush"] == True):
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x188904 + (self.jp_version * 0x1d8), [0x8d, 0x30, 0x00, 0x00], MAIN_RAM)] #0x0000308d topo fight
                            )
                    if(curr_location == 0x308d): #topo fight
                        if(ctx.slot_data["topo_dance_battle_logic"] != 1):
                            topo_moves: List[int] = []
                            if(ctx.slot_data["topo_dance_battle_logic"] == 2):
                                #new_core_checks: List[bool] = [val & 0b10000000 == 0b10000000 for val in save_data] 
                                simple_moves = [2, 0, 3, 1] * 6
                                for _ in range(3):
                                    flip = random.randint(0, 3)
                                    if(flip > 0):
                                        simple_moves.reverse()
                                        #logger.info("reverse %s", simple_moves)
                                    offset = random.randint(0, 3)
                                    topo_moves = topo_moves + simple_moves[offset:offset+17]
                            else:
                                topo_moves = [random.randint(0,3) for _ in range(51)]
                            
                            topo_addresses = [
                                0x188a7c + (self.jp_version * 0x1c4),
                                0x188b34 + (self.jp_version * 0x1c4),
                                0x188bec + (self.jp_version * 0x1c4)
                            ]
                            musashi_addresses = [
                                0x188aa4 + (self.jp_version * 0x1c4),
                                0x188b5c + (self.jp_version * 0x1c4),
                                0x188c14 + (self.jp_version * 0x1c4)
                            ]
                            write_instructions = []
                            for i in range(3):
                                for j in range(17):
                                    write_instructions.append((topo_addresses[i]+j*2, [topo_moves[i*17+j]], MAIN_RAM))
                                    write_instructions.append((musashi_addresses[i]+j*8, [topo_moves[i*17+j]], MAIN_RAM))
                            #logger.info("all moves %s", topo_moves)
                            if(self.message_level > 0):
                                logger.info("writing Topo Dance Moves")
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                write_instructions
                            )
                            """
                        if(ctx.slot_data["soda_fountain_boss_rush"] == True):
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x1886a4, [0x8f, 0x30, 0x00, 0x00], MAIN_RAM)] #0x0000308f tod fight
                            )"""
                    #if(curr_location == 0x2017)

                    if(ctx.slot_data["quest_item_sanity"] == True):
                        write_instructions = []
                        if(curr_location in [0x1010, 0x1052, 0x1077, 0x1094] and ctx.slot_data["playthrough_method"] == 1): #in chapter 2/3/4/5/6 town
                            if(len(self.chapter3_items) > 0 and 0xc8 in self.completed_progression):
                                for item_id in self.chapter3_items:
                                    if(not item_id in self.bakery_inventory_expansion):
                                        self.bakery_inventory_expansion.append(item_id)
                                        if(self.message_level > 0):
                                            logger.info("%s added to Bakery",item_id_to_name[item_id])
                                self.chapter3_items = []
                            if(len(self.chapter4_items) > 0 and (0x258 in self.completed_progression and 0x1e0 in self.completed_progression and 0x1ae in self.completed_progression)):
                                for item_id in self.chapter4_items:
                                    if(not item_id in self.bakery_inventory_expansion):
                                        self.bakery_inventory_expansion.append(item_id)
                                        if(self.message_level > 0):
                                            logger.info("%s added to Bakery",item_id_to_name[item_id])
                                self.chapter4_items = []
                            if(len(self.chapter5_items) > 0 and 0x384 in self.completed_progression):
                                for item_id in self.chapter5_items:
                                    if(not item_id in self.bakery_inventory_expansion):
                                        self.bakery_inventory_expansion.append(item_id)
                                        if(self.message_level > 0):
                                            logger.info("%s added to Bakery",item_id_to_name[item_id])
                                self.chapter5_items = []
                        if(curr_location in [0x1010, 0x1077, 0x1094]): #in chapter 2/4/5/6 town
                            if(not item_name_to_id["Well H20"] in received_list and self.quest_item_checks[0]):
                                write_instructions.append((well_water_id[self.jp_version][curr_location], [0x0], MAIN_RAM)) #remove water from the well
                        if(curr_location == 0x3022): #at graveyard
                            write_instructions.append((0x17d844 + (self.jp_version * 0x200), [0x0], MAIN_RAM)) #remove jon's key
                        if(curr_location == 0x3029): #at second peak
                            write_instructions.append((0x18e294 + (self.jp_version * 0xe8), [0x0], MAIN_RAM)) #remove first log
                            write_instructions.append((0x18e298 + (self.jp_version * 0xe8), [0x0], MAIN_RAM)) #remove second log
                            write_instructions.append((0x18e29c + (self.jp_version * 0xe8), [0x0], MAIN_RAM)) #remove third log
                            write_instructions.append((0x18e2a0 + (self.jp_version * 0xe8), [0x0], MAIN_RAM)) #remove fourth log
                        if(curr_location == 0x1052): #at Chapter 3 town
                            write_instructions.append((0x18f068 + (self.jp_version * 0x1f0), [0x0], MAIN_RAM)) #remove Key
                            write_instructions.append((0x18f7b0 + (self.jp_version * 0x1f0), [0x0], MAIN_RAM)) #remove Rope
                            write_instructions.append((0x18fa84 + (self.jp_version * 0x1f0), [0x0], MAIN_RAM)) #remove Angel Statue
                        if(curr_location == 0x3047): #at underground lake
                            write_instructions.append((0x188aa0 + (self.jp_version * 0x1d4), [0x0], MAIN_RAM)) #remove Misteria
                        if(curr_location == 0x2057 and ctx.slot_data["grocery_sanity"] == True): #at Chapter 3 grocery
                            write_instructions.append((0x1e3804 + (self.jp_version * -0x4b0), [0x0], MAIN_RAM)) #remove free Orange
                        if(curr_location == 0x3034): #at Basement Lobby
                            write_instructions.append((0x189178 + (self.jp_version * 0x1d4), [0x0], MAIN_RAM)) #remove Ugly Belt
                        if(curr_location == 0x304b): #at Scrap Depository
                            write_instructions.append((0x17d648 + (self.jp_version * 0x200), [0x0, 0x0, 0x5], MAIN_RAM)) #remove first Gondola Gizmo
                            write_instructions.append((0x17d6d0 + (self.jp_version * 0x200), [0x0, 0x0, 0x5], MAIN_RAM)) #remove replacement Gondola Gizmo
                        if(curr_location == 0x1077): #at Chapter 4 town
                            write_instructions.append((0x1910dc + (self.jp_version * 0x1f0), [0x0], MAIN_RAM)) #remove Calendar
                            write_instructions.append((0x1910f8 + (self.jp_version * 0x1f0), [0x0], MAIN_RAM)) #remove Rock Salt
                        if(curr_location == 0x301e): #at outside steamwood
                            write_instructions.append((0x185858 + (self.jp_version * 0x1c8), [0x0], MAIN_RAM)) #remove Handle #0
                        if(curr_location == 0x3020): #at steamwood 2
                            write_instructions.append((0x184d5c + (self.jp_version * 0x1c8), [0x0], MAIN_RAM)) #remove Handle #1
                            write_instructions.append((0x184dc8 + (self.jp_version * 0x1c8), [0x0], MAIN_RAM)) #remove Handle #4
                            write_instructions.append((0x184e24 + (self.jp_version * 0x1c8), [0x0], MAIN_RAM)) #remove Handle #8
                            write_instructions.append((0x184f98 + (self.jp_version * 0x1c0), [0x0], MAIN_RAM)) #remove Profits
                        if(curr_location == 0x1094): #at Chapter 5 town
                            write_instructions.append((0x183df8 + (self.jp_version * 0x200), [0x0], MAIN_RAM)) #remove Musashi's share of the profits
                        if(curr_location == 0x3014): #at Somnolent Forest
                            write_instructions.append((0x190db0 + (self.jp_version * 0x5c), [0x0], MAIN_RAM)) #remove Jon's Note

                        if(curr_location in [0x1052, 0x1077, 0x1094] and game_state[17][13] & 0b1000000 != 0b1000000): #in town chapter 3,4,5 gate not unlocked
                            #save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, 
                            #    [(gate_angles[self.jp_version][curr_location][0], 1, MAIN_RAM), 
                            #    (gate_angles[self.jp_version][curr_location][1], 1, MAIN_RAM)]
                            #))                            
                            addresses = [(gate_angles[self.jp_version][curr_location][0] + ((i-30) * 0x84), 1, MAIN_RAM) for i in range(50)]
                            save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, addresses))
                            if(self.message_level == 3):
                                logger.info("checking if gates are open %s", save_data)
                            found_gates = False
                            gate_index = -1
                            if(len(save_data) > 1):
                                for i in range(len(save_data)-1):
                                    if(save_data[i][0] == 0xfa and save_data[i+1][0] == 0x6):
                                        if(self.message_level == 3):
                                            logger.info("found gate at index %s", i)
                                        gate_index = i
                                        found_gates = True
                            if(found_gates):
                                write_instructions.append((gate_angles[self.jp_version][curr_location][0] + ((gate_index-30) * 0x84), [0x0], MAIN_RAM)) #close doors
                                write_instructions.append((gate_angles[self.jp_version][curr_location][0] + ((gate_index-29) * 0x84), [0x0], MAIN_RAM)) #close doors
                                if(self.message_level == 3):
                                    logger.info("closing gates")
                            elif(self.message_level == 3):
                                logger.info("no open gates found")

                            #if(save_data[0][0] == 0x6 and save[1][0] == 0xfa): #door open
                            #    write_instructions.append((gate_angles[self.jp_version][curr_location][0], [0x0], MAIN_RAM)) #close doors
                            #    write_instructions.append((gate_angles[self.jp_version][curr_location][1], [0x0], MAIN_RAM)) #close doors
                            #    if(self.message_level == 3):
                            #        logger.info("closing gates")
                
                        if(curr_location in quest_item_dialog): 
                            for loc_id, dialog_id in quest_item_dialog[curr_location].items():
                                if(loc_id in ctx.locations_info or loc_id + jp_id_offset in ctx.locations_info):
                                    if(loc_id in ctx.missing_locations or loc_id + jp_id_offset in ctx.missing_locations):
                                        barray = await self.assemble_short_binary_array_for_textbox(ctx,loc_id + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                                        if(self.message_level == 3):
                                            logger.info("quest item dialog %s", loc_id)

                                        if(self.jp_version == 1 and loc_id in [standard_location_name_to_id["Handle #0 - Steamwood 2"],standard_location_name_to_id["Agree to Fix Steamwood - Grillin Village"]]):
                                            barray = barray[:23]
                                            barray.append(0x00)
                                        else:
                                            barray = barray[:39]
                                            barray.append(0x00)
                                        
                                        write_instructions.append((dialog_id[self.jp_version]+4, barray, MAIN_RAM))
                                else:
                                    if(not standard_location_name_to_id["Well H20 - Grillin Village"] + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset) in self.table_ids_to_hint):
                                        for i in range(29):
                                            self.table_ids_to_hint.append(standard_location_name_to_id["Well H20 - Grillin Village"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                                    logger.info("no scout information found")
                                    #logger.info("item 7 id %s", standard_location_name_to_id["Item 7 - Bakery"])
                                    await ctx.send_msgs([{
                                        "cmd": "LocationScouts",
                                        "locations": self.table_ids_to_hint,
                                        "create_as_hint": 0
                                    }])
                                    break
                        
                        if(len(write_instructions) > 0):
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                write_instructions
                            )



                        

                                    



                        """
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x1fab10, bakery_inventory, MAIN_RAM)]
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x189aa0, [len(bakery_inventory)], MAIN_RAM)]
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x189ab0, [len(bakery_inventory)], MAIN_RAM)]
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x189ab4, [0x20, 0x80], MAIN_RAM)] #somehow coresponds to 0x801f
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x189ab8, [0x10, 0xab], MAIN_RAM)]
                        )
                    elif(curr_location == 0x2056): #chapter 3 Jam
                        await self.remove_extra_legendary_armor_from_bakery(ctx)
                        #logger.info("bakery inventory %s",self.bakery_inventory)
                        #logger.info("bakery inventory bytes %s",bytes(self.bakery_inventory))
                        #logger.info("bakery inventory len %s",len(self.bakery_inventory))
                        #logger.info("bakery inventory len bytes %s",bytes(len(self.bakery_inventory)))
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x1fab10, bakery_inventory, MAIN_RAM)]
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x186718, [len(bakery_inventory)], MAIN_RAM)]
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x186708, [len(bakery_inventory)], MAIN_RAM)]
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x18671c, [0x20, 0x80], MAIN_RAM)] #somehow coresponds to 0x801f
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x186720, [0x10, 0xab], MAIN_RAM)]
                        )
                    elif(curr_location == 0x207b): #chapter 4 Jam
                        await self.remove_extra_legendary_armor_from_bakery(ctx)
                        #logger.info("bakery inventory %s",self.bakery_inventory)
                        #logger.info("bakery inventory bytes %s",bytes(self.bakery_inventory))
                        #logger.info("bakery inventory len %s",len(self.bakery_inventory))
                        #logger.info("bakery inventory len bytes %s",bytes(len(self.bakery_inventory)))
                        if(not 0x68 in bakery_inventory):
                            bakery_inventory = [0x69,0x68] + bakery_inventory
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x1fab10, bakery_inventory, MAIN_RAM)]
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x186fe0, [len(bakery_inventory)], MAIN_RAM)]
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x186ff0, [len(bakery_inventory)], MAIN_RAM)]
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x186ff4, [0x20, 0x80], MAIN_RAM)] #somehow coresponds to 0x801f
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x186ff8, [0x10, 0xab], MAIN_RAM)]
                        )
                    elif(curr_location == 0x2098): #chapter 5 Jam
                        await self.remove_extra_legendary_armor_from_bakery(ctx)
                        #logger.info("bakery inventory %s",self.bakery_inventory)
                        #logger.info("bakery inventory bytes %s",bytes(self.bakery_inventory))
                        #logger.info("bakery inventory len %s",len(self.bakery_inventory))
                        #logger.info("bakery inventory len bytes %s",bytes(len(self.bakery_inventory)))
                        if(not 0x68 in bakery_inventory):
                            bakery_inventory = [0x69,0x68] + bakery_inventory
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x1fab10, bakery_inventory, MAIN_RAM)]
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x186cf0, [len(bakery_inventory)], MAIN_RAM)]
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x186ce0, [len(bakery_inventory)], MAIN_RAM)]
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x186cf4, [0x20, 0x80], MAIN_RAM)] #somehow coresponds to 0x801f
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x186cf8, [0x10, 0xab], MAIN_RAM)]
                        )"""
                    if(curr_location == 0x2018): #chapter 2 Conners
                        await self.check_if_bracelet_needs_removed(ctx)
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x18c630 + (self.jp_version * 0x258), [0x9, 0x0], MAIN_RAM)] #andi $v0 $s0 0x4000 to andi $v0 $s0 0x09
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x18c578 + (self.jp_version * 0x258), [0x9, 0x0], MAIN_RAM)] #andi $v0 $s0 0x4000 to andi $v0 $s0 0x09
                        )
                    if(curr_location == 0x2059): #chapter 3 Conners
                        await self.check_if_bracelet_needs_removed(ctx)
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x1891e0 + (self.jp_version * 0x21c), [0x9, 0x0], MAIN_RAM)] #andi $v0 $s0 0x4000 to andi $v0 $s0 0x09
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x189298 + (self.jp_version * 0x21c), [0x9, 0x0], MAIN_RAM)] #andi $v0 $s0 0x4000 to andi $v0 $s0 0x09
                        )
                    if(curr_location == 0x207e): #chapter 4 Conners
                        await self.check_if_bracelet_needs_removed(ctx)
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x189ab8 + (self.jp_version * 0x21c), [0x9, 0x0], MAIN_RAM)] #andi $v0 $s0 0x4000 to andi $v0 $s0 0x09
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x189b70 + (self.jp_version * 0x21c), [0x9, 0x0], MAIN_RAM)] #andi $v0 $s0 0x4000 to andi $v0 $s0 0x09
                        )
                    if(curr_location == 0x209b): #chapter 5 Conners
                        await self.check_if_bracelet_needs_removed(ctx)
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x1897b8 + (self.jp_version * 0x21c), [0x9, 0x0], MAIN_RAM)] #andi $v0 $s0 0x4000 to andi $v0 $s0 0x09
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x189870 + (self.jp_version * 0x21c), [0x9, 0x0], MAIN_RAM)] #andi $v0 $s0 0x4000 to andi $v0 $s0 0x09
                        )
                    if(curr_location == 0x3029): #twinpeak second peak
                        #await self.update_progression(ctx)
                        if(self.progression_state == 0xf0): #about to meet Hotelo at twinpeak
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x18e096 + (self.jp_version * 0xe8), [0x0], MAIN_RAM)] #change entrance from 1 to 0 to prevent softlock
                            )
                            if(self.message_level > 0):
                                logger.info("applied shortcut to hotelo softlock fix")

                        if(self.progression_state > 0x59 and False): #Jon has left the peak
                            save_data: bytes = (await bizhawk.read(
                                ctx.bizhawk_ctx,
                                [(0x0ae65a + (self.jp_version * -0xea0), 1, MAIN_RAM)]
                            ))[0]
                            raft_state = int.from_bytes(save_data, byteorder='little')
                            if(raft_state & 0b11000000 != 0b11000000):
                                #logger.info("Raft incomplete, checking for logs")
                                self.check_for_logs = 1
                    #if(ctx.slot_data["fast_walk"] == True):
                    #    await bizhawk.write(
                    #        ctx.bizhawk_ctx,
                    #        [(0x15a7e4 + (self.jp_version * 0x2a8), [0xa0, 0xff, 0x03, 0x3c, 0x2c, 0x00, 0x23, 0xae, 0x1e + (self.jp_version * 0xaa), 0x6a, 0x05, 0x08, 0x00, 0x00, 0x00, 0x00], MAIN_RAM)] #andi $v0 $s0 0x4000 to andi $v0 $s0 0x09
                    #    ) #jmp c8 6a 05 08 for jp version JP 8015ab20
                self.old_step_count = step_count

            if(self.level_transition == 0):
                if(curr_location == 0x300b and ctx.slot_data["boulder_chase_zoom"] != 2): #running from boulder
                    self.counter_for_delayed_check += 1
                    if(self.counter_for_delayed_check>4):
                        self.counter_for_delayed_check = 0
                        save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                            0x12695C + (self.jp_version * 0xa70), 2, MAIN_RAM
                        )]))[0]
                        zoom = int.from_bytes(save_data, byteorder='little')
                        if(zoom == 0x64):
                            if(self.message_level > 0):
                                logger.info("applying zoom")
                            if(ctx.slot_data["boulder_chase_zoom"] == 1):
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [((0x12695C + (self.jp_version * 0xa70)), [0x30], MAIN_RAM)] 
                                )
                            else:
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [((0x12695C + (self.jp_version * 0xa70)), [0x20, 0x1], MAIN_RAM)] 
                                )
                if(curr_location == 0x301d or curr_location == 0x3020): #steamwood
                    if(ctx.slot_data["steamwood_elevator_logic"] != 1 or (curr_location == 0x3020 and ctx.slot_data["quest_item_sanity"])): #not vanilla elevator
                        self.counter_for_delayed_check += 1
                        if(self.counter_for_delayed_check>2):
                            self.counter_for_delayed_check = 0
                            save_data: bytes = bytes([0,0,0])
                            if(curr_location == 0x301d):
                                save_data = (await bizhawk.read(ctx.bizhawk_ctx, [(0x120744 + (self.jp_version * 0xa70), 1, MAIN_RAM),(0x126b62 + (self.jp_version * 0xa70), 2, MAIN_RAM),(0x1206d2 + (self.jp_version * 0xa70), 1, MAIN_RAM),(0x120704 + (self.jp_version * 0xa70), 1, MAIN_RAM),(0x120638 + (self.jp_version * 0xa70), 1, MAIN_RAM),(0x1205C6 + (self.jp_version * 0xa70), 1, MAIN_RAM),(0x1205F8 + (self.jp_version * 0xa70), 1, MAIN_RAM)]))
                                #is_musashi_on_elevator = int.from_bytes(save_data[0], byteorder='little')
                                #elevator_state = int.from_bytes(save_data[2], byteorder='little')
                                #elevator_floor = int.from_bytes(save_data[3], byteorder='little')
                            else:
                                save_data = (await bizhawk.read(ctx.bizhawk_ctx, [(0x120638 + (self.jp_version * 0xa70), 1, MAIN_RAM),(0x126b62 + (self.jp_version * 0xa70), 2, MAIN_RAM),(0x1205c6 + (self.jp_version * 0xa70), 1, MAIN_RAM),(0x1205f8 + (self.jp_version * 0xa70), 1, MAIN_RAM),(0x12052c + (self.jp_version * 0xa70), 1, MAIN_RAM),(0x1204ba + (self.jp_version * 0xa70), 1, MAIN_RAM),(0x1204ec + (self.jp_version * 0xa70), 1, MAIN_RAM)]))
                            is_musashi_on_elevator = max(int.from_bytes(save_data[0], byteorder='little'),int.from_bytes(save_data[4], byteorder='little'))
                                #logger.info("elevator data %s", save_data)
                                #is_musashi_on_elevator: int = save_data[0]
                            elevator_state = max(int.from_bytes(save_data[2], byteorder='little'),int.from_bytes(save_data[5], byteorder='little'))
                            elevator_floor = max(int.from_bytes(save_data[3], byteorder='little'),int.from_bytes(save_data[6], byteorder='little'))
                            musashi_z = int.from_bytes(save_data[1], byteorder='little')
                            musashi_floor = 1
                            if(musashi_z > 0xfdc0):
                                musashi_floor_handle = 0
                                musashi_floor = 1
                            elif(musashi_z > 0xfbc0):
                                musashi_floor_handle = 0
                                musashi_floor = 2
                            elif(musashi_z > 0xf9c0):
                                musashi_floor_handle = 1
                                musashi_floor = 3
                            elif(musashi_z > 0xf7c0):
                                musashi_floor_handle = 2
                            if(curr_location == 0x3020 and ctx.slot_data["quest_item_sanity"] and musashi_floor_handle != self.musashi_old_floor):
                                self.musashi_old_floor = musashi_floor_handle
                                loc_id = standard_location_name_to_id["Handle #1 - Steamwood 2"] + musashi_floor_handle
                                dialog_id = [0x19bf90, 0x19c0d4]
                                if(loc_id in ctx.locations_info or loc_id + jp_id_offset in ctx.locations_info):
                                    if(loc_id in ctx.missing_locations or loc_id + jp_id_offset in ctx.missing_locations):
                                        barray = await self.assemble_short_binary_array_for_textbox(ctx,loc_id + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                                        if(self.message_level == 3):
                                            logger.info("quest item dialog handle# %s", [1,4,8][musashi_floor_handle])
                                        barray = barray[:47]
                                        barray.append(0x00)
                                        await bizhawk.write(
                                            ctx.bizhawk_ctx,
                                            [(dialog_id[self.jp_version]+4, barray, MAIN_RAM)]
                                        )
                                        #write_instructions.append((dialog_id[self.jp_version]+4, barray, MAIN_RAM))
                            
                            if(ctx.slot_data["steamwood_elevator_logic"] != 1):
                                if(self.elevator_active == False and (is_musashi_on_elevator == 1 or (musashi_floor != elevator_floor and elevator_state == 1))):
                                    self.elevator_active = True
                                    #logger.info("Musashi floor %s", musashi_floor)
                                    #logger.info("Elevator floor %s", elevator_floor)
                                    #logger.info("Restarting Elevator")
                                    if(curr_location == 0x301d):
                                        await bizhawk.write(
                                            ctx.bizhawk_ctx,
                                            [((0x17f6cc + (self.jp_version * 0x200)), [0xff, 0xff], MAIN_RAM)] 
                                        )
                                    else:
                                        await bizhawk.write(
                                            ctx.bizhawk_ctx,
                                            [((0x180704 + (self.jp_version * 0x200)), [0xff, 0xff], MAIN_RAM)] 
                                        )
                                elif(self.elevator_active == True and is_musashi_on_elevator == 0):
                                    if(musashi_floor == 1):
                                        if(elevator_state == 7):
                                            #logger.info("Stopping Elevator")
                                            self.elevator_active = False
                                            if(curr_location == 0x301d):
                                                await bizhawk.write(
                                                    ctx.bizhawk_ctx,
                                                    [((0x17f6cc + (self.jp_version * 0x200)), [0x00, 0x00], MAIN_RAM)] 
                                                )
                                            else:
                                                await bizhawk.write(
                                                    ctx.bizhawk_ctx,
                                                    [((0x180704 + (self.jp_version * 0x200)), [0x00, 0x00], MAIN_RAM)] 
                                                )
                                    elif(ctx.slot_data["steamwood_elevator_logic"] == 2):
                                        if(musashi_floor == 2):
                                            if(elevator_state == 2):
                                                #logger.info("Stopping Elevator")
                                                self.elevator_active = False
                                                if(curr_location == 0x301d):
                                                    await bizhawk.write(
                                                        ctx.bizhawk_ctx,
                                                        [((0x17f6cc + (self.jp_version * 0x200)), [0x00, 0x00], MAIN_RAM)] 
                                                    )
                                                else:
                                                    await bizhawk.write(
                                                        ctx.bizhawk_ctx,
                                                        [((0x180704 + (self.jp_version * 0x200)), [0x00, 0x00], MAIN_RAM)] 
                                                    )
                                        elif(musashi_floor == 3):
                                            if(elevator_state == 3):
                                                #logger.info("Stopping Elevator")
                                                self.elevator_active = False
                                                if(curr_location == 0x301d):
                                                    await bizhawk.write(
                                                        ctx.bizhawk_ctx,
                                                        [((0x17f6cc + (self.jp_version * 0x200)), [0x00, 0x00], MAIN_RAM)] 
                                                    )
                                                else:
                                                    await bizhawk.write(
                                                        ctx.bizhawk_ctx,
                                                        [((0x180704 + (self.jp_version * 0x200)), [0x00, 0x00], MAIN_RAM)] 
                                                    )
                                    elif(ctx.slot_data["steamwood_elevator_logic"] == 3):
                                        if(musashi_floor == 2):
                                            if(elevator_state == 6):
                                                self.elevator_active = False
                                                if(curr_location == 0x301d):
                                                    await bizhawk.write(
                                                        ctx.bizhawk_ctx,
                                                        [((0x17f6cc + (self.jp_version * 0x200)), [0x00, 0x00], MAIN_RAM)] 
                                                    )
                                                else:
                                                    await bizhawk.write(
                                                        ctx.bizhawk_ctx,
                                                        [((0x180704 + (self.jp_version * 0x200)), [0x00, 0x00], MAIN_RAM)] 
                                                    )
                                        elif(musashi_floor == 3):
                                            if(elevator_state == 5):
                                                self.elevator_active = False
                                                if(curr_location == 0x301d):
                                                    await bizhawk.write(
                                                        ctx.bizhawk_ctx,
                                                        [((0x17f6cc + (self.jp_version * 0x200)), [0x00, 0x00], MAIN_RAM)] 
                                                    )
                                                else:
                                                    await bizhawk.write(
                                                        ctx.bizhawk_ctx,
                                                        [((0x180704 + (self.jp_version * 0x200)), [0x00, 0x00], MAIN_RAM)] 
                                                    )


                if(curr_location == 0x3060 or curr_location == 0x3062 or curr_location == 0x305d or curr_location == 0x305e or curr_location == 0x3063):
                    self.counter_for_delayed_check += 1
                    if(self.counter_for_delayed_check>9):
                        self.counter_for_delayed_check = 0
                        if(curr_location in dialog_location_table):
                            for loc_id, dialog_id in dialog_location_table[curr_location].items():
                                if(loc_id in ctx.locations_info or loc_id + jp_id_offset in ctx.locations_info):
                                    if(loc_id in short_text_boxes):
                                        barray = await self.assemble_short_binary_array_for_textbox(ctx, loc_id + ((ctx.slot_data["set_lang"] == 2) * jp_id_offset))
                                    else:
                                        barray = await self.assemble_binary_array_for_textbox(ctx, loc_id + ((ctx.slot_data["set_lang"] == 2) * jp_id_offset))
                                    await bizhawk.write(
                                        ctx.bizhawk_ctx,
                                        [(dialog_id[self.jp_version]+4, barray, MAIN_RAM)]
                                    )
                if(curr_location == 0x3025): #Twinpeak Entrance
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [(0x18570c + (self.jp_version * 0x200), [0], MAIN_RAM)]
                    ) #disable changing progression when opening bracelet chest
                    #en
                    #volatile uint32_t *disableBraceletProgression = 0x8018570c;
                    #*(disableBraceletProgression)=0;
                    #jp
                    #volatile uint32_t *disableBraceletProgression = 0x8018590c;
                    #*(disableBraceletProgression)=0;
                if(curr_location == 0x3029 and self.check_for_logs): #Twinpeak second peak check if raft needs updated
                    self.counter_for_delayed_check += 1
                    if(self.counter_for_delayed_check>12):
                        self.counter_for_delayed_check = 0
                        await self.update_inventory(ctx)
                        if(0x4e in self.curr_inventory and 0x50 in self.curr_inventory and 0x51 in self.curr_inventory and 0x52 in self.curr_inventory):
                            #logger.info("Raft complete, removing Logs")
                            self.check_for_logs = 0
                            save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                0x0ae65a + (self.jp_version * -0xea0), 1, MAIN_RAM
                            )]))[0]
                            raft_state = int.from_bytes(save_data, byteorder='little')
                            raft_state = raft_state | 0b11000000
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x0ae65a + (self.jp_version * -0xea0), [raft_state], MAIN_RAM)]
                            )
                            for i in range(len(self.curr_inventory)):
                                if(self.curr_inventory[i] in [0x4d,0x4e,0x50,0x51,0x52]): #Jon's key and four logs
                                    await bizhawk.write(
                                        ctx.bizhawk_ctx,
                                        [((0x0ba1e7+i + (self.jp_version * -0xea0)), [0x0], MAIN_RAM)] 
                                    )
                if(curr_location == 0x302a): #rafting minigame
                    if(ctx.slot_data["raft_difficulty"] == 3 or ctx.slot_data["raft_hp"] != 4):
                        self.counter_for_delayed_check += 1
                        if(self.counter_for_delayed_check > 4):
                            self.counter_for_delayed_check = 0
                            save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(0x0ba287 + (self.jp_version * -0xea0), 1, MAIN_RAM),(0x17ec48 + (self.jp_version * 0x200), 1, MAIN_RAM)]))
                            self.raft_hp = int.from_bytes(save_data[0], byteorder='little')
                            #logger.info("log data %s", save_data)
                            #self.raft_hp = save_data[0]
                            if(ctx.slot_data["raft_hp"] != 4 and int.from_bytes(save_data[1], byteorder='little') == 4):
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x0ba287 + (self.jp_version * -0xea0), [ctx.slot_data["raft_hp"]], MAIN_RAM), (0x17ec48 + (self.jp_version * 0x200), [ctx.slot_data["raft_hp"]], MAIN_RAM)] #fix starting raft hp
                                )
                            if(ctx.slot_data["raft_difficulty"] == 3):
                                self.raft_regrow_timer += 1 
                                if(self.raft_hp == 4):
                                    self.raft_regrow_timer = 0
                                if(self.raft_regrow_timer >= ctx.slot_data["raft_regrow"]):
                                    self.raft_regrow_timer = 0
                                    await bizhawk.write(
                                        ctx.bizhawk_ctx,
                                        [(0x0ba287 + (self.jp_version * -0xea0), [self.raft_hp + 1], MAIN_RAM)] #add a log
                                    )

                    """if(ctx.slot_data["skip_minigame_follow_leno"] == True):
                        save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                            0x0ba284, 1, MAIN_RAM
                        )]))[0]
                        leno_state = int.from_bytes(save_data, byteorder='little')
                        if(leno_state > 0 and leno_state < 0x3):
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x0ba284, [0x0e], MAIN_RAM), (0x190614, [0x22, 0x30, 0x00, 0x04], MAIN_RAM)] #graveyard 0x04003022
                            )"""
                if(self.check_if_lumina_was_found):
                    if(ctx.slot_data["lumina_randomzied"] == True):
                        save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                            0x0ae658 + (self.jp_version * -0xea0), 1, MAIN_RAM
                        )]))[0]
                        lumina_state = int.from_bytes(save_data, byteorder='little')
                        lumina_state = lumina_state & 0b1
                        if((lumina_state == 1 and not curr_location in [0x3005, 0x3006, 0x3008, 0x3009, 0x300a]) or self.progression_state >= 0xa):
                            self.check_if_lumina_was_found = 0

                            await ctx.check_locations([standard_location_name_to_id["Lumina - Spiral Tower"] + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset)])
                            #await ctx.send_msgs([{
                            #    "cmd": "LocationChecks",
                            #    "locations": [standard_location_name_to_id["Lumina - Spiral Tower"] + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset)]
                            #}])
                    else:
                        self.check_if_lumina_was_found = 0

                if(self.check_if_lumina_needs_removed):
                    if(ctx.slot_data["lumina_randomzied"] == True):
                        self.update_list_of_received_items(ctx)
                        if(curr_location < 0x3000 or curr_location > 0x300f): #check if past chapter 1
                            if(not item_name_to_id["Lumina"] in received_list):
                                if(self.message_level > 0):
                                    logger.info("Yeeting Lumina")
                                save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                    0x0ae658 + (self.jp_version * -0xea0), 1, MAIN_RAM
                                )]))[0]
                                lumina_state = int.from_bytes(save_data, byteorder='little')
                                lumina_state = lumina_state & 0b11111110
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x0ae658 + (self.jp_version * -0xea0), [lumina_state], MAIN_RAM)]
                                )
                                save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                    0x078ec0 + (self.jp_version * -0xea0), 1, MAIN_RAM
                                )]))[0]
                                lumina_state = int.from_bytes(save_data, byteorder='little')
                                lumina_state = lumina_state & 0b11111110
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x078ec0 + (self.jp_version * -0xea0), [lumina_state], MAIN_RAM)]
                                )
                                self.check_if_lumina_needs_removed = 0
                            else:
                                self.check_if_lumina_needs_removed = 0
                    else:
                        self.check_if_lumina_needs_removed = 0
                if(curr_location in bakery_locations):
                    curr_inventory = set(game_state[19])
                    if(0x56 in curr_inventory and not 0x56 in self.old_inventory):
                        self.try_to_update_connections = True
                    if(0x4d in curr_inventory and not 0x4d in self.old_inventory):
                        self.try_to_update_connections = True
                    self.old_inventory = curr_inventory
                if(ctx.slot_data["bakery_sanity"] == True or ctx.slot_data["restaurant_sanity"] == True):
                    if(curr_location in bakery_locations or curr_location in restaurant_locations):
                        if(len(self.bakery_dialog)>0 or len(self.restaurant_dialog)>0):
                            if(False in self.bakery_checks or False in self.restaurant_checks):
                                save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                    0x11514A + (self.jp_version * 0xa70), 1, MAIN_RAM
                                )]))[0]
                                new_cursor_pos = int.from_bytes(save_data, byteorder='little')

                                save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                    0x115130 + (self.jp_version * 0xa70), 1, MAIN_RAM
                                )]))[0]
                                check_if_question_mark = int.from_bytes(save_data, byteorder='little')
                                if(self.cursor_pos != new_cursor_pos and (check_if_question_mark == 0xec or new_cursor_pos > 0 or self.cursor_pos>0)):
                                    self.cursor_pos = new_cursor_pos
                                    #logger.info("cursor pos %s", self.cursor_pos)
                                    if(ctx.slot_data["bakery_sanity"] == True and curr_location in bakery_locations):
                                        if(self.cursor_pos < len(self.bakery_checks) and (self.cursor_pos+1) * 2 <= len(self.bakery_dialog) and self.cursor_pos < len(self.bakery_inventory)):
                                            if(self.bakery_inventory[self.cursor_pos]==0x3e):
                                                #logger.info("bakery text %s",self.assemble_binary_array_for_bakery_dialog(self.bakery_dialog[(self.cursor_pos)*2],self.bakery_dialog[(self.cursor_pos)*2+1]))
                                                await bizhawk.write(
                                                    ctx.bizhawk_ctx,
                                                    [(0x1faae0, self.assemble_binary_array_for_dialog(self.bakery_dialog[(self.cursor_pos)*2],self.bakery_dialog[(self.cursor_pos)*2+1]), MAIN_RAM)]
                                                )
                                                await bizhawk.write(
                                                    ctx.bizhawk_ctx,
                                                    [(0x1269f0 + (self.jp_version * 0xa70), [0xe0, 0xaa, 0x1f, 0x80], MAIN_RAM)]
                                                )
                                                await bizhawk.write(
                                                    ctx.bizhawk_ctx,
                                                    [(0x126a00 + (self.jp_version * 0xa70), [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], MAIN_RAM)]
                                                )
                                                await bizhawk.write(
                                                    ctx.bizhawk_ctx,
                                                    [(0x1269f4 + (self.jp_version * 0xa70), [0x01], MAIN_RAM)]
                                                )
                                    if(ctx.slot_data["restaurant_sanity"] == True and curr_location in bakery_locations):
                                        if(self.cursor_pos < len(self.restaurant_checks) and (self.cursor_pos+1) * 2 <= len(self.restaurant_dialog) and self.cursor_pos < len(self.bakery_inventory)):
                                            if(self.bakery_inventory[self.cursor_pos]==0x40):
                                                #logger.info("bakery text %s",self.assemble_binary_array_for_bakery_dialog(self.bakery_dialog[(self.cursor_pos)*2],self.bakery_dialog[(self.cursor_pos)*2+1]))
                                                await bizhawk.write(
                                                    ctx.bizhawk_ctx,
                                                    [(0x1faae0, self.assemble_binary_array_for_dialog(self.restaurant_dialog[(self.cursor_pos)*2],self.restaurant_dialog[(self.cursor_pos)*2+1]), MAIN_RAM)]
                                                )
                                                await bizhawk.write(
                                                    ctx.bizhawk_ctx,
                                                    [(0x1269f0 + (self.jp_version * 0xa70), [0xe0, 0xaa, 0x1f, 0x80], MAIN_RAM)]
                                                )
                                                await bizhawk.write(
                                                    ctx.bizhawk_ctx,
                                                    [(0x126a00 + (self.jp_version * 0xa70), [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], MAIN_RAM)]
                                                )
                                                await bizhawk.write(
                                                    ctx.bizhawk_ctx,
                                                    [(0x1269f4 + (self.jp_version * 0xa70), [0x01], MAIN_RAM)]
                                                )
                                    if(ctx.slot_data["restaurant_sanity"] == True and curr_location in restaurant_locations):
                                        if(self.cursor_pos < len(self.restaurant_checks) and (self.cursor_pos+1) * 2 <= len(self.restaurant_dialog) and self.cursor_pos < len(self.restaurant_inventory)):
                                            if(self.restaurant_inventory[self.cursor_pos]==0x40):
                                                #logger.info("bakery text %s",self.assemble_binary_array_for_bakery_dialog(self.bakery_dialog[(self.cursor_pos)*2],self.bakery_dialog[(self.cursor_pos)*2+1]))
                                                await bizhawk.write(
                                                    ctx.bizhawk_ctx,
                                                    [(0x1faae0, self.assemble_binary_array_for_dialog(self.restaurant_dialog[(self.cursor_pos)*2],self.restaurant_dialog[(self.cursor_pos)*2+1]), MAIN_RAM)]
                                                )
                                                await bizhawk.write(
                                                    ctx.bizhawk_ctx,
                                                    [(0x1269f0 + (self.jp_version * 0xa70), [0xe0, 0xaa, 0x1f, 0x80], MAIN_RAM)]
                                                )
                                                await bizhawk.write(
                                                    ctx.bizhawk_ctx,
                                                    [(0x126a00 + (self.jp_version * 0xa70), [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], MAIN_RAM)]
                                                )
                                                await bizhawk.write(
                                                    ctx.bizhawk_ctx,
                                                    [(0x1269f4 + (self.jp_version * 0xa70), [0x01], MAIN_RAM)]
                                                )

                if(ctx.slot_data["grocery_sanity"] == True):
                    if(curr_location in grocery_locations):
                        if(len(self.grocery_dialog)>0):
                            if(False in self.grocery_checks):
                                save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                    0x11514A + (self.jp_version * 0xa70), 1, MAIN_RAM
                                )]))[0]
                                new_cursor_pos = int.from_bytes(save_data, byteorder='little')

                                save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                    0x115130 + (self.jp_version * 0xa70), 1, MAIN_RAM
                                )]))[0]
                                check_if_question_mark = int.from_bytes(save_data, byteorder='little')
                                if(self.cursor_pos != new_cursor_pos and (check_if_question_mark == 0xec or new_cursor_pos > 0 or self.cursor_pos>0)):
                                    self.cursor_pos = new_cursor_pos
                                    #logger.info("cursor pos %s", self.cursor_pos)
                                    if(self.cursor_pos < len(self.grocery_checks) and (self.cursor_pos+1) * 2 <= len(self.grocery_dialog) and self.cursor_pos < len(self.grocery_inventory)):
                                        if(self.grocery_inventory[self.cursor_pos]==0x42):
                                            #logger.info("bakery text %s",self.assemble_binary_array_for_bakery_dialog(self.bakery_dialog[(self.cursor_pos)*2],self.bakery_dialog[(self.cursor_pos)*2+1]))
                                            await bizhawk.write(
                                                ctx.bizhawk_ctx,
                                                [(0x1faae0, self.assemble_binary_array_for_dialog(self.grocery_dialog[(self.cursor_pos)*2],self.grocery_dialog[(self.cursor_pos)*2+1]), MAIN_RAM)]
                                            )
                                            await bizhawk.write(
                                                ctx.bizhawk_ctx,
                                                [(0x1269f0 + (self.jp_version * 0xa70), [0xe0, 0xaa, 0x1f, 0x80], MAIN_RAM)]
                                            )
                                            await bizhawk.write(
                                                ctx.bizhawk_ctx,
                                                [(0x126a00 + (self.jp_version * 0xa70), [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], MAIN_RAM)]
                                            )
                                            await bizhawk.write(
                                                ctx.bizhawk_ctx,
                                                [(0x1269f4 + (self.jp_version * 0xa70), [0x01], MAIN_RAM)]
                                            )
                                        elif(self.grocery_inventory[self.cursor_pos]==0x0):
                                            await bizhawk.write(
                                                ctx.bizhawk_ctx,
                                                [(0x115130 + (self.jp_version * 0xa70), [0xe8], MAIN_RAM)] #clear text box
                                            )
                if(curr_location == 0x1011): #at upper town chapter 2
                    if(self.progression_state == 0x78):
                        if(game_state[19].count(0x4d) > 1):
                            new_inventory: List[int] = []
                            manual_counter = 0
                            for val in game_state[19]:
                                if(val == 0x4d):
                                    manual_counter = manual_counter + 1
                                if(manual_counter < 2 or val != 0x4d):
                                    new_inventory.append(val) 
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x0ba1e7 + (self.jp_version * -0xea0), new_inventory, MAIN_RAM)]
                            )
                            if(self.message_level > 0):
                                logger.info("removing extra manual")
                
                if(len(self.messagequeue) > 0):
                    self.messagetimer = self.messagetimer + 1
                    if(self.messagetimer > 1):
                        self.messagetimer = 0
                        await bizhawk.display_message(ctx.bizhawk_ctx, self.messagequeue.pop(0))
                        if(len(self.messagequeue) > 30):
                            i = 0
                            while i < len(self.messagequeue) and len(self.messagequeue) > 30:
                                if(not "(Prog)" in self.messagequeue[i]):
                                    self.messagequeue.pop(i)
                                else:
                                    i = i + 1
                            if(len(self.messagequeue) > 30):
                                self.messagequeue = self.messagequeue[-30:]
                            
                if(curr_location == 0x304b and ctx.slot_data["quest_item_sanity"]):
                    save_data = (await bizhawk.read(ctx.bizhawk_ctx, [(0x126b5e + (self.jp_version * 0xa70), 2, MAIN_RAM),(0x126b66 + (self.jp_version * 0xa70), 2, MAIN_RAM)]))
                    musashi_x = int.from_bytes(save_data[0], byteorder='little', signed = True)
                    musashi_y = int.from_bytes(save_data[1], byteorder='little', signed = True)
                    gizmo_positions = [[-204, 58], [-45, 18], [150, -43], [189, -289]]
                    gizmo_distances = [abs(musashi_y - y) + abs(musashi_x - x) for x, y in gizmo_positions]
                    closest_gizmo = min(range(len(gizmo_distances)), key=gizmo_distances.__getitem__)
                    if(closest_gizmo != self.old_closest_gizmo):
                        self.old_closest_gizmo = closest_gizmo
                        loc_id = standard_location_name_to_id["Gondola Gizmo 1 - Scrap Depository"] + closest_gizmo
                        dialog_id = [0x184360, 0x184424]
                        dialog_id_2 = [0x184450, 0x1844ec]
                        if(loc_id in ctx.locations_info or loc_id + jp_id_offset in ctx.locations_info):
                            if(loc_id in ctx.missing_locations or loc_id + jp_id_offset in ctx.missing_locations):
                                barray = await self.assemble_short_binary_array_for_textbox(ctx,loc_id + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                                if(self.message_level == 3):
                                    logger.info("gondola gizmo dialog # %s : %s", closest_gizmo + 1, gizmo_distances)
                                barray = barray[:47]
                                barray.append(0x00)
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(dialog_id[self.jp_version]+4, barray, MAIN_RAM),
                                    (dialog_id_2[self.jp_version]+4, barray, MAIN_RAM)]
                                )
                """if(ctx.slot_data["bakery_sanity"] == True):
                    if(curr_location in bakery_locations):
                        if(len(self.bakery_dialog)>0):
                            if(False in self.bakery_checks):
                                save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                    0x11514A, 1, MAIN_RAM
                                )]))[0]
                                new_cursor_pos = int.from_bytes(save_data, byteorder='little')

                                save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                    0x115130, 1, MAIN_RAM
                                )]))[0]
                                check_if_question_mark = int.from_bytes(save_data, byteorder='little')
                                if(self.cursor_pos != new_cursor_pos and (check_if_question_mark == 0xec or new_cursor_pos > 0)):
                                    self.cursor_pos = new_cursor_pos
                                    #logger.info("cursor pos %s", self.cursor_pos)
                                    if(self.cursor_pos < len(self.bakery_checks) and (self.cursor_pos+1) * 2 <= len(self.bakery_dialog)):
                                        if(self.bakery_inventory[self.cursor_pos]==0x3e):
                                            #logger.info("bakery text %s",self.assemble_binary_array_for_bakery_dialog(self.bakery_dialog[(self.cursor_pos)*2],self.bakery_dialog[(self.cursor_pos)*2+1]))
                                            await bizhawk.write(
                                                ctx.bizhawk_ctx,
                                                [(0x1faae0, self.assemble_binary_array_for_dialog(self.bakery_dialog[(self.cursor_pos)*2],self.bakery_dialog[(self.cursor_pos)*2+1]), MAIN_RAM)]
                                            )
                                            await bizhawk.write(
                                                ctx.bizhawk_ctx,
                                                [(0x1269f0, [0xe0, 0xaa, 0x1f, 0x80], MAIN_RAM)]
                                            )
                                            await bizhawk.write(
                                                ctx.bizhawk_ctx,
                                                [(0x126a00, [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], MAIN_RAM)]
                                            )
                                            await bizhawk.write(
                                                ctx.bizhawk_ctx,
                                                [(0x1269f4, [0x01], MAIN_RAM)]
                                            )

                if(ctx.slot_data["restaurant_sanity"] == True):
                    if(curr_location in restaurant_locations):
                        if(len(self.restaurant_dialog)>0):
                            if(False in self.restaurant_checks):
                                save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                    0x11514A, 1, MAIN_RAM
                                )]))[0]
                                new_cursor_pos = int.from_bytes(save_data, byteorder='little')

                                save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                    0x115130, 1, MAIN_RAM
                                )]))[0]
                                check_if_question_mark = int.from_bytes(save_data, byteorder='little')
                                if(self.cursor_pos != new_cursor_pos and (check_if_question_mark == 0xec or new_cursor_pos > 0)):
                                    self.cursor_pos = new_cursor_pos
                                    #logger.info("cursor pos %s", self.cursor_pos)
                                    if(self.cursor_pos < len(self.restaurant_checks) and (self.cursor_pos+1) * 2 <= len(self.restaurant_dialog) and self.cursor_pos < len(self.restaurant_inventory)):
                                        if(self.restaurant_checks[self.cursor_pos] == False or self.restaurant_inventory[self.cursor_pos]==0x40):
                                            #logger.info("bakery text %s",self.assemble_binary_array_for_bakery_dialog(self.bakery_dialog[(self.cursor_pos)*2],self.bakery_dialog[(self.cursor_pos)*2+1]))
                                            await bizhawk.write(
                                                ctx.bizhawk_ctx,
                                                [(0x1faae0, self.assemble_binary_array_for_dialog(self.restaurant_dialog[(self.cursor_pos)*2],self.restaurant_dialog[(self.cursor_pos)*2+1]), MAIN_RAM)]
                                            )
                                            await bizhawk.write(
                                                ctx.bizhawk_ctx,
                                                [(0x1269f0, [0xe0, 0xaa, 0x1f, 0x80], MAIN_RAM)]
                                            )
                                            await bizhawk.write(
                                                ctx.bizhawk_ctx,
                                                [(0x126a00, [0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00, 0x00], MAIN_RAM)]
                                            )
                                            await bizhawk.write(
                                                ctx.bizhawk_ctx,
                                                [(0x1269f4, [0x01], MAIN_RAM)]
                                            )"""




            #if not ctx.finished_game and len(ctx.items_received) == 35:
            if not ctx.finished_game:
                if(ctx.slot_data["goal"] == 2): #Rescue x NPCs
                    if len(set(received_list)&(set(npc_ids))) >= ctx.slot_data["npc_goal"]:
                        await ctx.send_msgs([{
                            "cmd": "StatusUpdate",
                            "status": ClientStatus.CLIENT_GOAL
                        }])
                elif(ctx.slot_data["goal"] == 3): #Skullpion goal
                    if save_data_toys[11] & 0b10000000 == 0b10000000:
                        await ctx.send_msgs([{
                            "cmd": "StatusUpdate",
                            "status": ClientStatus.CLIENT_GOAL
                        }])
                elif(ctx.slot_data["goal"] == 4): #Relic Keeper goal
                    if save_data_toys[17] & 0b10000000 == 0b10000000:
                        await ctx.send_msgs([{
                            "cmd": "StatusUpdate",
                            "status": ClientStatus.CLIENT_GOAL
                        }])
                elif(ctx.slot_data["goal"] == 5): #Frost Dragon goal
                    if save_data_toys[23] & 0b10000000 == 0b10000000:
                        await ctx.send_msgs([{
                            "cmd": "StatusUpdate",
                            "status": ClientStatus.CLIENT_GOAL
                        }])
                elif(ctx.slot_data["goal"] == 6): #Ant Queen goal
                    if save_data_toys[29] & 0b10000000 == 0b10000000:
                        await ctx.send_msgs([{
                            "cmd": "StatusUpdate",
                            "status": ClientStatus.CLIENT_GOAL
                        }])
                elif(ctx.slot_data["goal"] == 7): #ToD goal
                    if save_data_toys[35] & 0b10000000 == 0b10000000:
                        await ctx.send_msgs([{
                            "cmd": "StatusUpdate",
                            "status": ClientStatus.CLIENT_GOAL
                        }])
                elif(ctx.slot_data["goal"] == 8): #DL goal
                    #if save_data_toys[40] & 0b10000000 == 0b10000000: #toy only happens with 6 legendary armors
                    if(curr_location == 0x30A4 or curr_location == 0x30A2 or curr_location == 0x30A5):
                        await ctx.send_msgs([{
                            "cmd": "StatusUpdate",
                            "status": ClientStatus.CLIENT_GOAL
                        }])
                elif(ctx.slot_data["goal"] == 9): #kill X crest guardian
                    if(self.num_bosses_killed >= ctx.slot_data["guardian_goal"]):
                        await ctx.send_msgs([{
                            "cmd": "StatusUpdate",
                            "status": ClientStatus.CLIENT_GOAL
                        }])
                else: #Rescue all NPCs
                    if set(received_list).issuperset(set(npc_ids)):
                        await ctx.send_msgs([{
                            "cmd": "StatusUpdate",
                            "status": ClientStatus.CLIENT_GOAL
                        }])
            
            if (self.request_hints == 0):
                self.request_hints = 1 
                if(ctx.slot_data["set_lang"] == 2):
                    self.table_ids_to_hint = jp_table_ids_to_hint.copy()
                else:
                    self.table_ids_to_hint = en_table_ids_to_hint.copy()

                if(ctx.slot_data["bakery_sanity"] == True):
                    if(not standard_location_name_to_id["Item 1 - Bakery"] + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset) in self.table_ids_to_hint):
                        for i in range(7):
                            self.table_ids_to_hint.append(standard_location_name_to_id["Item 1 - Bakery"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                if(ctx.slot_data["restaurant_sanity"] == True):
                    if(not standard_location_name_to_id["Item 1 - Restaurant"] + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset) in self.table_ids_to_hint):
                        for i in range(7):
                            self.table_ids_to_hint.append(standard_location_name_to_id["Item 1 - Restaurant"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                if(ctx.slot_data["grocery_sanity"] == True):
                    if(not standard_location_name_to_id["Item 1 - Grocery"] + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset) in self.table_ids_to_hint):
                        for i in range(12):
                            self.table_ids_to_hint.append(standard_location_name_to_id["Item 1 - Grocery"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                if(ctx.slot_data["toy_sanity"] == True):
                    if(not standard_location_name_to_id["Musashi - Toy Shop"] + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset) in self.table_ids_to_hint):
                        for i in range(30):
                            self.table_ids_to_hint.append(standard_location_name_to_id["Musashi - Toy Shop"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                if(ctx.slot_data["tech_sanity"] == True):
                    if(not standard_location_name_to_id["Improved Fusion (Artisan) - Allucaneet Castle"] + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset) in self.table_ids_to_hint):
                        for i in range(7):
                            self.table_ids_to_hint.append(standard_location_name_to_id["Improved Fusion (Artisan) - Allucaneet Castle"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))       
                if(ctx.slot_data["scroll_sanity"] == True):
                    if(not standard_location_name_to_id["Earth Scroll - Twinpeak First Peak"] + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset) in self.table_ids_to_hint):
                        for i in range(5):
                            self.table_ids_to_hint.append(standard_location_name_to_id["Earth Scroll - Twinpeak First Peak"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                if(ctx.slot_data["core_sanity"] == True):
                    if(not standard_location_name_to_id["Defeat Earth Crest Guardian - Skullpion Arena"] + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset) in self.table_ids_to_hint):
                        for i in range(4):
                            self.table_ids_to_hint.append(standard_location_name_to_id["Defeat Earth Crest Guardian - Skullpion Arena"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                if(ctx.slot_data["quest_item_sanity"] == True):
                    if(not standard_location_name_to_id["Well H20 - Grillin Village"] + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset) in self.table_ids_to_hint):
                        for i in range(29):
                            self.table_ids_to_hint.append(standard_location_name_to_id["Well H20 - Grillin Village"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                await ctx.send_msgs([{
                    "cmd": "LocationScouts",
                    "locations": self.table_ids_to_hint,
                    "create_as_hint": 0
                }])

            if((ctx.slot_data["deathlink"] and self.deathlink == -1) or self.deathlink == 1):
                if self.death_link_timer > 0 and self.has_died == 0:
                    self.death_link_timer -= 1
                    if self.death_link_timer == 0:
                        logger.info("death link grace period has ended")
                if "DeathLink" not in ctx.tags:
                    await ctx.update_death_link(True)
                    self.previous_death_link = ctx.last_death_link
                if self.death_link_timer == 0:
                    curr_hp_bytes: bytes = (await bizhawk.read(
                        ctx.bizhawk_ctx,
                        [(PLAYER_CURR_HP_MEMORY + (self.jp_version * -0xea0), 2, MAIN_RAM)]
                    ))[0]
                    curr_hp: int = int.from_bytes(curr_hp_bytes, byteorder='little')
                    if curr_hp == 0 and self.has_died == 0:
                        self.has_died = 1
                        curr_maxhp_bytes: bytes = (await bizhawk.read(
                            ctx.bizhawk_ctx,
                            [(0x078eb2 + (self.jp_version * -0xea0), 2, MAIN_RAM)]
                        ))[0]
                        max_hp: int = int.from_bytes(curr_hp_bytes, byteorder='little')
                        if(max_hp > 0):
                            logger.info("%s died",ctx.username)
                            await ctx.send_death(f"{ctx.username} had a nightmare about a horrid death!")
                    if curr_hp > 0 and self.has_died == 1:
                        self.has_died = 0
                        logger.info("%s revived",ctx.username)
                        self.death_link_timer = 240
                    #ctx.handle_deathlink_state(curr_hp>0)
                if self.previous_death_link != ctx.last_death_link:
                    self.previous_death_link = ctx.last_death_link
                    if self.death_link_timer == 0 and self.has_died == 0:
                        logger.info("received death link")
                        await self.kill_player(ctx)
                        self.has_died = 1
                    
        except bizhawk.RequestFailedError:
            # The connector didn't respond. Exit handler and return to main loop to reconnect
            pass
        #except KeyError:
        #    logger.info("missing data for Key")

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        """For handling packages from the server. Called from `BizHawkClientContext.on_package`."""
        #taken from ape escape https://github.com/Thedragon005/Archipelago-Ape-Escape/blob/12dace2cdecf019ae7cfcb49dfd64ecb56a6c409/worlds/apeescape/Client.py#L504
        if cmd == "Bounced":
            if "tags" in args and False:
                assert ctx.slot is not None
                source_name = args["data"]["source"]
                if "TrapLink" in args["tags"] and args["data"]["source"] != ctx.slot_info[ctx.slot].name:
                    trap_name: str = args["data"]["trap_name"]
                    if(self.message_level == 3):
                        from CommonClient import logger
                        logger.info("[TrapLink] received <%s>", trap_name)

                    #local_trap_name: str = trap_to_local_traps.get(trap_name)
                    #print(local_trap_name)
                    #trap_value: int = trap_name_to_value.get(local_trap_name)

                    #message = f"Received linked {trap_name} from {source_name}"
                    #logger.info(message)
                    #self.priority_trap_queue.insert(0,[trap_value,time.time()])
                    #Utils.async_start(self.send_bizhawk_message(ctx,message,"Passthrough", ""))

        if cmd in {"PrintJSON"} and "type" in args and ctx.slot_data is not None:
            # When a message is received
            if args["type"] == "ItemSend" and ctx.slot_data["set_lang"] == 1:
                item = args["item"]
                networkItem = NetworkItem(*item)
                recieverID = args["receiving"]
                senderID = networkItem.player
                if recieverID == ctx.slot or senderID == ctx.slot:
                    itemCategory = networkItem.flags
                    if(len(self.messagequeue) < 31 or itemCategory & IC.progression == IC.progression):
                        if itemCategory & IC.trap == IC.trap:
                            itemClass = "(Trap) "
                        elif itemCategory & IC.progression == IC.progression:
                            itemClass = "(Prog) "
                        elif itemCategory & IC.useful == IC.useful:
                            itemClass = "(Useful) "
                        else:
                            itemClass = ""

                        recieverName = ctx.player_names[recieverID]
                        senderName = ctx.player_names[senderID]

                        message = ""
                        itemName = ctx.item_names.lookup_in_slot(networkItem.item, recieverID)
                        if recieverID != ctx.slot and senderID == ctx.slot:
                            message = f"Sent '{itemName}' {itemClass}to {recieverName}"
                        elif recieverID == ctx.slot and senderID != ctx.slot:
                            message = f"Received '{itemName}' {itemClass}from {senderName}"
                        else: #if recieverID == ctx.slot and senderID == ctx.slot:
                            message = f"You found '{itemName}'"

                        self.messagequeue.append(message)
                # If there is a PRINTJSON which is sent by the player
                #if "TrapLink" in ctx.tags and recieverID == ctx.slot and itemName in trap_name_to_value:
                #    Utils.async_start(self.send_trap_link(ctx, itemName))



    def fix_dialog(self, text: List[str]):
        if(len(text)>0):
            line_1_max = 0
            line_2_max = 0
            for i in range(len(text)):
                if(i%2 == 1):
                    if(len(text[i])>line_1_max):
                        line_1_max = len(text[i])
                if(i%2 == 0):
                    if(len(text[i])>line_2_max):
                        line_2_max = len(text[i])
            for i in range(len(text)):
                if(i%2 == 1):
                    if(len(text[i])<line_1_max):
                        for _ in range(line_1_max - len(text[i])):
                            text[i] = text[i] + " "
                if(i%2 == 0):
                    if(len(text[i])<line_2_max):
                        for _ in range(line_2_max - len(text[i])):
                            text[i] = text[i] + " "
        pass

    def encode_jp(self, s1: str) -> bytearray:
        result: bytearray = []
        count = 0
        for character in s1:
            if(character in jp_encoding):
                result.append(jp_encoding[character])
            else:
                count = count + 1
                result.append(jp_encoding["？"])
            if(count > 2):
                break
        return result

    def encode_jp_shop(self, s1: str) -> bytearray:
        result: bytearray = []
        count = 0
        for character in s1:
            if(character in jp_encoding):
                result.append(jp_encoding[character])
            else:
                if(count > 2):
                    result.append(jp_encoding[" "])
                else:
                    count = count + 1
                    result.append(jp_encoding["？"])
            #if(count > 2):
                #break
        return result

    def assemble_binary_array_for_dialog(self, s1: str, s2: str) -> bytearray:
        result: bytearray = []
        result.append(0x01)
        result.append(0x02)
        if(self.jp_version == False):
            result.extend(s1.encode("utf-8"))
            result.append(0x01)
            result.append(0x01)
            result.append(0x0a)
            s = "for "
            result.extend(s.encode("utf-8"))
            result.extend(s2.encode("utf-8"))
        else:
            result.extend(self.encode_jp_shop(s1))
            result.append(0x01)
            result.append(0x01)
            result.append(0x0a)
            result.extend(self.encode_jp_shop(s2))
        result.append(0x00)
        if(len(result) < 49):
            return result
        
        result = result[:47]
        result.append(0x00)

        return result

    def decode_booleans(self, val: int, bits: int):
        result = []
        for bit in range(bits):
            mask: int = 1 << bit
            result.append((val & mask) == mask)
        return result
    
    def decode_booleans_with_exclusions(self, val: int, bits: int, exclude: List[int]):
        result = []
        for bit in range(bits):
            if not bit in exclude:
                mask: int = 1 << bit
                result.append((val & mask) == mask)
        return result
    
    def update_list_of_received_items(self, ctx: "BizHawkClientContext"):
        result = []
        for i in range(len(ctx.items_received)):
            result.append(ctx.items_received[i][0])
        self.list_of_received_items = result
        pass

    async def update_max_hp(self, ctx: "BizHawkClientContext", item_count: int):
        curr_max_hp_bytes: bytes = (await bizhawk.read(
            ctx.bizhawk_ctx,
            [(0x078eb2 + (self.jp_version * -0xea0), 2, MAIN_RAM)]
        ))[0]
        curr_max_hp: int = int.from_bytes(curr_max_hp_bytes, byteorder='little')
        new_hp = ctx.slot_data["starting_hp"]
        mayor_berry = ctx.slot_data["quest_item_sanity"]
        for i in range(item_count):
            if(ctx.items_received[i][0] == 0x0ba21b + ((ctx.slot_data["set_lang"] == 2) * jp_id_offset)):
                new_hp += 25
        if(not mayor_berry and new_hp > ctx.slot_data["starting_hp"]):
            new_hp += 25
        max_hp = ctx.slot_data["starting_hp"]
        for i in range(len(ctx.items_received)):
            if(ctx.items_received[i][0] == 0x0ba21b + ((ctx.slot_data["set_lang"] == 2) * jp_id_offset)):
                max_hp += 25
        if(not mayor_berry):
            max_hp += 25
        max_hp = min(max_hp, 500)
        new_hp = min(new_hp, 500)
        if(curr_max_hp != new_hp and curr_max_hp != max_hp):
            await bizhawk.write(
                ctx.bizhawk_ctx,
                [(0x078eb2 + (self.jp_version * -0xea0), new_hp.to_bytes(2, 'little'), MAIN_RAM), #max hp
                (0x078eb4 + (self.jp_version * -0xea0), new_hp.to_bytes(2, 'little'), MAIN_RAM)] #current hp
            )

    async def update_legendary_armor(self, ctx: "BizHawkClientContext"):
        from CommonClient import logger
        #logger.info("updating legendary armor list")
        save_data: bytes = (await bizhawk.read(
            ctx.bizhawk_ctx,
            [(0x0ae64b + (self.jp_version * -0xea0), 2, MAIN_RAM)]
        ))[0]
        holdint = [save_data[0],save_data[1]]
        self.legendary_armor = self.decode_booleans_with_exclusions(int.from_bytes(holdint, byteorder='little'), 10, [0,1,2])
        #logger.info("lengendary armor %s",self.legendary_armor)
        pass
    
    async def update_inventory(self, ctx: "BizHawkClientContext"):
        #from CommonClient import logger
        #logger.info("updating inventory list")
        save_data: bytes = (await bizhawk.read(
            ctx.bizhawk_ctx,
            [(0x0ba1e7 + (self.jp_version * -0xea0), 12, MAIN_RAM)]
        ))[0]
        self.curr_inventory = list(save_data)
        #logger.info("inventory list %s", self.curr_inventory)
        pass

    async def update_progression(self, ctx: "BizHawkClientContext"):
        from CommonClient import logger
        #logger.info("updating inventory list")
        save_data: bytes = (await bizhawk.read(
            ctx.bizhawk_ctx,
            [(0x078e80 + (self.jp_version * -0xea0), 2, MAIN_RAM)]
        ))[0]
        self.progression_state = int.from_bytes(save_data, byteorder='little')
        #logger.info("progression state %x", self.progression_state)
        pass

    async def check_if_bracelet_needs_removed(self, ctx: "BizHawkClientContext"):
        from CommonClient import logger
        #logger.info("checking for extra bracelet")
        await self.update_legendary_armor(ctx)
        if(self.legendary_armor[4] == 1):
            await self.update_inventory(ctx)
            for i in range(len(self.curr_inventory)):
                if(self.curr_inventory[i] == 0x49 or self.curr_inventory[i] == 0x47):
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [((0x0ba1e7+i + (self.jp_version * -0xea0)), [0x0], MAIN_RAM)] 
                    )
                    if(self.message_level > 0):
                        logger.info("removing extra bracelet or glasses")
        pass

    async def remove_extra_legendary_armor_from_bakery(self, ctx: "BizHawkClientContext"):
        from CommonClient import logger
        #logger.info("checking for extra armor")
        await self.update_legendary_armor(ctx)
        if(self.legendary_armor[4] == 1):
            if(0x49 in self.bakery_inventory_expansion):
                self.bakery_inventory_expansion.remove(0x49)
                if(self.message_level > 0):
                    logger.info("removing extra bracelet from bakery")
        if(self.legendary_armor[5] == 1):
            if(0x4a in self.bakery_inventory_expansion):
                self.bakery_inventory_expansion.remove(0x4a)
                if(self.message_level > 0):
                    logger.info("removing extra old shirt from bakery")
        if(self.legendary_armor[6] == 1):
            if(0x4b in self.bakery_inventory_expansion):
                self.bakery_inventory_expansion.remove(0x4b)
                if(self.message_level > 0):
                    logger.info("removing extra red shoes from bakery")
        pass

    async def fill_restaurant_dialog(self, ctx: "BizHawkClientContext"):
        for i in range(7):
            loc_id = standard_location_name_to_id["Item 1 - Restaurant"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset)
            if(loc_id in ctx.locations_info):
                if(self.restaurant_checks[i]==True):
                    if(self.jp_version == False):
                        s = "Purchased"
                    else:
                        s = "かいもの"
                else:
                    s = ctx.item_names.lookup_in_slot(ctx.locations_info[loc_id].item, ctx.locations_info[loc_id].player)
                self.restaurant_dialog = self.restaurant_dialog + [s]
                s = ctx.player_names[ctx.locations_info[loc_id].player]
                self.restaurant_dialog = self.restaurant_dialog + [s]
            else:
                if(not standard_location_name_to_id["Item 1 - Restaurant"] + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset) in self.table_ids_to_hint):
                    for i in range(7):
                        self.table_ids_to_hint.append(standard_location_name_to_id["Item 1 - Restaurant"] + i + ((ctx.slot_data["set_lang"] - 1) * jp_id_offset))
                await ctx.send_msgs([{
                    "cmd": "LocationScouts",
                    "locations": self.table_ids_to_hint,
                    "create_as_hint": 0
                }])
                break
        self.fix_dialog(self.restaurant_dialog)
        pass
    async def assemble_binary_array_for_boss_textbox(self, ctx: "BizHawkClientContext", loc_id: int, length: int):
        result: bytearray = []
        if(self.jp_version == False):
            s = "<"+ctx.username+">"
            result = bytearray(s,"utf-8")
            result.append(0x0a)
            s = "Found "
            result.extend(s.encode("utf-8"))
            result.append(0x01)
            result.append(0x02)
            s = ctx.item_names.lookup_in_slot(ctx.locations_info[loc_id].item, ctx.locations_info[loc_id].player)
            result.extend(s.encode("utf-8"))
            result.append(0x01)
            result.append(0x01)
            s = " for "
            result.extend(s.encode("utf-8"))
            s = ctx.player_names[ctx.locations_info[loc_id].player]
            result.extend(s.encode("utf-8"))
        else:
            s = "ムサシは"
            result.extend(self.encode_jp(s))
            result.append(0x01)
            result.append(0x02)
            s = ctx.item_names.lookup_in_slot(ctx.locations_info[loc_id].item, ctx.locations_info[loc_id].player)
            result.extend(self.encode_jp(s))
            result.append(0x01)
            result.append(0x01)
            s = "をゲット！"
            result.extend(self.encode_jp(s))
        if(len(result) == length):
            return result
        elif(len(result) > length):
            result = result[:length]
        else:
            s = " " * (length - len(result))
            if(self.jp_version == False):
                result.extend(s.encode("utf-8"))
            else:
                result.extend(self.encode_jp(s))
        return result

    async def assemble_binary_array_for_textbox(self, ctx: "BizHawkClientContext", loc_id: int):
        if(self.jp_version == False):
            s = "<"+ctx.username+">"
            result = bytearray(s,"utf-8")
            result.append(0x0a)
            s = "Found "
            result.extend(s.encode("utf-8"))
            result.append(0x01)
            result.append(0x02)
            s = ctx.item_names.lookup_in_slot(ctx.locations_info[loc_id].item, ctx.locations_info[loc_id].player)
            result.extend(s.encode("utf-8"))
            result.append(0x01)
            result.append(0x01)
            s = " for "
            result.extend(s.encode("utf-8"))
            s = ctx.player_names[ctx.locations_info[loc_id].player]
            result.extend(s.encode("utf-8"))
        else:
            s = "ムサシは"
            result: bytearray = []
            result.extend(self.encode_jp(s))
            result.append(0x01)
            result.append(0x02)
            s = ctx.item_names.lookup_in_slot(ctx.locations_info[loc_id].item, ctx.locations_info[loc_id].player)
            result.extend(self.encode_jp(s))
            result.append(0x01)
            result.append(0x01)
            s = "をゲット！"
            result.extend(self.encode_jp(s))
        result.append(0x00)
        if(len(result) < 85):
            return result
        
        result = result[:83]
        result.append(0x00)

        return result

    async def assemble_short_binary_array_for_textbox(self, ctx: "BizHawkClientContext", loc_id: int):
        result = await self.assemble_binary_array_for_textbox(ctx,loc_id) 
        
        if(len(result) < 56):
            return result

        result: bytearray = []
        if(self.jp_version == False):
            s = "Found "
            result = bytearray(s,"utf-8")
            result.append(0x01)
            result.append(0x02)
            s = ctx.item_names.lookup_in_slot(ctx.locations_info[loc_id].item, ctx.locations_info[loc_id].player)
            result.extend(s.encode("utf-8"))
            result.append(0x01)
            result.append(0x01)
            s = " for "
            result.extend(s.encode("utf-8"))
            s = ctx.player_names[ctx.locations_info[loc_id].player]
            result.extend(s.encode("utf-8"))
        else:
            s = "ムサシは"
            result.extend(self.encode_jp(s))
            result.append(0x01)
            result.append(0x02)
            s = ctx.item_names.lookup_in_slot(ctx.locations_info[loc_id].item, ctx.locations_info[loc_id].player)
            result.extend(self.encode_jp(s))
            result.append(0x01)
            result.append(0x01)
            s = "をゲット！"
            result.extend(self.encode_jp(s))
        result.append(0x00)

        if(len(result) < 56):
            return result
        
        result = result[:54]
        result.append(0x00)

        return result

    async def assemble_binary_array_for_toyshop(self, ctx: "BizHawkClientContext", loc_id: int, max: int):

        result: bytearray = bytearray([2,0,0])
        result.append(0x01)
        result.append(0x02)
        s = ctx.item_names.lookup_in_slot(ctx.locations_info[loc_id].item, ctx.locations_info[loc_id].player)
        if(self.jp_version == False):
            result.extend(s.encode("utf-8"))
            result.append(0x01)
            result.append(0x01)
            result.append(0x0a)
            s = "for "
            result.extend(s.encode("utf-8"))
            s = ctx.player_names[ctx.locations_info[loc_id].player]
            result.extend(s.encode("utf-8"))
        else:
            result.extend(self.encode_jp(s))
            result.append(0x01)
            result.append(0x01)
            result.append(0x0a)
            s = ctx.player_names[ctx.locations_info[loc_id].player]
            result.extend(self.encode_jp(s))
        result.append(0x00)

        if(len(result) < max):
            return result
        
        result = result[:(max - 1)]
        result.append(0x00)

        return result

            