_configs = []
_skipped = 0


def get():
    return _configs


def add(config):
    _configs.append(config)


def add_skipped():
    global _skipped
    _skipped += 1


def get_skipped():
    return _skipped
