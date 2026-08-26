import pytest

from systems.free_practice import CATEGORIES, CATEGORY_LABELS, FreePracticeLevel, get_exercises


def test_every_category_has_a_label():
    for category in CATEGORIES:
        assert category in CATEGORY_LABELS


def test_get_exercises_returns_content_for_each_non_numpad_category():
    for category in CATEGORIES:
        if category == "numpad":
            continue
        exercises = get_exercises(category)
        assert exercises
        assert all(isinstance(e, str) and e for e in exercises)


def test_get_exercises_rejects_unknown_category():
    with pytest.raises(ValueError):
        get_exercises("no_existe")


def test_free_practice_level_has_no_number():
    assert FreePracticeLevel.LEVEL_NUMBER is None
    assert FreePracticeLevel.TIME_LIMIT_SECONDS > 0
