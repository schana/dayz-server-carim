class Config:
    def __init__(self):
        self.traders = list()
        self.objects = list()

    def generate(self):
        result = '\n'.join(t.generate() for t in self.traders)
        result += '\n' + '\n'.join(o.generate() for o in self.objects)
        result += '\n<FileEnd>'
        return result


class Trader:
    def __init__(self, marker, position, safezone=200):
        self.marker = marker
        self.position = position
        self.safezone = safezone
        self.vehicle = None

    def set_vehicle(self, vehicle):
        self.vehicle = vehicle

    def generate(self):
        result = '<TraderMarker> {}'.format(self.marker)
        result += '\n<TraderMarkerPosition> ' + ','.join(str(p) for p in self.position)
        result += '\n<TraderMarkerSafezone> ' + str(self.safezone)
        if self.vehicle is not None:
            result += '\n' + self.vehicle.generate()
        return result


class Vehicle:
    def __init__(self, position, orientation):
        self.position = position
        self.orientation = orientation

    def generate(self):
        result = '<VehicleSpawn> ' + ','.join(str(p) for p in self.position)
        result += '\n<VehicleSpawnOri> {},0,0'.format(self.orientation)
        return result


class Object:
    def __init__(self, class_name, position, orientation):
        self.class_name = class_name
        self.position = position
        self.orientation = orientation
        self.attachments = list()

    def generate(self):
        result = '<Object> {}'.format(self.class_name)
        result += '\n<ObjectPosition> ' + ','.join(str(p) for p in self.position)
        result += '\n<ObjectOrientation> {},0,0\n'.format(self.orientation)
        result += '\n'.join(a.generate() for a in self.attachments)
        return result


class Attachment:
    def __init__(self, class_name):
        self.class_name = class_name

    def generate(self):
        return '<ObjectAttachment> {}'.format(self.class_name)
