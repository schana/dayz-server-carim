import json
import logging
import pathlib

from carim.configuration import decorators
from carim.global_resources import auth, resourcesdir
from carim.util import file_writing

log = logging.getLogger(__name__)


@decorators.register
@decorators.server
def omega_config(directory):
    with open(pathlib.Path(resourcesdir.get(), 'modifications/omega/omega.json')) as f:
        cfg = json.load(f)
    cfg['cftools']['service_api_key'] = auth.get()['cf']['service_api_key']
    cfg['cftools']['service_id'] = auth.get()['cf']['service_id']
    cfg['general']['pre_execution_script'] = {
        'enabled': True,
        'execution_time_limit': 10,
        'path': auth.get()['preexec']['path']
    }
    with open(pathlib.Path(resourcesdir.get(), 'modifications/omega/mods.json')) as f:
        mods_config = json.load(f)
    cfg['mods'] = mods_config
    with file_writing.f_open(pathlib.Path(directory, 'omega.cfg'), mode='w') as f:
        json.dump(cfg, f, indent=2)


@decorators.register
@decorators.server(directory='profiles')
def cf_tools_config(directory):
    cfg = {
        'service_api_key': auth.get()['cf']['service_api_key'],
        'service_id': auth.get()['cf']['service_id']
    }
    with file_writing.f_open(pathlib.Path(directory, 'cftools.cfg'), mode='w') as f:
        json.dump(cfg, f, indent=2)


@decorators.register
@decorators.config
def omega_manager(directory):
    cfg = None
    with file_writing.f_open(pathlib.Path(resourcesdir.get(), 'modifications/omega/manager.cfg')) as f:
        cfg = json.load(f)
    cfg['steam'] = {
        'username': auth.get()['steam']['username'],
        'api_key': auth.get()['steam']['api_key'],
        'password': auth.get()['steam']['password'],
        'mobile_authenticator': False
    }
    with file_writing.f_open(pathlib.Path(directory, 'manager.cfg'), mode='w') as f:
        json.dump(cfg, f, indent=2)
