LEVEL_NUMBER = 10
NAME = "EL DURO DEL TECLADO"
TIME_LIMIT_SECONDS = 30

# El nivel final: combina mayusculas, minusculas, numeros, simbolos,
# acentos, frases, codigo, fechas y cantidades (seccion 7).
EXERCISES = [
    "El Sr. Ramirez confirmo el Pedido #77821 por RD$45,900.50.",
    "def calcular_total(precio, cantidad):\n    return precio * cantidad",
    "La reunion es el 14/02/2026 a las 9:30am en la oficina 4B.",
    "ÑOÑO utilizo el codigo A1B2-C3D4 para acceder al sistema.",
    "Envie 3 correos, 2 reportes y 1 factura antes del mediodia.",
]


def get_exercises():
    return EXERCISES
