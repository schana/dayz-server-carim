import argparse
import pathlib
import shutil
import json
from xml.etree import ElementTree
import logging
from carim.models import auth, types, configs
from carim import configuration

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s - %(message)s')
log = logging.getLogger(__name__)


def main():
    parser = argparse.ArgumentParser(description='Automate configuration')
    parser.add_argument('-c', dest='clean', action='store_true', help='clean generated')
    parser.add_argument('-d', dest='deploy', required=True,
                        help='deploy directory containing the original dayz server files')
    parser.add_argument('-a', dest='auth', required=True, help='auth config file')
    args = parser.parse_args()
    if args.clean:
        clean()
    types.set(ElementTree.parse(pathlib.Path(args.deploy, 'mpmissions/dayzOffline.chernarusplus/db/types.xml')))
    auth.set(json.load(open(args.auth)))
    configuration.scan()
    for c in configs.get():
        c()
    log.info('complete')

    cats = set()
    for t in types.get().getroot():
        c = t.find('category')
        if c is not None:
            cats.add(c.get('name'))
    print(cats)


def clean():
    log.info('removing old generated')
    for p in pathlib.Path('.').glob('generated-*'):
        log.info('removing {}'.format(p))
        shutil.rmtree(p)


if __name__ == '__main__':
    main()
