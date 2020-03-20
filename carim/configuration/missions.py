import logging
import pathlib
import re
from xml.dom import minidom
from xml.etree import ElementTree

from carim.configuration import base
from carim.models import types, deploydir, vpp_map
from carim.util import file_writing

log = logging.getLogger(__name__)


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


@mission
def map_config(directory):
    file_writing.copy('resources/server/chernarusplus_tiers_have_traders_removed.map',
                      pathlib.Path(directory, 'areaflags.map'))


@mission(directory='env')
def remove_territories_near_traders(directory):
    for p in pathlib.Path(deploydir.get(), 'mpmissions/dayzOffline.chernarusplus/env').glob('*.xml'):
        log.info(p)
        territory = ElementTree.parse(p).getroot()
        for zone in territory.findall('.//zone'):
            raw = (zone.get('x'), zone.get('z'), zone.get('r'))
            x = float(raw[0])
            z = float(raw[1])
            r = float(raw[2])
            clean_traders = (mark[1] for mark in vpp_map.marks[:3])
            for position in clean_traders:
                if vpp_map.overlaps(position, 500, x, z, r):
                    find_string = './/zone[@x="{}"][@z="{}"][@r="{}"]...'.format(*raw)
                    parents = territory.findall(find_string)
                    for parent in parents:
                        if zone in parent:
                            parent.remove(zone)
                            log.info('removed zone {}, {}, {}'.format(*raw))
                    break
        rough_string = ElementTree.tostring(territory, encoding='unicode')
        spaces = re.compile(r'>\s*<', flags=re.DOTALL)
        rough_string = re.sub(spaces, '>\n<', rough_string)
        reparsed = minidom.parseString(rough_string)
        with file_writing.f_open(pathlib.Path(directory, p.name), mode='w') as f:
            f.write(reparsed.toprettyxml(indent='  ', newl=''))
