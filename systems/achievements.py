from core.paths import get_user_data_path
from systems.save_manager import load_json, save_json

ACHIEVEMENT_DEFINITIONS = [
    {"id": "primer_nivel", "name": "Primer Tecleo", "description": "Completa tu primer nivel."},
    {"id": "tres_estrellas", "name": "Perfeccionista", "description": "Consigue 3 estrellas en un nivel."},
    {"id": "precision_perfecta", "name": "Cero Errores", "description": "Completa un nivel con 100% de precision."},
    {"id": "combo_50", "name": "Racha Imparable", "description": "Alcanza un combo de x50 o mas."},
    {"id": "velocista", "name": "Dedos Rapidos", "description": "Alcanza 60 WPM o mas en un nivel."},
    {"id": "maestro_teclado", "name": "El Duro del Teclado", "description": "Completa los 10 niveles principales."},
]


class Achievements:
    def __init__(self, path=None):
        self.path = path or get_user_data_path("achievements.json")
        self.data = load_json(self.path, default={"unlocked": []})

    def is_unlocked(self, achievement_id):
        return achievement_id in self.data["unlocked"]

    def unlock(self, achievement_id):
        if achievement_id in self.data["unlocked"]:
            return False
        self.data["unlocked"].append(achievement_id)
        self.save()
        return True

    def save(self):
        save_json(self.path, self.data)


def check_level_result_achievements(achievements, result, progression, statistics):
    """Revisa el resultado de un nivel superado y desbloquea logros nuevos.

    Devuelve la lista de ids recien desbloqueados (vacia si ninguno).
    """
    newly_unlocked = []

    def try_unlock(achievement_id):
        if achievements.unlock(achievement_id):
            newly_unlocked.append(achievement_id)

    if statistics.data["levels_completed"] >= 1:
        try_unlock("primer_nivel")
    if result["stars"] == 3:
        try_unlock("tres_estrellas")
    if result["precision"] >= 100:
        try_unlock("precision_perfecta")
    if result["max_combo"] >= 50:
        try_unlock("combo_50")
    if result["wpm"] >= 60:
        try_unlock("velocista")
    if len(progression.data["level_records"]) >= 10:
        try_unlock("maestro_teclado")

    return newly_unlocked
