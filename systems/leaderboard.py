from core.paths import get_user_data_path
from systems.save_manager import load_json, save_json


class Leaderboard:
    """Tabla local de mejores WPM por nombre (seccion 27 del documento
    maestro). Una entrada por nombre: su mejor corrida, no el historial
    completo."""

    def __init__(self, path=None):
        self.path = path or get_user_data_path("leaderboard.json")
        self.data = load_json(self.path, default={"entries": {}})

    def register_run(self, name, wpm, precision, level_number, score):
        name = (name or "").strip() or "Jugador"
        existing = self.data["entries"].get(name)

        if existing is not None and wpm <= existing["wpm"]:
            return False

        self.data["entries"][name] = {
            "wpm": wpm,
            "precision": precision,
            "level_number": level_number,
            "score": score,
        }
        self.save()
        return True

    def get_top(self, limit=10):
        ranked = sorted(self.data["entries"].items(), key=lambda item: item[1]["wpm"], reverse=True)
        return ranked[:limit]

    def save(self):
        save_json(self.path, self.data)
