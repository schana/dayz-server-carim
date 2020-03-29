import pathlib
from xml.etree import ElementTree

from carim.configuration import decorators
from carim.global_resources import types


@decorators.register
@decorators.mod('@SQUAD MSF-C')
@decorators.profile
def items_msfc():
    for p in pathlib.Path('resources/original-mod-files/MSF-C').glob('*.xml'):
        with open(p) as f:
            raw = '<types>' + f.read() + '</types>'
            new_types = ElementTree.fromstring(raw)
        types.get().getroot().extend(new_types)
