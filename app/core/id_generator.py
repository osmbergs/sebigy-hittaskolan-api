from ulid import ULID


def new_id():
    return str(ULID())
