from config import settings
from core import scoring
from ui import keyboard_widget


def draw(screen, font_text, font_hud, session, level_module):
    width, _ = screen.get_size()
    input_manager = session["input_manager"]
    timer = session["timer"]
    target = input_manager.target_text
    typed = input_manager.typed

    completed = session["completed_managers"]
    live_correct = sum(m.correct_count for m in completed) + input_manager.correct_count
    live_typed = sum(len(m.typed) for m in completed) + len(typed)
    live_errors = sum(m.error_count for m in completed) + input_manager.error_count

    elapsed = timer.elapsed()
    wpm_live = scoring.calculate_wpm(live_correct, elapsed)
    precision_live = scoring.calculate_precision(live_correct, live_typed)

    level_label = (
        level_module.NAME
        if level_module.LEVEL_NUMBER is None
        else f"NIVEL {level_module.LEVEL_NUMBER} - {level_module.NAME}"
    )
    hud_line_1 = (
        f"{level_label}    "
        f"EJERCICIO {session['exercise_index'] + 1}/{len(session['exercises'])}"
    )
    hud_line_2 = (
        f"TIEMPO {int(timer.remaining()):02d}s    "
        f"WPM {wpm_live:.0f}    "
        f"PRECISION {precision_live:.0f}%    "
        f"ERRORES {live_errors}    "
        f"COMBO x{input_manager.combo}"
    )
    # Dos lineas separadas para que no se corte con niveles de nombre largo.
    for i, line in enumerate((hud_line_1, hud_line_2)):
        surf = font_hud.render(line, True, settings.COLORS["text"])
        screen.blit(surf, (40, 40 + i * (surf.get_height() + 6)))

    _draw_target_text(screen, font_text, target, typed, width)

    next_char = target[len(typed)] if len(typed) < len(target) else None
    keyboard_widget.draw(screen, font_hud, next_char)


def _draw_target_text(screen, font_text, target, typed, width):
    x, y = 40, 140
    max_x = width - 40
    line_height = font_text.get_height() + 8
    cursor_x, cursor_y = x, y

    for i, ch in enumerate(target):
        if ch == "\n":
            cursor_x = x
            cursor_y += line_height
            continue

        if i < len(typed):
            color = (
                settings.COLORS["text_correct"]
                if typed[i] == ch
                else settings.COLORS["text_error"]
            )
        elif i == len(typed):
            color = settings.COLORS["accent"]
        else:
            color = settings.COLORS["text_pending"]

        ch_surf = font_text.render(ch, True, color)

        if cursor_x + ch_surf.get_width() > max_x:
            cursor_x = x
            cursor_y += line_height

        screen.blit(ch_surf, (cursor_x, cursor_y))
        cursor_x += ch_surf.get_width()
