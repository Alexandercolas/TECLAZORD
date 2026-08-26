from config import settings
from systems.achievements import ACHIEVEMENT_DEFINITIONS


def draw(screen, font_title, font_hud, achievements):
    width, height = screen.get_size()

    title_surf = font_title.render("LOGROS", True, settings.COLORS["accent"])
    screen.blit(title_surf, title_surf.get_rect(center=(width // 2, 80)))

    y = 180
    for definition in ACHIEVEMENT_DEFINITIONS:
        unlocked = achievements.is_unlocked(definition["id"])
        color = settings.COLORS["accent"] if unlocked else settings.COLORS["text_pending"]
        mark = "[X]" if unlocked else "[ ]"
        label = f"{mark} {definition['name']} - {definition['description']}"

        surf = font_hud.render(label, True, color)
        screen.blit(surf, surf.get_rect(center=(width // 2, y)))
        y += surf.get_height() + 16

    hint_surf = font_hud.render("ESC para volver al menu", True, settings.COLORS["text_pending"])
    screen.blit(hint_surf, hint_surf.get_rect(center=(width // 2, height - 60)))
