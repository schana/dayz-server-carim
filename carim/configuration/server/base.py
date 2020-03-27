import pathlib

from carim.configuration import decorators
from carim.util import file_writing


@decorators.server
def server_dz_config(directory):
    file_writing.copy('resources/modifications/server/serverDZ.cfg', pathlib.Path(directory, 'serverDZ.cfg'))
    file_writing.copy('resources/modifications/server/serverDZ.cfg', pathlib.Path(directory, 'serverDZ.cfg.active'))
