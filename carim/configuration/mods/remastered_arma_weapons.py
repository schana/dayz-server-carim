from xml.etree import ElementTree

from carim.configuration import decorators
from carim.global_resources import types


@decorators.register
@decorators.mod('@[Remastered] Arma Weapon Pack')
@decorators.profile
def items_remastered_arma():
    raw = '<types>'
    with open('resources/original-mod-files/[Remastered] Arma Weapon Pack/class_names.txt') as f:
        for line in f:
            type_name = line.strip()
            raw += (
                f'<type name="{type_name}">'
                '<nominal>5</nominal>'
                '<lifetime>10800</lifetime>'
                '<restock>1800</restock>'
                '<min>1</min>'
                '<quantmin>-1</quantmin>'
                '<quantmax>-1</quantmax>'
                '<cost>100</cost>'
                '<flags count_in_cargo="1" count_in_hoarder="1" count_in_map="1" count_in_player="0" crafted="0" deloot="0"/>'
                '<category name="weapons"/>'
                '<usage name="Military"/>'
                '<value name="Tier4"/>'
                '<value name="Tier3"/>'
                '</type>'
            )
    raw += '</types>'
    new_types = ElementTree.fromstring(raw)
    types.get().getroot().extend(new_types)
