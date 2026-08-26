from config import settings


def draw(screen, font_title, font_hud):
    width, height = screen.get_size()

    title_surf = font_title.render("TECLAZO RD", True, settings.COLORS["accent"])
    screen.blit(title_surf, title_surf.get_rect(center=(width // 2, height // 3)))

    hint_lines = [
        "ENTER elegir nivel  -  E estadisticas  -  L logros",
        "R leaderboard  -  P practica  -  X modo examen",
        "N modo numpad  -  V modo versus  -  C configuracion  -  ESC salir",
    ]
    y = height // 2
    for line in hint_lines:
        surf = font_hud.render(line, True, settings.COLORS["text"])
        screen.blit(surf, surf.get_rect(center=(width // 2, y)))
        y += surf.get_height() + 8
