import random

import pygame

from config import settings
from core import scoring
from core.audio import SoundManager
from core.effects import EffectManager
from core.input_manager import InputManager
from core.keymap import NUMPAD_KEYS, is_numpad_key
from core.player import Player
from core.progression import Progression
from core.timer import GameTimer
from levels import registry
from systems.achievements import Achievements, check_level_result_achievements
from systems.exam import ExamLevel, get_exercises as get_exam_exercises
from systems.free_practice import CATEGORIES as FREE_PRACTICE_CATEGORIES
from systems.free_practice import FreePracticeLevel, get_exercises as get_free_practice_exercises
from systems.game_settings import GameSettings
from systems.key_stats import KeyStats
from systems.leaderboard import Leaderboard
from systems.numpad_training import NumpadLevel, get_exercises as get_numpad_exercises
from systems.statistics import Statistics
from systems.survival import (
    SURVIVAL_GRACE_CHARACTERS, SURVIVAL_MIN_PRECISION_PERCENT, SurvivalLevel,
    get_exercises as get_survival_exercises,
)
from systems.time_attack import DURATIONS as TIME_ATTACK_DURATIONS
from systems.time_attack import TimeAttackLevel, get_exercises as get_time_attack_exercises
from systems.training import TrainingLevel, generate_personalized_exercises
from systems.versus import VersusLevel, get_exercises as get_versus_exercises
from ui import (
    achievements_screen, exam_result_screen, free_practice_select_screen, game_screen,
    leaderboard_screen, level_select, menu, message_screen, name_entry_screen, results_screen,
    settings_screen, statistics_screen, survival_result_screen, time_attack_select_screen,
    versus_result_screen,
)

SCENE_MENU = "menu"
SCENE_LEVEL_SELECT = "level_select"
SCENE_LEVEL = "level"
SCENE_RESULTS = "results"
SCENE_STATISTICS = "statistics"
SCENE_ACHIEVEMENTS = "achievements"
SCENE_MESSAGE = "message"
SCENE_SETTINGS = "settings"
SCENE_LEADERBOARD = "leaderboard"
SCENE_NAME_ENTRY = "name_entry"
SCENE_VERSUS_NAME = "versus_name"
SCENE_VERSUS_RESULT = "versus_result"
SCENE_FREE_PRACTICE_SELECT = "free_practice_select"
SCENE_TIME_ATTACK_SELECT = "time_attack_select"

MAX_NAME_LENGTH = 20

FADE_DURATION_SECONDS = 0.18
FADE_ALPHA_MAX = 190
ERROR_FLASH_DURATION_SECONDS = 0.15
ERROR_FLASH_ALPHA_MAX = 70
COMBO_POPUP_DURATION_SECONDS = 0.7

# Fila superior de numeros: si se presionan durante el Modo Numpad, cuentan
# como error a proposito, para forzar el habito de usar el teclado numerico.
TOP_ROW_DIGIT_KEYS = {getattr(pygame, f"K_{i}") for i in range(10)} | {pygame.K_PERIOD}


