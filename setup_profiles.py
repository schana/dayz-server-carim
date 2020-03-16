import argparse
import functools
import itertools
import logging
import pathlib
import shutil
import time
import json
import trader
import xml.etree.ElementTree as ET

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s - %(message)s')
log = logging.getLogger('profiles')
DIR = time.strftime('generated-%Y%m%d%H%M%S', time.gmtime())
configs = []
types = ET.ElementTree()
auth = {}


def config(_func=None, *, directory=None):
    def config_decorator(func):
        @functools.wraps(func)
        def config_wrapper(*args, **kwargs):
            log.info('processing {}'.format(func.__name__))
            if directory is not None:
                p = pathlib.Path(DIR, directory)
                p.mkdir(parents=True, exist_ok=True)
                log.info('created directory {}'.format(directory))
                return func(*args, **kwargs, directory=str(p))
            else:
                return func(*args, **kwargs)

        configs.append(config_wrapper)
        return config_wrapper

    if _func is None:
        return config_decorator
    else:
        return config_decorator(_func)


def located_config(_func=None, *, directory=None, dir_prefix=None):
    if _func is None:
        if directory is not None:
            return config(directory=str(pathlib.Path(dir_prefix, directory)))
        else:
            return config
    else:
        if directory is not None:
            return config(_func, directory=str(pathlib.Path(dir_prefix, directory)))
        else:
            return config(_func)


def profile(_func=None, *, directory=None):
    return located_config(_func, directory=directory, dir_prefix='servers/0/profiles')


def game(_func=None, *, directory=None):
    return located_config(_func, directory=directory, dir_prefix='servers/0/mpmissions/dayzOffline.chernarusplus')


@profile(directory='Trader')
def trader_file_and_admins(directory):
    for p in pathlib.Path('omega/Trader').glob('*'):
        shutil.copy(p, directory)
    with open(pathlib.Path(directory, 'TraderAdmins.txt'), mode='w') as f:
        for superuser in auth.get('superusers', []):
            log.info('adding {} as trader admin'.format(superuser['name']))
            f.write(superuser['steam64'] + '\n')
        f.write('<FileEnd>')


@profile(directory='Airdrop')
def airdrop(directory):
    p = pathlib.Path('omega/Airdrop/AirdropSettings.json')
    shutil.copy(p, directory)


@profile(directory='SimpleBase')
def simple_base(directory):
    with open('omega/Simple Base/types.xml') as f:
        it = itertools.chain('<type>', f, '</type>')
        new_types = ET.fromstringlist(it)
    types.getroot().extend(new_types)
    # profile config
    # destruction config


@profile(directory='VPPAdminTools/Permissions/SuperAdmins')
def vpp_admin_tools_permissions(directory):
    with open(pathlib.Path(directory, 'SuperAdmins.txt'), mode='w') as f:
        for superuser in auth.get('superusers', []):
            log.info('adding {} as superuser'.format(superuser['name']))
            f.write(superuser['steam64'] + '\n')


@profile(directory='CodeLock')
def code_lock(directory):
    new_type = ET.parse('omega/Code Lock/types.xml')
    types.getroot().append(new_type.getroot())
    # config
    users = []
    for superuser in auth.get('superusers', []):
        users.append({
            'playerId': superuser['steam64'],
            'playerPerms': {
                'CanOpenLocks': "true",
                'CanChangePasscodes': "true",
                'CanRemoveLocks': "true"
            }
        })
        log.info('adding {} as code lock admin'.format(superuser['name']))
    with open(pathlib.Path(directory, 'CodeLockPerms.json'), mode='w') as f:
        json.dump(users, f, indent=2)


@profile
def items_clouds():
    with open('omega/Cl0uds/Types V9.1 only.xml') as f:
        it = itertools.chain('<type>', f, '</type>')
        new_types = ET.fromstringlist(it)
    types.getroot().extend(new_types)


@profile
def items_mass():
    new_types = ET.parse('omega/MasssManyItemOverhaul/types(NOT A REPLACER).xml')
    types.getroot().extend(new_types.getroot())


@profile
def items_msfc():
    for p in pathlib.Path('omega/MSF-C').glob('*.xml'):
        with open(p) as f:
            it = itertools.chain('<type>', f, '</type>')
            new_types = ET.fromstringlist(it)
        types.getroot().extend(new_types)


