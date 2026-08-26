from systems.survival import SURVIVAL_GRACE_CHARACTERS, SURVIVAL_MIN_PRECISION_PERCENT, SurvivalLevel, get_exercises


def test_survival_level_has_no_number_and_a_safety_ceiling():
    assert SurvivalLevel.LEVEL_NUMBER is None
    assert SurvivalLevel.TIME_LIMIT_SECONDS > 60  # mucho mas largo que cualquier ronda real


def test_get_exercises_returns_content():
    assert len(get_exercises()) > 20


def test_grace_period_and_threshold_are_sane():
    assert SURVIVAL_GRACE_CHARACTERS > 0
    assert 0 < SURVIVAL_MIN_PRECISION_PERCENT < 100
