# Brave Fencer Musashi Setup Guide

## Required Software
- [Archipelago](https://github.com/ArchipelagoMW/Archipelago/releases). Please use version 0.4.4 or later for integrated
BizHawk support.
- Brave Fencer Musashi NTSC: BIN(s)/CUE. 
- Delta Patcher program that handles xdelta [Releases page](https://github.com/marco-calautti/DeltaPatcher/releases/latest). 
Alternatively if on Linux download the `Delta Patcher` on flatpak
- [BizHawk](https://tasvideos.org/BizHawk/ReleaseHistory) 2.7 or later. Other emulators are not supported.
- The latest `bfm.apworld` file. You can find this on the [Releases page](https://github.com/releases/latest). Put this in your `Archipelago/lib/worlds` folder.
- Brave Fencer Musashi AP Randomizer xdelta patch file [Releases page](https://github.com/releases/latest)

### Configuring BizHawk

Once you have installed BizHawk, open `EmuHawk.exe` and change the following settings:

- If you're using BizHawk 2.7 or 2.8, go to `Config > Customize`. On the Advanced tab, switch the Lua Core from
`NLua+KopiLua` to `Lua+LuaInterface`, then restart EmuHawk. (If you're using BizHawk 2.9, you can skip this step.)
- Under `Config > Customize`, check the "Run in background" option to prevent disconnecting from the client while you're
tabbed out of EmuHawk.
- Open any PlayStation game in EmuHawk and go to `Config > Controllers…` to configure your inputs. If you can't click
`Controllers…`, it's because you need to load a game first.
- Consider clearing keybinds in `Config > Hotkeys…` if you don't intend to use them. Select the keybind and press Esc to
clear it.

## Patching the BIN file

-launch `Delta Patcher`
-For original file select an unmodified `Brave Fencer Musashi (USA) (Track 1).bin`
-For xDelta patch select the downloaded xdelta patch linked above.
-`Apply patch`
-A patched bin can be used for multiple games just keep careful track of save files and memory cards. It is also suggested to update the folder name to denote a patched file

## Generating a Game

1. Create your options file (YAML). After installing the `bfm.apworld` file, you can generate a template within the Archipelago Launcher by clicking `Generate Template Settings`.
2. Follow the general Archipelago instructions for [generating a game](https://archipelago.gg/tutorial/Archipelago/setup/en#generating-a-game).
3. Open `ArchipelagoLauncher.exe`
4. Select "BizHawk Client" in the right-side column. On your first time opening BizHawk Client, you may also be asked to
locate `EmuHawk.exe` in your BizHawk install.

## Connecting to a Server

1. If EmuHawk didn't launch automatically, open it manually.
2. Open your `Brave Fencer Musashi (USA).cue` file in EmuHawk.
5. In EmuHawk, go to `Tools > Lua Console`. This window must stay open in order to send or recieve items.
6. In the Lua Console window, go to `Script > Open Script…`.
7. Navigate to your Archipelago install folder and open `data/lua/connector_bizhawk_generic.lua`.
8. The emulator and client will eventually connect to each other. The BizHawk Client window should indicate that it
connected and recognized Brave Fencer Musashi.
9. To connect the client to the server, enter your room's address and port (e.g. `archipelago.gg:38281`) into the
top text field of the client and click Connect.

You should now be able to receive and send items. You'll need to do these steps every time you want to reconnect. It is
safe to make progress offline; everything will re-sync when you reconnect.

## A Note to New Players of Brave Fencer Musashi

A speedrun of the game may take 2-4 hours depending on catagory, a first time casual run may take 12-20 hours. Consider playing this game with quicker goal settings (to be added to options page TBD) or playing this game in an async.

## Notes and Limitations

1. Consider using savestates