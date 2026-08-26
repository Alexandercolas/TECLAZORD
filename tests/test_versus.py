from systems.versus import VersusLevel, determine_winner, get_exercises


def test_get_exercises_returns_single_text():
    exercises = get_exercises()
    assert len(exercises) == 1
    assert len(exercises[0]) > 50


def test_versus_level_has_no_number():
    assert VersusLevel.LEVEL_NUMBER is None
    assert VersusLevel.TIME_LIMIT_SECONDS > 0


def test_higher_wpm_wins():
    p1 = {"wpm": 60.0, "precision": 90.0}
    p2 = {"wpm": 50.0, "precision": 95.0}
    assert determine_winner("Alex", p1, "Carlos", p2) == "GANA Alex!"


def test_lower_wpm_loses_even_with_better_precision():
    p1 = {"wpm": 40.0, "precision": 99.0}
    p2 = {"wpm": 55.0, "precision": 80.0}
    assert determine_winner("Alex", p1, "Carlos", p2) == "GANA Carlos!"


def test_tied_wpm_breaks_by_precision():
    p1 = {"wpm": 50.0, "precision": 92.0}
    p2 = {"wpm": 50.0, "precision": 88.0}
    assert "Alex" in determine_winner("Alex", p1, "Carlos", p2)
    assert "precision" in determine_winner("Alex", p1, "Carlos", p2)


def test_full_tie_is_a_draw():
    p1 = {"wpm": 50.0, "precision": 90.0}
    p2 = {"wpm": 50.0, "precision": 90.0}
    assert determine_winner("Alex", p1, "Carlos", p2) == "EMPATE!"
