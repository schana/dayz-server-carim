_dir = None


def get():
    return _dir


def set(directory):
    global _dir
    _dir = directory
