import argparse
import json
import logging
import pathlib
import shutil
from xml.etree import ElementTree

from carim import configuration
from carim.configuration import trader, missions
from carim.models import auth, types, configs, outdir, errors, vpp_map, deploydir
from carim.util import modify_types

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s - %(message)s')
log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Automate configuration')
    parser.add_argument('-c', dest='clean', action='store_true', help='clean generated')
    parser.add_argument('-d', dest='deploy', required=True,
                        help='deploy directory containing the original dayz server files')
    parser.add_argument('-a', dest='auth', required=True, help='auth config file')
    parser.add_argument('-o', dest='output', help='output destination directory', default=outdir.get())
    args = parser.parse_args()
    if args.clean:
        clean()

    outdir.set(args.output)
    deploydir.set(args.deploy)
    types.set(ElementTree.parse(pathlib.Path(deploydir.get(), 'mpmissions/dayzOffline.chernarusplus/db/types.xml')))
    auth.set(json.load(open(args.auth)))
    vpp_map.initialize()
    configuration.scan()

    for c in configs.get():
        c()
    modify_types.modify_types()
    missions.types_config()
    trader.trader_items()

    log.info('errors {}'.format(len(errors.get())))
    for e in errors.get():
        log.error(e)
    log.info('complete')


def clean():
    log.info('removing old generated')
    for p in pathlib.Path('.').glob('generated-*'):
        log.info('removing {}'.format(p))
        shutil.rmtree(p)


if __name__ == '__main__':
    main()
