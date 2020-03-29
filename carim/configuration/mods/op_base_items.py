import pathlib
from xml.etree import ElementTree

from carim.configuration import decorators
from carim.global_resources import types, resourcesdir


@decorators.register
@decorators.mod('@OP_BaseItems')
@decorators.profile
def items_op_base_items():
    with open(pathlib.Path(resourcesdir.get(), 'original-mod-files/OP_BaseItems/types.xml')) as f:
        raw = '<types>' + f.read() + '</types>'
        new_types = ElementTree.fromstring(raw)
    types.get().getroot().extend(new_types)
