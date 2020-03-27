import json
import pathlib

from carim.models import vpp_map

from carim.configuration import decorators
from carim.util import file_writing


@decorators.profile
def vanilla_plus_plus_map(directory):
    with file_writing.f_open(pathlib.Path(directory, 'VPPMapConfig.json'), mode='w') as f:
        json.dump(vpp_map.get_config(), f, indent=2)
