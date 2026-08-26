from config import settings


def draw(screen, font_title, font_hud, title, buffer_text, subtitle=""):
    width, height = screen.get_size()

    title_surf = font_title.render(title, True, settings.COLORS["accent"])
    screen.blit(title_surf, title_surf.get_rect(center=(width // 2, height // 3)))

    if subtitle:
        subtitle_surf = font_hud.render(subtitle, True, settings.COLORS["text_pending"])
        screen.blit(subtitle_surf, subtitle_surf.get_rect(center=(width // 2, height // 3 + 50)))

    input_surf = font_hud.render(buffer_text + "_", True, settings.COLORS["text"])
    screen.blit(input_surf, input_surf.get_rect(center=(width // 2, height // 2)))

    hint_surf = font_hud.render(
        "Escribe tu nombre y presiona ENTER    -    ESC para cancelar",
        True,
        settings.COLORS["text_pending"],
    )
    screen.blit(hint_surf, hint_surf.get_rect(center=(width // 2, height // 2 + 60)))
