import json
import pathlib

from carim.configuration import base
from carim.models import auth


@base.config(directory='servers/0')
def omega_config(directory):
    cfg = None
    with open('omega/omega.cfg') as f:
        cfg = json.load(f)
    cfg['cftools']['service_api_key'] = auth.get()['cf']['service_api_key']
    cfg['cftools']['service_id'] = auth.get()['cf']['service_id']
    with open(pathlib.Path(directory, 'omega.cfg'), mode='w') as f:
        json.dump(cfg, f, indent=2)


@base.config(directory='servers/0/profiles')
def cf_tools_config(directory):
    cfg = {
        'service_api_key': auth.get()['cf']['service_api_key'],
        'service_id': auth.get()['cf']['service_id']
    }
    with open(pathlib.Path(directory, 'cftools.cfg'), mode='w') as f:
        json.dump(cfg, f, indent=2)


@base.config(directory='.')
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
