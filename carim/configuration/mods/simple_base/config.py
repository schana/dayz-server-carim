import json
import pathlib
from xml.etree import ElementTree

from carim.configuration import decorators
from carim.configuration.mods.simple_base import model
from carim.global_resources import types, resourcesdir
from carim.util import file_writing


@decorators.register
@decorators.mod('@Simple Base')
@decorators.profile(directory='SimpleBase')
def simple_base_profile(directory):
    with open('resources/original-mod-files/Simple Base/types.xml') as f:
        raw = '<types>' + f.read() + '</types>'
        new_types = ElementTree.fromstring(raw)
    types.get().getroot().extend(new_types)
    with open('resources/original-mod-files/Simple Base/ServerProfileFolder/SimpleBase/config.txt') as f:
        lines = f.readlines()
    config = model.Config()
    config.parse_defaults(lines)
    with open(pathlib.Path(resourcesdir.get(), 'modifications/mods/simple_base/config.json')) as f:
        changes = json.load(f)
    for k, v in changes.items():
        config.set(k, v)
    with file_writing.f_open(pathlib.Path(directory, 'config.txt'), mode='w') as f:
        f.write(config.generate())
