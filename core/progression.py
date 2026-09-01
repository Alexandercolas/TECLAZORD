from config.settings import LEVEL_UNLOCK_SCORE
from core.paths import get_user_data_path
from systems.save_manager import load_json, save_json


class Progression:
    def __init__(self, path=None):
        self.path = path or get_user_data_path("progress.json")
        self.data = load_json(self.path, default={"unlocked_levels": [1], "level_records": {}})

    def is_unlocked(self, level_number):
        return level_number in self.data["unlocked_levels"]

    def register_result(self, level_number, score, wpm, precision, elapsed_seconds, max_combo):
        record = self.data["level_records"].setdefault(str(level_number), {})

        if "best_score" not in record or score > record["best_score"]:
            record["best_score"] = score
            record["best_wpm"] = wpm
            record["best_precision"] = precision

        if "best_time_seconds" not in record or elapsed_seconds < record["best_time_seconds"]:
            record["best_time_seconds"] = elapsed_seconds

        if max_combo > record.get("best_combo", 0):
            record["best_combo"] = max_combo

        next_level = level_number + 1
        if score >= LEVEL_UNLOCK_SCORE and next_level not in self.data["unlocked_levels"]:
            self.data["unlocked_levels"].append(next_level)

        self.save()

    def save(self):
        save_json(self.path, self.data)
