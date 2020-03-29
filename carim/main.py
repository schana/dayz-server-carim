import argparse
import json
import logging
import pathlib
import shutil
from xml.etree import ElementTree

from carim import configuration
from carim.configuration.mods.trader import trader
from carim.configuration.server import missions
from carim.configuration.server import types as modify_types
from carim.global_resources import auth, types, configs, outdir, errors, deploydir, locations, mods, resourcesdir


def main():
    parser = argparse.ArgumentParser(description='Automate configuration')
    parser.add_argument('-c', dest='clean', action='store_true', help='clean generated')
    parser.add_argument('-d', dest='deploy', required=True,
                        help='deploy directory containing the original dayz server files')
    parser.add_argument('-a', dest='auth', required=True, help='auth config file')
    parser.add_argument('-o', dest='output', help='output destination directory', default=outdir.get())
    parser.add_argument('-v', dest='verbosity', help='verbosity of the output', action='count', default=0)
    parser.add_argument('-r', dest='resources', help='resources directory to use', default=resourcesdir.get())
    args = parser.parse_args()

    log_level = logging.INFO
    if args.verbosity > 0:
        log_level = logging.DEBUG
    logging.basicConfig(level=log_level, format='%(asctime)s %(levelname)s %(name)s - %(message)s')
    log = logging.getLogger(__name__)

    if args.clean:
        clean()

    # Initialize all the global resources
    outdir.set(args.output)
    deploydir.set(args.deploy)
    resourcesdir.set(args.resources)
    types.set(ElementTree.parse(pathlib.Path(deploydir.get(), 'mpmissions/dayzOffline.chernarusplus/db/types.xml')))
    auth.set(json.load(open(args.auth)))
    locations.initialize()
    with open(pathlib.Path(resourcesdir.get(), 'modifications/omega/mods.json')) as f:
        mods_config = json.load(f)
    for mod in mods_config:
        mods.add(mod.get('directory'))

    # Scan the configurations and apply them
    configuration.scan()
    for c in configs.get():
        c()
    # Unregistered configurations that have a special order requirement
    modify_types.modify_types()
    missions.types_config()
    trader.trader_items()

    log.info('errors {}'.format(len(errors.get())))
    for e in errors.get():
        log.error(e)
    log.info('applied {} registered configurations'.format(len(configs.get())))
    log.debug('order: {}'.format(json.dumps([f.__name__ for f in configs.get()], indent=2)))
    log.info('complete')


def clean():
    log = logging.getLogger(__name__)
    log.info('removing old generated')
    for p in pathlib.Path('.').glob('generated-*'):
        log.info('removing {}'.format(p))
        shutil.rmtree(p)


if __name__ == '__main__':
    main()
