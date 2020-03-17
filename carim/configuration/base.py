import functools
import logging
import pathlib

from carim.models import outdir, configs

log = logging.getLogger(__name__)


def config(_func=None, *, directory=None):
    def config_decorator(func):
        @functools.wraps(func)
        def config_wrapper(*args, **kwargs):
            log.info('processing {}'.format(func.__name__))
            if directory is not None:
                p = pathlib.Path(outdir.get(), directory)
                p.mkdir(parents=True, exist_ok=True)
                log.info('created directory {}'.format(directory))
                return func(*args, **kwargs, directory=str(p))
            else:
                return func(*args, **kwargs)

        configs.add(config_wrapper)
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