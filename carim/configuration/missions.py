import pathlib
from xml.dom import minidom
from xml.etree import ElementTree
import re

from carim.configuration import base
from carim.models import types
from carim.util import file_writing


def mission(_func=None, *, directory='.', register=True):
    return base.located_config(_func, directory=directory, dir_prefix='servers/0/mpmissions/dayzOffline.chernarusplus',
                               register=register)


@mission(directory='db', register=False)
def types_config(directory):
    types.get().getroot()[:] = sorted(types.get().getroot(), key=lambda child: child.get('name').lower())
    rough_string = ElementTree.tostring(types.get().getroot(), encoding='unicode')
    spaces = re.compile(r'>\s*<', flags=re.DOTALL)
    rough_string = re.sub(spaces, '>\n<', rough_string)
    reparsed = minidom.parseString(rough_string)
    with file_writing.f_open(pathlib.Path(directory, 'types.xml'), mode='w') as f:
        f.write(reparsed.toprettyxml(indent='  ', newl=''))
