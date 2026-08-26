LEVEL_NUMBER = 3
NAME = "EL TECLADO ENTERO"
TIME_LIMIT_SECONDS = 90

# Aparece practicamente todo el teclado alfanumerico: todas las letras,
# mayusculas y espacio (seccion 7). Enter y Shift ya se ejercitan de forma
# implicita (Shift al escribir mayusculas); un modo con saltos de linea
# reales queda para una fase posterior si hace falta.
EXERCISES = [
    "Buenos dias",
    "Estoy aprendiendo a escribir rapido",
    "El trabajo comienza temprano",
    "La practica hace al maestro",
]


def get_exercises():
    return EXERCISES
