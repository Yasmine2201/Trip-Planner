# COMMON STRINGS
INVALID_BODY_ERROR = 'Invalid request. Data did not pass validation.'
NOT_FOUND_ERROR = '{Model} not found.'


# COMMON FUNCTIONS #
def default(value, default_value):
    return value if value is not None else default_value


def make_jwt_header(token: str) -> dict:
    return {
        "Authorization": f"Bearer {token}"
    }


# COMMON EXCEPTIONS #
class ForbiddenActionError(Exception):
    def __init__(self, msg: str = None):
        super().__init__(msg)
        self.msg = msg


# COMMON META CLASSES #
class Singleton(type):
    _instances = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instances:
            cls._instances[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instances[cls]
