LEVEL_NUMBER = 4
NAME = "LOS NUMEROS"
TIME_LIMIT_SECONDS = 60

# Seccion 7: numeros de la fila superior y del teclado numerico. El
# teclado visual (ui/keyboard_widget.py) resalta ambos bloques por igual,
# ya que el documento no exige usar exclusivamente el Numpad aqui -
# ese modo dedicado es una expansion futura (seccion 16).
EXERCISES = [
    "1234567890",
    "0987654321",
    "12345",
    "67890",
    "100",
    "250",
    "500",
    "1000",
    "2500",
    "10000",
]


def get_exercises():
    return EXERCISES
