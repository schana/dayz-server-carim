import pathlib

from carim.configuration import decorators
from carim.global_resources import resourcesdir
from carim.util import file_writing


@decorators.server
def server_dz_config(directory):
    file_writing.copy(pathlib.Path(resourcesdir.get(), 'modifications/server/serverDZ.cfg'),
                      pathlib.Path(directory, 'serverDZ.cfg'))
    file_writing.copy(pathlib.Path(resourcesdir.get(), 'modifications/server/serverDZ.cfg'),
                      pathlib.Path(directory, 'serverDZ.cfg.active'))
