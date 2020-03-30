import json
import pathlib
from collections import namedtuple

from carim.global_resources import resourcesdir

marks = list()

Position = namedtuple('Position', ('x', 'z'))


def initialize():
    with open(pathlib.Path(resourcesdir.get(), 'modifications/server/locations.json')) as f:
        location_data = json.load(f)
    global marks
    marks = [(l.get('name'), Position(l.get('x'), l.get('z'))) for l in location_data]


def overlaps(position, p_r, x, z, r):
    return (x - position.x) ** 2 + (z - position.z) ** 2 <= (r + p_r) ** 2
