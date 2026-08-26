from core.player import Player


def test_starts_at_zero_xp(tmp_path):
    player = Player(path=str(tmp_path / "player.json"))
    assert player.data["total_xp"] == 0


def test_default_name_is_jugador(tmp_path):
    player = Player(path=str(tmp_path / "player.json"))
    assert player.data["name"] == "Jugador"


def test_set_name_trims_and_persists(tmp_path):
    path = str(tmp_path / "player.json")
    player = Player(path=path)
    player.set_name("  Alex  ")
    assert player.data["name"] == "Alex"

    reloaded = Player(path=path)
    assert reloaded.data["name"] == "Alex"


def test_set_name_blank_falls_back_to_jugador(tmp_path):
    player = Player(path=str(tmp_path / "player.json"))
    player.set_name("   ")
    assert player.data["name"] == "Jugador"


def test_add_xp_accumulates_and_persists(tmp_path):
    path = str(tmp_path / "player.json")
    player = Player(path=path)
    player.add_xp(100)
    player.add_xp(50)
    assert player.data["total_xp"] == 150

    reloaded = Player(path=path)
    assert reloaded.data["total_xp"] == 150
