import json
import logging
import pathlib

from carim.configuration import decorators
from carim.configuration.mods.vanilla_plus_plus_map import model
from carim.global_resources import auth
from carim.util import file_writing

log = logging.getLogger(__name__)


@decorators.register
@decorators.mod('@VPPAdminTools')
@decorators.profile(directory='VPPAdminTools/Permissions/SuperAdmins')
def vpp_admin_tools_permissions(directory):
    with file_writing.f_open(pathlib.Path(directory, 'SuperAdmins.txt'), mode='w') as f:
        for superuser in auth.get().get('superusers', []):
            log.info('adding {} as superuser'.format(superuser['name']))
            f.write(superuser['steam64'] + '\n')


@decorators.register
@decorators.mod('@VPPAdminTools')
@decorators.profile(directory='VPPAdminTools/ConfigurablePlugins/TeleportManager')
def vpp_teleports(directory):
    with file_writing.f_open(pathlib.Path(directory, 'TeleportLocation.json'), mode='w') as f:
        json.dump(model.get_admin_teleport_config(), f, indent=2)
