from config import settings
from systems.free_practice import CATEGORIES, CATEGORY_LABELS


def draw(screen, font_title, font_hud, selected_index):
    width, height = screen.get_size()

    title_surf = font_title.render("PRACTICA LIBRE", True, settings.COLORS["accent"])
    screen.blit(title_surf, title_surf.get_rect(center=(width // 2, 90)))

    y = 220
    for i, category in enumerate(CATEGORIES):
        color = settings.COLORS["accent"] if i == selected_index else settings.COLORS["text"]
        surf = font_hud.render(CATEGORY_LABELS[category], True, color)
        screen.blit(surf, surf.get_rect(center=(width // 2, y)))
        y += surf.get_height() + 22

    hint_surf = font_hud.render(
        "ARRIBA/ABAJO elegir  -  ENTER jugar  -  ESC volver", True, settings.COLORS["text_pending"],
    )
    screen.blit(hint_surf, hint_surf.get_rect(center=(width // 2, height - 60)))
