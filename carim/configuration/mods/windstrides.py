from xml.etree import ElementTree

from carim.configuration import decorators
from carim.global_resources import types


@decorators.register
@decorators.mod('@WindstridesClothingPack')
@decorators.profile
def items_windstrides():
    with open('resources/original-mod-files/WindstridesClothingPack/types.xml') as f:
        raw = '<types>' + f.read() + '</types>'
        new_types = ElementTree.fromstring(raw)
    types.get().getroot().extend(new_types)
