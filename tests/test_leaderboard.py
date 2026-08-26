from systems.leaderboard import Leaderboard


def test_starts_empty(tmp_path):
    board = Leaderboard(path=str(tmp_path / "leaderboard.json"))
    assert board.get_top() == []


def test_registers_first_run_for_a_name(tmp_path):
    board = Leaderboard(path=str(tmp_path / "leaderboard.json"))
    updated = board.register_run("Alex", wpm=72.0, precision=95.0, level_number=5, score=8000)
    assert updated is True
    assert board.get_top() == [("Alex", {"wpm": 72.0, "precision": 95.0, "level_number": 5, "score": 8000})]


def test_only_updates_when_beating_own_previous_best(tmp_path):
    board = Leaderboard(path=str(tmp_path / "leaderboard.json"))
    board.register_run("Alex", wpm=72.0, precision=95.0, level_number=5, score=8000)

    worse = board.register_run("Alex", wpm=60.0, precision=90.0, level_number=5, score=6000)
    assert worse is False
    assert board.get_top()[0][1]["wpm"] == 72.0

    better = board.register_run("Alex", wpm=80.0, precision=97.0, level_number=5, score=9000)
    assert better is True
    assert board.get_top()[0][1]["wpm"] == 80.0


def test_ranks_multiple_names_by_wpm_descending(tmp_path):
    board = Leaderboard(path=str(tmp_path / "leaderboard.json"))
    board.register_run("Luis", wpm=61.0, precision=90.0, level_number=3, score=5000)
    board.register_run("Alex", wpm=72.0, precision=95.0, level_number=5, score=8000)
    board.register_run("Carlos", wpm=68.0, precision=93.0, level_number=4, score=7000)

    top = board.get_top()
    assert [name for name, _ in top] == ["Alex", "Carlos", "Luis"]


def test_get_top_respects_limit(tmp_path):
    board = Leaderboard(path=str(tmp_path / "leaderboard.json"))
    for i in range(5):
        board.register_run(f"Jugador{i}", wpm=float(i), precision=90.0, level_number=1, score=100)
    assert len(board.get_top(limit=3)) == 3


def test_blank_name_falls_back_to_jugador(tmp_path):
    board = Leaderboard(path=str(tmp_path / "leaderboard.json"))
    board.register_run("   ", wpm=50.0, precision=90.0, level_number=1, score=100)
    assert board.get_top()[0][0] == "Jugador"


def test_persists_and_reloads(tmp_path):
    path = str(tmp_path / "leaderboard.json")
    board = Leaderboard(path=path)
    board.register_run("Alex", wpm=72.0, precision=95.0, level_number=5, score=8000)

    reloaded = Leaderboard(path=path)
    assert reloaded.get_top()[0][0] == "Alex"
