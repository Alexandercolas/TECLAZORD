from config import settings
from systems.versus import determine_winner


def draw(screen, font_title, font_hud, versus_state):
    width, height = screen.get_size()

    p1_name = versus_state["p1_name"]
    p2_name = versus_state["p2_name"]
    p1 = versus_state["p1_result"]
    p2 = versus_state["p2_result"]
    winner_line = determine_winner(p1_name, p1, p2_name, p2)

    title_surf = font_title.render("RESULTADO DEL DUELO", True, settings.COLORS["accent"])
    screen.blit(title_surf, title_surf.get_rect(center=(width // 2, 90)))

    lines = [
        f"{p1_name}: {p1['wpm']} WPM  ({p1['precision']}% precision, {p1['errors']} errores)",
        f"{p2_name}: {p2['wpm']} WPM  ({p2['precision']}% precision, {p2['errors']} errores)",
        "",
        winner_line,
    ]

    y = 250
    for line in lines:
        color = settings.COLORS["accent"] if line == winner_line else settings.COLORS["text"]
        surf = font_hud.render(line, True, color)
        screen.blit(surf, surf.get_rect(center=(width // 2, y)))
        y += surf.get_height() + 16

    hint_surf = font_hud.render("ESC para volver al menu", True, settings.COLORS["text_pending"])
    screen.blit(hint_surf, hint_surf.get_rect(center=(width // 2, height - 60)))
