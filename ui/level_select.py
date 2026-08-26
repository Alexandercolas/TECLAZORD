from config import settings


def draw(screen, font_title, font_hud, level_numbers, selected_index, progression):
    width, height = screen.get_size()

    title_surf = font_title.render("NIVELES", True, settings.COLORS["accent"])
    screen.blit(title_surf, title_surf.get_rect(center=(width // 2, 80)))

    y = 200
    for i, level_number in enumerate(level_numbers):
        unlocked = progression.is_unlocked(level_number)
        record = progression.data["level_records"].get(str(level_number))

        label = f"NIVEL {level_number}"
        if not unlocked:
            label += "  (bloqueado)"
        elif record:
            label += f"  -  mejor puntuacion: {int(record['best_score'])}"

        color = settings.COLORS["text"] if unlocked else settings.COLORS["text_pending"]
        if i == selected_index:
            color = settings.COLORS["accent"]

        surf = font_hud.render(label, True, color)
        screen.blit(surf, surf.get_rect(center=(width // 2, y)))
        y += surf.get_height() + 20

    hint_surf = font_hud.render(
        "ARRIBA/ABAJO para elegir    -    ENTER para jugar    -    ESC para volver",
        True,
        settings.COLORS["text_pending"],
    )
    screen.blit(hint_surf, hint_surf.get_rect(center=(width // 2, height - 60)))
