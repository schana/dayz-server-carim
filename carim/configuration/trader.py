import json
import logging
import pathlib

from carim.configuration import profiles
from carim.models import trader, types, trader_objects
from carim.util import file_writing, modify_types

log = logging.getLogger(__name__)


class TraderName:
    AUTO = 'auto'
    CLOTHING = 'clothing'
    FOOD = 'food'
    WEAPONS = 'weapons'
    ACCESSORIES = 'accessories'
    TOOLS = 'tools'
    BM = 'bm'


@profiles.profile(directory='Trader', register=False)  # run after type modifications
def trader_items(directory):
    with open('resources/modifications/trader_inventory.json') as f:
        inventory = json.load(f)

    traders_config = trader.Config()
    trader_names = [
        TraderName.AUTO,
        TraderName.CLOTHING,
        TraderName.FOOD,
        TraderName.WEAPONS,
        TraderName.ACCESSORIES,
        TraderName.TOOLS,
        TraderName.BM
    ]
    traders = {}

    for trader_name in trader_names:
        categories = inventory.get(trader_name, list())
        current_trader = trader.Trader(trader_name)
        traders[trader_name] = current_trader
        traders_config.traders.append(current_trader)
        for category in categories:
            new_category = trader.Category(category.get('category'))
            current_trader.categories.append(new_category)
            build_category(new_category, category)

    add_dynamic(traders)
    build_green_mountain_free_traders(traders_config)

    with file_writing.f_open(pathlib.Path(directory, 'TraderConfig.txt'), mode='w') as f:
        f.write(traders_config.generate())


def build_category(new_category, category_config):
    for item in category_config.get('items', list()):
        item_class = item.get("class", "max")
        item_type = get_item_type_for_name(item_class)
        new_item = item_type(item.get('name'), item.get('buy'), item.get('sell'))
        new_category.items.append(new_item)


def get_item_type_for_name(name):
    if name == "vehicle":
        return trader.Vehicle
    elif name == "magazine":
        return trader.Magazine
    elif name == "weapon":
        return trader.Weapon
    elif name == "steak":
        return trader.Steak
    elif name == "quantity":
        return trader.Item
    else:
        return trader.Singular


def add_dynamic(traders):
    with open('resources/modifications/trader_inventory_dynamic.json') as f:
        trader_config = json.load(f)
    temp_traders = {}
    for entry in trader_config:
        trader_name = entry.get('trader')
        if trader_name not in temp_traders:
            temp_traders[trader_name] = list()
        category_name = entry.get('category')
        categories = {}
        temp_traders[trader_name].append(categories)
        for item in entry.get('items'):
            expanded = {}
            matching = item.get('matching')
            buy = item.get('buy')
            sell = item.get('sell')
            quantity = item.get('quantity', None)
            item_type = get_item_type_for_name(item.get('item_class'))
            match = modify_types.Match(matching)
            for t in types.get().getroot():
                result = match.match(t)
                if result:
                    items = expanded.get(result.groups.get('captured'), list())
                    items.append(trader.Singular(t.get('name'), item.get('buy'), item.get('sell')))
                    expanded[result.groups.get('captured')] = items
            for key in expanded:
                current_cat_name = category_name.format(captured=key)
                current_cat = categories.get(current_cat_name, trader.Category(current_cat_name))
                if quantity is not None:
                    current_cat.items += [item_type(i.name, buy, sell, quantity) for i in expanded[key] if
                                          i not in current_cat]
                else:
                    current_cat.items += [item_type(i.name, buy, sell) for i in expanded[key] if i not in current_cat]
                categories[current_cat_name] = current_cat
    for key in temp_traders:
        for cat_set in temp_traders[key]:
            for c in cat_set.values():
                log.info('added {} items to {}'.format(len(c.items), (key, c.name)))
            traders[key].categories += cat_set.values()


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
