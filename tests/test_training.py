from systems.key_stats import KeyStats
from systems.training import generate_personalized_exercises


def test_no_exercises_when_not_enough_data(tmp_path):
    stats = KeyStats(path=str(tmp_path / "key_stats.json"))
    stats.register_errors({"7": 2})  # por debajo del minimo (3)
    assert generate_personalized_exercises(stats) == []


def test_no_exercises_when_no_data(tmp_path):
    stats = KeyStats(path=str(tmp_path / "key_stats.json"))
    assert generate_personalized_exercises(stats) == []


def test_generates_drills_from_top_failed_characters(tmp_path):
    stats = KeyStats(path=str(tmp_path / "key_stats.json"))
    stats.register_errors({"7": 18, "p": 14, "ñ": 11, "@": 9})

    exercises = generate_personalized_exercises(stats)

    assert exercises[0] == "7" * 6
    assert exercises[1] == "7p" * 3
    assert exercises[2] == "7pñ" * 2
    assert exercises[3] == "usuario_7"


def test_handles_a_single_problem_character(tmp_path):
    stats = KeyStats(path=str(tmp_path / "key_stats.json"))
    stats.register_errors({"7": 5})

    exercises = generate_personalized_exercises(stats)

    assert exercises == ["777777", "usuario_7"]
