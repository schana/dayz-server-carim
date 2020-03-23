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
        matching = action.get('matching')
        process_type = remove if action['action'] == 'remove' else modify
        for m in matching:
            process_type(matching=m, modification=action.get('modification', dict()))


class Fields:
    NAME = 'name'
    CATEGORY = 'category'
    VALUE = 'value'
    OPERATOR = 'operator'


class Match:
    def __init__(self, matching):
        self.fields = {Fields.OPERATOR: all}
        if Fields.NAME in matching:
            self.fields[Fields.NAME] = re.compile(matching.get(Fields.NAME))
        if Fields.CATEGORY in matching:
            self.fields[Fields.CATEGORY] = re.compile(matching.get(Fields.CATEGORY).get('name'))
        if Fields.VALUE in matching:
            self.fields[Fields.VALUE] = []
            for value in matching.get(Fields.VALUE):
                self.fields[Fields.VALUE].append(re.compile(value.get('name')))
        if Fields.OPERATOR in matching:
            self.fields[Fields.OPERATOR] = any if matching.get(Fields.OPERATOR).lower() == 'any' else all

    def match(self, t):
        match_result = MatchResult(self.fields[Fields.OPERATOR])
        if Fields.NAME in self.fields:
            match_result.add_interim(self.fields[Fields.NAME].match(t.attrib.get(Fields.NAME)))
        if Fields.CATEGORY in self.fields:
            category = t.find(Fields.CATEGORY)
            if category is None:
                match_result.add_interim(False)
            else:
                match_result.add_interim(self.fields[Fields.CATEGORY].match(category.attrib.get('name')))
        if Fields.VALUE in self.fields:
            if len(self.fields[Fields.VALUE]) == 0:
                if t.find(Fields.VALUE) is None:
                    match_result.add_interim(True)
                else:
                    match_result.add_interim(False)
            for value_match in self.fields[Fields.VALUE]:
                r = False
                for value in t.findall(Fields.VALUE):
                    m = value_match.match(value.attrib.get('name'))
                    if m:
                        r = True
                        match_result.add_interim(m)
                if not r:
                    match_result.add_interim(r)
        return match_result


class MatchResult:
    def __init__(self, operator):
        self.groups = dict()
        self.interim_results = list()
        self.operator = operator

    def add_interim(self, result):
        if result:
            self.interim_results.append(bool(result))
            if isinstance(result, re.Match) and result.groupdict():
                self.groups = dict(**self.groups, **result.groupdict())
        else:
            self.interim_results.append(False)

    def get_result(self):
        return self.operator(self.interim_results)

    def __bool__(self):
        return self.get_result()


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
        },
        {
            "name": "deloot",
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
