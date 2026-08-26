from core import scoring


def test_wpm_zero_when_no_elapsed_time():
    assert scoring.calculate_wpm(50, 0) == 0.0


def test_wpm_basic_conversion():
    # 50 caracteres correctos en 60 segundos = 10 palabras/minuto.
    assert scoring.calculate_wpm(50, 60) == 10.0


def test_precision_with_no_input_defaults_to_full():
    assert scoring.calculate_precision(0, 0) == 100.0


def test_precision_partial():
    assert scoring.calculate_precision(8, 10) == 80.0


def test_calculate_stars_thresholds():
    thresholds = {1: 70, 2: 85, 3: 95}
    assert scoring.calculate_stars(60, thresholds) == 0
    assert scoring.calculate_stars(75, thresholds) == 1
    assert scoring.calculate_stars(90, thresholds) == 2
    assert scoring.calculate_stars(97, thresholds) == 3


def test_score_never_negative():
    weights = {
        "speed_multiplier": 1.0,
        "precision_multiplier": 1.0,
        "combo_multiplier": 1.0,
        "time_bonus_multiplier": 1.0,
        "error_penalty_multiplier": 100.0,
    }
    score = scoring.calculate_score(
        wpm=1, precision_pct=1, errors=50, max_combo=0, time_remaining_pct=0, weights=weights
    )
    assert score == 0.0


def test_xp_base_completion():
    assert scoring.calculate_xp(is_three_star=False, is_new_record=False, max_combo=5) == 100


def test_xp_three_star_bonus():
    assert scoring.calculate_xp(is_three_star=True, is_new_record=False, max_combo=5) == 150


def test_xp_new_record_bonus():
    assert scoring.calculate_xp(is_three_star=False, is_new_record=True, max_combo=5) == 200


def test_xp_combo_bonus_per_block_of_twenty():
    assert scoring.calculate_xp(is_three_star=False, is_new_record=False, max_combo=19) == 100
    assert scoring.calculate_xp(is_three_star=False, is_new_record=False, max_combo=20) == 120
    assert scoring.calculate_xp(is_three_star=False, is_new_record=False, max_combo=45) == 140


def test_xp_all_bonuses_combined():
    xp = scoring.calculate_xp(is_three_star=True, is_new_record=True, max_combo=20)
    assert xp == 100 + 50 + 100 + 20
