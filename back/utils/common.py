# COMMON FUNCTIONS #


def default(value, default_value):
    return value if value is not None else default_value


def make_jwt_header(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}"
    }


# COMMON META CLASSES #
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
