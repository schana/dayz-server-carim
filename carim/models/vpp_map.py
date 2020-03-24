from collections import namedtuple

_markers = []
marks = list()


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
    for m in marks:
        add(Marker(
            name=m[0],
            icon=Icon.DEFAULT,
            color=WHITE,
            position=m[1],
            active=True,
            active_3d=True
        ))


def add(marker):
    _markers.append(marker)


def get_config():
    return {
        'M_STATIC_MARKER_ARRAY': [m.get_config() for m in _markers],
        'm_CanUse3DMarkers': 1,
        'm_OwnPositionMarkerDisabled': 0,
        'm_ForceMapItemOnly': 0
    }


def get_admin_teleport_config():
    return {
        'm_TeleportLocations': [m.get_admin_teleport_config() for m in _markers]
    }


class Marker:
    def __init__(self, name, icon, color, position, active, active_3d):
        self.name = name
        self.icon = icon
        self.color = color
        self.position = position
        self.active = active
        self.active_3d = active_3d

    def get_config(self):
        return {
            'M_MARKER_NAME': self.name,
            'M_ICON_PATH': self.icon,
            'M_COLOR': [self.color.r, self.color.g, self.color.b],
            'M_POSITION': [self.position.x, 0, self.position.z],
            'M_ISACTIVE': 1 if self.active else 0,
            'M_IS_3D_ACTIVE': 1 if self.active_3d else 0
        }

    def get_admin_teleport_config(self):
        return {
            'm_Name': self.name,
            'm_Position': [
                self.position.x,
                0,
                self.position.z
            ]
        }


Position = namedtuple('Position', ('x', 'z'))


def overlaps(position, p_r, x, z, r):
    return (x - position.x) ** 2 + (z - position.z) ** 2 <= (r + p_r) ** 2


Color = namedtuple('Color', ('r', 'g', 'b'))

WHITE = Color(255, 255, 255)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)


class Icon:
    DEFAULT = "VanillaPPMap\\GUI\\Textures\\CustomMapIcons\\waypointeditor_CA.paa"
