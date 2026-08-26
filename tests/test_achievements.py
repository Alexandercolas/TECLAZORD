from core.progression import Progression
from systems.achievements import Achievements, check_level_result_achievements
from systems.statistics import Statistics


def _make(tmp_path):
    achievements = Achievements(path=str(tmp_path / "achievements.json"))
    progression = Progression(path=str(tmp_path / "progress.json"))
    statistics = Statistics(path=str(tmp_path / "statistics.json"))
    return achievements, progression, statistics


def _result(**overrides):
    result = {"stars": 1, "precision": 80.0, "max_combo": 5, "wpm": 30.0}
    result.update(overrides)
    return result


def test_first_level_unlocks_primer_nivel(tmp_path):
    achievements, progression, statistics = _make(tmp_path)
    statistics.data["levels_completed"] = 1

    unlocked = check_level_result_achievements(achievements, _result(), progression, statistics)

    assert "primer_nivel" in unlocked
    assert achievements.is_unlocked("primer_nivel")


def test_does_not_unlock_twice(tmp_path):
    achievements, progression, statistics = _make(tmp_path)
    statistics.data["levels_completed"] = 1

    check_level_result_achievements(achievements, _result(), progression, statistics)
    unlocked_again = check_level_result_achievements(achievements, _result(), progression, statistics)

    assert unlocked_again == []


def test_three_stars_and_perfect_precision_and_combo_and_speed(tmp_path):
    achievements, progression, statistics = _make(tmp_path)
    statistics.data["levels_completed"] = 1

    result = _result(stars=3, precision=100.0, max_combo=60, wpm=75.0)
    unlocked = check_level_result_achievements(achievements, result, progression, statistics)

    assert set(unlocked) == {
        "primer_nivel", "tres_estrellas", "precision_perfecta", "combo_50", "velocista",
    }


def test_maestro_teclado_requires_ten_distinct_levels(tmp_path):
    achievements, progression, statistics = _make(tmp_path)
    statistics.data["levels_completed"] = 1
    for level_number in range(1, 10):
        progression.data["level_records"][str(level_number)] = {"best_score": 500}

    unlocked = check_level_result_achievements(achievements, _result(), progression, statistics)
    assert "maestro_teclado" not in unlocked

    progression.data["level_records"]["10"] = {"best_score": 500}
    unlocked = check_level_result_achievements(achievements, _result(), progression, statistics)
    assert "maestro_teclado" in unlocked
