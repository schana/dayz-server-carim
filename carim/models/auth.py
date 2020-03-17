_auth = {}


def set(auth):
    global _auth
    _auth = auth


def get():
    return _auth
