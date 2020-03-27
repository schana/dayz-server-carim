import pathlib

from carim.configuration import decorators
from carim.util import file_writing


@decorators.profile(directory='ServerPanel')
def server_panel_coniguration(directory):
    file_writing.copy('resources/modifications/mods/server_panel/config.json',
                      pathlib.Path(directory, 'ServerPanel.json'))
