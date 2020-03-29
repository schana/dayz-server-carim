import pathlib
from xml.etree import ElementTree

from carim.configuration import decorators
from carim.global_resources import types, resourcesdir


@decorators.profile
def items_munghards():
    new_types = ElementTree.parse(
        pathlib.Path(resourcesdir.get(), 'original-mod-files/MunghardsItemPack/types/types.xml'))
    types.get().getroot().extend(new_types.getroot())
