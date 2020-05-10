import json
import logging
import math
import pathlib
import re
from xml.etree import ElementTree

from carim.configuration import decorators
from carim.global_resources import types, deploydir, resourcesdir, mission
from carim.util import file_writing

log = logging.getLogger(__name__)


@decorators.mission(directory='db')
def sort_and_write_types_config(directory):
    types.get().getroot()[:] = sorted(types.get().getroot(), key=lambda child: child.get('name').lower())
    with file_writing.f_open(pathlib.Path(directory, 'types.xml'), mode='w') as f:
        f.write(file_writing.convert_to_string(types.get().getroot()))


@decorators.register
@decorators.mission(directory='db')
def globals_config(directory):
    globals_xml = ElementTree.parse(
        pathlib.Path(deploydir.get(), 'mpmissions', mission.get(), 'db/globals.xml'))
    with open(pathlib.Path(resourcesdir.get(), 'modifications/server/globals.json')) as f:
        globals_modifications = json.load(f)
    for k, v in globals_modifications.items():
        item = globals_xml.getroot().find('.//var[@name="{}"]'.format(k))
        item.set('value', str(v))
    with file_writing.f_open(pathlib.Path(directory, 'globals.xml'), mode='w') as f:
        f.write(file_writing.convert_to_string(globals_xml.getroot()))


@decorators.register
@decorators.mission(directory='db')
def events_config(directory):
    events_xml = ElementTree.parse(
        pathlib.Path(deploydir.get(), 'mpmissions', mission.get(), 'db/events.xml'))
    with open(pathlib.Path(resourcesdir.get(), 'modifications/server/events.json')) as f:
        events_modifications = json.load(f)
    for mod in events_modifications:
        name_re = re.compile(mod.get('name'))
        for event in events_xml.getroot():
            if name_re.match(event.get('name')):
                ratio = mod.get('ratio')
                if ratio > 0:
                    event.find('active').text = '1'
                    for item in ('nominal',):
                        i = event.find(item)
                        i.text = str(math.floor(max(1, int(i.text)) * ratio))
                else:
                    event.find('active').text = '0'
    with file_writing.f_open(pathlib.Path(directory, 'events.xml'), mode='w') as f:
        f.write(file_writing.convert_to_string(events_xml.getroot()))
