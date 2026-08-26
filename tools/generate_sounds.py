"""Genera los efectos de sonido de TECLAZO RD como archivos .wav.

No se ejecuta durante el juego: es una herramienta de una sola vez para
producir assets/sounds/*.wav por sintesis (sin depender de bancos de
sonido externos, para mantener el proyecto 100% local). Vuelve a
ejecutarse solo si se quiere regenerar/ajustar los sonidos:

    python tools/generate_sounds.py
"""
import math
import os
import random
import struct
import wave

SAMPLE_RATE = 44100
OUTPUT_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "assets", "sounds")


def _envelope(i, n, duration, attack_seconds=0.004, decay_rate=3.0):
    t = i / SAMPLE_RATE
    attack = min(1.0, i / (SAMPLE_RATE * attack_seconds)) if attack_seconds > 0 else 1.0
    decay = math.exp(-decay_rate * t / duration)
    return attack * decay


def _tone(freq, duration, volume=0.5, wave_shape="square", decay_rate=3.0, attack_seconds=0.004):
    n = int(SAMPLE_RATE * duration)
    samples = []
    for i in range(n):
        t = i / SAMPLE_RATE
        phase = freq * t
        if wave_shape == "sine":
            value = math.sin(2 * math.pi * phase)
        elif wave_shape == "square":
            value = 1.0 if math.sin(2 * math.pi * phase) >= 0 else -1.0
        elif wave_shape == "saw":
            value = 2 * (phase - math.floor(0.5 + phase))
        else:
            raise ValueError(f"forma de onda desconocida: {wave_shape}")
        samples.append(value * volume * _envelope(i, n, duration, attack_seconds, decay_rate))
    return samples


def _noise(duration, volume=0.5, decay_rate=4.0):
    n = int(SAMPLE_RATE * duration)
    return [
        random.uniform(-1, 1) * volume * _envelope(i, n, duration, attack_seconds=0.001, decay_rate=decay_rate)
        for i in range(n)
    ]


def _mix(*sample_lists):
    length = max(len(s) for s in sample_lists)
    result = [0.0] * length
    for samples in sample_lists:
        for i, value in enumerate(samples):
            result[i] += value
    peak = max(1.0, max(abs(v) for v in result))
    return [v / peak for v in result]


def _concat(*sample_lists):
    result = []
    for samples in sample_lists:
        result.extend(samples)
    return result


def _write_wav(filename, samples):
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    path = os.path.join(OUTPUT_DIR, filename)
    with wave.open(path, "w") as wav_file:
        wav_file.setnchannels(1)
        wav_file.setsampwidth(2)
        wav_file.setframerate(SAMPLE_RATE)
        frames = b"".join(
            struct.pack("<h", max(-32767, min(32767, int(s * 32767)))) for s in samples
        )
        wav_file.writeframes(frames)
    print(f"  {filename}  ({len(samples) / SAMPLE_RATE:.2f}s)")


def make_type_correct():
    # Clic metalico, seco y corto: como el cerrojo de un rifle.
    tone = _tone(1500, 0.045, volume=0.5, wave_shape="square", decay_rate=14, attack_seconds=0.001)
    noise = _noise(0.03, volume=0.35, decay_rate=18)
    return _mix(tone, noise)


def make_type_error():
    # Zumbido grave y disonante: como un atasco / disparo fallido.
    tone1 = _tone(170, 0.15, volume=0.5, wave_shape="square", decay_rate=6)
    tone2 = _tone(158, 0.15, volume=0.4, wave_shape="square", decay_rate=6)
    noise = _noise(0.08, volume=0.3, decay_rate=10)
    return _mix(tone1, tone2, noise)


def make_menu_move():
    return _tone(700, 0.03, volume=0.3, wave_shape="square", decay_rate=20, attack_seconds=0.001)


def make_combo_milestone():
    n1 = _tone(600, 0.05, volume=0.4, wave_shape="square", decay_rate=8)
    n2 = _tone(950, 0.06, volume=0.5, wave_shape="square", decay_rate=8)
    return _concat(n1, n2)


def make_level_complete():
    # Arpegio marcial ascendente + golpe grave final (tambor de guerra).
    notes = [330, 415, 494, 660]
    arpeggio = _concat(*[_tone(f, 0.09, volume=0.5, wave_shape="square", decay_rate=6) for f in notes])
    boom = _mix(
        _noise(0.25, volume=0.55, decay_rate=4),
        _tone(90, 0.25, volume=0.5, wave_shape="sine", decay_rate=5),
    )
    return _concat(arpeggio, boom)


def make_level_failed():
    # Motivo descendente + golpe sordo: "mision fallida".
    notes = [392, 349, 293, 220]
    descend = _concat(*[_tone(f, 0.13, volume=0.5, wave_shape="saw", decay_rate=5) for f in notes])
    thud = _mix(
        _noise(0.2, volume=0.5, decay_rate=5),
        _tone(70, 0.2, volume=0.5, wave_shape="sine", decay_rate=5),
    )
    return _concat(descend, thud)


def make_achievement_unlocked():
    notes = [523, 659, 784, 1047]
    return _concat(*[_tone(f, 0.07, volume=0.55, wave_shape="square", decay_rate=7) for f in notes])


def main():
    print("Generando efectos de sonido en assets/sounds/ ...")
    _write_wav("type_correct.wav", make_type_correct())
    _write_wav("type_error.wav", make_type_error())
    _write_wav("menu_move.wav", make_menu_move())
    _write_wav("combo_milestone.wav", make_combo_milestone())
    _write_wav("level_complete.wav", make_level_complete())
    _write_wav("level_failed.wav", make_level_failed())
    _write_wav("achievement_unlocked.wav", make_achievement_unlocked())
    print("Listo.")


if __name__ == "__main__":
    main()
