# Modo Versus (seccion 27: "Modo competitivo local - Dos jugadores").
# Con un solo teclado fisico, la unica forma realista de competir es por
# turnos: cada jugador escribe el mismo texto por separado y se comparan
# los resultados al final (duelo asincrono, no simultaneo).

VERSUS_TEXT = (
    "En este duelo cada jugador escribe el mismo texto y se compara quien "
    "logra mas palabras por minuto sin sacrificar precision. Que gane el "
    "mejor mecanografo de la casa."
)


class VersusLevel:
    LEVEL_NUMBER = None
    NAME = "MODO VERSUS"
    TIME_LIMIT_SECONDS = 30


def get_exercises():
    return [VERSUS_TEXT]


def determine_winner(p1_name, p1_result, p2_name, p2_result):
    if p1_result["wpm"] > p2_result["wpm"]:
        return f"GANA {p1_name}!"
    if p2_result["wpm"] > p1_result["wpm"]:
        return f"GANA {p2_name}!"
    if p1_result["precision"] > p2_result["precision"]:
        return f"GANA {p1_name} (por precision)!"
    if p2_result["precision"] > p1_result["precision"]:
        return f"GANA {p2_name} (por precision)!"
    return "EMPATE!"
