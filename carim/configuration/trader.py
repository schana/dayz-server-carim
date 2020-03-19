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

    # TODO: stop repeating this array
    traders = ['auto', 'clothing', 'food', 'weapons', 'accessories', 'tools', 'bm']
    traders_config = trader.Config()
    for trader_name in traders:
        categories = inventory.get(trader_name, list())
        current_trader = trader.Trader(trader_name)
        traders_config.traders.append(current_trader)
        for category in categories:
            new_category = trader.Category(category.get('category'))
            current_trader.categories.append(new_category)
            for item in category.get('items', list()):
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

    clothing_trader = traders_config.traders[1]
    add_cl0ud_clothes(clothing_trader)
    with file_writing.f_open(pathlib.Path(directory, 'TraderConfig.txt'), mode='w') as f:
        f.write(traders_config.generate())


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
