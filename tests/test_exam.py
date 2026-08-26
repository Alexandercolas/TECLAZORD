from systems.exam import classify_wpm, get_exercises


def test_get_exercises_returns_single_long_text():
    exercises = get_exercises()
    assert len(exercises) == 1
    assert len(exercises[0]) > 100


def test_classify_wpm_thresholds():
    assert classify_wpm(5) == "PRINCIPIANTE"
    assert classify_wpm(20) == "BASICO"
    assert classify_wpm(35) == "INTERMEDIO"
    assert classify_wpm(50) == "AVANZADO"
    assert classify_wpm(70) == "EXPERTO"
    assert classify_wpm(120) == "EXPERTO"
