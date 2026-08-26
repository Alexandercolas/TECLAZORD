from core.input_manager import InputManager


def test_correct_characters_build_combo():
    im = InputManager("fj")
    im.handle_text_input("f")
    im.handle_text_input("j")
    assert im.correct_count == 2
    assert im.error_count == 0
    assert im.combo == 2
    assert im.max_combo == 2
    assert im.is_complete()


def test_wrong_character_resets_combo_but_keeps_max():
    im = InputManager("fj")
    im.handle_text_input("f")
    im.handle_text_input("x")
    assert im.correct_count == 1
    assert im.error_count == 1
    assert im.combo == 0
    assert im.max_combo == 1


def test_records_which_expected_character_was_missed():
    im = InputManager("f7")
    im.handle_text_input("x")  # se esperaba 'f'
    im.handle_text_input("y")  # se esperaba '7'
    assert im.character_errors == {"f": 1, "7": 1}


def test_repeated_misses_on_same_character_accumulate():
    im = InputManager("77")
    im.handle_text_input("x")
    im.handle_text_input("y")
    assert im.character_errors == {"7": 2}


def test_backspace_removes_last_typed_character():
    im = InputManager("fj")
    im.handle_text_input("f")
    im.handle_backspace()
    assert im.typed == ""
    assert not im.is_complete()


def test_ignores_input_past_target_length():
    im = InputManager("f")
    im.handle_text_input("f")
    im.handle_text_input("x")
    assert im.typed == "f"
    assert im.error_count == 0
