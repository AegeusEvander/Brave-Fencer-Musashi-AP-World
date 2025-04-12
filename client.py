"""
A module containing the BizHawkClient base class and metaclass
"""

from __future__ import annotations

import abc
from typing import TYPE_CHECKING, Any, ClassVar

from worlds.LauncherComponents import Component, SuffixIdentifier, Type, components, launch as launch_component

from .locations import location_table, location_name_groups, standard_location_name_to_id, sphere_one
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


def launch_client(*args) -> None:
    from .context import launch
    launch_component(launch, name="BFMBizHawkClient", args=args)


component = Component("BFM BizHawk Client", "BFMBizHawkClient", component_type=Type.CLIENT, func=launch_client,
                      file_identifier=SuffixIdentifier())
components.append(component)

MAIN_RAM: typing.Final[str] = "MainRAM"
PLAYER_LIFE_POINTS_SHORT_OFFSET: typing.Final[int] = 0x078EB4
bincho_checks = [0] * 8


class AutoBizHawkClientRegister(abc.ABCMeta):
    game_handlers: ClassVar[dict[tuple[str, ...], dict[str, BizHawkClient]]] = {}

    def __new__(cls, name: str, bases: tuple[type, ...], namespace: dict[str, Any]) -> AutoBizHawkClientRegister:
        new_class = super().__new__(cls, name, bases, namespace)

        # Register handler
        if "system" in namespace:
            systems = (namespace["system"],) if type(namespace["system"]) is str else tuple(sorted(namespace["system"]))
            if systems not in AutoBizHawkClientRegister.game_handlers:
                AutoBizHawkClientRegister.game_handlers[systems] = {}

            if "game" in namespace:
                AutoBizHawkClientRegister.game_handlers[systems][namespace["game"]] = new_class()

        # Update launcher component's suffixes
        if "patch_suffix" in namespace:
            if namespace["patch_suffix"] is not None:
                existing_identifier: SuffixIdentifier = component.file_identifier
                new_suffixes = [*existing_identifier.suffixes]

                if type(namespace["patch_suffix"]) is str:
                    new_suffixes.append(namespace["patch_suffix"])
                else:
                    new_suffixes.extend(namespace["patch_suffix"])

                component.file_identifier = SuffixIdentifier(*new_suffixes)

        return new_class

    @staticmethod
    async def get_handler(ctx: "BizHawkClientContext", system: str) -> BizHawkClient | None:
        for systems, handlers in AutoBizHawkClientRegister.game_handlers.items():
            if system in systems:
                for handler in handlers.values():
                    if await handler.validate_rom(ctx):
                        return handler

        return None


#class BFMClient(BizHawkClient):
class BFMClient(abc.ABC, metaclass=AutoBizHawkClientRegister):
    system: ClassVar[str | tuple[str, ...]] = "PSX"
    """The system(s) that the game this client is for runs on"""

    game: ClassVar[str] = Constants.GAME_NAME
    """The game this client is for"""

    patch_suffix: ClassVar[str | tuple[str, ...] | None] = ".apbfm"
    """The file extension(s) this client is meant to open and patch (e.g. ".apz3")"""

    #@abc.abstractmethod
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
                return False
        except Exception:
            return False

        ctx.game = self.game
        ctx.items_handling = 0b011
        ctx.want_slot_data = True
        ctx.watcher_timeout = 0.125  # value taken from Forbiden Memories, taken from Pokemon Emerald's client
        #self.random = Random()  # used for silly random deathlink messages
        logger.info(f"Brave Fencer Musashi Client v{__version__}. For updates:")
        logger.info("https://github.com/releases/latest")
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

    #@abc.abstractmethod
    async def game_watcher(self, ctx: "BizHawkClientContext") -> None:
        """Runs on a loop with the approximate interval `ctx.watcher_timeout`. The currently loaded ROM is guaranteed
        to have passed your validator when this function is called, and the emulator is very likely to be connected."""
        save_data = await bizhawk.read(ctx.bizhawk_ctx,[(0x0ae671, 1, MAIN_RAM)])[0]
        new_bincho_checks = decode_booleans(save_data,8)
        if(new_bincho_checks[0] != bincho_checks[0]):
            bincho_checks[0] = new_bincho_checks[0]
            from CommonClient import logger
            logger.info("Trying to send Guard check %s",standard_location_name_to_id["Guard Bincho - Somnolent Forest"])
            await ctx.send_msgs([{
                "cmd": "LocationChecks",
                "locations": standard_location_name_to_id["Guard Bincho - Somnolent Forest"]
            }])

    def on_package(self, ctx: "BizHawkClientContext", cmd: str, args: dict) -> None:
        """For handling packages from the server. Called from `BizHawkClientContext.on_package`."""
        pass


    def decode_booleans(val, bits):
        result = []
        for bit in xrange(bits):
            mask = 1 << bit
            result.append((val & mask) == mask)
        return result