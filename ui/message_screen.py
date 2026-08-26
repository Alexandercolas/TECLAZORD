from config import settings


def draw(screen, font_title, font_hud, title, message):
    width, height = screen.get_size()

    title_surf = font_title.render(title, True, settings.COLORS["accent"])
    screen.blit(title_surf, title_surf.get_rect(center=(width // 2, height // 3)))

    message_surf = font_hud.render(message, True, settings.COLORS["text"])
    screen.blit(message_surf, message_surf.get_rect(center=(width // 2, height // 2)))

    hint_surf = font_hud.render("ESC para volver al menu", True, settings.COLORS["text_pending"])
    screen.blit(hint_surf, hint_surf.get_rect(center=(width // 2, height - 100)))
