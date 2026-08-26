from config import settings


def draw(screen, font_title, font_hud, game_settings, player):
    width, height = screen.get_size()

    title_surf = font_title.render("CONFIGURACION", True, settings.COLORS["accent"])
    screen.blit(title_surf, title_surf.get_rect(center=(width // 2, 100)))

    sound_status = "ACTIVADO" if game_settings.data["sound_enabled"] else "DESACTIVADO"
    volume_pct = int(game_settings.data["volume"] * 100)

    lines = [
        f"Nombre: {player.data['name']}",
        f"Sonido: {sound_status}",
        f"Volumen: {volume_pct}%",
        "",
        "N para cambiar tu nombre (usado en el leaderboard)",
        "M para activar/desactivar el sonido",
        "FLECHA IZQUIERDA / DERECHA para ajustar el volumen",
    ]

    y = 260
    for line in lines:
        surf = font_hud.render(line, True, settings.COLORS["text"])
        screen.blit(surf, surf.get_rect(center=(width // 2, y)))
        y += surf.get_height() + 18

    hint_surf = font_hud.render("ESC para volver al menu", True, settings.COLORS["text_pending"])
    screen.blit(hint_surf, hint_surf.get_rect(center=(width // 2, height - 60)))
