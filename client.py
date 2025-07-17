"""
A module containing the BizHawkClient base class and metaclass
"""

from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Any, ClassVar, List

from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch as launch_component

from .locations import location_table, location_name_groups, standard_location_name_to_id, sphere_one, location_base_id, table_ids_to_hint
from .dialog_locations import dialog_location_table, short_text_boxes
#if TYPE_CHECKING:
#    from .context import BizHawkClientContext
from .utils import Constants
from .version import __version__
from .hair_color import hair_color_addresses, default_hair_color, new_hair_color
from .items import npc_ids, item_id_to_name, item_name_to_id
from .store_info import bakery_locations, store_table, restaurant_pointers, restaurant_pointers_pointers, restaurant_locations, grocery_locations


from NetUtils import ClientStatus
from collections import Counter
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
    from NetUtils import JSONMessagePart

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
    

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        """Should return whether the currently loaded ROM should be handled by this client. You might read the game name
        from the ROM header, for example. This function will only be asked to validate ROMs from the system set by the
        client class, so you do not need to check the system yourself.

        Once this function has determined that the ROM should be handled by this client, it should also modify `ctx`
        as necessary (such as setting `ctx.game = self.game`, modifying `ctx.items_handling`, etc...)."""
        from CommonClient import logger
        logger.info("Attempting to validate rom")
        bfm_identifier_ram_address: int = 0x00ba94

        # = SLUS-00726MUSASHI in ASCII, code taken from AP Forbidden Memories
        bytes_expected: bytes = bytes.fromhex("534C55532D30303732364D555341534849")
        try:
            bytes_actual: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                bfm_identifier_ram_address, len(bytes_expected), MAIN_RAM
            )]))[0]
            if bytes_actual != bytes_expected:
                bytes_actual = (await bizhawk.read(ctx.bizhawk_ctx, [(
                    0x009f9a, len(bytes_expected), MAIN_RAM
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
                                return False
        except Exception:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b011
        ctx.want_slot_data = True
        #ctx.watcher_timeout = 0.125  # value taken from Forbiden Memories, taken from Pokemon Emerald's client
        ctx.watcher_timeout = 0.25  
        #self.random = Random()  # used for silly random deathlink messages
        logger.info(f"Brave Fencer Musashi Client v{__version__}. For updates:")
        logger.info("https://github.com/AegeusEvander/Brave-Fencer-Musashi-AP-World/releases")
        #logger.info(f"This Archipelago slot was generated with v{ctx.slot_data["version"]}")
        return True
    
    async def kill_player(self, ctx: "BizHawkClientContext") -> None:
        """sets player HP to 0"""
        # # Player HP at 078EB4 2 Bytes MAINRAM
        #     await bizhawk.write
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(PLAYER_CURR_HP_MEMORY, (0).to_bytes(2, "little"), MAIN_RAM)]
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
            game_state: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                0x0b99de, 1, MAIN_RAM
            )]))[0]
            if check_game_state != game_state:
                self.received_count = 0
                self.hair_color_updated = 0
                self.old_step_count = 0
                self.check_if_lumina_needs_removed = 1
                return
            #global bincho_checks
            from CommonClient import logger

            save_data: bytes = (await bizhawk.read(
                ctx.bizhawk_ctx,
                [(0x0ae671, 8, MAIN_RAM)]
            ))[0]
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

            save_data = (await bizhawk.read(
                ctx.bizhawk_ctx,
                [(0x0ae650, 2, MAIN_RAM)]
            ))[0]
            holdint = [save_data[0],save_data[1]]
            new_minku_checks = self.decode_booleans(int.from_bytes(holdint, byteorder='little'), 13)
            
            save_data: bytes = (await bizhawk.read(
                ctx.bizhawk_ctx,
                [(0x0ae651, 5, MAIN_RAM)]
            ))[0]
            holdint = [save_data[0],save_data[1],save_data[2],save_data[3]]
            new_chest_checks = self.decode_booleans_with_exclusions(int.from_bytes(holdint, byteorder='little'), 32, self.chest_indices_to_skip)
            #logger.info("What was read 0 in 0aae671 %s",self.bincho_checks)
            holdint = [save_data[4]]
            new_chest_checks.extend(self.decode_booleans(int.from_bytes(holdint, byteorder='little'), 7))

            locations_to_send_to_server = []
            #logger.info("What was read 1 in 0aae671 %s",new_bincho_checks)
            if(new_bincho_checks != self.bincho_checks):
                for i in range(len(new_bincho_checks)):
                    if(new_bincho_checks[i]):
                        locations_to_send_to_server.append(location_base_id + i)
                #logger.info("Sending Bincho checks")
                if(new_bincho_checks[0] == True and self.bincho_checks[0] == False):
                    #logger.info("Sending Guard bincho check")
                    self.update_list_of_received_items(ctx)
                    #logger.info("items receieved %s", self.list_of_received_items)
                    if(not item_name_to_id["Guard"] in self.list_of_received_items):
                        save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                            0x0ae666, 1, MAIN_RAM
                        )]))[0]
                        guard_state = int.from_bytes(save_data, byteorder='little')
                        if(guard_state & 0x1 == 0x1):
                            logger.info("Sending Macho back to Twinpeak")
                            guard_state = guard_state & 0xfe
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x0ae666, [guard_state], MAIN_RAM)]
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
                        locations_to_send_to_server.append(location_base_id + i + 35)
                #logger.info("What was read in 0ae671 %s",save_data)
                #logger.info("Trying to send %s",locations_to_send_to_server)

            if(new_chest_checks != self.chest_checks):
                for i in range(len(new_chest_checks)):
                    if(new_chest_checks[i]):
                        locations_to_send_to_server.append(location_base_id + i + 48)
            
            if(new_bakery_checks != self.bakery_checks):
                #logger.info("bakery checks %s", new_bakery_checks)
                for i in range(len(new_bakery_checks)):
                    if(new_bakery_checks[i]):
                        locations_to_send_to_server.append(location_base_id + i + 82)
                        if(i*2 < len(self.bakery_dialog)):
                            if(not "Purchased" in self.bakery_dialog[i*2]):
                                self.bakery_dialog[i*2] = "Purchased"
                                self.fix_dialog(self.bakery_dialog)

            if(new_restaurant_checks != self.restaurant_checks):
                #logger.info("bakery checks %s", new_bakery_checks)
                for i in range(len(new_restaurant_checks)):
                    if(new_restaurant_checks[i]):
                        locations_to_send_to_server.append(location_base_id + i + 89)
                        if(i*2 < len(self.restaurant_dialog)):
                            if(not "Purchased" in self.restaurant_dialog[i*2]):
                                self.restaurant_dialog[i*2] = "Purchased"
                                self.fix_dialog(self.restaurant_dialog)

            if(new_grocery_checks != self.grocery_checks):
                #logger.info("bakery checks %s", new_bakery_checks)
                for i in range(len(new_grocery_checks)):
                    if(new_grocery_checks[i]):
                        locations_to_send_to_server.append(standard_location_name_to_id["Item 1 - Grocery"] + i)
                        if(i*2 < len(self.grocery_dialog)):
                            if(not "Purchased" in self.grocery_dialog[i*2]):
                                self.grocery_dialog[i*2] = "Purchased"
                                self.fix_dialog(self.grocery_dialog)

            if(new_bincho_checks != self.bincho_checks or new_minku_checks != self.minku_checks or new_chest_checks != self.chest_checks or new_bakery_checks != self.bakery_checks or new_restaurant_checks != self.restaurant_checks or new_grocery_checks != self.grocery_checks):
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": locations_to_send_to_server
                }])
                self.bincho_checks = new_bincho_checks
                self.minku_checks = new_minku_checks
                self.chest_checks = new_chest_checks
                self.bakery_checks = new_bakery_checks
                self.restaurant_checks = new_restaurant_checks
                self.grocery_checks = new_grocery_checks

            
            curr_location_data: bytes = (await bizhawk.read(
                ctx.bizhawk_ctx,
                [(0x0b9a08, 2, MAIN_RAM)]
            ))[0]
            curr_location = int.from_bytes(curr_location_data,byteorder='little')
            if(curr_location == 0x3005): #main menu/first moon cutscene
                self.level_transition = 1
            if(curr_location == 0x3012): #waking up from nightmare
                self.level_transition = 1
                self.received_count = 0
                self.old_step_count = 0
                self.death_link_timer = 240
                self.has_died = 0
                self.check_if_lumina_needs_removed = 1
                curr_hp_bytes: bytes = (await bizhawk.read(
                    ctx.bizhawk_ctx,
                    [(0x078eb4, 2, MAIN_RAM)]
                ))[0]
                curr_hp: int = int.from_bytes(curr_hp_bytes, byteorder='little')
                if curr_hp < 5:
                    new_hp = 150
                    await bizhawk.write(
                        ctx.bizhawk_ctx,
                        [(0x078eb4, new_hp.to_bytes(2, 'little'), MAIN_RAM)]
                    )   

            #logger.info("curr_location %s",curr_location)
            #logger.info("in Town")
            #if(curr_location == 4112 or curr_location == 4178):
            #not save menu
            #if(curr_location != 12296):

            received_list: List[int] = [received_item[0] for received_item in ctx.items_received]
            if(self.old_step_count != 0 and self.level_transition != 1):
                if(self.received_count < len(ctx.items_received)):
                    #logger.info("list %s",ctx.items_received[self.received_count])
                    item_id = ctx.items_received[self.received_count][0]
                    #logger.info("list %s",item_id)
                    if(item_id>0x0ba1f7 and item_id<0x0ba21b):
                        npc_state: bytes = (await bizhawk.read(
                            ctx.bizhawk_ctx,
                            [(item_id, 1, MAIN_RAM)]
                        ))[0]
                        if(npc_state[0] == 0b0):
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(item_id, [0b1], MAIN_RAM)]
                            )
                            logger.info("adding to rescue list %s",item_id_to_name[item_id])
                            #logger.info("IDs of receieved items %s",set(received_list))
                            #logger.info("IDs of all NPCs %s",set(npc_ids))
                        else:
                            logger.info("already in rescue list: %s",item_id_to_name[item_id])
                        if(item_id == item_name_to_id["Guard"]):
                            save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                0x0ae666, 1, MAIN_RAM
                            )]))[0]
                            guard_state = int.from_bytes(save_data, byteorder='little')
                            if(guard_state & 0x1 == 0x0):
                                logger.info("Sending Guard to Twinpeak")
                                guard_state = guard_state | 0x1
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x0ae666, [guard_state], MAIN_RAM)]
                                )
                    elif(item_id==0x0ba21b): #found max health berry
                        curr_max_hp_bytes: bytes = (await bizhawk.read(
                            ctx.bizhawk_ctx,
                            [(0x078eb2, 2, MAIN_RAM)]
                        ))[0]
                        curr_max_hp: int = int.from_bytes(curr_max_hp_bytes, byteorder='little')
                        new_hp = 175
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
                            )#current hp
                    elif(item_id == 0xa):
                        if(ctx.slot_data["grocery_s_revive"] == True):
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x10ee64, [0x1e, 0, 0x1e, 0], MAIN_RAM)]
                            )#lower s-revive price
                    elif(item_id < 0x6a and item_id > 0x12):
                        if(not item_id in self.bakery_inventory_expansion):
                            self.bakery_inventory_expansion.append(item_id)
                    elif(item_id == 0x78):
                        curr_money_bytes: bytes = (await bizhawk.read(
                            ctx.bizhawk_ctx,
                            [(0x078e8C, 4, MAIN_RAM)]
                        ))[0]
                        curr_money: int = int.from_bytes(curr_money_bytes, byteorder='little')
                        new_money = curr_money
                        num_boons_byte: bytes = (await bizhawk.read(
                            ctx.bizhawk_ctx,
                            [(0x0ba246, 1, MAIN_RAM)]
                        ))[0]
                        num_boons: int = int.from_bytes(num_boons_byte, byteorder='little')
                        boon_count = 0
                        for i in range(self.received_count+1):
                            if(ctx.items_received[i][0] == 0x78):
                                boon_count += 1
                                if(boon_count > num_boons):
                                    new_money += 100
                        if(curr_money < new_money):
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x078e8C, new_money.to_bytes(4, 'little'), MAIN_RAM)]
                            )
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x0ba246, boon_count.to_bytes(1, 'little'), MAIN_RAM)]  #0x0ba238 is queen ant toy, maybe 0x0ba246
                            )
                            logger.info("added 1000 Drans to wallet")
                    elif(item_id == 0x79):
                        logger.info("Returning Lumina")
                        save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                            0x0ae658, 1, MAIN_RAM
                        )]))[0]
                        lumina_state = int.from_bytes(save_data, byteorder='little')
                        lumina_state = lumina_state | 0b1
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x0ae658, [lumina_state], MAIN_RAM)]
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
                        logger.info("New stock added to Bakery")
                    elif(item_id < 0x78 and item_id > 0x70):
                        logger.info("%s added to Restaurant",item_id_to_name[item_id])
                    elif(item_id < 0xc or item_id == 0x6a or item_id == 0x6b or item_id== 0x6d):
                        logger.info("%s added to Grocery",item_id_to_name[item_id])
                    else:
                        logger.info("unhandled item receieved %s",item_id_to_name[item_id])
                    self.received_count += 1
            if(self.hair_color_updated == 0):
                curr_hair_color: bytes = (await bizhawk.read(
                    ctx.bizhawk_ctx,
                    [(hair_color_addresses[0], 3, MAIN_RAM)]
                ))[0]
                if(curr_hair_color == bytes.fromhex(ctx.slot_data["hair_color"])):
                    self.hair_color_updated = 1
                else:
                    logger.info("Coloring Hair")
                    for address in hair_color_addresses:
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(address, bytes.fromhex(ctx.slot_data["hair_color"]), MAIN_RAM)]
                        )
        
            if(curr_location != self.old_location):
                steps_bytes: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                    0x078E7C, 4, MAIN_RAM #replaced by timer (for steps0x078F08, 4, MAIN_RAM)
                )]))[0]
                step_count = int.from_bytes(steps_bytes,byteorder='little')
                if(self.level_transition == 0 or curr_location == 0x3005):
                    self.old_step_count = step_count
                    self.level_transition = 1
                elif(self.old_step_count != step_count):
                    self.old_location = curr_location
                    self.level_transition = 0
                    self.check_for_logs = 0
                    if(curr_location in dialog_location_table):
                        for loc_id, dialog_id in dialog_location_table[curr_location].items():
                            if(loc_id in ctx.locations_info):
                                if(loc_id in short_text_boxes):
                                    barray = await self.assemble_short_binary_array_for_textbox(ctx, loc_id)
                                else:
                                    barray = await self.assemble_binary_array_for_textbox(ctx, loc_id)
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(dialog_id+4, barray, MAIN_RAM)]
                                )
                            else:
                                logger.info("no scout information found try reentering area (after taking a couple steps)")
                                await ctx.send_msgs([{
                                    "cmd": "LocationScouts",
                                    "locations": table_ids_to_hint,
                                    "create_as_hint": 0
                                }])
                                break
                    if(curr_location in bakery_locations): # 0x2015chapter 2 Jam, also changes to 0x2056 chapter 3

                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x11514A, [0x0], MAIN_RAM)]
                        )
                        if(curr_location == 0x207b or curr_location == 0x2098):
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
                        await self.update_progression(ctx)
                        if(ctx.slot_data["bakery_sanity"] == True):
                            self.update_list_of_received_items(ctx)
                            self.bakery_dialog = []
                            self.cursor_pos = -1


                            for i in range(len(self.bakery_inventory_sanity)):
                                loc_id = standard_location_name_to_id["Item 1 - Bakery"] + i
                                if(loc_id in ctx.locations_info):
                                    if(self.bakery_checks[i]==True):
                                        s = "Purchased"
                                    else:
                                        s = ctx.item_names.lookup_in_slot(ctx.locations_info[loc_id].item, ctx.locations_info[loc_id].player)
                                    self.bakery_dialog = self.bakery_dialog + [s]
                                    s = ctx.player_names[ctx.locations_info[loc_id].player]
                                    self.bakery_dialog = self.bakery_dialog + [s]
                                else:
                                    if(not standard_location_name_to_id["Item 1 - Bakery"] in table_ids_to_hint):
                                        for i in range(7):
                                            table_ids_to_hint.append(standard_location_name_to_id["Item 1 - Bakery"] + i)
                                    #logger.info("no scout information found try reentering area (after taking a couple steps) %s", table_ids_to_hint)
                                    #logger.info("item 7 id %s", standard_location_name_to_id["Item 7 - Bakery"])
                                    await ctx.send_msgs([{
                                        "cmd": "LocationScouts",
                                        "locations": table_ids_to_hint,
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
                            if(item_name_to_id["Progressive Bread"] in self.list_of_received_items):
                                bread_to_add = self.bakery_inventory_default[:self.list_of_received_items.count(item_name_to_id["Progressive Bread"])]
                            
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

                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(store_table[curr_location].inventory_id, self.bakery_inventory, MAIN_RAM)]
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(store_table[curr_location].inventory_length_id, [len(self.bakery_inventory)], MAIN_RAM)]
                        )
                        if(store_table[curr_location].inventory_length_id_expanded):
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(store_table[curr_location].inventory_length_id_expanded, [len(self.bakery_inventory)], MAIN_RAM)]
                            )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(store_table[curr_location].inventory_pointer_upper_pointer, store_table[curr_location].inventory_pointer_upper, MAIN_RAM)] #somehow coresponds to 0x801f
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(store_table[curr_location].inventory_pointer_lower_pointer, store_table[curr_location].inventory_pointer_lower, MAIN_RAM)]
                        )
                    if(curr_location in restaurant_locations):
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x11514A, [0x0], MAIN_RAM)]
                        )
                        #logger.info("entered restaurant")
                        if(ctx.slot_data["restaurant_sanity"] == True):
                            if(False in self.restaurant_checks or not set(received_list).issuperset(set(self.restaurant_inventory_default))):
                                self.update_list_of_received_items(ctx)
                                self.restaurant_dialog = []
                                self.cursor_pos = -1

                                for i in range(7):
                                    loc_id = standard_location_name_to_id["Item 1 - Restaurant"] + i
                                    if(loc_id in ctx.locations_info):
                                        if(self.restaurant_checks[i]==True):
                                            s = "Purchased"
                                        else:
                                            s = ctx.item_names.lookup_in_slot(ctx.locations_info[loc_id].item, ctx.locations_info[loc_id].player)
                                        self.restaurant_dialog = self.restaurant_dialog + [s]
                                        s = ctx.player_names[ctx.locations_info[loc_id].player]
                                        self.restaurant_dialog = self.restaurant_dialog + [s]
                                    else:
                                        if(not standard_location_name_to_id["Item 1 - Restaurant"] in table_ids_to_hint):
                                            for i in range(7):
                                                table_ids_to_hint.append(standard_location_name_to_id["Item 1 - Restaurant"] + i)
                                        await ctx.send_msgs([{
                                            "cmd": "LocationScouts",
                                            "locations": table_ids_to_hint,
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
                                    restaurant_dialog_pointers = restaurant_dialog_pointers + restaurant_pointers[curr_location][self.restaurant_inventory[i]]

                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(store_table[curr_location].inventory_id, self.restaurant_inventory, MAIN_RAM)]
                                )
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(store_table[curr_location].inventory_length_id, [len(self.restaurant_inventory)], MAIN_RAM)]
                                )
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(restaurant_pointers_pointers[curr_location], restaurant_dialog_pointers, MAIN_RAM)]
                                )
                    if(curr_location in grocery_locations): # 0x2015chapter 2 Jam, also changes to 0x2056 chapter 3
                        if(ctx.slot_data["grocery_sanity"] == True):
                            await self.update_progression(ctx)
                            self.update_list_of_received_items(ctx)
                            self.grocery_dialog = []
                            self.cursor_pos = -1
                            
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x11514A, [0x0], MAIN_RAM)] #set cursor to zero incase it is greater than the current index
                            )
                            if(len(self.grocery_inventory_sanity)<12 or 0 in self.grocery_inventory_sanity):
                                save_data: bytes = (await bizhawk.read(
                                    ctx.bizhawk_ctx,
                                    [(0x0BA202, 1, MAIN_RAM)]
                                ))[0]
                                rice_ball = 0
                                rice_state = int.from_bytes(save_data, byteorder='little')
                                if(rice_state == 0x4):
                                    logger.info("rice ball item available")
                                    rice_ball = 1
                                save_data: bytes = (await bizhawk.read(
                                    ctx.bizhawk_ctx,
                                    [(0x0BA213, 1, MAIN_RAM)]
                                ))[0]
                                neatball = 0
                                neatball_state = int.from_bytes(save_data, byteorder='little')
                                if(neatball_state == 0x3):
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
                                if(self.progression_state >= 0x12c):
                                    if(len(self.grocery_inventory_sanity) < 11): #no Riceball or Neatball yet
                                        self.grocery_inventory_sanity = self.grocery_inventory_sanity + [0x42]
                                        self.grocery_inventory_default = self.grocery_inventory_default + [0xb]
                                    else: #have either Riceball or Neatball
                                        self.grocery_inventory_sanity[7] = 0x42
                                        self.grocery_inventory_default = self.grocery_inventory_default[:7] + [0xb] + self.grocery_inventory_default[7:]

                            if(curr_location == 0x207c or curr_location == 0x2099): #Chapter 4/5/6
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
                                loc_id = standard_location_name_to_id["Item 1 - Grocery"] + i
                                if(loc_id in ctx.locations_info):
                                    if(self.grocery_checks[i]==True):
                                        s = "Purchased"
                                    else:
                                        s = ctx.item_names.lookup_in_slot(ctx.locations_info[loc_id].item, ctx.locations_info[loc_id].player)
                                    self.grocery_dialog = self.grocery_dialog + [s]
                                    s = ctx.player_names[ctx.locations_info[loc_id].player]
                                    self.grocery_dialog = self.grocery_dialog + [s]
                                else:
                                    if(not standard_location_name_to_id["Item 1 - Grocery"] in table_ids_to_hint):
                                        for i in range(12):
                                            table_ids_to_hint.append(standard_location_name_to_id["Item 1 - Grocery"] + i)
                                    #logger.info("no scout information found try reentering area (after taking a couple steps) %s", table_ids_to_hint)
                                    #logger.info("item 7 id %s", standard_location_name_to_id["Item 7 - Bakery"])
                                    await ctx.send_msgs([{
                                        "cmd": "LocationScouts",
                                        "locations": table_ids_to_hint,
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
                            #logger.info("inventory after after final adds grocery to add %s", self.grocery_inventory)
                        
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(store_table[curr_location].inventory_id, self.grocery_inventory, MAIN_RAM)]
                            )
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(store_table[curr_location].inventory_length_id, [len(self.grocery_inventory)]*8, MAIN_RAM)]
                            )
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(store_table[curr_location].inventory_pointer_upper_pointer, store_table[curr_location].inventory_pointer_upper, MAIN_RAM)] #somehow coresponds to 0x801f
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
                    elif(curr_location == 0x2018): #chapter 2 Conners
                        await self.check_if_bracelet_needs_removed(ctx)
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x18c630, [0x9, 0x0], MAIN_RAM)] #andi $v0 $s0 0x4000 to andi $v0 $s0 0x09
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x18c578, [0x9, 0x0], MAIN_RAM)] #andi $v0 $s0 0x4000 to andi $v0 $s0 0x09
                        )
                    elif(curr_location == 0x2059): #chapter 3 Conners
                        await self.check_if_bracelet_needs_removed(ctx)
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x1891e0, [0x9, 0x0], MAIN_RAM)] #andi $v0 $s0 0x4000 to andi $v0 $s0 0x09
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x189298, [0x9, 0x0], MAIN_RAM)] #andi $v0 $s0 0x4000 to andi $v0 $s0 0x09
                        )
                    elif(curr_location == 0x207e): #chapter 4 Conners
                        await self.check_if_bracelet_needs_removed(ctx)
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x189ab8, [0x9, 0x0], MAIN_RAM)] #andi $v0 $s0 0x4000 to andi $v0 $s0 0x09
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x189b70, [0x9, 0x0], MAIN_RAM)] #andi $v0 $s0 0x4000 to andi $v0 $s0 0x09
                        )
                    elif(curr_location == 0x209b): #chapter 5 Conners
                        await self.check_if_bracelet_needs_removed(ctx)
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x1897b8, [0x9, 0x0], MAIN_RAM)] #andi $v0 $s0 0x4000 to andi $v0 $s0 0x09
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x189870, [0x9, 0x0], MAIN_RAM)] #andi $v0 $s0 0x4000 to andi $v0 $s0 0x09
                        )
                    elif(curr_location == 0x3029): #twinpeak second peak
                        await self.update_progression(ctx)
                        if(self.progression_state > 0x59): #Jon has left the peak
                            save_data: bytes = (await bizhawk.read(
                                ctx.bizhawk_ctx,
                                [(0x0ae65a, 1, MAIN_RAM)]
                            ))[0]
                            raft_state = int.from_bytes(save_data, byteorder='little')
                            if(raft_state & 0b11000000 != 0b11000000):
                                logger.info("Raft incomplete, checking for logs")
                                self.check_for_logs = 1

                self.old_step_count = step_count

            if(self.level_transition == 0):
                if(curr_location == 0x3060 or curr_location == 0x3062 or curr_location == 0x305d or curr_location == 0x305e or curr_location == 0x3063):
                    self.counter_for_delayed_check += 1
                    if(self.counter_for_delayed_check>9):
                        self.counter_for_delayed_check = 0
                        if(curr_location in dialog_location_table):
                            for loc_id, dialog_id in dialog_location_table[curr_location].items():
                                if(loc_id in ctx.locations_info):
                                    if(loc_id in short_text_boxes):
                                        barray = await self.assemble_short_binary_array_for_textbox(ctx, loc_id)
                                    else:
                                        barray = await self.assemble_binary_array_for_textbox(ctx, loc_id)
                                    await bizhawk.write(
                                        ctx.bizhawk_ctx,
                                        [(dialog_id+4, barray, MAIN_RAM)]
                                    )
                elif(curr_location == 0x3029 and self.check_for_logs): #Twinpeak second peak check if raft needs updated
                    self.counter_for_delayed_check += 1
                    if(self.counter_for_delayed_check>19):
                        self.counter_for_delayed_check = 0
                        await self.update_inventory(ctx)
                        if(0x4e in self.curr_inventory and 0x50 in self.curr_inventory and 0x51 in self.curr_inventory and 0x52 in self.curr_inventory):
                            logger.info("Raft complete, removing Logs")
                            self.check_for_logs = 0
                            save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                0x0ae65a, 1, MAIN_RAM
                            )]))[0]
                            raft_state = int.from_bytes(save_data, byteorder='little')
                            raft_state = raft_state | 0b11000000
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x0ae65a, [raft_state], MAIN_RAM)]
                            )
                            for i in range(len(self.curr_inventory)):
                                if(self.curr_inventory[i] in [0x4d,0x4e,0x50,0x51,0x52]): #Jon's key and four logs
                                    await bizhawk.write(
                                        ctx.bizhawk_ctx,
                                        [((0x0ba1e7+i), [0x0], MAIN_RAM)] 
                                    )
                if(self.check_if_lumina_was_found):
                    if(ctx.slot_data["lumina_randomzied"] == True):
                        save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                            0x0ae658, 1, MAIN_RAM
                        )]))[0]
                        lumina_state = int.from_bytes(save_data, byteorder='little')
                        lumina_state = lumina_state & 0b1
                        if(lumina_state == 1):
                            self.check_if_lumina_was_found = 0
                            await ctx.send_msgs([{
                                "cmd": "LocationChecks",
                                "locations": [standard_location_name_to_id["Lumina - Spiral Tower"]]
                            }])
                    else:
                        self.check_if_lumina_was_found = 0

                if(self.check_if_lumina_needs_removed):
                    if(ctx.slot_data["lumina_randomzied"] == True):
                        self.update_list_of_received_items(ctx)
                        if(curr_location < 0x3000 or curr_location > 0x300f): #check if past chapter 1
                            if(not item_name_to_id["Lumina"] in self.list_of_received_items):
                                logger.info("Yeeting Lumina")
                                save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                    0x0ae658, 1, MAIN_RAM
                                )]))[0]
                                lumina_state = int.from_bytes(save_data, byteorder='little')
                                lumina_state = lumina_state & 0b11111110
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x0ae658, [lumina_state], MAIN_RAM)]
                                )
                                save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                    0x078ec0, 1, MAIN_RAM
                                )]))[0]
                                lumina_state = int.from_bytes(save_data, byteorder='little')
                                lumina_state = lumina_state & 0b11111110
                                await bizhawk.write(
                                    ctx.bizhawk_ctx,
                                    [(0x078ec0, [lumina_state], MAIN_RAM)]
                                )
                                self.check_if_lumina_needs_removed = 0
                            else:
                                self.check_if_lumina_needs_removed = 0
                    else:
                        self.check_if_lumina_needs_removed = 0
                if(ctx.slot_data["bakery_sanity"] == True or ctx.slot_data["restaurant_sanity"] == True):
                    if(curr_location in bakery_locations or curr_location in restaurant_locations):
                        if(len(self.bakery_dialog)>0 or len(self.restaurant_dialog)>0):
                            if(False in self.bakery_checks or False in self.restaurant_checks):
                                save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                    0x11514A, 1, MAIN_RAM
                                )]))[0]
                                new_cursor_pos = int.from_bytes(save_data, byteorder='little')

                                save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                    0x115130, 1, MAIN_RAM
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

                if(ctx.slot_data["grocery_sanity"] == True):
                    if(curr_location in grocery_locations):
                        if(len(self.grocery_dialog)>0):
                            if(False in self.grocery_checks):
                                save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                    0x11514A, 1, MAIN_RAM
                                )]))[0]
                                new_cursor_pos = int.from_bytes(save_data, byteorder='little')

                                save_data: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                                    0x115130, 1, MAIN_RAM
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
                                        elif(self.grocery_inventory[self.cursor_pos]==0x0):
                                            await bizhawk.write(
                                                ctx.bizhawk_ctx,
                                                [(0x115130, [0xe8], MAIN_RAM)] #clear text box
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
            if not ctx.finished_game and set(received_list).issuperset(set(npc_ids)):
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])
            
            if (self.request_hints == 0):
                self.request_hints = 1 
                if(ctx.slot_data["bakery_sanity"] == True):
                    if(not standard_location_name_to_id["Item 1 - Bakery"] in table_ids_to_hint):
                        for i in range(7):
                            table_ids_to_hint.append(standard_location_name_to_id["Item 1 - Bakery"] + i)
                if(ctx.slot_data["restaurant_sanity"] == True):
                    if(not standard_location_name_to_id["Item 1 - Restaurant"] in table_ids_to_hint):
                        for i in range(7):
                            table_ids_to_hint.append(standard_location_name_to_id["Item 1 - Restaurant"] + i)
                if(ctx.slot_data["grocery_sanity"] == True):
                    if(not standard_location_name_to_id["Item 1 - Grocery"] in table_ids_to_hint):
                        for i in range(12):
                            table_ids_to_hint.append(standard_location_name_to_id["Item 1 - Grocery"] + i)
                await ctx.send_msgs([{
                    "cmd": "LocationScouts",
                    "locations": table_ids_to_hint,
                    "create_as_hint": 0
                }])

            if(ctx.slot_data["deathlink"]):
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
                        [(PLAYER_CURR_HP_MEMORY, 2, MAIN_RAM)]
                    ))[0]
                    curr_hp: int = int.from_bytes(curr_hp_bytes, byteorder='little')
                    if curr_hp == 0 and self.has_died == 0:
                        self.has_died = 1
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

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        """For handling packages from the server. Called from `BizHawkClientContext.on_package`."""
        pass


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

    def assemble_binary_array_for_dialog(self, s1: str, s2: str):
        result: bytearray = []
        result.append(0x01)
        result.append(0x02)
        result.extend(s1.encode("utf-8"))
        result.append(0x01)
        result.append(0x01)
        result.append(0x0a)
        s = "for "
        result.extend(s.encode("utf-8"))
        result.extend(s2.encode("utf-8"))
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

    async def update_legendary_armor(self, ctx: "BizHawkClientContext"):
        from CommonClient import logger
        #logger.info("updating legendary armor list")
        save_data: bytes = (await bizhawk.read(
            ctx.bizhawk_ctx,
            [(0x0ae64b, 2, MAIN_RAM)]
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
            [(0x0ba1e7, 12, MAIN_RAM)]
        ))[0]
        self.curr_inventory = list(save_data)
        #logger.info("inventory list %s", self.curr_inventory)
        pass

    async def update_progression(self, ctx: "BizHawkClientContext"):
        from CommonClient import logger
        #logger.info("updating inventory list")
        save_data: bytes = (await bizhawk.read(
            ctx.bizhawk_ctx,
            [(0x078e80, 2, MAIN_RAM)]
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
                        [((0x0ba1e7+i), [0x0], MAIN_RAM)] 
                    )
                    logger.info("removing extra bracelet or glasses")
        pass

    async def remove_extra_legendary_armor_from_bakery(self, ctx: "BizHawkClientContext"):
        from CommonClient import logger
        #logger.info("checking for extra armor")
        await self.update_legendary_armor(ctx)
        if(self.legendary_armor[4] == 1):
            if(0x49 in self.bakery_inventory_expansion):
                self.bakery_inventory_expansion.remove(0x49)
                logger.info("removing extra bracelet from bakery")
        if(self.legendary_armor[5] == 1):
            if(0x4a in self.bakery_inventory_expansion):
                self.bakery_inventory_expansion.remove(0x4a)
                logger.info("removing extra old shirt from bakery")
        if(self.legendary_armor[6] == 1):
            if(0x4b in self.bakery_inventory_expansion):
                self.bakery_inventory_expansion.remove(0x4b)
                logger.info("removing extra red shoes from bakery")
        pass

    async def fill_restaurant_dialog(self, ctx: "BizHawkClientContext"):
        for i in range(7):
            loc_id = standard_location_name_to_id["Item 1 - Restaurant"] + i
            if(loc_id in ctx.locations_info):
                if(self.restaurant_checks[i]==True):
                    s = "Purchased"
                else:
                    s = ctx.item_names.lookup_in_slot(ctx.locations_info[loc_id].item, ctx.locations_info[loc_id].player)
                self.restaurant_dialog = self.restaurant_dialog + [s]
                s = ctx.player_names[ctx.locations_info[loc_id].player]
                self.restaurant_dialog = self.restaurant_dialog + [s]
            else:
                if(not standard_location_name_to_id["Item 1 - Restaurant"] in table_ids_to_hint):
                    for i in range(7):
                        table_ids_to_hint.append(standard_location_name_to_id["Item 1 - Restaurant"] + i)
                await ctx.send_msgs([{
                    "cmd": "LocationScouts",
                    "locations": table_ids_to_hint,
                    "create_as_hint": 0
                }])
                break
        self.fix_dialog(self.restaurant_dialog)
        pass

    async def assemble_binary_array_for_textbox(self, ctx: "BizHawkClientContext", loc_id: int):
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
        result.append(0x00)
        return result

    async def assemble_short_binary_array_for_textbox(self, ctx: "BizHawkClientContext", loc_id: int):
        result = await self.assemble_binary_array_for_textbox(ctx,loc_id) 
        
        if(len(result) < 56):
            return result

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
        result.append(0x00)

        if(len(result) < 56):
            return result
        
        result = result[:54]
        result.append(0x00)

        return result

            