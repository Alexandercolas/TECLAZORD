from systems.key_stats import KeyStats


def test_starts_empty(tmp_path):
    stats = KeyStats(path=str(tmp_path / "key_stats.json"))
    assert stats.data["error_counts"] == {}
    assert stats.most_failed() == []


def test_register_errors_accumulates(tmp_path):
    stats = KeyStats(path=str(tmp_path / "key_stats.json"))
    stats.register_errors({"7": 3, "p": 1})
    stats.register_errors({"7": 2, "ñ": 1})

    assert stats.data["error_counts"] == {"7": 5, "p": 1, "ñ": 1}


def test_ignores_space_and_newline(tmp_path):
    stats = KeyStats(path=str(tmp_path / "key_stats.json"))
    stats.register_errors({" ": 5, "\n": 2, "a": 1})
    assert stats.data["error_counts"] == {"a": 1}


def test_most_failed_sorted_descending(tmp_path):
    stats = KeyStats(path=str(tmp_path / "key_stats.json"))
    stats.register_errors({"a": 1, "b": 5, "c": 3})
    assert stats.most_failed(limit=2) == [("b", 5), ("c", 3)]


def test_most_failed_by_category(tmp_path):
    stats = KeyStats(path=str(tmp_path / "key_stats.json"))
    stats.register_errors({"p": 4, "7": 6, "@": 2, "ñ": 1})

    assert stats.most_failed_letters() == [("p", 4), ("ñ", 1)]
    assert stats.most_failed_numbers() == [("7", 6)]
    assert stats.most_failed_symbols() == [("@", 2)]


def test_persists_and_reloads(tmp_path):
    path = str(tmp_path / "key_stats.json")
    stats = KeyStats(path=path)
    stats.register_errors({"7": 3})

    reloaded = KeyStats(path=path)
    assert reloaded.data["error_counts"] == {"7": 3}
