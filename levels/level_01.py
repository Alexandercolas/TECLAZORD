LEVEL_NUMBER = 1
NAME = "EL CALENTON"
TIME_LIMIT_SECONDS = 90

# Fila base (home row) primero, sin presion, siguiendo la seccion 7 del
# documento maestro. Luego combinaciones cortas y un par de palabras
# sencillas hechas solo con estas letras.
EXERCISES = [
    "fj fj fj",
    "dk dk dk",
    "as as as",
    "lñ lñ lñ",
    "gh gh gh",
    "fjdk aslñ gh",
    "jf kd la ñg",
    "al lag laga",
    "sal sala salsa",
    "gaja jala",
]


def get_exercises():
    return EXERCISES
