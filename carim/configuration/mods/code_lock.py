import json
import logging
import pathlib
from xml.etree import ElementTree

from carim.configuration import decorators
from carim.global_resources import types, auth, resourcesdir
from carim.util import file_writing

log = logging.getLogger(__name__)


@decorators.register
@decorators.mod('@Code Lock')
@decorators.profile(directory='CodeLock')
def code_lock(directory):
    new_type = ElementTree.parse(pathlib.Path(resourcesdir.get(), 'original-mod-files/Code lock/types.xml'))
    types.get().getroot().append(new_type.getroot())

    with open(pathlib.Path(resourcesdir.get(), 'original-mod-files/Code lock/CodeLockConfig.json')) as f:
        code_lock_config = json.load(f)
    code_lock_config['CanAttachToTents'] = 'true'
    code_lock_config['DestroyTool'] = 'true'
    with file_writing.f_open(pathlib.Path(directory, 'CodeLockConfig.json'), mode='w') as f:
        json.dump(code_lock_config, f, indent=2)
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
