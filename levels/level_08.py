LEVEL_NUMBER = 8
NAME = "MODO PROGRAMADOR"
TIME_LIMIT_SECONDS = 45

# Escritura tecnica (seccion 7): palabras clave, simbolos de codigo y
# saltos de linea reales. El "\n" se escribe con la tecla Enter, que
# core/game.py traduce a este mismo caracter en el InputManager.
EXERCISES = [
    'print("Hola mundo")',
    "for i in range(10):\n    print(i)",
    "if nivel >= 10:\n    ganar()\nelse:\n    seguir()",
    "while activo:\n    avanzar()",
    "def sumar(a, b):\n    return a + b",
    "class Jugador:\n    pass",
    "import os",
    'config = {"debug": True}',
    "items = [1, 2, 3]",
    "if a <= b and a >= c and a != d:\n    ok = True",
]


def get_exercises():
    return EXERCISES
