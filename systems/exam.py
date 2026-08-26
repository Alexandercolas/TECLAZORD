# Modo Examen (seccion 27): simula una prueba real de mecanografia. Un
# solo texto largo y continuo, tiempo fijo, sin niveles ni desbloqueos.
# El resultado se reporta como un "certificado" en vez de la pantalla
# de resultados normal de nivel.

EXAM_TEXT = (
    "La velocidad de escritura se mide en palabras por minuto y depende "
    "de la practica constante. Un buen mecanografista combina precision "
    "y rapidez sin mirar el teclado. Escribir 45 palabras por minuto con "
    "95% de precision ya se considera un nivel solido. Anota tu resultado: "
    "10, 25, 50 o incluso 100 palabras por minuto son posibles con "
    "entrenamiento diario. El objetivo de TECLAZO RD es que domines el "
    "teclado completo sin pensar donde estan las teclas."
)

WPM_LEVEL_THRESHOLDS = [
    (70, "EXPERTO"),
    (50, "AVANZADO"),
    (35, "INTERMEDIO"),
    (20, "BASICO"),
]


class ExamLevel:
    LEVEL_NUMBER = None
    NAME = "MODO EXAMEN"
    TIME_LIMIT_SECONDS = 60


def get_exercises():
    return [EXAM_TEXT]


def classify_wpm(wpm):
    for threshold, label in WPM_LEVEL_THRESHOLDS:
        if wpm >= threshold:
            return label
    return "PRINCIPIANTE"
