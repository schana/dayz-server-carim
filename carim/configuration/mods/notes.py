from xml.etree import ElementTree

from carim.configuration import decorators
from carim.global_resources import types


@decorators.register
@decorators.mod('@Notes')
@decorators.profile
def items_notes():
    with open('resources/original-mod-files/Notes/types.xml') as f:
        raw = '<types>' + f.read() + '</types>'
        new_types = ElementTree.fromstring(raw)
    types.get().getroot().extend(new_types)
