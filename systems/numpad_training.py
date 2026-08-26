# Modo dedicado al teclado numerico (seccion 17): a diferencia de todos
# los demas modos, aqui SOLO cuentan las teclas fisicas del Numpad -
# ver core/game.py._handle_numpad_keydown, que usa core/keymap.py para
# distinguirlas de la fila superior de numeros.
#
# Nota: esto asume Num Lock activado (comportamiento estandar en la
# mayoria de los teclados de oficina, que es el publico objetivo del
# documento maestro).

EXERCISES = [
    "789",
    "456",
    "123",
    "0.5",
    "753159",
    "12.34",
    "2026",
    "100.00",
    "45.50",
    "999",
]


class NumpadLevel:
    LEVEL_NUMBER = None
    NAME = "ENTRENAMIENTO NUMPAD"
    TIME_LIMIT_SECONDS = 60


def get_exercises():
    return EXERCISES
