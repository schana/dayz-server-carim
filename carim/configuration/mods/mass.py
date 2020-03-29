from xml.etree import ElementTree

from carim.configuration import decorators
from carim.global_resources import types


@decorators.register
@decorators.mod('@MasssManyItemOverhaul')
@decorators.profile
def items_mass():
    new_types = ElementTree.parse('resources/original-mod-files/MasssManyItemOverhaul/types(NOT A REPLACER).xml')
    types.get().getroot().extend(new_types.getroot())
