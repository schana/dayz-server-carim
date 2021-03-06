from collections import namedtuple

from carim.global_resources import locations


def get_markers():
    return [Marker(
        name=m[0],
        icon=Icon.DEFAULT,
        color=WHITE,
        position=m[1],
        active=True,
        active_3d=True
    ) for m in locations.marks]


def get_config():
    return {
        'M_STATIC_MARKER_ARRAY': [m.get_config() for m in get_markers()],
        'm_CanUse3DMarkers': 1,
        'm_OwnPositionMarkerDisabled': 0,
        'm_ForceMapItemOnly': 0
    }


def get_admin_teleport_config():
    return {
        'm_TeleportLocations': [m.get_admin_teleport_config() for m in get_markers()]
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


Color = namedtuple('Color', ('r', 'g', 'b'))

WHITE = Color(255, 255, 255)
RED = Color(255, 0, 0)
GREEN = Color(0, 255, 0)
BLUE = Color(0, 0, 255)


class Icon:
    DEFAULT = "VanillaPPMap\\GUI\\Textures\\CustomMapIcons\\waypointeditor_CA.paa"
