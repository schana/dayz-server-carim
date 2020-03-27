import itertools
from xml.etree import ElementTree

from carim.configuration import decorators
from carim.global_resources import types


@decorators.profile
def items_clouds():
    with open('resources/original-mod-files/Cl0uds/Types V9.1 - sorted by camos.xml') as f:
        it = itertools.chain('<type>', f, '</type>')
        new_types = ElementTree.fromstringlist(it)
    types.get().getroot().extend(new_types)
