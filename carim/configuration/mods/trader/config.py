import logging
import pathlib

from carim.configuration import decorators
from carim.global_resources import auth
from carim.util import file_writing

log = logging.getLogger(__name__)


@decorators.profile(directory='Trader')
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
