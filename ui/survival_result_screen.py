from config import settings


def draw(screen, font_title, font_hud, result):
    width, height = screen.get_size()

    title_surf = font_title.render("GAME OVER", True, settings.COLORS["text_error"])
    screen.blit(title_surf, title_surf.get_rect(center=(width // 2, 100)))

    minutes, seconds = divmod(int(result.get("survival_time_seconds", 0)), 60)
    time_label = f"{minutes}m {seconds}s" if minutes else f"{seconds}s"

    lines = [
        f"Sobreviviste: {time_label}",
        f"WPM: {result['wpm']}",
        f"Precision final: {result['precision']}%",
        f"Errores: {result['errors']}",
        f"Combo maximo: x{result['max_combo']}",
    ]

    if result.get("leaderboard_updated"):
        lines.append("")
        lines.append("NUEVO MEJOR PERSONAL EN EL LEADERBOARD")

    y = 250
    for line in lines:
        surf = font_hud.render(line, True, settings.COLORS["text"])
        screen.blit(surf, surf.get_rect(center=(width // 2, y)))
        y += surf.get_height() + 16

    hint_surf = font_hud.render(
        "ENTER para elegir nivel    -    ESC para el menu", True, settings.COLORS["text_pending"],
    )
    screen.blit(hint_surf, hint_surf.get_rect(center=(width // 2, height - 60)))
