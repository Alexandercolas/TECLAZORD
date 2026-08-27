WINDOW_WIDTH = 1024
WINDOW_HEIGHT = 720
FPS = 60
TITLE = "TECLAZO RD"

COLORS = {
    "background": (18, 18, 28),
    "text": (230, 230, 235),
    "text_correct": (90, 200, 120),
    "text_error": (220, 70, 70),
    "text_pending": (140, 140, 150),
    "accent": (240, 190, 40),
    "panel": (30, 30, 45),
}

FONT_NAME = "arial"
FONT_SIZE_TEXT = 34
FONT_SIZE_HUD = 22
FONT_SIZE_TITLE = 52

DATA_DIR = "data"

# Puntuacion minima para desbloquear el siguiente nivel.
LEVEL_UNLOCK_SCORE = 500

# Pesos de la formula conceptual del documento maestro:
# PUNTUACION = Velocidad + Precision + Combo + Bonificacion de tiempo - Penalizacion por errores
SCORING_WEIGHTS = {
    "speed_multiplier": 8.0,
    "precision_multiplier": 6.0,
    "combo_multiplier": 4.0,
    "time_bonus_multiplier": 3.0,
    "error_penalty_multiplier": 15.0,
}

# Porcentaje de precision necesario para 1/2/3 estrellas.
STAR_THRESHOLDS = {1: 70, 2: 85, 3: 95}

SOUND_VOLUME = 0.5
SOUND_FILES = {
    "type_correct": "assets/sounds/type_correct.wav",
    "type_error": "assets/sounds/type_error.wav",
    "menu_move": "assets/sounds/menu_move.wav",
    "combo_milestone": "assets/sounds/combo_milestone.wav",
    "level_complete": "assets/sounds/level_complete.wav",
    "level_failed": "assets/sounds/level_failed.wav",
    "achievement_unlocked": "assets/sounds/achievement_unlocked.wav",
    "phrase_complete": "assets/sounds/phrase_complete.wav",
}
