import json
import logging
import math
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


@mission(directory='db')
def globals_config(directory):
    globals_xml = ElementTree.parse(
        pathlib.Path(deploydir.get(), 'mpmissions/dayzOffline.chernarusplus/db/globals.xml'))
    with open('resources/modifications/server/globals.json') as f:
        globals_modifications = json.load(f)
    for k, v in globals_modifications.items():
        item = globals_xml.getroot().find('.//var[@name="{}"]'.format(k))
        item.set('value', str(v))
    with file_writing.f_open(pathlib.Path(directory, 'globals.xml'), mode='w') as f:
        f.write(file_writing.convert_to_string(globals_xml.getroot()))


@mission(directory='db')
def events_config(directory):
    events_xml = ElementTree.parse(
        pathlib.Path(deploydir.get(), 'mpmissions/dayzOffline.chernarusplus/db/events.xml'))
    with open('resources/modifications/server/events.json') as f:
        events_modifications = json.load(f)
    for mod in events_modifications:
        name_re = re.compile(mod.get('name'))
        for event in events_xml.getroot():
            if name_re.match(event.get('name')):
                event.find('active').text = '1'
                for item in ('nominal',):
                    i = event.find(item)
                    i.text = str(math.floor(max(1, int(i.text)) * mod.get('ratio')))
    with file_writing.f_open(pathlib.Path(directory, 'events.xml'), mode='w') as f:
        f.write(file_writing.convert_to_string(events_xml.getroot()))


@mission
def map_config(directory):
    file_writing.copy('resources/modifications/server/chernarusplus_tiers_have_traders_removed.map',
                      pathlib.Path(directory, 'areaflags.map'))


@mission(directory='env')
def territory_config(directory):
    with open('resources/modifications/server/territories.json') as f:
        territories_modifications = json.load(f)
    for p in pathlib.Path(deploydir.get(), 'mpmissions/dayzOffline.chernarusplus/env').glob('*.xml'):
        filename = p.name
        territory = ElementTree.parse(p).getroot()
        remove_zones_if_near_traders(territory, filename)
        if filename in territories_modifications:
            ratio = territories_modifications.get(filename)
            log.info('applying ratio of {} to {}'.format(ratio, filename))
            for zone in territory.findall('.//zone'):
                dmin = zone.get('dmin')
                dmax = zone.get('dmax')
                zone.set('dmin', str(math.floor(int(dmin) * ratio)))
                zone.set('dmax', str(math.floor(int(dmax) * ratio)))
        with file_writing.f_open(pathlib.Path(directory, filename), mode='w') as f:
            f.write(file_writing.convert_to_string(territory))


def remove_zones_if_near_traders(territory, name):
    count = 0
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
                        count += 1
                        parent.remove(zone)
                        log.debug('removed zone {}, {}, {}'.format(*raw))
                break
    if count > 0:
        log.info('removed {} zones from {}'.format(count, name))


@mission
def remove_building_spawns_near_traders(directory):
    p = pathlib.Path(deploydir.get(), 'mpmissions/dayzOffline.chernarusplus/mapgrouppos.xml')
    count = 0
    mapgroups = ElementTree.parse(p).getroot()
    for group in mapgroups.findall('.//group'):
        raw = group.get('pos')
        # log.info('{} {}'.format(group.get('name'), raw))
        x, y, z = (float(i) for i in raw.split(' '))
        clean_traders = (mark[1] for mark in vpp_map.marks[:4])
        for position in clean_traders:
            if vpp_map.overlaps(position, 200, x, z, 1):
                find_string = './/group[@pos="{}"]...'.format(raw)
                parents = mapgroups.findall(find_string)
                for parent in parents:
                    if group in parent:
                        count += 1
                        parent.remove(group)
                        log.debug('removed group {}, {}, {}'.format(group.get('name'), x, z))
                break
    if count > 0:
        log.info('removed {} groups from {}'.format(count, p.name))
    rough_string = ElementTree.tostring(mapgroups, encoding='unicode')
    spaces = re.compile(r'>\s*<', flags=re.DOTALL)
    rough_string = re.sub(spaces, '>\n<', rough_string)
    reparsed = minidom.parseString(rough_string)
    with file_writing.f_open(pathlib.Path(directory, p.name), mode='w') as f:
        f.write(reparsed.toprettyxml(indent='  ', newl=''))
