_auth = {}


def get():
    return _auth


def set(auth):
    global _auth
    _auth = auth
