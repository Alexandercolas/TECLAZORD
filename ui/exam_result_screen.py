from datetime import date

from config import settings
from systems.exam import classify_wpm


def draw(screen, font_title, font_hud, result, player):
    width, height = screen.get_size()

    title_surf = font_title.render("CERTIFICADO DE MECANOGRAFIA", True, settings.COLORS["accent"])
    screen.blit(title_surf, title_surf.get_rect(center=(width // 2, 90)))

    level_label = classify_wpm(result["wpm"])
    today = date.today().strftime("%d/%m/%Y")

    lines = [
        f"Nombre: {player.data['name']}",
        f"Fecha: {today}",
        "",
        f"WPM: {result['wpm']}",
        f"Precision: {result['precision']}%",
        f"Errores: {result['errors']}",
        f"Nivel alcanzado: {level_label}",
    ]

    if result.get("leaderboard_updated"):
        lines.append("")
        lines.append("NUEVO MEJOR PERSONAL EN EL LEADERBOARD")

    y = 220
    for line in lines:
        surf = font_hud.render(line, True, settings.COLORS["text"])
        screen.blit(surf, surf.get_rect(center=(width // 2, y)))
        y += surf.get_height() + 14

    hint_surf = font_hud.render(
        "ENTER para elegir nivel    -    ESC para el menu", True, settings.COLORS["text_pending"],
    )
    screen.blit(hint_surf, hint_surf.get_rect(center=(width // 2, height - 60)))
