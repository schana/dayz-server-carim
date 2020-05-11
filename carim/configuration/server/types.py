import json
import logging
import pathlib
from xml.etree import ElementTree

from carim.configuration import decorators
from carim.global_resources import types, item_type, matching_model, resourcesdir, mission

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
        process_type = remove if action['action'] == 'remove' else modify
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
            t.find('nominal').text = str(int(ratio_modifier * int(t.find('nominal').text)))
            t.find('min').text = str(int(ratio_modifier * int(t.find('min').text)))
    log.info('modified {} items with ratio {}'.format(count, ratio_modifier))


def remove(matching=None, modification=None):
    match = matching_model.Match(matching)
    count = 0
    for t in types.get().getroot():
        if match.match(t):
            count += 1
            log.debug('removing ' + t.attrib.get('name'))
            apply_modification(t, _REMOVE_MODIFICATION)
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
