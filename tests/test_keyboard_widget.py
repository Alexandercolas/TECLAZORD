from ui.keyboard_widget import _resolve_target_key


def test_none_when_no_next_char():
    assert _resolve_target_key(None) is None


def test_space_has_no_key_to_highlight():
    assert _resolve_target_key(" ") is None


def test_letter_is_lowercased():
    assert _resolve_target_key("A") == "a"


def test_digit_passes_through():
    assert _resolve_target_key("7") == "7"


def test_shifted_symbol_resolves_to_base_key():
    assert _resolve_target_key("!") == "1"
    assert _resolve_target_key("@") == "2"
    assert _resolve_target_key(":") == ";"
    assert _resolve_target_key('"') == "'"


def test_newline_resolves_to_enter():
    assert _resolve_target_key("\n") == "\n"
