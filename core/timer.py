import time


class GameTimer:
    """Cuenta atras de un ejercicio. El reloj es inyectable para poder probarlo sin esperar tiempo real."""

    def __init__(self, duration_seconds, clock=time.perf_counter):
        self.duration = duration_seconds
        self._clock = clock
        self._start_time = None

    def start(self):
        self._start_time = self._clock()

    def elapsed(self):
        if self._start_time is None:
            return 0.0
        return self._clock() - self._start_time

    def remaining(self):
        return max(0.0, self.duration - self.elapsed())

    def is_expired(self):
        return self.elapsed() >= self.duration
