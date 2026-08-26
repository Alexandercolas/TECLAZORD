from config import settings


def draw(screen, font_title, font_hud, leaderboard):
    width, height = screen.get_size()

    title_surf = font_title.render("LEADERBOARD LOCAL", True, settings.COLORS["accent"])
    screen.blit(title_surf, title_surf.get_rect(center=(width // 2, 90)))

    top_entries = leaderboard.get_top(10)
    y = 210

    if not top_entries:
        empty_surf = font_hud.render(
            "Aun no hay resultados. Juega un nivel o el Modo Examen.",
            True,
            settings.COLORS["text_pending"],
        )
        screen.blit(empty_surf, empty_surf.get_rect(center=(width // 2, y)))
    else:
        for rank, (name, entry) in enumerate(top_entries, start=1):
            line = f"{rank}. {name} - {entry['wpm']:.0f} WPM  ({entry['precision']:.0f}% precision)"
            color = settings.COLORS["accent"] if rank == 1 else settings.COLORS["text"]
            surf = font_hud.render(line, True, color)
            screen.blit(surf, surf.get_rect(center=(width // 2, y)))
            y += surf.get_height() + 16

    hint_surf = font_hud.render("ESC para volver al menu", True, settings.COLORS["text_pending"])
    screen.blit(hint_surf, hint_surf.get_rect(center=(width // 2, height - 60)))
