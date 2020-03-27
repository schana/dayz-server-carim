import pathlib
from xml.etree import ElementTree

from carim.configuration import decorators
from carim.global_resources import types


@decorators.profile
def items_munghards():
    for p in pathlib.Path('resources/original-mod-files/MunghardsItemPack/types').glob('*.xml'):
        new_types = ElementTree.parse(p)
        types.get().getroot().extend(new_types.getroot())
