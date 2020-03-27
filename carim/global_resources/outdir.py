import time

_dir = time.strftime('generated-%Y%m%d%H%M%S', time.gmtime())


def get():
    return _dir


def set(directory):
    global _dir
    _dir = directory
