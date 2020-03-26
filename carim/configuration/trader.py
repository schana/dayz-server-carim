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
            log.info('added {} items to {}'.format(len(new_category.items), (trader_name, new_category.name)))

    add_dynamic(traders)

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
        current_traders = entry.get('trader')
        if not isinstance(current_traders, list):
            current_traders = [current_traders]
        for trader_name in current_traders:
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
                log.info('added {} dynamic items to {}'.format(len(c.items), (key, c.name)))
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
