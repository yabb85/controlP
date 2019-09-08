from ..pioneer import Pioneer

PIONEER = Pioneer('192.168.1.100', 8102)


def get_pioneer():
    return PIONEER
