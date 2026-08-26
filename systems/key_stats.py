from systems.save_manager import load_json, save_json

DEFAULT_KEY_STATS_PATH = "data/key_stats.json"


class KeyStats:
    """Cuenta cuantas veces se ha fallado cada caracter, a traves de todas
    las sesiones (seccion 14 y 15 del documento maestro)."""

    def __init__(self, path=None):
        self.path = path or DEFAULT_KEY_STATS_PATH
        self.data = load_json(self.path, default={"error_counts": {}})

    def register_errors(self, character_errors):
        counts = self.data["error_counts"]
        for char, amount in character_errors.items():
            if char in (" ", "\n"):
                continue
            counts[char] = counts.get(char, 0) + amount
        self.save()

    def most_failed(self, predicate=None, limit=5):
        items = self.data["error_counts"].items()
        if predicate is not None:
            items = [(char, count) for char, count in items if predicate(char)]
        return sorted(items, key=lambda pair: pair[1], reverse=True)[:limit]

    def most_failed_letters(self, limit=5):
        return self.most_failed(lambda char: char.isalpha(), limit)

    def most_failed_numbers(self, limit=5):
        return self.most_failed(lambda char: char.isdigit(), limit)

    def most_failed_symbols(self, limit=5):
        return self.most_failed(lambda char: not char.isalnum(), limit)

    def save(self):
        save_json(self.path, self.data)
