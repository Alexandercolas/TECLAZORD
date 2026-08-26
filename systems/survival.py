# Supervivencia (seccion 16): el texto sigue apareciendo sin limite de
# tiempo fijo. Si la precision del jugador cae demasiado: GAME OVER
# (ver core/game.py._survival_precision_too_low).

from systems.time_attack import get_exercises as _get_mixed_exercises

SURVIVAL_MIN_PRECISION_PERCENT = 80
# Ignora la caida de precision hasta que haya al menos esta cantidad de
# caracteres escritos, para no terminar la partida por un tropiezo inicial.
SURVIVAL_GRACE_CHARACTERS = 15


class SurvivalLevel:
    LEVEL_NUMBER = None
    NAME = "SUPERVIVENCIA"
    TIME_LIMIT_SECONDS = 600  # techo de seguridad; normalmente termina antes por precision


def get_exercises():
    return _get_mixed_exercises()
