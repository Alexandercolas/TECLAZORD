from systems.save_manager import load_json, save_json

DEFAULT_PLAYER_PATH = "data/player.json"


class Player:
    def __init__(self, path=None):
        self.path = path or DEFAULT_PLAYER_PATH
        self.data = load_json(self.path, default={"total_xp": 0, "name": "Jugador"})
        self.data.setdefault("name", "Jugador")

    def add_xp(self, amount):
        self.data["total_xp"] += amount
        self.save()

    def set_name(self, name):
        self.data["name"] = name.strip() or "Jugador"
        self.save()

    def save(self):
        save_json(self.path, self.data)
