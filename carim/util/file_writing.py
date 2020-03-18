import logging
import shutil
import time
import io

from carim.models import errors

log = logging.getLogger(__name__)


def copy(src, dst):
    log.info('copy {} -> {}'.format(src, dst))
    start = time.time()
    while time.time() - start < 10:
        try:
            shutil.copy(src, dst)
            log.info('success')
            return
        except PermissionError as e:
            log.warning('failed {}'.format(e))
            time.sleep(0.2)
            continue
    errors.add('copy {} -> {}'.format(src, dst))


def f_open(path, **kwargs):
    log.info('open {} {}'.format(path, kwargs))
    start = time.time()
    while time.time() - start < 10:
        try:
            f = open(path, **kwargs)
            log.info('success')
            return f
        except PermissionError as e:
            log.warning('failed {}'.format(e))
            time.sleep(0.2)
            continue
    errors.add('open {}'.format(path))
    return io.StringIO()
