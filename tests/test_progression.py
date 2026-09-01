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


def test_first_completion_with_zero_score_still_records_best_score(tmp_path):
    # Bug real: la formula de puntuacion puede dar exactamente 0 (muchos
    # errores). La condicion original era "score > best_score" (0 > 0 es
    # False), asi que best_score nunca se guardaba aunque best_time_seconds
    # si (se guarda incondicionalmente) - el registro quedaba con datos a
    # medias y ui/level_select.py explotaba con KeyError al leer
    # record['best_score']. Debe quedar guardado siempre, aunque sea 0.
    progression = Progression(path=str(tmp_path / "progress.json"))
    progression.register_result(1, score=0, wpm=2, precision=10, elapsed_seconds=45, max_combo=0)

    record = progression.data["level_records"]["1"]
    assert "best_score" in record
    assert record["best_score"] == 0
    assert record["best_wpm"] == 2
    assert record["best_precision"] == 10


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
