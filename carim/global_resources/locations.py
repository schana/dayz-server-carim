from collections import namedtuple

_markers = []
marks = list()

Position = namedtuple('Position', ('x', 'z'))


def initialize():
    # TODO: move this to separate config file
    global marks
    marks = [
        ('Green Mountain Trader', Position(3727, 6007)),
        ('Kumyrna Trader', Position(8355, 5986)),
        ('Altar Trader', Position(8164, 9113)),
        ('Zabolotye Black Market Trader', Position(1602.85, 10413.2)),
        ('NWAF', Position(4541, 10289)),
        ('NEAF', Position(12121, 12521))
    ]


def overlaps(position, p_r, x, z, r):
    return (x - position.x) ** 2 + (z - position.z) ** 2 <= (r + p_r) ** 2
