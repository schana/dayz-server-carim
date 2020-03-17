import json
import pathlib
import logging

from carim.configuration import base
from carim.models import auth

log = logging.getLogger(__name__)


@base.server
def omega_config(directory):
    cfg = None
    with open('omega/omega.cfg') as f:
        cfg = json.load(f)
    cfg['cftools']['service_api_key'] = auth.get()['cf']['service_api_key']
    cfg['cftools']['service_id'] = auth.get()['cf']['service_id']
    with open(pathlib.Path(directory, 'omega.cfg'), mode='w') as f:
        json.dump(cfg, f, indent=2)


@base.server(directory='profiles')
def cf_tools_config(directory):
    cfg = {
        'service_api_key': auth.get()['cf']['service_api_key'],
        'service_id': auth.get()['cf']['service_id']
    }
    with open(pathlib.Path(directory, 'cftools.cfg'), mode='w') as f:
        json.dump(cfg, f, indent=2)


@base.config
def omega_manager(directory):
    cfg = None
    with open('omega/manager.cfg') as f:
        cfg = json.load(f)
    cfg['steam'] = {
        'username': auth.get()['steam']['username'],
        'api_key': auth.get()['steam']['api_key'],
        'password': auth.get()['steam']['password'],
        'mobile_authenticator': False
    }
    with open(pathlib.Path(directory, 'manager.cfg'), mode='w') as f:
        json.dump(cfg, f, indent=2)


@base.server
def priority_queue(directory):
    users = []
    for priority_user in auth.get().get('priority', []):
        users.append(priority_user['steam64'])
        log.info('adding {} to priority queue'.format(priority_user['name']))
    with open(pathlib.Path(directory, 'priority.txt'), mode='w') as f:
        f.writelines(user + ';' for user in users)
