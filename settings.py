from typing import ClassVar, Dict, Any, Type, List, Union

from settings import Group, UserFilePath, UserFolderPath, Bool, FilePath

class BFMSettings(Group):
    class RomPath(UserFilePath):
        """Path to the Brave Fencer Musashi .cue file (not the bin)"""
        description = "Brave Fencer Musashi .cue file"
        is_exe = False

    class UsingMono(Bool):
        """Linux users only: Using Mono, not Proton to launch Bizhawk"""

    class AutoOpenUT(Bool):
        """auto start universal tracker"""

    class ExportFolder(UserFolderPath):
        """Folder Path to place exported geometry files"""
        description = "Folder Path to place exported geometry files"

    #class UTPackPath(FilePath):
    #    """Path to the BFM Map Pack."""
    #    ut_dialog_name = "BFM Map Pack zip file"
    #    required = False

    rom_path: RomPath = RomPath("Brave Fencer Musashi.cue")
    using_mono: Union[UsingMono, bool] = True
    autostart_ut: Union[AutoOpenUT, bool] = True
    export_folder: ExportFolder = ExportFolder(":pick a folder to save:")
    #ut_pack_path: Union[UTPackPath, str] = UTPackPath()
