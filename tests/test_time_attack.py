from systems.time_attack import DURATIONS, TimeAttackLevel, get_exercises


def test_durations_are_positive_and_increasing():
    assert DURATIONS == sorted(DURATIONS)
    assert all(d > 0 for d in DURATIONS)


def test_get_exercises_mixes_multiple_levels_and_is_shuffled():
    exercises = get_exercises()
    assert len(exercises) > 20  # suma de niveles 1-8
    assert all(isinstance(e, str) and e for e in exercises)


def test_time_attack_level_has_no_number():
    assert TimeAttackLevel.LEVEL_NUMBER is None
