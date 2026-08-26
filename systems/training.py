# Entrenamiento personalizado (seccion 15 del documento maestro): genera
# ejercicios cortos a partir de las teclas que el jugador falla mas.

MIN_TOTAL_ERRORS_FOR_TRAINING = 3


class TrainingLevel:
    """Un nivel sintetico (no forma parte de levels/registry.py) usado
    unicamente por el Modo Errores. No cuenta para progreso ni records."""

    LEVEL_NUMBER = None
    NAME = "ENTRENAMIENTO PERSONALIZADO"
    TIME_LIMIT_SECONDS = 60


def generate_personalized_exercises(key_stats, limit=4):
    if sum(key_stats.data["error_counts"].values()) < MIN_TOTAL_ERRORS_FOR_TRAINING:
        return []

    top_chars = [char for char, _ in key_stats.most_failed(limit=limit)]
    if not top_chars:
        return []

    exercises = [top_chars[0] * 6]

    if len(top_chars) >= 2:
        exercises.append((top_chars[0] + top_chars[1]) * 3)

    if len(top_chars) >= 3:
        exercises.append("".join(top_chars[:3]) * 2)

    exercises.append(f"usuario_{top_chars[0]}")

    return exercises
