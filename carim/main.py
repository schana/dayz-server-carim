import argparse
import json
import logging
import pathlib
import shutil
from xml.etree import ElementTree

from carim import configuration
from carim.configuration import trader, missions
from carim.models import auth, types, configs
from carim.util import modify_types

logging.basicConfig(level=logging.INFO, format='%(asctime)s %(levelname)s %(name)s - %(message)s')
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
    modify_types.modify_types()
    missions.types_config()
    trader.trader_items()
    log.info('complete')

    inspect_types = False
    if inspect_types:
        cats = set()
        type_spec = {}
        for t in types.get().getroot():
            seen_tags = set()
            for child in t:
                if child.tag in seen_tags and child.tag not in ('value', 'usage'):
                    print(ElementTree.tostring(t))
                seen_tags.add(child.tag)
                values = set(type_spec.get(child.tag, list()))
                values.update(child.attrib.keys())
                # if child.text is not None:
                #     values.add(child.text)
                type_spec[child.tag] = sorted(list(values))
            c = t.find('category')
            if c is not None:
                cats.add(c.get('name'))
        print(cats)
        print(json.dumps(type_spec, indent=2))


def clean():
    log.info('removing old generated')
    for p in pathlib.Path('.').glob('generated-*'):
        log.info('removing {}'.format(p))
        shutil.rmtree(p)


if __name__ == '__main__':
    main()
