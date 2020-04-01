# DayZ Server Configuration
Open source configuration and automation developed for the Carim DayZ Server, but usable by all.
This is intended to be used in conjunction with [CFTools](cftools.de).

[Carim Server on Discord](https://discord.gg/kdPnVu4)

## Usage

1. Perform initial setup of [CFTools OmegaManager](https://wiki.cftools.de/display/CFTOOL/OmegaManager)
1. Copy `auth.json` and `preexec.bat` somewhere outside of the repository for security purposes
1. Edit the files with the appropriate values
1. Run `preexec.bat`
1. Your server should now be configured to automatically pull updates and apply them every time your server restarts

### Advanced Usage

All the configurations are stored in the `resources` directory.
It is encouraged to copy everything except `original-mod-files` into your own resources directory where you can
individually manage your server's configuration.

#### Useful files in resources

* `auth.json` is where admins, priority, steam credentials, etc. are stored
* `preexec.bat` is the script that runs the config utility with logging
* `modifications/omega/mods.json` contains the mods enabled on the server
* `modifications/server/types_config.json` is where `types.xml` is configured
* `modifications/mods` is the folder containing all the mod specific configuration

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

### Adding a configuration

Configurations are represented as functions. Decorators are added to specify how the application should treat them.

#### Decorators `carim.configuration.decorators`

Decorators for configs should always be applied in the following order

* `@register` indicates that the configuration should be registered to be automatically applied at runtime
  * If order of application is important, then this should be omitted. For example, the Trader config relies on Types config,
  so it is not registered so execution order can be manually managed.
* `@mod` indicates that the config should only be applied if the specified mod is enabled
* `@config` marks the function as a configuration and handles creating directories for the output as well as logging
  * decorators that inherit from `config` can also be used
  * they usually only add specific directory prefixes
  * `located_config`, `server`, `mission`, `profile`

Examples:

```python
from carim.configuration import decorators

@decorators.register                # registers this config to be applied automatically
@decorators.mod('@SQUAD MSF-C')     # only apply this config if this mod is enabled
@decorators.profile                 # denotes the function as a configuration
def items_msfc():
    # do things
```

```python
from carim.configuration import decorators

@decorators.register
@decorators.mod('@VPPAdminTools')
@decorators.profile(directory='VPPAdminTools/ConfigurablePlugins/TeleportManager')
# directory parameter is a relative path to where the configuration should be placed
# the profile decorator adds the prefix 'servers/0/profiles' to this
# the directory parameter for the function will be populated with the output path to where configs should be written
def vpp_teleports(directory):
    with file_writing.f_open(pathlib.Path(directory, 'TeleportLocation.json'), mode='w') as f:
        # file_writing.f_open is a utility that handles errors when writing to files
        # this is helpful when you try to write to a file that is currently opened by the server process
        # write the config
```

#### Registering

Automatic registering of configurations is handled in the `__init__.py` for each package within `carim.configuration`.
When adding a new module within the configuration package, corresponding entries must be added in the relevant `__init__.py` file.

For examples, see the following:
* `mods/__init__.py`
* `omega/__init__.py`
* `server/__init__.py`
* `universal/__init__.py`

<img src="Carim.png" width="400">
