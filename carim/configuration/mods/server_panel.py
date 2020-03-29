import pathlib

from carim.configuration import decorators
from carim.global_resources import resourcesdir
from carim.util import file_writing


@decorators.register
@decorators.mod('@Server_Information_Panel')
@decorators.profile(directory='ServerPanel')
def server_panel_coniguration(directory):
    file_writing.copy(pathlib.Path(resourcesdir.get(), 'modifications/mods/server_panel/config.json'),
                      pathlib.Path(directory, 'ServerPanel.json'))
