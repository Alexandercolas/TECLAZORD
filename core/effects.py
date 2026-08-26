import time


class EffectManager:
    """Efectos visuales de corta duracion (fundidos, destellos, popups de
    combo). El reloj es inyectable para poder probar sin esperar tiempo real."""

    def __init__(self, clock=time.perf_counter):
        self._clock = clock
        self.active = []

    def trigger(self, effect_type, duration, data=None):
        self.active.append({
            "type": effect_type,
            "start": self._clock(),
            "duration": duration,
            "data": data or {},
        })

    def update(self):
        now = self._clock()
        self.active = [e for e in self.active if now - e["start"] < e["duration"]]

    def progress(self, effect):
        return min(1.0, (self._clock() - effect["start"]) / effect["duration"])

    def get(self, effect_type):
        return [e for e in self.active if e["type"] == effect_type]
