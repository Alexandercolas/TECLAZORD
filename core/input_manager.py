class InputManager:
    """Compara lo que el jugador escribe contra el texto objetivo, caracter a caracter.

    Usa texto Unicode (evento TEXTINPUT de Pygame) en vez de codigos de tecla,
    porque KEYDOWN no distingue mayusculas por Shift ni entrega bien la Ñ y
    los acentos que el juego necesita en espanol.
    """

    def __init__(self, target_text):
        self.target_text = target_text
        self.typed = ""
        self.correct_count = 0
        self.error_count = 0
        self.combo = 0
        self.max_combo = 0
        # Cuantas veces se fallo esperando cada caracter especifico, para
        # el entrenamiento inteligente (seccion 15): {"7": 3, "ñ": 1, ...}.
        self.character_errors = {}

    def handle_text_input(self, char):
        """Devuelve True si el caracter fue correcto, False si fue un error,
        o None si el ejercicio ya estaba completo (se ignora)."""
        index = len(self.typed)
        if index >= len(self.target_text):
            return None

        expected = self.target_text[index]
        self.typed += char

        if char == expected:
            self.correct_count += 1
            self.combo += 1
            self.max_combo = max(self.max_combo, self.combo)
            return True
        else:
            self.error_count += 1
            self.combo = 0
            self.character_errors[expected] = self.character_errors.get(expected, 0) + 1
            return False

    def handle_backspace(self):
        self.typed = self.typed[:-1]

    def is_complete(self):
        return len(self.typed) >= len(self.target_text)
