import pygame

from config import settings


class SoundManager:
    """Envuelve pygame.mixer. Si no hay dispositivo de audio disponible,
    se degrada a silencio en vez de romper el juego."""

    def __init__(self):
        self.device_available = True
        self.master_enabled = True
        self.sounds = {}

        try:
            pygame.mixer.init()
        except pygame.error:
            self.device_available = False
            return

        for name, path in settings.SOUND_FILES.items():
            try:
                sound = pygame.mixer.Sound(path)
                sound.set_volume(settings.SOUND_VOLUME)
                self.sounds[name] = sound
            except (pygame.error, FileNotFoundError):
                pass

    def set_master_enabled(self, enabled):
        self.master_enabled = enabled

    def set_volume(self, volume):
        for sound in self.sounds.values():
            sound.set_volume(volume)

    def play(self, name):
        if not self.device_available or not self.master_enabled:
            return
        sound = self.sounds.get(name)
        if sound is not None:
            sound.play()
