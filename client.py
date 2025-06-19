"""
A module containing the BizHawkClient base class and metaclass
"""

from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Any, ClassVar, List

from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch as launch_component

from .locations import location_table, location_name_groups, standard_location_name_to_id, sphere_one, location_base_id, table_ids_to_hint
from .dialog_locations import dialog_location_table
#if TYPE_CHECKING:
#    from .context import BizHawkClientContext
from .utils import Constants
from .version import __version__
from .hair_color import hair_color_addresses, default_hair_color, new_hair_color
from .items import npc_ids, item_id_to_name


from NetUtils import ClientStatus
from collections import Counter
import worlds._bizhawk as bizhawk
from worlds._bizhawk.client import BizHawkClient

if TYPE_CHECKING:
    from worlds._bizhawk.context import BizHawkClientContext
    from NetUtils import JSONMessagePart

MAIN_RAM: typing.Final[str] = "MainRAM"
PLAYER_LIFE_POINTS_SHORT_OFFSET: typing.Final[int] = 0x078EB4

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
    chest_indices_to_skip = [0, 1, 2, 3, 4, 25]
    bakery_inventory = [0x53,0xd,0xe,0xf,0x10]
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
        return True
    
    async def kill_player(self, ctx: "BizHawkClientContext") -> None:
        """Return True if this method thinks it actually killed the player, False otherwise"""
        # # Player HP at 078EB4 2 Bytes MAINRAM
        #     await bizhawk.write
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(PLAYER_LIFE_POINTS_SHORT_OFFSET, (0).to_bytes(2, "little"), MAIN_RAM)]
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
                return
            #global bincho_checks
            from CommonClient import logger

            save_data: bytes = (await bizhawk.read(
                ctx.bizhawk_ctx,
                [(0x0ae671, 5, MAIN_RAM)]
            ))[0]
            holdint = [save_data[0],save_data[1],save_data[2],save_data[3]]
            new_bincho_checks = self.decode_booleans(int.from_bytes(holdint, byteorder='little'), 32)
            #logger.info("What was read 0 in 0aae671 %s",self.bincho_checks)
            holdint = [save_data[4]]
            new_bincho_checks.extend(self.decode_booleans(int.from_bytes(holdint, byteorder='little'), 3))

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
            

            if(new_bincho_checks != self.bincho_checks or new_minku_checks != self.minku_checks or new_chest_checks != self.chest_checks):
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": locations_to_send_to_server
                }])
                self.bincho_checks = new_bincho_checks
                self.minku_checks = new_minku_checks
                self.chest_checks = new_chest_checks

            
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
            if self.death_link_timer > 0 and self.has_died == 0:
                self.death_link_timer -= 1
                if self.death_link_timer == 0:
                    logger.info("death link grace period has ended")

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
                    elif(item_id < 0x78):
                        if(not item_id in self.bakery_inventory):
                            self.bakery_inventory.append(item_id)
                    elif(item_id == 0x78):
                        curr_money_bytes: bytes = (await bizhawk.read(
                            ctx.bizhawk_ctx,
                            [(0x078e8C, 4, MAIN_RAM)]
                        ))[0]
                        curr_money: int = int.from_bytes(curr_money_bytes, byteorder='little')
                        new_money = curr_money
                        num_boons_byte: bytes = (await bizhawk.read(
                            ctx.bizhawk_ctx,
                            [(0x0ba238, 1, MAIN_RAM)]
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
                                [(0x0ba238, boon_count.to_bytes(1, 'little'), MAIN_RAM)]
                            )
                            logger.info("added 1000 Drans to wallet")
                    else:
                        logger.info("unhandled item receieved %s",item_id)
                    self.received_count += 1
            if(self.hair_color_updated == 0):
                curr_hair_color: bytes = (await bizhawk.read(
                    ctx.bizhawk_ctx,
                    [(hair_color_addresses[0], 3, MAIN_RAM)]
                ))[0]
                if(curr_hair_color == bytes.fromhex(ctx.slot_data["h"])):
                    self.hair_color_updated = 1
                else:
                    logger.info("Coloring Hair")
                    for address in hair_color_addresses:
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(address, bytes.fromhex(ctx.slot_data["h"]), MAIN_RAM)]
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
                    if(curr_location in dialog_location_table):
                        for loc_id, dialog_id in dialog_location_table[curr_location].items():
                            if(loc_id in ctx.locations_info):
                                s = "<"+ctx.username+">"
                                barray = bytearray(s,"utf-8")
                                barray.append(0x0a)
                                s = "Found "
                                barray.extend(s.encode("utf-8"))
                                barray.append(0x01)
                                barray.append(0x02)
                                s = ctx.item_names.lookup_in_slot(ctx.locations_info[loc_id].item, ctx.locations_info[loc_id].player)
                                #logger.info("found scout item")# %s",s)
                                barray.extend(s.encode("utf-8"))
                                barray.append(0x01)
                                barray.append(0x01)
                                s = " for "
                                barray.extend(s.encode("utf-8"))
                                s = ctx.player_names[ctx.locations_info[loc_id].player]
                                barray.extend(s.encode("utf-8"))
                                barray.append(0x00)
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
                    if(curr_location == 0x2015): #chapter 2 Jam, also changes to 0x2056 chapter 3
                        await self.remove_extra_legendary_armor_from_bakery(ctx)
                        logger.info("bakery inventory %s",self.bakery_inventory)
                        #logger.info("bakery inventory bytes %s",bytes(self.bakery_inventory))
                        logger.info("bakery inventory len %s",len(self.bakery_inventory))
                        #logger.info("bakery inventory len bytes %s",bytes(len(self.bakery_inventory)))
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x1fab10, self.bakery_inventory, MAIN_RAM)]
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x189aa0, [len(self.bakery_inventory)], MAIN_RAM)]
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x189ab0, [len(self.bakery_inventory)], MAIN_RAM)]
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
                        logger.info("bakery inventory %s",self.bakery_inventory)
                        #logger.info("bakery inventory bytes %s",bytes(self.bakery_inventory))
                        logger.info("bakery inventory len %s",len(self.bakery_inventory))
                        #logger.info("bakery inventory len bytes %s",bytes(len(self.bakery_inventory)))
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x1fab10, self.bakery_inventory, MAIN_RAM)]
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x186718, [len(self.bakery_inventory)], MAIN_RAM)]
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x186708, [len(self.bakery_inventory)], MAIN_RAM)]
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
                        logger.info("bakery inventory %s",self.bakery_inventory)
                        #logger.info("bakery inventory bytes %s",bytes(self.bakery_inventory))
                        logger.info("bakery inventory len %s",len(self.bakery_inventory))
                        #logger.info("bakery inventory len bytes %s",bytes(len(self.bakery_inventory)))
                        if(not 0x68 in self.bakery_inventory):
                            self.bakery_inventory = [0x69,0x68] + self.bakery_inventory
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x1fab10, self.bakery_inventory, MAIN_RAM)]
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x186fe0, [len(self.bakery_inventory)], MAIN_RAM)]
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x186ff0, [len(self.bakery_inventory)], MAIN_RAM)]
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
                        logger.info("bakery inventory %s",self.bakery_inventory)
                        #logger.info("bakery inventory bytes %s",bytes(self.bakery_inventory))
                        logger.info("bakery inventory len %s",len(self.bakery_inventory))
                        #logger.info("bakery inventory len bytes %s",bytes(len(self.bakery_inventory)))
                        if(not 0x68 in self.bakery_inventory):
                            self.bakery_inventory = [0x69,0x68] + self.bakery_inventory
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x1fab10, self.bakery_inventory, MAIN_RAM)]
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x186cf0, [len(self.bakery_inventory)], MAIN_RAM)]
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x186ce0, [len(self.bakery_inventory)], MAIN_RAM)]
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x186cf4, [0x20, 0x80], MAIN_RAM)] #somehow coresponds to 0x801f
                        )
                        await bizhawk.write(
                            ctx.bizhawk_ctx,
                            [(0x186cf8, [0x10, 0xab], MAIN_RAM)]
                        )
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

                self.old_step_count = step_count
                """if(curr_location == 0x3014):
                    #Hawker
                    dialog: bytes = (await bizhawk.read(ctx.bizhawk_ctx, [(
                        0x191cbc, 20, MAIN_RAM
                    )]))[0]
                    logger.info("read hawker dialog %s",dialog)
                    await ctx.send_msgs([{
                        "cmd": "LocationScouts",
                        "locations": [standard_location_name_to_id["Hawker Bincho - Somnolent Forest Deadend"]],
                        "create_as_hint": 0
                    }])
                    #logger.info("scout info %s",ctx.locations_info.items()[standard_location_name_to_id["Hawker Bincho - Somnolent Forest Deadend"]])
                    if(ctx.locations_info):
                        if(standard_location_name_to_id["Hawker Bincho - Somnolent Forest Deadend"] in ctx.locations_info):
                            s = "<"+ctx.username+">"
                            barray = bytearray(s,"utf-8")
                            barray.append(0x0a)
                            s = "Found "
                            barray.extend(s.encode("utf-8"))
                            barray.append(0x01)
                            barray.append(0x02)
                            s = ctx.item_names.lookup_in_slot(ctx.locations_info[standard_location_name_to_id["Hawker Bincho - Somnolent Forest Deadend"]].item, ctx.locations_info[standard_location_name_to_id["Hawker Bincho - Somnolent Forest Deadend"]].player)
                            logger.info("scout item name %s",s)
                            barray.extend(s.encode("utf-8"))
                            barray.append(0x01)
                            barray.append(0x01)
                            s = " for "
                            barray.extend(s.encode("utf-8"))
                            s = ctx.player_names[ctx.locations_info[standard_location_name_to_id["Hawker Bincho - Somnolent Forest Deadend"]].player]
                            barray.extend(s.encode("utf-8"))
                            barray.append(0x00)
                            await bizhawk.write(
                                ctx.bizhawk_ctx,
                                [(0x191cc0, barray, MAIN_RAM)]
                            )
                        else:
                            logger.info("no hawker found")"""

            #if not ctx.finished_game and len(ctx.items_received) == 35:
            if not ctx.finished_game and set(received_list).issuperset(set(npc_ids)):
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])
            
            if (self.request_hints == 0):
                self.request_hints = 1
                await ctx.send_msgs([{
                    "cmd": "LocationScouts",
                    "locations": table_ids_to_hint,
                    "create_as_hint": 0
                }])

            if(ctx.slot_data["X"]):
                if "DeathLink" not in ctx.tags:
                    await ctx.update_death_link(True)
                    self.previous_death_link = ctx.last_death_link
                if self.death_link_timer == 0:
                    curr_hp_bytes: bytes = (await bizhawk.read(
                        ctx.bizhawk_ctx,
                        [(0x078eb4, 2, MAIN_RAM)]
                    ))[0]
                    curr_hp: int = int.from_bytes(curr_hp_bytes, byteorder='little')
                    if curr_hp == 0 and self.has_died == 0:
                        self.has_died = 1
                        logger.info("%s died",ctx.username)
                        await ctx.send_death(f"{ctx.username} had a nightmare about a horrid death!")
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
    
    async def update_legendary_armor(self, ctx: "BizHawkClientContext"):
        from CommonClient import logger
        logger.info("updating legendary armor list")
        save_data: bytes = (await bizhawk.read(
            ctx.bizhawk_ctx,
            [(0x0ae64b, 2, MAIN_RAM)]
        ))[0]
        holdint = [save_data[0],save_data[1]]
        self.legendary_armor = self.decode_booleans_with_exclusions(int.from_bytes(holdint, byteorder='little'), 10, [0,1,2])
        logger.info("lengendary armor %s",self.legendary_armor)
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

    async def check_if_bracelet_needs_removed(self, ctx: "BizHawkClientContext"):
        from CommonClient import logger
        logger.info("checking for extra bracelet")
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
        logger.info("checking for extra armor")
        await self.update_legendary_armor(ctx)
        if(self.legendary_armor[4] == 1):
            if(0x49 in self.bakery_inventory):
                self.bakery_inventory.remove(0x49)
                logger.info("removing extra bracelet from bakery")
        if(self.legendary_armor[5] == 1):
            if(0x4a in self.bakery_inventory):
                self.bakery_inventory.remove(0x4a)
                logger.info("removing extra old shirt from bakery")
        if(self.legendary_armor[6] == 1):
            if(0x4b in self.bakery_inventory):
                self.bakery_inventory.remove(0x4b)
                logger.info("removing extra red shoes from bakery")
        pass


            