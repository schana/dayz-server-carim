import pathlib

from carim.configuration import base
from carim.models import types


def mission(_func=None, *, directory='.'):
    return base.located_config(_func, directory=directory, dir_prefix='servers/0/mpmissions/dayzOffline.chernarusplus')


@mission(directory='db')
def types_config(directory):
    types.get().write(pathlib.Path(directory, 'types.xml'))
