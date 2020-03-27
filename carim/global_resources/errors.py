_errors = []


def get():
    return _errors


def add(e):
    _errors.append(e)
