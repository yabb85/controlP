from .ampli import AmpliSignal
from .player import PlayerSignal


def get_ampli_signal():
    return AMPLI


def get_player_signal():
    return PLAYER


PLAYER = PlayerSignal()

AMPLI = AmpliSignal()
