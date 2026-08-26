def calculate_wpm(correct_chars, elapsed_seconds):
    """Words Per Minute, usando la convencion estandar de 5 caracteres = 1 palabra."""
    if elapsed_seconds <= 0:
        return 0.0
    minutes = elapsed_seconds / 60
    return (correct_chars / 5) / minutes


def calculate_precision(correct_chars, total_typed):
    if total_typed <= 0:
        return 100.0
    return (correct_chars / total_typed) * 100


def calculate_score(wpm, precision_pct, errors, max_combo, time_remaining_pct, weights):
    """Formula conceptual del documento maestro (seccion 9), con pesos configurables."""
    speed_score = wpm * weights["speed_multiplier"]
    precision_score = precision_pct * weights["precision_multiplier"]
    combo_score = max_combo * weights["combo_multiplier"]
    time_bonus = time_remaining_pct * weights["time_bonus_multiplier"]
    error_penalty = errors * weights["error_penalty_multiplier"]
    return max(0.0, speed_score + precision_score + combo_score + time_bonus - error_penalty)


def calculate_stars(precision_pct, thresholds):
    stars = 0
    for star, threshold in sorted(thresholds.items()):
        if precision_pct >= threshold:
            stars = star
    return stars


def calculate_xp(is_three_star, is_new_record, max_combo):
    """Seccion 11 del documento maestro."""
    xp = 100  # nivel completado
    if is_three_star:
        xp += 50
    if is_new_record:
        xp += 100
    xp += (max_combo // 20) * 20  # racha de 20: +20 XP (por cada bloque de 20)
    return xp

