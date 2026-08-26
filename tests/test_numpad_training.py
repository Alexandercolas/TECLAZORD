from systems.numpad_training import NumpadLevel, get_exercises


def test_get_exercises_are_digit_and_period_only():
    for exercise in get_exercises():
        assert all(ch.isdigit() or ch == "." for ch in exercise)


def test_numpad_level_has_no_number_and_is_time_limited():
    assert NumpadLevel.LEVEL_NUMBER is None
    assert NumpadLevel.TIME_LIMIT_SECONDS > 0
