import json
import pathlib
import re
from xml.etree import ElementTree

from carim.configuration import decorators
from carim.global_resources import deploydir, mission, resourcesdir, types as db_types
from carim.util import file_writing


@decorators.register
@decorators.mission
def spawnable_types_config(directory):
    """
    This configuration operates in an overriding fashion. That is, if a preset or list of items is specified
    for a type in the config, any existing entries for that type with the same tag and attribute will be erased.
    """
    p = pathlib.Path(deploydir.get(), 'mpmissions', mission.get(), 'cfgspawnabletypes.xml')
    with open(p) as f:
        # The parser in ElementTree was having trouble with the comments in the xml file
        # So, we're removing them manually beforehand
        raw = f.read()
        raw = re.sub(r'<!--.*-->', '', raw)
        spawnable_xml = ElementTree.fromstring(raw)
    with open(pathlib.Path(resourcesdir.get(), 'modifications/server/spawnable_types.json')) as f:
        spawnable_modifications = json.load(f)
    for type_config in spawnable_modifications:
        if len(db_types.get().getroot().findall('.//type[@name="{}"]'.format(type_config.get('type')))) == 0:
            continue
        types = spawnable_xml.findall('.//type[@name="{}"]'.format(type_config.get('type')))
        if len(types) == 0:
            new_type = ElementTree.SubElement(spawnable_xml, 'type', dict(name=type_config.get('type')))
            types = [new_type]
        for t in types:
            if 'cargo_presets' in type_config:
                handle_presets(t, 'cargo', type_config.get('cargo_presets'))
            if 'attachments_presets' in type_config:
                handle_presets(t, 'attachments', type_config.get('attachments_presets'))
            if 'cargo_items' in type_config:
                handle_items(t, 'cargo', type_config.get('cargo_items'))
            if 'attachments' in type_config:
                handle_items(t, 'attachments', type_config.get('attachments'))
    with file_writing.f_open(pathlib.Path(directory, 'cfgspawnabletypes.xml'), mode='w') as f:
        f.write(file_writing.convert_to_string(spawnable_xml))


def handle_presets(type_element, preset_type, config):
    for cp in type_element.findall('.//{}[@preset]'.format(preset_type)):
        type_element.remove(cp)
    for preset in config:
        ElementTree.SubElement(type_element, preset_type, dict(preset=preset))


def handle_items(type_element, preset_type, config):
    for cp in type_element.findall('.//{}[@chance]'.format(preset_type)):
        type_element.remove(cp)
    for group in config:
        e = ElementTree.SubElement(type_element, preset_type, dict(chance=group.get('chance')))
        for item in group.get('items'):
            ElementTree.SubElement(e, 'item', dict(name=item.get('name'), chance=item.get('chance')))
