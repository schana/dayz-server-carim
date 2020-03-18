import pathlib

from carim.configuration import base
from carim.models import types


def mission(_func=None, *, directory='.', register=True):
    return base.located_config(_func, directory=directory, dir_prefix='servers/0/mpmissions/dayzOffline.chernarusplus',
                               register=register)


@mission(directory='db', register=False)
def types_config(directory):
    types.get().write(pathlib.Path(directory, 'types.xml'))
