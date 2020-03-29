import pathlib
from xml.etree import ElementTree

from carim.configuration import decorators
from carim.global_resources import types, resourcesdir


@decorators.register
@decorators.mod('@Cl0uds Military Gear')
@decorators.profile
def items_clouds():
    with open(pathlib.Path(resourcesdir.get(), 'original-mod-files/Cl0uds/Types V9.1 - sorted by camos.xml')) as f:
        raw = '<types>' + f.read() + '</types>'
        new_types = ElementTree.fromstring(raw)
    types.get().getroot().extend(new_types)
