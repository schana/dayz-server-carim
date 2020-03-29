from xml.etree import ElementTree

from carim.configuration import decorators
from carim.global_resources import types


@decorators.register
@decorators.mod('@DayzWeaponsPainting')
@decorators.profile
def items_dayz_weapons_painting():
    with open('resources/original-mod-files/DayzWeaponsPainting/types.xml') as f:
        raw = '<types>' + f.read() + '</types>'
        new_types = ElementTree.fromstring(raw)
    types.get().getroot().extend(new_types)
