from typing import ClassVar, Dict, Any, Type, List, Union

from settings import Group, UserFilePath, Bool

class BFMSettings(Group):
    class RomPath(UserFilePath):
        """Path to the Brave Fencer Musashi .cue file (not the bin)"""
        description = "Brave Fencer Musashi .cue file"
        is_exe = False

    class UsingMono(Bool):
        """Linux users only: Using Mono, not Proton to launch Bizhawk"""

    class AutoOpenUT(Bool):
        """auto start universal tracker"""

    rom_path: RomPath = RomPath("Brave Fencer Musashi.cue")
    using_mono: Union[UsingMono, bool] = True
    autostart_ut: Union[AutoOpenUT, bool] = True
