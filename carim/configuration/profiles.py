import itertools
import json
import logging
import pathlib
import shutil
from xml.etree import ElementTree

from carim.configuration import base
from carim.models import auth, types, vpp_map

log = logging.getLogger(__name__)


def profile(_func=None, *, directory='.'):
    return base.located_config(_func, directory=directory, dir_prefix='servers/0/profiles')


@profile(directory='Trader')
def trader_file_and_admins(directory):
    for p in pathlib.Path('omega/Trader').glob('*'):
        shutil.copy(p, directory)
    with open(pathlib.Path(directory, 'TraderAdmins.txt'), mode='w') as f:
        for superuser in auth.get().get('superusers', []):
            log.info('adding {} as trader admin'.format(superuser['name']))
            f.write(superuser['steam64'] + '\n')
        f.write('<FileEnd>')


@profile(directory='Airdrop')
def airdrop(directory):
    p = pathlib.Path('omega/Airdrop/AirdropSettings.json')
    shutil.copy(p, directory)


@profile(directory='SimpleBase')
def simple_base(directory):
    with open('omega/Simple Base/types.xml') as f:
        it = itertools.chain('<type>', f, '</type>')
        new_types = ElementTree.fromstringlist(it)
    types.get().getroot().extend(new_types)
    # profile config
    # destruction config


@profile(directory='VPPAdminTools/Permissions/SuperAdmins')
def vpp_admin_tools_permissions(directory):
    with open(pathlib.Path(directory, 'SuperAdmins.txt'), mode='w') as f:
        for superuser in auth.get().get('superusers', []):
            log.info('adding {} as superuser'.format(superuser['name']))
            f.write(superuser['steam64'] + '\n')


@profile(directory='CodeLock')
def code_lock(directory):
    new_type = ElementTree.parse('omega/Code Lock/types.xml')
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
    with open(pathlib.Path(directory, 'CodeLockPerms.json'), mode='w') as f:
        json.dump(users, f, indent=2)


@profile
def items_clouds():
    with open('omega/Cl0uds/Types V9.1 only.xml') as f:
        it = itertools.chain('<type>', f, '</type>')
        new_types = ElementTree.fromstringlist(it)
    types.get().getroot().extend(new_types)


@profile
def items_mass():
    new_types = ElementTree.parse('omega/MasssManyItemOverhaul/types(NOT A REPLACER).xml')
    types.get().getroot().extend(new_types.getroot())


@profile
def items_msfc():
    for p in pathlib.Path('omega/MSF-C').glob('*.xml'):
        with open(p) as f:
            it = itertools.chain('<type>', f, '</type>')
            new_types = ElementTree.fromstringlist(it)
        types.get().getroot().extend(new_types)


@profile
def items_munghards():
    for p in pathlib.Path('omega/MunghardsItemPack/types').glob('*.xml'):
        new_types = ElementTree.parse(p)
        types.get().getroot().extend(new_types.getroot())


@profile
def vanilla_plus_plus_map(directory):
    marks = [
        ('Green Mountain Trader', vpp_map.Position(3727, 6007)),
        ('Kumyrna Trader', vpp_map.Position(8355, 5986))
    ]
    for m in marks:
        vpp_map.add(vpp_map.Marker(
            name=m[0],
            icon=vpp_map.Icon.DEFAULT,
            color=vpp_map.WHITE,
            position=m[1],
            active=True,
            active_3d=True
        ))
    with open(pathlib.Path(directory, 'VPPMapConfig.json'), 'w') as f:
        json.dump(vpp_map.get_config(), f, indent=2)
