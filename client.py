"""
A module containing the BizHawkClient base class and metaclass
"""

from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Any, ClassVar, List

from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch as launch_component

from .locations import location_table, location_name_groups, standard_location_name_to_id, sphere_one, location_base_id
#if TYPE_CHECKING:
#    from .context import BizHawkClientContext
from .utils import Constants
from .version import __version__


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
    received_count = 0

    async def validate_rom(self, ctx: "BizHawkClientContext") -> bool:
        """Should return whether the currently loaded ROM should be handled by this client. You might read the game name
        from the ROM header, for example. This function will only be asked to validate ROMs from the system set by the
        client class, so you do not need to check the system yourself.

        Once this function has determined that the ROM should be handled by this client, it should also modify `ctx`
        as necessary (such as setting `ctx.game = self.game`, modifying `ctx.items_handling`, etc...)."""
        from CommonClient import logger
        logger.info("Attempting to validate rom")
        bfm_identifier_ram_address: int = 0x00ba94

        # = SLUS-00726MUSASHI in ASCII, code taken from AP Forbiden Memories
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
        ctx.watcher_timeout = 0.125  # value taken from Forbiden Memories, taken from Pokemon Emerald's client
        #self.random = Random()  # used for silly random deathlink messages
        logger.info(f"Brave Fencer Musashi Client v{__version__}. For updates:")
        logger.info("https://github.com/AegeusEvander/Brave-Fencer-Musashi-AP-World/releases")
        return True
    
    async def kill_player(self, ctx: "BizHawkClientContext") -> bool:
        """Return True if this method thinks it actually killed the player, False otherwise"""
        # # Player HP at 078EB4 2 Bytes MAINRAM
        #     await bizhawk.write
        await bizhawk.write(
            ctx.bizhawk_ctx,
            [(PLAYER_LIFE_POINTS_SHORT_OFFSET, (0).to_bytes(2, "little"), MAIN_RAM)]
        )
        return True

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
                return
            global bincho_checks
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
            
            #logger.info("What was read 1 in 0aae671 %s",new_bincho_checks)
            if(new_bincho_checks != self.bincho_checks):
                locations_to_send_to_server = []
                for i in range(len(new_bincho_checks)):
                    if(new_bincho_checks[i]):
                        locations_to_send_to_server.append(location_base_id + i)
                #logger.info("What was read in 0ae671 %s",save_data)
                logger.info("Trying to send %s",locations_to_send_to_server)
                await ctx.send_msgs([{
                    "cmd": "LocationChecks",
                    "locations": locations_to_send_to_server
                }])
                self.bincho_checks = new_bincho_checks
            #logger.info("items Received %s",ctx.items_received)
            
            
            curr_location_data: bytes = (await bizhawk.read(
                ctx.bizhawk_ctx,
                [(0x0b9a08, 2, MAIN_RAM)]
            ))[0]
            curr_location = int.from_bytes(curr_location_data,byteorder='little')
            #logger.info("curr_location %s",curr_location)
            #if(curr_location == 4112 or curr_location == 4178):
            #not save menu
            if(curr_location != 12296):
                #logger.info("in Town")
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
                            logger.info("sent id to rescue list %s",item_id)
                        else:
                            logger.info("id already in rescue list %s",item_id)
                    else:
                        logger.info("unhandled item receieved %s",item_id)
                    self.received_count += 1

            if not ctx.finished_game and len(ctx.items_received) == 17:
                await ctx.send_msgs([{
                    "cmd": "StatusUpdate",
                    "status": ClientStatus.CLIENT_GOAL
                }])

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