import logging
#import os
#import sys

#from https://github.com/ArchipelagoMW/Archipelago/blob/09aba95c039f2d304c15466b7cff6f0ee8f12aa8/worlds/apquest/components.py
def run_client(*args: str) -> None:
    #from .launch import bfm_client
    from worlds._bizhawk.client import launch_client as biz_launch
    from worlds._bizhawk.context import _run_game as emu_launch
    from urllib.parse import urlsplit
    import argparse
    import settings
    import asyncio
    from Utils import is_linux

    #launch(bfm_client, name="BFM Client", args=args)
    #logging.info("attempting to launch bizhawk client")
    parser = argparse.ArgumentParser(description="Brave Fencer Musashi Client Launcher")
    parser.add_argument("url", type=str, nargs="?", help="Archipelago Webhost uri to auto connect to.")
    args = parser.parse_args(args)

    #logging.info("args %s", args.url)
    #logging.info("arg split : %s", urlsplit(args.url))
    #logging.info("netloc : %s", urlsplit(args.url).netloc)
    #logging.info("curr dir : %s", os.path.abspath(sys.path[0]))

    #relPath = '../ArchipelagoBizHawkClient'
   # tarPath = os.path.join(os.path.dirname(os.path.abspath(sys.path[0])), relPath)
    #open_file(f"./ArchipelagoLauncher \"BizHawk Client\" -- {args.url}")
    #subprocess.call(("./ArchipelagoLauncher", "\"BizHawk Client\"", "--", f"{args.url}"))
    #subprocess.call(("./ArchipelagoBizHawkClient", "--connect", f"{urlsplit(args.url).netloc}"))
    netloc = urlsplit(args.url).netloc
    if(len(netloc) > 5):
        biz_launch("--connect", f"{netloc}")
    else:
        biz_launch()
    rom_path = settings.get_settings().brave_fencer_musashi_settings.rom_path
    if(is_linux):
        if(settings.get_settings().brave_fencer_musashi_settings.using_mono == False):
            asyncio.run(_run_game(rom_path))
        else:
            asyncio.run(launch_emu(rom_path))
    else:
        asyncio.run(launch_emu(rom_path))
    if(settings.get_settings().brave_fencer_musashi_settings.autostart_ut):
        try:
            from worlds.tracker import launch_client as ut_launch
            if(len(netloc) > 5):
                ut_launch("--connect", f"{netloc}")
            else:
                ut_launch()
            
        except:
            logger.info("%s", traceback.format_exc())
    #logging.info("rom_path : %s", rom_path)
    
    #asyncio.run(_run_game("/home/aegeusevander/Documents/BraveFencerMusashiISO/Brave Fencer Musashi (USA).cue"))
    #asyncio.run(launch_emu("/home/aegeusevander/Documents/BraveFencerMusashiISO/Brave Fencer Musashi (USA).cue"))
    #Utils.async_start(emu_launch("/home/aegeusevander/Documents/BraveFencerMusashiISO/Brave Fencer Musashi (USA).cue"))
    #subprocess.call((tarPath, "--connect", f"{urlsplit(args.url).netloc}"))

async def launch_emu(rom: str):
    from worlds._bizhawk.context import _run_game as emu_launch
    return await emu_launch(rom)
    #return await emu_launch("Z:\home\aegeusevander\Documents\BraveFencerMusashiISO\Brave Fencer Musashi (USA).cue")

#taken from Bizhawk Context
async def _run_game(rom: str):
    import os
    import subprocess
    import settings
    import Utils
    auto_start = settings.get_settings().bizhawkclient_options.rom_start

    if auto_start is True:
        emuhawk_path = settings.get_settings().bizhawkclient_options.emuhawk_path
        lua_path = os.path.relpath(Utils.local_path('data', 'lua', 'connector_bizhawk_generic.lua'), os.path.expanduser("."))
        rom_path = os.path.relpath(os.path.realpath(rom), os.path.expanduser("."))
        #logging.info("lua path %s", lua_path)
        subprocess.Popen(
            [
                emuhawk_path,
                f"--lua={lua_path}",
                rom_path,
            ],
            cwd=Utils.local_path("."),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    elif isinstance(auto_start, str):
        import shlex

        subprocess.Popen(
            [
                *shlex.split(auto_start),
                os.path.realpath(rom)
            ],
            cwd=Utils.local_path("."),
            stdin=subprocess.DEVNULL,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL
        )