@profile
def items_munghards():
    for p in pathlib.Path('omega/MunghardsItemPack/types').glob('*.xml'):
        new_types = ET.parse(p)
        types.getroot().extend(new_types.getroot())


@profile
def vanilla_plus_plus_map():
    # map config
    pass


@game(directory='db')
def types_config(directory):
    types.write(pathlib.Path(directory, 'types.xml'))


@config(directory='servers/0')
def omega_config(directory):
    cfg = None
    with open('omega/omega.cfg') as f:
        cfg = json.load(f)
    cfg['cftools']['service_api_key'] = auth['cf']['service_api_key']
    cfg['cftools']['service_id'] = auth['cf']['service_id']
    with open(pathlib.Path(directory, 'omega.cfg'), mode='w') as f:
        json.dump(cfg, f, indent=2)


@config(directory='servers/0/profiles')
def cf_tools_config(directory):
    cfg = {
        'service_api_key': auth['cf']['service_api_key'],
        'service_id': auth['cf']['service_id']
    }
    with open(pathlib.Path(directory, 'cftools.cfg'), mode='w') as f:
        json.dump(cfg, f, indent=2)


@config(directory='.')
def omega_manager(directory):
    cfg = None
    with open('omega/manager.cfg') as f:
        cfg = json.load(f)
    cfg['steam'] = {
        'username': auth['steam']['username'],
        'api_key': auth['steam']['api_key'],
        'password': auth['steam']['password'],
        'mobile_authenticator': False
    }
    with open(pathlib.Path(directory, 'manager.cfg'), mode='w') as f:
        json.dump(cfg, f, indent=2)


@profile(directory='Trader')
def trader_items(directory):
    food = trader.Category('Food')
    weapons = trader.Category('Weapons')
    explosives = trader.Category('Explosives')
    clothes = trader.Category('Clothes')
    containers = trader.Category('Containers')
    tools = trader.Category('Tools')
    other = trader.Category('Other')
    vehicles = trader.Category('Vehicles')

    for t in types.getroot():
        cat = t.find('category')
        if cat is not None:
            cat_name = cat.get('name')
            item_name = t.get('name')
            if cat_name == 'weapons':
                weapons.items.append(trader.Weapon(item_name, 1, 1))
            elif cat_name == 'containers':
                containers.items.append(trader.Singular(item_name, 1, 1))
            elif cat_name == 'clothes':
                clothes.items.append(trader.Singular(item_name, 1, 1))
            elif cat_name == 'explosives':
                explosives.items.append(trader.Item(item_name, 1, 1, 1))
            elif cat_name == 'food':
                food.items.append(trader.Item(item_name, 1, 1, 1))
            elif cat_name == 'tools':
                tools.items.append(trader.Singular(item_name, 1, 1))
            else:
                other.items.append(trader.Item(item_name, 1, 1, 1))

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
    accessories_trader.categories = [other]
    clothing_trader.categories = [clothes]
    vehicles_trader.categories = [containers, vehicles]

    trader_config = trader.Config()
    trader_config.traders = [food_trader, tool_trader, weapon_trader, accessories_trader, clothing_trader, vehicles_trader]
    with open(pathlib.Path(directory, 'TraderConfig.txt'), mode='w') as f:
        f.write(trader_config.generate())


def clean():
    log.info('removing old generated')
    for p in pathlib.Path('.').glob('generated-*'):
        log.info('removing {}'.format(p))
        shutil.rmtree(p)


def main():
    global types, auth
    parser = argparse.ArgumentParser(description='Automate configuration')
    parser.add_argument('-c', dest='clean', action='store_true', help='clean generated')
    parser.add_argument('-d', dest='deploy', required=True,
                        help='deploy directory containing the original dayz server files')
    parser.add_argument('-a', dest='auth', required=True, help='auth config file')
    args = parser.parse_args()
    if args.clean:
        clean()
    types = ET.parse(pathlib.Path(args.deploy, 'mpmissions/dayzOffline.chernarusplus/db/types.xml'))
    auth = json.load(open(args.auth))
    for c in configs:
        c()
    log.info('complete')
    cats = set()
    for t in types.getroot():
        c = t.find('category')
        if c is not None:
            cats.add(c.get('name'))
    print(cats)


if __name__ == '__main__':
    main()
