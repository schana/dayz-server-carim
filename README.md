# DayZ Server Configuration
Open source configuration and automation developed for the Carim DayZ Server, but usable by all. This is intended to be used in conjunction with [CFTools](cftools.de).

[Carim Server on Discord](https://discord.gg/kdPnVu4)

## Usage

1. Perform initial setup of [CFTools OmegaManager](https://wiki.cftools.de/display/CFTOOL/OmegaManager)
1. Copy `auth.json` and `preexec.bat` somewhere outside of the repository for security purposes
1. Edit the files with the appropriate values
1. Run `preexec.bat`
1. Your server should now be configured to automatically pull updates and apply them every time your server restarts

## Included Mod Configuration

```
@Airdrop-Upgraded
@Base Fortifications
@Cl0uds Military Gear
@Code Lock
@DayzWeaponsPainting
@Leather Crafting
@MasssManyItemOverhaul
@MunghardsItempack
@Notes
@OP_BaseItems
@SQUAD MSF-C
@Server_Information_Panel
@Simple Base
@Trader
@VPPAdminTools
@VanillaPlusPlusMap
@WindstridesClothingPack
```

## Development usage

```
usage: main.py [-h] [-c] -d DEPLOY -a AUTH [-o OUTPUT] [-v] [-r RESOURCES]
               [-m MISSION]

Automate configuration

optional arguments:
  -h, --help    show this help message and exit
  -c            clean generated
  -d DEPLOY     deploy directory containing the original dayz server files
  -a AUTH       auth config file
  -o OUTPUT     output destination directory
  -v            verbosity of the output
  -r RESOURCES  resources directory to use
  -m MISSION    mission name

Example:
python3 -m carim.main -c -d <path to omega deploy directory> -a <path to your auth config> -o <path to output config to>
```

Configuration is generated and output in a folder named `generated-<timestamp>`. The contents of this can be copied into your omega directory.

<img src="Carim.png" width="400">
