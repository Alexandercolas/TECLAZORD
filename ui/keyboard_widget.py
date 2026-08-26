import pygame

from config import settings

MAIN_ROWS = [
    list("`1234567890-="),
    list("qwertyuiop[]"),
    list("asdfghjklñ;'"),
    list("zxcvbnm,./"),
]

NUMPAD_ROWS = [
    list("789"),
    list("456"),
    list("123"),
    ["0", "."],
]

# Simbolos generados con Shift (Nivel 6): se resalta la tecla fisica base,
# no un simbolo que no existe en el diagrama simplificado del teclado.
SHIFT_TO_BASE_KEY = {
    "!": "1", "@": "2", "#": "3", "$": "4", "%": "5",
    "^": "6", "&": "7", "*": "8", "(": "9", ")": "0",
    "_": "-", "+": "=", "{": "[", "}": "]",
    ":": ";", '"': "'", "<": ",", ">": ".", "?": "/", "~": "`",
}

KEY_SIZE = 34
KEY_GAP = 5


def draw(screen, font_hud, next_char):
    target_key = _resolve_target_key(next_char)
    _draw_rows(screen, font_hud, MAIN_ROWS, start_x=40, stagger=True, target_key=target_key)
    _draw_enter_key(screen, font_hud, target_key)
    width, _ = screen.get_size()
    numpad_x = width - 40 - 3 * (KEY_SIZE + KEY_GAP)
    _draw_rows(screen, font_hud, NUMPAD_ROWS, start_x=numpad_x, stagger=False, target_key=target_key)


def _resolve_target_key(next_char):
    if not next_char:
        return None
    if next_char == "\n":
        return "\n"
    lowered = next_char.lower()
    if lowered == " ":
        return None
    return SHIFT_TO_BASE_KEY.get(lowered, lowered)


def _draw_enter_key(screen, font_hud, target_key):
    row_index = 1  # a la derecha de la fila QWERTY, como en un teclado real
    row_start_x = 40 + row_index * (KEY_SIZE // 2)
    x = row_start_x + len(MAIN_ROWS[row_index]) * (KEY_SIZE + KEY_GAP)

    _, height = screen.get_size()
    base_y = height - 210
    y = base_y + row_index * (KEY_SIZE + KEY_GAP)

    _draw_key(screen, font_hud, x, y, "ENTER", target_key == "\n", width=KEY_SIZE * 2 + KEY_GAP)


def _draw_rows(screen, font_hud, rows, start_x, stagger, target_key):
    _, height = screen.get_size()
    base_y = height - 210

    for row_index, row in enumerate(rows):
        offset_x = start_x + (row_index * (KEY_SIZE // 2) if stagger else 0)
        y = base_y + row_index * (KEY_SIZE + KEY_GAP)
        for col_index, key in enumerate(row):
            x = offset_x + col_index * (KEY_SIZE + KEY_GAP)
            _draw_key(screen, font_hud, x, y, key, key == target_key)


def _draw_key(screen, font_hud, x, y, label, highlighted, width=KEY_SIZE):
    rect = pygame.Rect(x, y, width, KEY_SIZE)
    fill_color = settings.COLORS["accent"] if highlighted else settings.COLORS["panel"]
    pygame.draw.rect(screen, fill_color, rect, border_radius=6)
    pygame.draw.rect(screen, settings.COLORS["text_pending"], rect, width=1, border_radius=6)

    text_color = settings.COLORS["background"] if highlighted else settings.COLORS["text"]
    surf = font_hud.render(label.upper(), True, text_color)
    screen.blit(surf, surf.get_rect(center=rect.center))
