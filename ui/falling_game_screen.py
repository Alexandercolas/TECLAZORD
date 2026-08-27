import pygame

from config import settings
from core import scoring
from ui import keyboard_widget

FALL_ZONE_TOP = 140
FALL_ZONE_BOTTOM_MARGIN = 240  # deja espacio libre para el teclado visual


def draw(screen, font_text, font_hud, session, level_module, fall_progress):
    width, height = screen.get_size()
    input_manager = session["input_manager"]
    typed = input_manager.typed
    target = input_manager.target_text
    timer = session["timer"]

    completed = session["completed_managers"]
    live_correct = sum(m.correct_count for m in completed) + input_manager.correct_count
    live_typed = sum(len(m.typed) for m in completed) + len(typed)
    live_errors = sum(m.error_count for m in completed) + input_manager.error_count

    elapsed = timer.elapsed()
    wpm_live = scoring.calculate_wpm(live_correct, elapsed)
    precision_live = scoring.calculate_precision(live_correct, live_typed)

    hud_line_1 = (
        f"NIVEL {level_module.LEVEL_NUMBER} - {level_module.NAME}    "
        f"EJERCICIO {session['exercise_index'] + 1}/{len(session['exercises'])}"
    )
    hud_line_2 = (
        f"TIEMPO {int(timer.remaining()):02d}s    "
        f"WPM {wpm_live:.0f}    "
        f"PRECISION {precision_live:.0f}%    "
        f"ERRORES {live_errors}    "
        f"COMBO x{input_manager.combo}"
    )
    for i, line in enumerate((hud_line_1, hud_line_2)):
        surf = font_hud.render(line, True, settings.COLORS["text"])
        screen.blit(surf, (40, 40 + i * (surf.get_height() + 6)))

    fall_zone_bottom = height - FALL_ZONE_BOTTOM_MARGIN
    pygame.draw.line(
        screen, settings.COLORS["text_pending"],
        (40, fall_zone_bottom), (width - 40, fall_zone_bottom),
    )

    _draw_falling_phrase(screen, font_hud, target, typed, width, fall_progress, FALL_ZONE_TOP, fall_zone_bottom)

    next_char = target[len(typed)] if len(typed) < len(target) else None
    keyboard_widget.draw(screen, font_hud, next_char)


def _draw_falling_phrase(screen, font, target, typed, width, fall_progress, zone_top, zone_bottom):
    y = zone_top + fall_progress * (zone_bottom - zone_top)

    char_surfaces = []
    total_width = 0
    for i, ch in enumerate(target):
        if i < len(typed):
            color = settings.COLORS["text_correct"] if typed[i] == ch else settings.COLORS["text_error"]
        elif i == len(typed):
            color = settings.COLORS["accent"]
        else:
            color = settings.COLORS["text_pending"]

        surf = font.render(ch, True, color)
        char_surfaces.append(surf)
        total_width += surf.get_width()

    x = (width - total_width) // 2
    for surf in char_surfaces:
        screen.blit(surf, (x, int(y)))
        x += surf.get_width()
