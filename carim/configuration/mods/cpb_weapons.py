from xml.etree import ElementTree

from carim.configuration import decorators
from carim.global_resources import types


@decorators.register
@decorators.mod('@CPBWeapons')
@decorators.profile
def items_cpb_weapons():
    with open('resources/original-mod-files/CPBWeapons/types(NOT A REPLACE).xml') as f:
        new_types = ElementTree.fromstring(f.read())
    types.get().getroot().extend(new_types)
