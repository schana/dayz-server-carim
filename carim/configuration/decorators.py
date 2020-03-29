import functools
import inspect
import logging
import pathlib

from carim.global_resources import outdir, configs, mods


def register(func):
    @functools.wraps(func)
    def wrapped(*args, **kwargs):
        return func(*args, **kwargs)

    configs.add(wrapped)
    return wrapped


def mod(mod_name):
    def disable_if_not_enabled(func):
        @functools.wraps(func)
        def config_wrapper(*args, **kwargs):
            if mod_name in mods.get():
                return func(*args, **kwargs)
            else:
                configs.add_skipped()
                log = logging.getLogger(func.__module__)
                log.warning('skipping {} because {} is not enabled'.format(func.__name__, mod_name))

        return config_wrapper

    return disable_if_not_enabled


def config(_func=None, *, directory='.'):
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

        return config_wrapper

    if _func is None:
        return config_decorator
    else:
        return config_decorator(_func)


def located_config(_func=None, *, directory='.', dir_prefix=None):
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


def server(_func=None, *, directory='.'):
    return located_config(_func, directory=directory, dir_prefix='servers/0')


def mission(_func=None, *, directory='.'):
    return located_config(_func, directory=directory, dir_prefix='servers/0/mpmissions/dayzOffline.chernarusplus',
                          )


def profile(_func=None, *, directory='.'):
    return located_config(_func, directory=directory, dir_prefix='servers/0/profiles')
