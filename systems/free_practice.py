# Practica libre (seccion 16): el jugador elige una categoria y practica
# ejercicios de esa categoria, sin presion de desbloqueo. Reutiliza el
# contenido ya escrito para los niveles en vez de duplicarlo.

from levels import level_01, level_02, level_03, level_04, level_05, level_06, level_07, level_08

CATEGORIES = ["letras", "numeros", "simbolos", "numpad", "codigo", "oficina"]

CATEGORY_LABELS = {
    "letras": "LETRAS",
    "numeros": "NUMEROS",
    "simbolos": "SIMBOLOS",
    "numpad": "TECLADO NUMERICO",
    "codigo": "CODIGO",
    "oficina": "OFICINA",
}


class FreePracticeLevel:
    LEVEL_NUMBER = None
    NAME = "PRACTICA LIBRE"
    TIME_LIMIT_SECONDS = 60


def get_exercises(category):
    if category == "letras":
        return level_01.get_exercises() + level_02.get_exercises() + level_03.get_exercises()
    if category == "numeros":
        return level_04.get_exercises()
    if category == "simbolos":
        return level_06.get_exercises()
    if category == "codigo":
        return level_08.get_exercises()
    if category == "oficina":
        return level_05.get_exercises() + level_07.get_exercises()
    raise ValueError(f"categoria desconocida: {category}")
