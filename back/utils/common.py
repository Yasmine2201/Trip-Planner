import math

__all__ = [
    'INVALID_BODY_ERROR',
    'NOT_FOUND_ERROR',
    'default',
    'make_jwt_header',
    'haversine',
    'ForbiddenActionError',
    'Singleton'
]

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


def haversine(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
    """
    Calculate the great circle distance between two points
    on the earth (specified in decimal degrees)
    """
    earth_radius = 6371
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat / 2) ** 2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon / 2) ** 2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1 - a))
    return earth_radius * c


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
