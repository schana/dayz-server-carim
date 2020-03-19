import itertools
import json
import logging
import pathlib
from xml.etree import ElementTree

from carim.configuration import base
from carim.models import auth, types, vpp_map, simple_base
from carim.util import file_writing

log = logging.getLogger(__name__)

# TODO: move this to separate config file
marks = [
    ('Green Mountain Trader', vpp_map.Position(3727, 6007)),
    ('Kumyrna Trader', vpp_map.Position(8355, 5986)),
    ('Altar Trader', vpp_map.Position(8164, 9113)),
    ('Zabolotye Black Market Trader', vpp_map.Position(1602.85, 10413.2)),
    ('NWAF', vpp_map.Position(4541, 10289)),
    ('NEAF', vpp_map.Position(12121, 12521))
]


def profile(_func=None, *, directory='.', register=True):
    return base.located_config(_func, directory=directory, dir_prefix='servers/0/profiles', register=register)


@profile(directory='Trader')
def trader_file_and_admins(directory):
    files = ['TraderVariables.txt', 'TraderVehicleParts.txt']
    for file in files:
        p = pathlib.Path('resources/original-mod-files/Trader', file)
        file_writing.copy(p, directory)
    with file_writing.f_open(pathlib.Path(directory, 'TraderAdmins.txt'), mode='w') as f:
        for superuser in auth.get().get('superusers', []):
            log.info('adding {} as trader admin'.format(superuser['name']))
            f.write(superuser['steam64'] + '\n')
        f.write('<FileEnd>')


@profile(directory='Airdrop')
def airdrop(directory):
    p = pathlib.Path('resources/original-mod-files/Airdrop/AirdropSettings.json')
    file_writing.copy(p, directory)


@profile(directory='SimpleBase')
def simple_base_profile(directory):
    with open('resources/original-mod-files/Simple Base/types.xml') as f:
        it = itertools.chain('<type>', f, '</type>')
        new_types = ElementTree.fromstringlist(it)
    types.get().getroot().extend(new_types)
    with open('resources/original-mod-files/Simple Base/ServerProfileFolder/SimpleBase/config.txt') as f:
        lines = f.readlines()
    config = simple_base.Config()
    config.parse_defaults(lines)
    with open('resources/modifications/simple_base.json') as f:
        changes = json.load(f)
    for k, v in changes.items():
        config.set(k, v)
    with file_writing.f_open(pathlib.Path(directory, 'config.txt'), mode='w') as f:
        f.write(config.generate())
    # destruction config


@profile(directory='VPPAdminTools/Permissions/SuperAdmins')
def vpp_admin_tools_permissions(directory):
    with file_writing.f_open(pathlib.Path(directory, 'SuperAdmins.txt'), mode='w') as f:
        for superuser in auth.get().get('superusers', []):
            log.info('adding {} as superuser'.format(superuser['name']))
            f.write(superuser['steam64'] + '\n')


@profile(directory='CodeLock')
def code_lock(directory):
    new_type = ElementTree.parse('resources/original-mod-files/Code Lock/types.xml')
    types.get().getroot().append(new_type.getroot())
    # config
    users = []
    for superuser in auth.get().get('superusers', []):
        users.append({
            'playerId': superuser['steam64'],
            'playerPerms': {
                'CanOpenLocks': "true",
                'CanChangePasscodes': "true",
                'CanRemoveLocks': "true"
            }
        })
        log.info('adding {} as code lock admin'.format(superuser['name']))
    with file_writing.f_open(pathlib.Path(directory, 'CodeLockPerms.json'), mode='w') as f:
        json.dump(users, f, indent=2)


@profile
def items_clouds():
    with open('resources/original-mod-files/Cl0uds/Types V9.1 only.xml') as f:
        it = itertools.chain('<type>', f, '</type>')
        new_types = ElementTree.fromstringlist(it)
    types.get().getroot().extend(new_types)


@profile
def items_mass():
    new_types = ElementTree.parse('resources/original-mod-files/MasssManyItemOverhaul/types(NOT A REPLACER).xml')
    types.get().getroot().extend(new_types.getroot())


@profile
def items_msfc():
    for p in pathlib.Path('resources/original-mod-files/MSF-C').glob('*.xml'):
        with open(p) as f:
            it = itertools.chain('<type>', f, '</type>')
            new_types = ElementTree.fromstringlist(it)
        types.get().getroot().extend(new_types)


@profile
def items_munghards():
    for p in pathlib.Path('resources/original-mod-files/MunghardsItemPack/types').glob('*.xml'):
        new_types = ElementTree.parse(p)
        types.get().getroot().extend(new_types.getroot())


@profile
def vanilla_plus_plus_map(directory):
    for m in marks:
        vpp_map.add(vpp_map.Marker(
            name=m[0],
            icon=vpp_map.Icon.DEFAULT,
            color=vpp_map.WHITE,
            position=m[1],
            active=True,
            active_3d=True
        ))
    with file_writing.f_open(pathlib.Path(directory, 'VPPMapConfig.json'), mode='w') as f:
        json.dump(vpp_map.get_config(), f, indent=2)


@profile(directory='VPPAdminTools/ConfigurablePlugins/TeleportManager')
def vpp_teleports(directory):
    with file_writing.f_open(pathlib.Path(directory, 'TeleportLocation.json'), mode='w') as f:
        json.dump(vpp_map.get_admin_teleport_config(), f, indent=2)
