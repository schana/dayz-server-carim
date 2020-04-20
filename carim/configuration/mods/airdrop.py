import json
import pathlib

from carim.configuration import decorators
from carim.global_resources import resourcesdir
from carim.util import file_writing


@decorators.register
@decorators.mod('@Airdrop-Upgraded')
@decorators.profile(directory='Airdrop')
def airdrop(directory):
    with open('resources/original-mod-files/Airdrop/AirdropSettings.json') as f:
        airdrop_settings = json.load(f)
    with open(pathlib.Path(resourcesdir.get(), 'modifications/mods/airdrop/modifications.json')) as f:
        airdrop_setting_modifications = json.load(f)
    # http://games.digiacom.com/Airdrop_Server_Guide.pdf
    for setting in ('Controls', 'Map', 'Aircraft', 'Messages', 'Container'):
        for k, v in airdrop_setting_modifications.get(setting).items():
            airdrop_settings[setting][k] = v

    drops = []
    drop_defaults = airdrop_setting_modifications.get('DropZoneDefaults')
    for drop in airdrop_setting_modifications.get('DropZones'):
        drops.append({**drop, **drop_defaults})
    airdrop_settings['DropZones'] = drops

    drop_types = []
    drop_type_defaults = airdrop_setting_modifications.get('DropTypeDefaults')
    for drop_type in airdrop_setting_modifications.get('DropTypes'):
        drop_types.append({**drop_type, **drop_type_defaults})
    airdrop_settings['DropTypes'] = drop_types

    with file_writing.f_open(pathlib.Path(directory, 'AirdropSettings.json'), mode='w') as f:
        json.dump(airdrop_settings, f, indent=2)
