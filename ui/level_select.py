from config import settings
from levels import registry

VISIBLE_ROWS = 9


def draw(screen, font_title, font_hud, level_numbers, selected_index, progression):
    width, height = screen.get_size()

    title_surf = font_title.render("NIVELES", True, settings.COLORS["accent"])
    screen.blit(title_surf, title_surf.get_rect(center=(width // 2, 70)))

    total = len(level_numbers)
    visible_rows = min(VISIBLE_ROWS, total)

    # Con mas de 9 niveles no caben todos en pantalla: se desplaza la
    # ventana visible para que el seleccionado siempre quede a la vista.
    start = max(0, selected_index - visible_rows // 2)
    start = min(start, max(0, total - visible_rows))
    end = start + visible_rows

    if start > 0:
        more_above = font_hud.render("^ ^ ^", True, settings.COLORS["text_pending"])
        screen.blit(more_above, more_above.get_rect(center=(width // 2, 128)))

    y = 160
    for i in range(start, end):
        level_number = level_numbers[i]
        level_name = registry.get_level(level_number).NAME
        unlocked = progression.is_unlocked(level_number)
        record = progression.data["level_records"].get(str(level_number))

        label = f"NIVEL {level_number} - {level_name}"
        if not unlocked:
            label += "  (bloqueado)"
        elif record:
            label += f"  -  mejor puntuacion: {int(record['best_score'])}"

        color = settings.COLORS["text"] if unlocked else settings.COLORS["text_pending"]
        if i == selected_index:
            color = settings.COLORS["accent"]

        surf = font_hud.render(label, True, color)
        screen.blit(surf, surf.get_rect(center=(width // 2, y)))
        y += surf.get_height() + 18

    if end < total:
        more_below = font_hud.render("v v v", True, settings.COLORS["text_pending"])
        screen.blit(more_below, more_below.get_rect(center=(width // 2, y + 8)))

    hint_surf = font_hud.render(
        "ARRIBA/ABAJO para elegir    -    ENTER para jugar    -    ESC para volver",
        True,
        settings.COLORS["text_pending"],
    )
    screen.blit(hint_surf, hint_surf.get_rect(center=(width // 2, height - 60)))
