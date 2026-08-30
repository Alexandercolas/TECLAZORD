from core.paths import get_user_data_path
from systems.save_manager import load_json, save_json


def _default_stats():
    return {
        "levels_completed": 0,
        "stars_earned": 0,
        "total_characters_typed": 0,
        "total_correct_characters": 0,
        "total_errors": 0,
        "total_time_played_seconds": 0.0,
        "best_wpm": 0.0,
        "best_combo": 0,
        "sum_wpm": 0.0,
        "sum_precision": 0.0,
    }


class Statistics:
    def __init__(self, path=None):
        self.path = path or get_user_data_path("statistics.json")
        self.data = load_json(self.path, default=_default_stats())

    def register_level_result(self, result, elapsed_seconds):
        self.data["levels_completed"] += 1
        self.data["stars_earned"] += result["stars"]
        self.data["total_correct_characters"] += result["correct_chars"]
        self.data["total_characters_typed"] += result["typed_chars"]
        self.data["total_errors"] += result["errors"]
        self.data["total_time_played_seconds"] += elapsed_seconds
        self.data["best_wpm"] = max(self.data["best_wpm"], result["wpm"])
        self.data["best_combo"] = max(self.data["best_combo"], result["max_combo"])
        self.data["sum_wpm"] += result["wpm"]
        self.data["sum_precision"] += result["precision"]
        self.save()

    @property
    def average_wpm(self):
        if self.data["levels_completed"] == 0:
            return 0.0
        return self.data["sum_wpm"] / self.data["levels_completed"]

    @property
    def average_precision(self):
        if self.data["levels_completed"] == 0:
            return 100.0
        return self.data["sum_precision"] / self.data["levels_completed"]

    @property
    def total_words_typed(self):
        return self.data["total_correct_characters"] / 5

    def save(self):
        save_json(self.path, self.data)
