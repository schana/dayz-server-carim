import json
import logging
import re
from xml.etree import ElementTree

from carim.configuration import base
from carim.models import types, item_type

log = logging.getLogger(__name__)


@base.server(directory='mpmissions/dayzOffline.chernarusplus/db', register=False)
def modify_types(directory):
    with open('resources/modifications/types_config.json') as f:
        type_config = json.load(f)
    for action in type_config:
        matching = action.get('matching', list())
        process_type = remove if action['action'] == 'remove' else modify
        if len(matching) > 0:
            for m in matching:
                process_type(matching=m, modification=action.get('modification', dict()))
        else:
            process_type(modification=action.get('modification', dict()))


class Match:
    def __init__(self, matching):
        self.name_re = re.compile('.*')
        self.category_re = re.compile('.*')
        if matching is not None:
            self.name_re = re.compile(matching.get('name', '.*'))
            self.category_re = re.compile(matching.get('category', dict()).get('name', '.*'))

    def match(self, t):
        if not self.name_re.match(t.attrib.get('name')):
            return False
        category = t.find('category')
        if category is None:
            return False
        if not self.category_re.match(category.attrib.get('name')):
            return False
        return True


_MAX_TIME = 3888000
_REMOVE_MODIFICATION = {
    "nominal": 0,
    "lifetime": 0,
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


def remove(matching=None, modification=None):
    match = Match(matching)
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
    match = Match(matching)
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
            if not modification.get(field).isempty():
                ElementTree.SubElement(item_element, field, attrib=modification.get(field))

    field = 'flags'
    if modification.get(field) is not None:
        for child in item_element.findall(field):
            for flag in modification.get(field):
                child.set(flag.get('name'), "1" if flag.get('value') else "0")
