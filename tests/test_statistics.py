from systems.statistics import Statistics


def _fake_result(**overrides):
    result = {
        "wpm": 40.0,
        "precision": 90.0,
        "errors": 2,
        "max_combo": 15,
        "stars": 2,
        "correct_chars": 90,
        "typed_chars": 100,
    }
    result.update(overrides)
    return result


def test_starts_empty(tmp_path):
    stats = Statistics(path=str(tmp_path / "statistics.json"))
    assert stats.data["levels_completed"] == 0
    assert stats.average_wpm == 0.0
    assert stats.average_precision == 100.0


def test_accumulates_across_levels(tmp_path):
    stats = Statistics(path=str(tmp_path / "statistics.json"))

    stats.register_level_result(_fake_result(wpm=40.0, precision=90.0), elapsed_seconds=60)
    stats.register_level_result(_fake_result(wpm=60.0, precision=100.0, max_combo=30), elapsed_seconds=45)

    assert stats.data["levels_completed"] == 2
    assert stats.data["stars_earned"] == 4
    assert stats.data["total_errors"] == 4
    assert stats.data["best_wpm"] == 60.0
    assert stats.data["best_combo"] == 30
    assert stats.average_wpm == 50.0
    assert stats.average_precision == 95.0
    assert stats.data["total_time_played_seconds"] == 105


def test_persists_and_reloads(tmp_path):
    path = str(tmp_path / "statistics.json")
    stats = Statistics(path=path)
    stats.register_level_result(_fake_result(), elapsed_seconds=30)

    reloaded = Statistics(path=path)
    assert reloaded.data["levels_completed"] == 1
