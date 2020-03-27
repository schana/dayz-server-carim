import functools
import inspect
import logging
import pathlib

from carim.global_resources import outdir, configs


def config(_func=None, *, directory='.', register=True):
    def config_decorator(func):
        @functools.wraps(func)
        def config_wrapper(*args, **kwargs):
            log = logging.getLogger(func.__module__)
            log.info('processing {}'.format(func.__name__))
            p = pathlib.Path(outdir.get(), directory)
            p.mkdir(parents=True, exist_ok=True)
            log.debug('created directory {}'.format(directory))
            if 'directory' in inspect.signature(func).parameters:
                return func(*args, **kwargs, directory=str(p))
            else:
                return func(*args, **kwargs)

        if register:
            configs.add(config_wrapper)
        return config_wrapper

    if _func is None:
        return config_decorator
    else:
        return config_decorator(_func)


def located_config(_func=None, *, directory='.', dir_prefix=None, register=True):
    if _func is None:
        if directory is not None:
            return config(directory=str(pathlib.Path(dir_prefix, directory)), register=register)
        else:
            return config
    else:
        if directory is not None:
            return config(_func, directory=str(pathlib.Path(dir_prefix, directory)), register=register)
        else:
            return config(_func)


def server(_func=None, *, directory='.', register=True):
    return located_config(_func, directory=directory, dir_prefix='servers/0', register=register)


def mission(_func=None, *, directory='.', register=True):
    return located_config(_func, directory=directory, dir_prefix='servers/0/mpmissions/dayzOffline.chernarusplus',
                          register=register)


def profile(_func=None, *, directory='.', register=True):
    return located_config(_func, directory=directory, dir_prefix='servers/0/profiles', register=register)
