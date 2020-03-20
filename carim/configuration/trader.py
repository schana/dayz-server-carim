import json
import logging
import pathlib

from carim.configuration import profiles
from carim.models import trader, types, trader_objects
from carim.util import file_writing

log = logging.getLogger(__name__)


@profiles.profile(directory='Trader', register=False)  # run after type modifications
def trader_items(directory):
    with open('resources/modifications/trader_inventory.json') as f:
        inventory = json.load(f)

    traders_config = trader.Config()
    traders = ['auto', 'clothing', 'food', 'weapons', 'accessories', 'tools', 'bm']

    for trader_name in traders:
        categories = inventory.get(trader_name, list())
        current_trader = trader.Trader(trader_name)
        traders_config.traders.append(current_trader)
        for category in categories:
            new_category = trader.Category(category.get('category'))
            current_trader.categories.append(new_category)
            build_category(new_category, category)

    clothing_trader = traders_config.traders[1]
    add_cl0ud_clothes(clothing_trader)

    build_green_mountain_free_traders(traders_config)

    with file_writing.f_open(pathlib.Path(directory, 'TraderConfig.txt'), mode='w') as f:
        f.write(traders_config.generate())


def build_green_mountain_free_traders(traders_config):
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
                    weapons.items.append(trader.Weapon(item_name, 0, 0))
                elif cat_name == 'containers':
                    containers.items.append(trader.Singular(item_name, 0, 0))
                elif cat_name == 'clothes':
                    clothes.items.append(trader.Singular(item_name, 0, 0))
                elif cat_name == 'explosives':
                    explosives.items.append(trader.Item(item_name, 1, 0, 0))
                elif cat_name == 'food':
                    food.items.append(trader.Item(item_name, 1, 0, 0))
                elif cat_name == 'tools':
                    tools.items.append(trader.Singular(item_name, 0, 0))

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
        vehicles.items.append(trader.Vehicle(v, 0, 0))

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
    # Order of traders must match markers in trader_locations.json
    traders_config.traders += [vehicles_trader, clothing_trader, food_trader, weapon_trader, accessories_trader,
                               tool_trader]


def build_category(new_category, category_config):
    for item in category_config.get('items', list()):
        item_class = item.get("class", "max")
        if item_class == "vehicle":
            item_type = trader.Vehicle
        elif item_class == "magazine":
            item_type = trader.Magazine
        elif item_class == "weapon":
            item_type = trader.Weapon
        elif item_class == "steak":
            item_type = trader.Steak
        else:
            item_type = trader.Singular
        new_item = item_type(item.get('name'), item.get('buy'), item.get('sell'))
        new_category.items.append(new_item)


def add_cl0ud_clothes(clothing_trader):
    cl0ud_clothes = {}
    for t in types.get().getroot():
        cat = t.find('category')
        if cat is not None:
            cat_name = cat.get('name')
            item_name = t.get('name')
            if t.find('nominal').text != '0':
                if cat_name == 'clothes':
                    if item_name.startswith('MilitaryGear'):
                        parts = item_name.split('_')
                        color = '_'.join(parts[2:])
                        if color not in ('Black', 'Brown', 'Olive', 'Tan'):
                            if color not in cl0ud_clothes:
                                cl0ud_clothes[color] = list()
                            buy, sell = 100, 50
                            if 'PlateCarrier' in item_name:
                                buy, sell = 1000, 500
                            cl0ud_clothes.get(color).append(trader.Singular(item_name, buy, sell))
    for k, items in cl0ud_clothes.items():
        new_category = trader.Category('Cl0uds {}'.format(k))
        new_category.items = items
        clothing_trader.categories.append(new_category)


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
