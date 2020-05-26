import json
import logging
import pathlib
from xml.etree import ElementTree

from carim.configuration import decorators
from carim.global_resources import types, item_type, matching_model, resourcesdir, mission, deploydir, locations
from carim.util import file_writing

log = logging.getLogger(__name__)
_MAX_TIME = 3888000
_REMOVE_MODIFICATION = {
    "nominal": 0,
    "lifetime": 1,
    "restock": _MAX_TIME,
    "min": 0,
    "cost": 0,
    "flags": [
        {
            "name": "count_in_cargo",
            "value": True
        },
        {
            "name": "count_in_hoarder",
            "value": True
        },
        {
            "name": "count_in_map",
            "value": True
        },
        {
            "name": "count_in_player",
            "value": True
        }
    ],
    "value": []
}


@decorators.server(directory='mpmissions/' + mission.get() + '/db')
def modify_types(directory):
    with open(pathlib.Path(resourcesdir.get(), 'modifications/server/types_config.json')) as f:
        type_config = json.load(f)
    for action in type_config:
        log.info(action.get('description'))
        matching = action.get('matching')
        if action['action'] == 'remove':
            process_type = remove
        elif action['action'] == 'ratio':
            process_type = ratio
        else:
            process_type = modify
        for m in matching:
            process_type(matching=m, modification=action.get('modification', dict()))

    with open(pathlib.Path(resourcesdir.get(), 'modifications/server/types_universal.json')) as f:
        type_universal_config = json.load(f)
    ratio_modifier = type_universal_config.get('ratio', 1)
    matching = {
        "nominal": "^[^0]"
    }
    m = matching_model.Match(matching)
    count = 0
    for t in types.get().getroot():
        if m.match(t) and t.find('nominal') is not None:
            count += 1
            t.find('nominal').text = str(max(1, int(ratio_modifier * int(t.find('nominal').text))))
            t.find('min').text = str(max(1, int(ratio_modifier * int(t.find('min').text))))
    log.info('modified {} items with ratio {}'.format(count, ratio_modifier))


def remove(matching=None, modification=None):
    match = matching_model.Match(matching)
    count = 0
    to_remove = list()
    for t in types.get().getroot():
        if match.match(t):
            count += 1
            log.debug('removing ' + t.attrib.get('name'))
            to_remove.append(t)
            # types.get().getroot().remove(t)
            # apply_modification(t, _REMOVE_MODIFICATION)
    for t in to_remove:
        types.get().getroot().remove(t)
    log.info('removed {} items matching {}'.format(count, matching))


def modify(matching=None, modification=None):
    if modification is None:
        return
    match = matching_model.Match(matching)
    count = 0
    for t in types.get().getroot():
        if match.match(t):
            count += 1
            log.debug('modifying ' + t.attrib.get('name'))
            apply_modification(t, modification)
    log.info('modified {} items matching {} with {}'.format(count, matching, json.dumps(modification)))


def ratio(matching=None, modification=None):
    match = matching_model.Match(matching)
    count = 0
    ratio_modifier = modification.get('ratio')
    for t in types.get().getroot():
        if match.match(t) and t.find('nominal') is not None:
            count += 1
            t.find('nominal').text = str(max(1, int(ratio_modifier * int(t.find('nominal').text))))
            t.find('min').text = str(max(1, int(ratio_modifier * int(t.find('min').text))))
            count += 1
            log.debug('applying ratio to ' + t.attrib.get('name'))
    log.info('modified {} items with ratio {}'.format(count, ratio_modifier))


def apply_modification(item_element: ElementTree.Element, modification):
    template = item_type.modification_template

    text_fields = [k for k in template.keys() if template.get(k) == 1]
    for field in text_fields:
        if modification.get(field) is not None:
            if item_element.find(field) is not None:
                item_element.find(field).text = str(modification.get(field))

    array_fields = [k for k in template.keys() if k != 'flags' and isinstance(template.get(k), list)]
    for field in array_fields:
        if modification.get(field) is not None:
            for child in item_element.findall(field):
                item_element.remove(child)
            values = modification.get(field)
            for value in values:
                ElementTree.SubElement(item_element, field, attrib=value)

    attribute_fields = [k for k in template.keys() if k != 'flags' and isinstance(template.get(k), dict)]
    for field in attribute_fields:
        if modification.get(field) is not None:
            for child in item_element.findall(field):
                item_element.remove(child)
            if modification.get(field):
                ElementTree.SubElement(item_element, field, attrib=modification.get(field))

    field = 'flags'
    if modification.get(field) is not None:
        for child in item_element.findall(field):
            for flag in modification.get(field):
                child.set(flag.get('name'), "1" if flag.get('value') else "0")


@decorators.register
@decorators.mission
def remove_spawns_outside_radius(directory):
    with open(pathlib.Path(resourcesdir.get(), 'modifications/server/types_universal.json')) as f:
        type_universal_config = json.load(f)
    radius = type_universal_config.get('limit_spawn_locations_radius', 0)
    if radius <= 0:
        return
    p = pathlib.Path(deploydir.get(), 'mpmissions', mission.get(), 'mapgrouppos.xml')
    count = 0
    areas = list(mark[1] for mark in locations.marks[:4])
    mapgroups = ElementTree.parse(p).getroot()
    for group in mapgroups.findall('.//group'):
        raw = group.get('pos')
        # log.info('{} {}'.format(group.get('name'), raw))
        x, y, z = (float(i) for i in raw.split(' '))
        is_good = False
        for position in areas:
            if locations.overlaps(position, radius, x, z, 1):
                is_good = True
        if not is_good:
            mapgroups.remove(group)
            count += 1
            log.debug('removed group {}, {}, {}'.format(group.get('name'), x, z))

    if count > 0:
        log.info('removed {} groups from {}'.format(count, p.name))
    with file_writing.f_open(pathlib.Path(directory, p.name), mode='w') as f:
        f.write(file_writing.convert_to_string(mapgroups))
