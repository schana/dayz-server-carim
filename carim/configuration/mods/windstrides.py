import itertools
import pathlib
from xml.etree import ElementTree

from carim.configuration import decorators
from carim.global_resources import types, resourcesdir


@decorators.register
@decorators.mod('@WindstridesClothingPack')
@decorators.profile
def items_windstrides():
    with open(pathlib.Path(resourcesdir.get(), 'original-mod-files/WindstridesClothingPack/types.xml')) as f:
        it = itertools.chain('<type>', f, '</type>')
        new_types = ElementTree.fromstringlist(it)
    types.get().getroot().extend(new_types)
