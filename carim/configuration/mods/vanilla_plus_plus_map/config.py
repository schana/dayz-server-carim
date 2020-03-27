import json
import pathlib

from carim.configuration import decorators
from carim.configuration.mods.vanilla_plus_plus_map import model
from carim.util import file_writing


@decorators.profile
def vanilla_plus_plus_map(directory):
    with file_writing.f_open(pathlib.Path(directory, 'VPPMapConfig.json'), mode='w') as f:
        json.dump(model.get_config(), f, indent=2)
