_types = None


def get():
    return _types


def set(types):
    global _types
    _types = types
