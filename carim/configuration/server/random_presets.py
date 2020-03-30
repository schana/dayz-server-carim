import json
import pathlib
import re
from xml.etree import ElementTree

from carim.configuration import decorators
from carim.global_resources import deploydir, mission, resourcesdir
from carim.util import file_writing


@decorators.register
@decorators.mission
def random_presets_config(directory):
    p = pathlib.Path(deploydir.get(), 'mpmissions', mission.get(), 'cfgrandompresets.xml')
    with open(p) as f:
        # The parser in ElementTree was having trouble with the comments in the xml file
        # So, we're removing them manually beforehand
        raw = f.read()
        raw = re.sub(r'<!--.*-->', '', raw)
        presets_xml = ElementTree.fromstring(raw)
    with open(pathlib.Path(resourcesdir.get(), 'modifications/server/random_presets.json')) as f:
        presets_modifications = json.load(f)
    for entry in presets_modifications:
        if 'cargo' in entry:
            cargo = entry.get('cargo')
            for item in entry.get('items'):
                for preset in presets_xml.findall(
                        './/cargo[@name="{}"]//item[@name="{}"]'.format(cargo, item.get('name'))):
                    preset.set('chance', item.get('chance'))
        if 'attachments' in entry:
            attachments = entry.get('attachments')
            for item in entry.get('items'):
                for preset in presets_xml.findall(
                        './/attachments[@name="{}"]//item[@name="{}"]'.format(attachments, item.get('name'))):
                    preset.set('chance', item.get('chance'))
    with file_writing.f_open(pathlib.Path(directory, 'cfgrandompresets.xml'), mode='w') as f:
        f.write(file_writing.convert_to_string(presets_xml))
