import logging
import pathlib

from carim.configuration import decorators
from carim.global_resources import auth
from carim.util import file_writing

log = logging.getLogger(__name__)


@decorators.register
@decorators.server
def priority_queue(directory):
    users = []
    for priority_user in auth.get().get('priority', []):
        users.append(priority_user['steam64'])
        log.info('adding {} to priority queue'.format(priority_user['name']))
    with file_writing.f_open(pathlib.Path(directory, 'priority.txt'), mode='w') as f:
        f.writelines(user + ';' for user in users)
