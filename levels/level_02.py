LEVEL_NUMBER = 2
NAME = "YA TA' SONANDO"
TIME_LIMIT_SECONDS = 90

# Se amplia el teclado (seccion 7): QWER TY UIOP y ZXCV BNM. Se empiezan
# a formar palabras sencillas usando solo estas letras mas la fila home
# del Nivel 1.
EXERCISES = [
    "qwer qwer",
    "ty ty ty",
    "uiop uiop",
    "zxcv zxcv",
    "bnm bnm",
    "casa mesa",
    "papa gato",
    "mano trabajo",
    "casa mesa papa gato mano trabajo",
]


def get_exercises():
    return EXERCISES
