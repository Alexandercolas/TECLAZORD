# Contrarreloj (seccion 16): maxima velocidad durante una duracion fija.
# Mezcla ejercicios de todos los niveles para variedad; core/game.py hace
# que el ejercicio se reinicie en bucle si el jugador termina la lista
# antes de que se acabe el tiempo (session["cycle_exercises"]).

import random

from levels import level_01, level_02, level_03, level_04, level_05, level_06, level_07, level_08

DURATIONS = [30, 60, 120]


class TimeAttackLevel:
    LEVEL_NUMBER = None
    NAME = "CONTRARRELOJ"
    TIME_LIMIT_SECONDS = 30  # se sobreescribe segun la duracion elegida


def get_exercises():
    pool = (
        level_01.get_exercises() + level_02.get_exercises() + level_03.get_exercises()
        + level_04.get_exercises() + level_05.get_exercises() + level_06.get_exercises()
        + level_07.get_exercises() + level_08.get_exercises()
    )
    shuffled = pool.copy()
    random.shuffle(shuffled)
    return shuffled
