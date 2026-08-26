from core.progression import Progression


def test_level_one_starts_unlocked(tmp_path):
    progression = Progression(path=str(tmp_path / "progress.json"))
    assert progression.is_unlocked(1)
    assert not progression.is_unlocked(2)


def test_high_score_unlocks_next_level(tmp_path):
    path = str(tmp_path / "progress.json")
    progression = Progression(path=path)

    progression.register_result(1, score=600, wpm=40, precision=90, elapsed_seconds=55, max_combo=30)
    assert progression.is_unlocked(2)

    reloaded = Progression(path=path)
    assert reloaded.is_unlocked(2)
    record = reloaded.data["level_records"]["1"]
    assert record["best_score"] == 600
    assert record["best_time_seconds"] == 55
    assert record["best_combo"] == 30


def test_low_score_does_not_unlock_next_level(tmp_path):
    progression = Progression(path=str(tmp_path / "progress.json"))
    progression.register_result(1, score=10, wpm=5, precision=50, elapsed_seconds=80, max_combo=3)
    assert not progression.is_unlocked(2)


def test_best_time_and_combo_track_independently_from_best_score(tmp_path):
    progression = Progression(path=str(tmp_path / "progress.json"))

    progression.register_result(1, score=600, wpm=40, precision=90, elapsed_seconds=60, max_combo=10)
    # Puntuacion mas baja, pero mejor tiempo y mejor combo: ambos deben
    # actualizarse aunque no se supere el mejor puntaje.
    progression.register_result(1, score=500, wpm=35, precision=85, elapsed_seconds=40, max_combo=25)

    record = progression.data["level_records"]["1"]
    assert record["best_score"] == 600
    assert record["best_time_seconds"] == 40
    assert record["best_combo"] == 25
