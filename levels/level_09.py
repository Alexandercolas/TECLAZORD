LEVEL_NUMBER = 9
NAME = "EL TIGUERE DEL TECLADO"
TIME_LIMIT_SECONDS = 30

# Modo avanzado (seccion 7): textos largos, cambios constantes entre
# letras, numeros y simbolos. El documento pide una precision minima:
# si el jugador baja de eso, el nivel se marca como fallido y no
# cuenta para records ni desbloqueos (ver core/game.py._finish_level).
MIN_PRECISION_PERCENT = 90

EXERCISES = [
    "El cliente #4521 pago $12,500.75 el 09/04/2026 antes de las 3:45pm.",
    "usuario_92 ingreso con clave Xk9#mP2! desde la IP 192.168.0.45.",
    "Factura#3390: 18 unidades x $250.00 = $4,500.00 (IVA incluido).",
    "Referencia RD-2026-00871 vence el 30/11/2026 a las 11:59pm.",
]


def get_exercises():
    return EXERCISES