class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((settings.WINDOW_WIDTH, settings.WINDOW_HEIGHT))
        pygame.display.set_caption(settings.TITLE)
        self.clock = pygame.time.Clock()

        self.font_text = pygame.font.SysFont(settings.FONT_NAME, settings.FONT_SIZE_TEXT)
        self.font_hud = pygame.font.SysFont(settings.FONT_NAME, settings.FONT_SIZE_HUD)
        self.font_title = pygame.font.SysFont(settings.FONT_NAME, settings.FONT_SIZE_TITLE, bold=True)

        self.running = True
        self.scene = SCENE_MENU
        self.progression = Progression()
        self.statistics = Statistics()
        self.player = Player()
        self.achievements = Achievements()
        self.key_stats = KeyStats()
        self.leaderboard = Leaderboard()
        self.game_settings = GameSettings()
        self.sound = SoundManager()
        self.sound.set_master_enabled(self.game_settings.data["sound_enabled"])
        self.sound.set_volume(self.game_settings.data["volume"])
        self.effects = EffectManager()
        self.level_session = None
        self.last_result = None
        self.level_select_index = 0
        self.message_title = ""
        self.message_body = ""
        self.name_entry_buffer = ""
        self.versus_state = None
        self.free_practice_index = 0
        self.time_attack_index = 1

    def run(self):
        while self.running:
            self.clock.tick(settings.FPS)
            self._handle_events()
            self.effects.update()
            self._render()
        pygame.quit()

    def _change_scene(self, new_scene):
        self.scene = new_scene
        self.effects.trigger("fade", FADE_DURATION_SECONDS)

    def _handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif self.scene == SCENE_MENU:
                self._handle_menu_event(event)
            elif self.scene == SCENE_LEVEL_SELECT:
                self._handle_level_select_event(event)
            elif self.scene == SCENE_LEVEL:
                self._handle_level_event(event)
            elif self.scene == SCENE_RESULTS:
                self._handle_results_event(event)
            elif self.scene == SCENE_STATISTICS:
                self._handle_statistics_event(event)
            elif self.scene == SCENE_ACHIEVEMENTS:
                self._handle_achievements_event(event)
            elif self.scene == SCENE_MESSAGE:
                self._handle_message_event(event)
            elif self.scene == SCENE_SETTINGS:
                self._handle_settings_event(event)
            elif self.scene == SCENE_LEADERBOARD:
                self._handle_leaderboard_event(event)
            elif self.scene == SCENE_NAME_ENTRY:
                self._handle_name_entry_event(event)
            elif self.scene == SCENE_VERSUS_NAME:
                self._handle_versus_name_event(event)
            elif self.scene == SCENE_VERSUS_RESULT:
                self._handle_versus_result_event(event)
            elif self.scene == SCENE_FREE_PRACTICE_SELECT:
                self._handle_free_practice_select_event(event)
            elif self.scene == SCENE_TIME_ATTACK_SELECT:
                self._handle_time_attack_select_event(event)

    def _handle_menu_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self._change_scene(SCENE_LEVEL_SELECT)
        elif event.key == pygame.K_e:
            self._change_scene(SCENE_STATISTICS)
        elif event.key == pygame.K_l:
            self._change_scene(SCENE_ACHIEVEMENTS)
        elif event.key == pygame.K_p:
            self._start_training_mode()
        elif event.key == pygame.K_c:
            self._change_scene(SCENE_SETTINGS)
        elif event.key == pygame.K_r:
            self._change_scene(SCENE_LEADERBOARD)
        elif event.key == pygame.K_x:
            self._start_exam_mode()
        elif event.key == pygame.K_n:
            self._start_numpad_mode()
        elif event.key == pygame.K_v:
            self._start_versus_mode()
        elif event.key == pygame.K_f:
            self._change_scene(SCENE_FREE_PRACTICE_SELECT)
        elif event.key == pygame.K_t:
            self._change_scene(SCENE_TIME_ATTACK_SELECT)
        elif event.key == pygame.K_s:
            self._start_survival_mode()
        elif event.key == pygame.K_a:
            self._start_random_mode()
        elif event.key == pygame.K_ESCAPE:
            self.running = False

    def _start_random_mode(self):
        """Elige al azar entre todo lo que existe: los 10 niveles
        desbloqueados y todos los modos especiales (menos Versus, que
        necesita nombres de 2 jugadores primero). Reutiliza los metodos
        _start_* existentes, no duplica logica de ninguno."""
        choices = []

        unlocked_levels = [n for n in registry.get_all_numbers() if self.progression.is_unlocked(n)]
        if unlocked_levels:
            choices.append(("level", random.choice(unlocked_levels)))

        for category in FREE_PRACTICE_CATEGORIES:
            choices.append(("free_practice", category))

        for duration in TIME_ATTACK_DURATIONS:
            choices.append(("time_attack", duration))

        choices.append(("exam", None))
        choices.append(("survival", None))
        choices.append(("numpad", None))

        if generate_personalized_exercises(self.key_stats):
            choices.append(("training", None))

        kind, value = random.choice(choices)

        if kind == "level":
            self._start_level(value)
        elif kind == "free_practice":
            if value == "numpad":
                self._start_numpad_mode()
            else:
                self._start_free_practice(value)
        elif kind == "time_attack":
            self._start_time_attack(value)
        elif kind == "exam":
            self._start_exam_mode()
        elif kind == "survival":
            self._start_survival_mode()
        elif kind == "numpad":
            self._start_numpad_mode()
        elif kind == "training":
            self._start_training_mode()

    def _start_training_mode(self):
        exercises = generate_personalized_exercises(self.key_stats)
        if not exercises:
            self.message_title = "ENTRENAMIENTO PERSONALIZADO"
            self.message_body = "Aun no hay suficientes datos. Juega algunos niveles primero."
            self._change_scene(SCENE_MESSAGE)
            return

        self.level_session = {
            "level_number": None,
            "level_module": TrainingLevel,
            "exercises": exercises,
            "exercise_index": 0,
            "input_manager": InputManager(exercises[0]),
            "completed_managers": [],
            "timer": GameTimer(TrainingLevel.TIME_LIMIT_SECONDS),
            "is_training": True,
            "is_exam": False,
            "is_numpad_mode": False,
            "is_versus": False,
        }
        self.level_session["timer"].start()
        self._change_scene(SCENE_LEVEL)

    def _start_exam_mode(self):
        exercises = get_exam_exercises()
        self.level_session = {
            "level_number": None,
            "level_module": ExamLevel,
            "exercises": exercises,
            "exercise_index": 0,
            "input_manager": InputManager(exercises[0]),
            "completed_managers": [],
            "timer": GameTimer(ExamLevel.TIME_LIMIT_SECONDS),
            "is_training": False,
            "is_exam": True,
            "is_numpad_mode": False,
            "is_versus": False,
        }
        self.level_session["timer"].start()
        self._change_scene(SCENE_LEVEL)

    def _start_numpad_mode(self):
        exercises = get_numpad_exercises()
        self.level_session = {
            "level_number": None,
            "level_module": NumpadLevel,
            "exercises": exercises,
            "exercise_index": 0,
            "input_manager": InputManager(exercises[0]),
            "completed_managers": [],
            "timer": GameTimer(NumpadLevel.TIME_LIMIT_SECONDS),
            "is_training": False,
            "is_exam": False,
            "is_numpad_mode": True,
            "is_versus": False,
        }
        self.level_session["timer"].start()
        self._change_scene(SCENE_LEVEL)

    def _start_versus_mode(self):
        self.versus_state = {
            "stage": "p1_name",
            "p1_name": "",
            "p2_name": "",
            "p1_result": None,
            "p2_result": None,
        }
        self.name_entry_buffer = ""
        self._change_scene(SCENE_VERSUS_NAME)

    def _handle_versus_name_event(self, event):
        if event.type == pygame.TEXTINPUT:
            if len(self.name_entry_buffer) < MAX_NAME_LENGTH:
                self.name_entry_buffer += event.text
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.name_entry_buffer = self.name_entry_buffer[:-1]
            elif event.key == pygame.K_RETURN:
                name = self.name_entry_buffer.strip() or "Jugador"
                player_number = 1 if self.versus_state["stage"] == "p1_name" else 2
                self.versus_state[f"p{player_number}_name"] = name
                self.name_entry_buffer = ""
                self._start_versus_round(player_number)
            elif event.key == pygame.K_ESCAPE:
                self._change_scene(SCENE_MENU)

    def _start_versus_round(self, player_number):
        player_name = self.versus_state[f"p{player_number}_name"]
        VersusLevel.NAME = f"TURNO DE {player_name.upper()}"

        exercises = get_versus_exercises()
        self.level_session = {
            "level_number": None,
            "level_module": VersusLevel,
            "exercises": exercises,
            "exercise_index": 0,
            "input_manager": InputManager(exercises[0]),
            "completed_managers": [],
            "timer": GameTimer(VersusLevel.TIME_LIMIT_SECONDS),
            "is_training": False,
            "is_exam": False,
            "is_numpad_mode": False,
            "is_versus": True,
            "versus_player_number": player_number,
        }
        self.level_session["timer"].start()
        self._change_scene(SCENE_LEVEL)

    def _handle_versus_result_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._change_scene(SCENE_MENU)

    def _handle_free_practice_select_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_UP:
            self.free_practice_index = (self.free_practice_index - 1) % len(FREE_PRACTICE_CATEGORIES)
            self.sound.play("menu_move")
        elif event.key == pygame.K_DOWN:
            self.free_practice_index = (self.free_practice_index + 1) % len(FREE_PRACTICE_CATEGORIES)
            self.sound.play("menu_move")
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            category = FREE_PRACTICE_CATEGORIES[self.free_practice_index]
            if category == "numpad":
                # El teclado numerico dedicado ya tiene su propio modo con
                # la deteccion de tecla fisica; se reutiliza en vez de duplicarlo.
                self._start_numpad_mode()
            else:
                self._start_free_practice(category)
        elif event.key == pygame.K_ESCAPE:
            self._change_scene(SCENE_MENU)

    def _start_free_practice(self, category):
        exercises = get_free_practice_exercises(category)
        FreePracticeLevel.NAME = f"PRACTICA LIBRE - {category.upper()}"

        self.level_session = {
            "level_number": None,
            "level_module": FreePracticeLevel,
            "exercises": exercises,
            "exercise_index": 0,
            "input_manager": InputManager(exercises[0]),
            "completed_managers": [],
            "timer": GameTimer(FreePracticeLevel.TIME_LIMIT_SECONDS),
            "is_training": True,
            "is_exam": False,
            "is_numpad_mode": False,
            "is_versus": False,
        }
        self.level_session["timer"].start()
        self._change_scene(SCENE_LEVEL)

    def _handle_time_attack_select_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        if event.key == pygame.K_UP:
            self.time_attack_index = (self.time_attack_index - 1) % len(TIME_ATTACK_DURATIONS)
            self.sound.play("menu_move")
        elif event.key == pygame.K_DOWN:
            self.time_attack_index = (self.time_attack_index + 1) % len(TIME_ATTACK_DURATIONS)
            self.sound.play("menu_move")
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self._start_time_attack(TIME_ATTACK_DURATIONS[self.time_attack_index])
        elif event.key == pygame.K_ESCAPE:
            self._change_scene(SCENE_MENU)

    def _start_time_attack(self, duration_seconds):
        exercises = get_time_attack_exercises()
        TimeAttackLevel.NAME = f"CONTRARRELOJ {duration_seconds}s"
        TimeAttackLevel.TIME_LIMIT_SECONDS = duration_seconds

        self.level_session = {
            "level_number": None,
            "level_module": TimeAttackLevel,
            "exercises": exercises,
            "exercise_index": 0,
            "input_manager": InputManager(exercises[0]),
            "completed_managers": [],
            "timer": GameTimer(duration_seconds),
            "is_training": False,
            "is_exam": False,
            "is_numpad_mode": False,
            "is_versus": False,
            "is_time_attack": True,
            # Con ejercicios cortos y hasta 120s de duracion, el jugador
            # puede agotar la lista antes de que se acabe el tiempo: se
            # reinicia en bucle en vez de terminar la ronda antes de tiempo.
            "cycle_exercises": True,
        }
        self.level_session["timer"].start()
        self._change_scene(SCENE_LEVEL)

    def _start_survival_mode(self):
        exercises = get_survival_exercises()
        self.level_session = {
            "level_number": None,
            "level_module": SurvivalLevel,
            "exercises": exercises,
            "exercise_index": 0,
            "input_manager": InputManager(exercises[0]),
            "completed_managers": [],
            "timer": GameTimer(SurvivalLevel.TIME_LIMIT_SECONDS),
            "is_training": False,
            "is_exam": False,
            "is_numpad_mode": False,
            "is_versus": False,
            "is_time_attack": False,
            "is_survival": True,
            "cycle_exercises": True,
        }
        self.level_session["timer"].start()
        self._change_scene(SCENE_LEVEL)

    def _survival_precision_too_low(self, session):
        managers = session["completed_managers"] + [session["input_manager"]]
        typed_count = sum(len(m.typed) for m in managers)
        if typed_count < SURVIVAL_GRACE_CHARACTERS:
            return False
        correct_count = sum(m.correct_count for m in managers)
        precision = scoring.calculate_precision(correct_count, typed_count)
        return precision < SURVIVAL_MIN_PRECISION_PERCENT

    def _handle_level_select_event(self, event):
        if event.type != pygame.KEYDOWN:
            return

        level_numbers = registry.get_all_numbers()

        if event.key == pygame.K_UP:
            self.level_select_index = (self.level_select_index - 1) % len(level_numbers)
            self.sound.play("menu_move")
        elif event.key == pygame.K_DOWN:
            self.level_select_index = (self.level_select_index + 1) % len(level_numbers)
            self.sound.play("menu_move")
        elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
            level_number = level_numbers[self.level_select_index]
            if self.progression.is_unlocked(level_number):
                self._start_level(level_number)
        elif event.key == pygame.K_ESCAPE:
            self._change_scene(SCENE_MENU)

    def _start_level(self, level_number):
        level_module = registry.get_level(level_number)
        exercises = level_module.get_exercises()
        self.level_session = {
            "level_number": level_number,
            "level_module": level_module,
            "exercises": exercises,
            "exercise_index": 0,
            "input_manager": InputManager(exercises[0]),
            "completed_managers": [],
            "timer": GameTimer(level_module.TIME_LIMIT_SECONDS),
            "is_training": False,
            "is_exam": False,
            "is_numpad_mode": False,
            "is_versus": False,
        }
        self.level_session["timer"].start()
        self._change_scene(SCENE_LEVEL)

    def _handle_keystroke_feedback(self, was_correct, input_manager):
        if was_correct is True:
            self.sound.play("type_correct")
            if input_manager.combo > 0 and input_manager.combo % 20 == 0:
                self.sound.play("combo_milestone")
                self.effects.trigger(
                    "combo_popup", COMBO_POPUP_DURATION_SECONDS, {"combo": input_manager.combo},
                )
        elif was_correct is False:
            self.sound.play("type_error")
            self.effects.trigger("flash_error", ERROR_FLASH_DURATION_SECONDS)

    def _handle_generic_input(self, event, input_manager):
        if event.type == pygame.TEXTINPUT:
            for char in event.text:
                self._handle_keystroke_feedback(input_manager.handle_text_input(char), input_manager)
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_RETURN:
            # El codigo del Nivel 8 necesita saltos de linea reales;
            # TEXTINPUT no dispara para Enter, asi que se traduce aqui.
            was_correct = input_manager.handle_text_input("\n")
            self._handle_keystroke_feedback(was_correct, input_manager)

    def _handle_numpad_keydown(self, event, input_manager):
        # A diferencia de todos los demas modos, aqui se ignora TEXTINPUT
        # por completo: solo cuenta de que tecla FISICA vino el digito.
        if event.type != pygame.KEYDOWN:
            return

        if is_numpad_key(event.key):
            char = NUMPAD_KEYS[event.key]
            if char == "\n":
                return
            was_correct = input_manager.handle_text_input(char)
            self._handle_keystroke_feedback(was_correct, input_manager)
        elif event.key in TOP_ROW_DIGIT_KEYS:
            # Se uso la fila superior en vez del Numpad: cuenta como error
            # a proposito, para reforzar el habito que pide este modo.
            was_correct = input_manager.handle_text_input("?")
            self._handle_keystroke_feedback(was_correct, input_manager)

    def _handle_level_event(self, event):
        session = self.level_session
        input_manager = session["input_manager"]

        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._change_scene(SCENE_LEVEL_SELECT)
            return

        if event.type == pygame.KEYDOWN and event.key == pygame.K_BACKSPACE:
            input_manager.handle_backspace()
        elif session.get("is_numpad_mode", False):
            self._handle_numpad_keydown(event, input_manager)
        else:
            self._handle_generic_input(event, input_manager)

        if session.get("is_survival", False) and self._survival_precision_too_low(session):
            self._finish_level()
            return

        if input_manager.is_complete():
            next_index = session["exercise_index"] + 1
            if next_index >= len(session["exercises"]) and session.get("cycle_exercises", False):
                next_index = 0
            if next_index < len(session["exercises"]):
                # Un ejercicio a la vez (no todos pegados en un solo texto),
                # para que quepa en pantalla incluso en niveles con muchas
                # lineas de codigo. La racha de combo se conserva entre
                # ejercicios para que se sienta continua.
                session["completed_managers"].append(input_manager)
                next_manager = InputManager(session["exercises"][next_index])
                next_manager.combo = input_manager.combo
                next_manager.max_combo = input_manager.combo
                session["exercise_index"] = next_index
                session["input_manager"] = next_manager
            else:
                self._finish_level()
                return

        if session["timer"].is_expired():
            self._finish_level()

    def _finish_versus_round(self, session, wpm, precision, error_count, max_combo, score):
        player_number = session["versus_player_number"]
        player_name = self.versus_state[f"p{player_number}_name"]
        round_result = {
            "wpm": round(wpm, 1),
            "precision": round(precision, 1),
            "errors": error_count,
            "max_combo": max_combo,
        }
        self.versus_state[f"p{player_number}_result"] = round_result

        # El duelo tambien alimenta el leaderboard: es una medicion real de
        # velocidad, igual que el Modo Examen.
        self.leaderboard.register_run(player_name, wpm, precision, None, score)

        if player_number == 1:
            self.versus_state["stage"] = "p2_name"
            self.name_entry_buffer = ""
            self._change_scene(SCENE_VERSUS_NAME)
        else:
            self.versus_state["stage"] = "done"
            self._change_scene(SCENE_VERSUS_RESULT)

    def _finish_level(self):
        session = self.level_session
        timer = session["timer"]
        level_module = session["level_module"]
        managers = session["completed_managers"] + [session["input_manager"]]

        correct_count = sum(m.correct_count for m in managers)
        error_count = sum(m.error_count for m in managers)
        typed_count = sum(len(m.typed) for m in managers)
        max_combo = max(m.max_combo for m in managers)

        elapsed = min(timer.elapsed(), level_module.TIME_LIMIT_SECONDS)
        wpm = scoring.calculate_wpm(correct_count, elapsed)
        precision = scoring.calculate_precision(correct_count, typed_count)
        time_remaining_pct = (timer.remaining() / level_module.TIME_LIMIT_SECONDS) * 100
        score = scoring.calculate_score(
            wpm, precision, error_count, max_combo, time_remaining_pct, settings.SCORING_WEIGHTS,
        )
        stars = scoring.calculate_stars(precision, settings.STAR_THRESHOLDS)

        character_errors = {}
        for manager in managers:
            for char, count in manager.character_errors.items():
                character_errors[char] = character_errors.get(char, 0) + count
        self.key_stats.register_errors(character_errors)

        min_precision = getattr(level_module, "MIN_PRECISION_PERCENT", None)
        passed = min_precision is None or precision >= min_precision
        is_training = session.get("is_training", False)
        is_exam = session.get("is_exam", False)
        is_numpad_mode = session.get("is_numpad_mode", False)
        is_versus = session.get("is_versus", False)
        is_time_attack = session.get("is_time_attack", False)
        is_survival = session.get("is_survival", False)

        # Supervivencia siempre termina en GAME OVER (por diseno, seccion
        # 16): nunca es una "victoria", asi que suena como un fallo.
        self.sound.play("level_failed" if (not passed or is_survival) else "level_complete")

        if is_versus:
            self._finish_versus_round(session, wpm, precision, error_count, max_combo, score)
            return

        self.last_result = {
            "level_number": session["level_number"],
            "wpm": round(wpm, 1),
            "precision": round(precision, 1),
            "errors": error_count,
            "max_combo": max_combo,
            "score": round(score),
            "stars": stars,
            "passed": passed,
            "min_precision": min_precision,
            "correct_chars": correct_count,
            "typed_chars": typed_count,
            "is_exam": is_exam,
            "is_survival": is_survival,
            "survival_time_seconds": elapsed,
        }

        if passed and not is_training and not is_numpad_mode:
            # El leaderboard cuenta niveles reales y el Modo Examen (una
            # medicion seria), pero no el Modo Errores ni el Modo Numpad:
            # son drills cortos, no una medicion real de velocidad.
            leaderboard_updated = self.leaderboard.register_run(
                self.player.data["name"], wpm, precision, session["level_number"], score,
            )
            self.last_result["leaderboard_updated"] = leaderboard_updated

        if (
            passed and not is_training and not is_exam and not is_numpad_mode
            and not is_time_attack and not is_survival
        ):
            previous_record = self.progression.data["level_records"].get(str(session["level_number"]), {})
            is_new_record = score > previous_record.get("best_score", 0)

            self.progression.register_result(
                session["level_number"], score, wpm, precision, elapsed, max_combo,
            )
            self.statistics.register_level_result(self.last_result, elapsed)

            xp_earned = scoring.calculate_xp(stars == 3, is_new_record, max_combo)
            self.player.add_xp(xp_earned)
            self.last_result["xp_earned"] = xp_earned
            self.last_result["total_xp"] = self.player.data["total_xp"]

            newly_unlocked = check_level_result_achievements(
                self.achievements, self.last_result, self.progression, self.statistics,
            )
            self.last_result["newly_unlocked_achievements"] = newly_unlocked
            if newly_unlocked:
                self.sound.play("achievement_unlocked")

        self._change_scene(SCENE_RESULTS)

    def _handle_results_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key in (pygame.K_RETURN, pygame.K_SPACE):
            self._change_scene(SCENE_LEVEL_SELECT)
        elif event.key == pygame.K_ESCAPE:
            self._change_scene(SCENE_MENU)

    def _handle_statistics_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._change_scene(SCENE_MENU)

    def _handle_achievements_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._change_scene(SCENE_MENU)

    def _handle_message_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._change_scene(SCENE_MENU)

    def _handle_settings_event(self, event):
        if event.type != pygame.KEYDOWN:
            return
        if event.key == pygame.K_m:
            self.game_settings.toggle_sound()
            self.sound.set_master_enabled(self.game_settings.data["sound_enabled"])
        elif event.key == pygame.K_LEFT:
            self.game_settings.set_volume(self.game_settings.data["volume"] - 0.1)
            self.sound.set_volume(self.game_settings.data["volume"])
        elif event.key == pygame.K_RIGHT:
            self.game_settings.set_volume(self.game_settings.data["volume"] + 0.1)
            self.sound.set_volume(self.game_settings.data["volume"])
        elif event.key == pygame.K_n:
            self.name_entry_buffer = ""
            self._change_scene(SCENE_NAME_ENTRY)
        elif event.key == pygame.K_ESCAPE:
            self._change_scene(SCENE_MENU)

    def _handle_leaderboard_event(self, event):
        if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            self._change_scene(SCENE_MENU)

    def _handle_name_entry_event(self, event):
        if event.type == pygame.TEXTINPUT:
            if len(self.name_entry_buffer) < MAX_NAME_LENGTH:
                self.name_entry_buffer += event.text
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                self.name_entry_buffer = self.name_entry_buffer[:-1]
            elif event.key == pygame.K_RETURN:
                if self.name_entry_buffer.strip():
                    self.player.set_name(self.name_entry_buffer)
                self._change_scene(SCENE_SETTINGS)
            elif event.key == pygame.K_ESCAPE:
                self._change_scene(SCENE_SETTINGS)

    def _render(self):
        self.screen.fill(settings.COLORS["background"])
        if self.scene == SCENE_MENU:
            menu.draw(self.screen, self.font_title, self.font_hud)
        elif self.scene == SCENE_LEVEL_SELECT:
            level_select.draw(
                self.screen, self.font_title, self.font_hud,
                registry.get_all_numbers(), self.level_select_index, self.progression,
            )
        elif self.scene == SCENE_LEVEL:
            game_screen.draw(
                self.screen, self.font_text, self.font_hud,
                self.level_session, self.level_session["level_module"],
            )
        elif self.scene == SCENE_RESULTS:
            if self.last_result and self.last_result.get("is_exam"):
                exam_result_screen.draw(self.screen, self.font_title, self.font_hud, self.last_result, self.player)
            elif self.last_result and self.last_result.get("is_survival"):
                survival_result_screen.draw(self.screen, self.font_title, self.font_hud, self.last_result)
            else:
                results_screen.draw(self.screen, self.font_title, self.font_hud, self.last_result)
        elif self.scene == SCENE_STATISTICS:
            statistics_screen.draw(
                self.screen, self.font_title, self.font_hud, self.statistics, self.player, self.key_stats,
            )
        elif self.scene == SCENE_ACHIEVEMENTS:
            achievements_screen.draw(self.screen, self.font_title, self.font_hud, self.achievements)
        elif self.scene == SCENE_MESSAGE:
            message_screen.draw(
                self.screen, self.font_title, self.font_hud, self.message_title, self.message_body,
            )
        elif self.scene == SCENE_SETTINGS:
            settings_screen.draw(self.screen, self.font_title, self.font_hud, self.game_settings, self.player)
        elif self.scene == SCENE_LEADERBOARD:
            leaderboard_screen.draw(self.screen, self.font_title, self.font_hud, self.leaderboard)
        elif self.scene == SCENE_NAME_ENTRY:
            name_entry_screen.draw(
                self.screen, self.font_title, self.font_hud, "TU NOMBRE", self.name_entry_buffer,
                f"Nombre actual: {self.player.data['name']}",
            )
        elif self.scene == SCENE_VERSUS_NAME:
            player_number = 1 if self.versus_state["stage"] == "p1_name" else 2
            name_entry_screen.draw(
                self.screen, self.font_title, self.font_hud, f"JUGADOR {player_number}", self.name_entry_buffer,
                "Escribe tu nombre para el duelo",
            )
        elif self.scene == SCENE_VERSUS_RESULT:
            versus_result_screen.draw(self.screen, self.font_title, self.font_hud, self.versus_state)
        elif self.scene == SCENE_FREE_PRACTICE_SELECT:
            free_practice_select_screen.draw(self.screen, self.font_title, self.font_hud, self.free_practice_index)
        elif self.scene == SCENE_TIME_ATTACK_SELECT:
            time_attack_select_screen.draw(self.screen, self.font_title, self.font_hud, self.time_attack_index)

        self._draw_effects()
        pygame.display.flip()

    def _draw_effects(self):
        size = self.screen.get_size()

        for effect in self.effects.get("flash_error"):
            alpha = int(ERROR_FLASH_ALPHA_MAX * (1 - self.effects.progress(effect)))
            if alpha > 0:
                overlay = pygame.Surface(size, pygame.SRCALPHA)
                overlay.fill((*settings.COLORS["text_error"], alpha))
                self.screen.blit(overlay, (0, 0))

        for effect in self.effects.get("combo_popup"):
            progress = self.effects.progress(effect)
            alpha = max(0, int(255 * (1 - progress)))
            y_offset = int(-30 * progress)
            text = f"COMBO x{effect['data']['combo']}!"
            surf = self.font_hud.render(text, True, settings.COLORS["accent"])
            surf.set_alpha(alpha)
            rect = surf.get_rect(center=(size[0] // 2, 220 + y_offset))
            self.screen.blit(surf, rect)

        for effect in self.effects.get("fade"):
            alpha = int(FADE_ALPHA_MAX * (1 - self.effects.progress(effect)))
            if alpha > 0:
                overlay = pygame.Surface(size, pygame.SRCALPHA)
                overlay.fill((0, 0, 0, alpha))
                self.screen.blit(overlay, (0, 0))
