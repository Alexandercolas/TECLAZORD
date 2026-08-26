from config import settings
from systems.achievements import ACHIEVEMENT_DEFINITIONS

_ACHIEVEMENT_NAMES = {definition["id"]: definition["name"] for definition in ACHIEVEMENT_DEFINITIONS}


def draw(screen, font_title, font_hud, result):
    if result is None:
        return

    width, height = screen.get_size()
    passed = result.get("passed", True)
    is_training = result.get("level_number") is None

    if is_training:
        title_text = "ENTRENAMIENTO COMPLETADO"
    else:
        title_text = "NIVEL COMPLETADO" if passed else "NIVEL FALLIDO"
    title_color = settings.COLORS["accent"] if passed else settings.COLORS["text_error"]

    if not passed:
        subtitle = f"Necesitas al menos {result['min_precision']:.0f}% de precision"
    elif is_training:
        subtitle = "Sigue practicando estas teclas"
    elif result["stars"]:
        subtitle = "*" * result["stars"]
    else:
        subtitle = "(sin estrellas)"

    lines = [
        (font_title, title_text, title_color),
        (font_hud, subtitle, settings.COLORS["text"]),
        (font_hud, f"WPM: {result['wpm']}", settings.COLORS["text"]),
        (font_hud, f"PRECISION: {result['precision']}%", settings.COLORS["text"]),
        (font_hud, f"ERRORES: {result['errors']}", settings.COLORS["text"]),
        (font_hud, f"COMBO MAXIMO: x{result['max_combo']}", settings.COLORS["text"]),
        (font_hud, f"PUNTUACION: {result['score']}", settings.COLORS["text"]),
    ]

    if passed and "xp_earned" in result:
        lines.append((font_hud, f"+{result['xp_earned']} XP", settings.COLORS["accent"]))
        for achievement_id in result.get("newly_unlocked_achievements", []):
            name = _ACHIEVEMENT_NAMES.get(achievement_id, achievement_id)
            lines.append((font_hud, f"LOGRO DESBLOQUEADO: {name}", settings.COLORS["accent"]))

    lines.append((font_hud, "", settings.COLORS["text"]))
    lines.append((font_hud, "ENTER para elegir nivel    -    ESC para el menu", settings.COLORS["text"]))

    y = height // 6
    for font, text, color in lines:
        surf = font.render(text, True, color)
        screen.blit(surf, surf.get_rect(center=(width // 2, y)))
        y += surf.get_height() + 12
