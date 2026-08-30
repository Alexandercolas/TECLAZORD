from core.paths import get_user_data_path
from systems.save_manager import load_json, save_json


class GameSettings:
    def __init__(self, path=None):
        self.path = path or get_user_data_path("settings.json")
        self.data = load_json(self.path, default={"sound_enabled": True, "volume": 0.5})

    def set_volume(self, volume):
        self.data["volume"] = round(max(0.0, min(1.0, volume)), 2)
        self.save()

    def toggle_sound(self):
        self.data["sound_enabled"] = not self.data["sound_enabled"]
        self.save()

    def save(self):
        save_json(self.path, self.data)
