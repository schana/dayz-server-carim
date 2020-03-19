import json
import logging
import pathlib

from carim.configuration import profiles
from carim.models import trader, types, trader_objects
from carim.util import file_writing

log = logging.getLogger(__name__)


@profiles.profile(directory='Trader', register=False)  # Needs to be generated after types are modified
def trader_items(directory):
    food = trader.Category('Food')
    weapons = trader.Category('Weapons')
    explosives = trader.Category('Explosives')
    clothes = trader.Category('Clothes')
    containers = trader.Category('Containers')
    tools = trader.Category('Tools')
    vehicles = trader.Category('Vehicles')

    for t in types.get().getroot():
        cat = t.find('category')
        if cat is not None:
            cat_name = cat.get('name')
            item_name = t.get('name')
            if t.find('nominal').text != '0':
                if cat_name == 'weapons':
                    weapons.items.append(trader.Weapon(item_name, 0, 1))
                elif cat_name == 'containers':
                    containers.items.append(trader.Singular(item_name, 0, 1))
                elif cat_name == 'clothes':
                    clothes.items.append(trader.Singular(item_name, 0, 1))
                elif cat_name == 'explosives':
                    explosives.items.append(trader.Item(item_name, 1, 0, 1))
                elif cat_name == 'food':
                    food.items.append(trader.Item(item_name, 1, 0, 1))
                elif cat_name == 'tools':
                    tools.items.append(trader.Singular(item_name, 0, 1))

    for v in ('OffroadHatchback',
              'OffroadHatchback_Blue',
              'OffroadHatchback_White',
              'Hatchback_02',
              'Hatchback_02_Blue',
              'Hatchback_02_Black',
              'Sedan_02',
              'Sedan_02_Red',
              'Sedan_02_Grey',
              'CivilianSedan',
              'CivilianSedan_Wine',
              'CivilianSedan_Black',
              'CrSk_BMW_525i_E34_black'):
        vehicles.items.append(trader.Vehicle(v, 1, 1))

    food_trader = trader.Trader('Food')
    tool_trader = trader.Trader('Tools')
    weapon_trader = trader.Trader('Weapons')
    accessories_trader = trader.Trader('Accessories')
    clothing_trader = trader.Trader('Clothing')
    vehicles_trader = trader.Trader('Vehicles')

    food_trader.categories = [food]
    tool_trader.categories = [tools]
    weapon_trader.categories = [weapons, explosives]
    accessories_trader.categories = []
    clothing_trader.categories = [clothes]
    vehicles_trader.categories = [containers, vehicles]

    trader_config = trader.Config()
    # Order of traders must match markers in trader_locations.json
    trader_config.traders = [vehicles_trader, clothing_trader, food_trader, weapon_trader, accessories_trader,
                             tool_trader]
    with file_writing.f_open(pathlib.Path(directory, 'TraderConfig.txt'), mode='w') as f:
        f.write(trader_config.generate())


@profiles.profile(directory='Trader')
def trader_objects_config(directory):
    to = trader_objects.Config()
    with open('resources/modifications/trader_locations.json') as f:
        locations = json.load(f)
    with open('resources/modifications/trader_outfits.json') as f:
        outfits = json.load(f)
    for name, config in locations.items():
        log.info('processing {}'.format(name))
        for trader_name, t in config.items():
            new_trader = trader_objects.Trader(t.get('marker'), t.get('location'), t.get('safezone', 200))
            new_object = trader_objects.Object(outfits.get(trader_name).get('class'), t.get('location'), t.get('o'))
            for attachment in outfits.get(trader_name).get('attachments'):
                new_object.attachments.append(trader_objects.Attachment(attachment))
            if 'vehicle' in t:
                raw_vehicle = t.get('vehicle')
                new_trader.set_vehicle(trader_objects.Vehicle(raw_vehicle.get('location'), raw_vehicle.get('o')))
            to.traders.append(new_trader)
            to.objects.append(new_object)

    with file_writing.f_open(pathlib.Path(directory, 'TraderObjects.txt'), mode='w') as f:
        f.write(to.generate())
