LEVEL_NUMBER = 11
NAME = "IT BASICS"
TIME_LIMIT_SECONDS = 90

# Fase 2 (niveles 11-20): vocabulario tecnico en ingles, con las frases
# cayendo de arriba hacia abajo en vez del formato estatico de los
# niveles 1-10 (ver FALLING_MODE en core/game.py).
FALLING_MODE = True

# Segundos de caida por caracter de la frase actual. Nivel 11 es el mas
# generoso (palabras sueltas, cortas); baja progresivamente hasta el
# Nivel 20 (oraciones completas, mas rapido por caracter).
SECONDS_PER_CHARACTER = 0.45

EXERCISES = [
    "hardware",
    "software",
    "keyboard",
    "monitor",
    "database",
    "network",
    "server",
    "firewall",
    "backup",
    "password",
]


def get_exercises():
    return EXERCISES
