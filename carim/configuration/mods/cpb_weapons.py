from xml.etree import ElementTree

from carim.configuration import decorators
from carim.global_resources import types


@decorators.register
@decorators.mod('@CPBWeapons')
@decorators.profile
def items_cpb_weapons():
    with open('resources/original-mod-files/CPBWeapons/types(NOT A REPLACE).xml') as f:
        new_types = ElementTree.fromstring(f.read())

    for new_type in new_types:
        for value in new_type.findall('.//value'):
            new_type.remove(value)
        ElementTree.SubElement(new_type, 'value', attrib=dict(name='Tier4'))
        ElementTree.SubElement(new_type, 'value', attrib=dict(name='Tier3'))

    types.get().getroot().extend(new_types)
