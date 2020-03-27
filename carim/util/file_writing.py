import io
import logging
import re
import shutil
import time
from xml.dom import minidom
from xml.etree import ElementTree

from carim.global_resources import errors

log = logging.getLogger(__name__)


def copy(src, dst):
    log.debug('copy {} -> {}'.format(src, dst))
    start = time.time()
    while time.time() - start < 10:
        try:
            shutil.copy(src, dst)
            return
        except PermissionError as e:
            log.warning('failed {}'.format(e))
            time.sleep(0.2)
            continue
    errors.add('copy {} -> {}'.format(src, dst))


def f_open(path, **kwargs):
    log.debug('open {} {}'.format(path, kwargs))
    start = time.time()
    while time.time() - start < 10:
        try:
            f = open(path, **kwargs)
            return f
        except PermissionError as e:
            log.warning('failed {}'.format(e))
            time.sleep(0.2)
            continue
    errors.add('open {}'.format(path))
    return io.StringIO()


def convert_to_string(root):
    rough_string = ElementTree.tostring(root, encoding='unicode')
    spaces = re.compile(r'>\s*<', flags=re.DOTALL)
    rough_string = re.sub(spaces, '>\n<', rough_string)
    return minidom.parseString(rough_string).toprettyxml(indent='  ', newl='')
