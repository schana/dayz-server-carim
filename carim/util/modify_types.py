import json
import logging
import re

from carim.configuration import base
from carim.models import types

log = logging.getLogger(__name__)


@base.server(directory='mpmissions/dayzOffline.chernarusplus/db', register=False)
def modify_types(directory):
    with open('omega/types_config.json') as f:
        type_config = json.load(f)
    for action in type_config:
        matching = action.get('matching', list())
        process_type = remove if action['action'] == 'remove' else modify
        if len(matching) > 0:
            for m in matching:
                process_type(matching=m, modifications=action.get('modifications', dict()))
        else:
            process_type(modifications=action.get('modifications', dict()))


def remove(matching=None, modifications=None):
    name_re = re.compile('.*')
    category_re = re.compile('.*')
    if matching is not None:
        name_re = re.compile(matching.get('name', '.*'))
        category_re = re.compile(matching.get('category', dict()).get('name', '.*'))

    for t in types.get().getroot():
        if not name_re.match(t.attrib.get('name')):
            continue
        category = t.find('category')
        if category is None:
            continue
        if not category_re.match(category.attrib.get('name')):
            continue

        log.info('removing ' + t.attrib.get('name'))


def modify(matching=None, modifications=None):
    if modifications is None:
        modifications = {}
    log.info('modifying')
    pass


