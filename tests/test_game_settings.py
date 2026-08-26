from systems.game_settings import GameSettings


def test_defaults(tmp_path):
    settings = GameSettings(path=str(tmp_path / "settings.json"))
    assert settings.data["sound_enabled"] is True
    assert settings.data["volume"] == 0.5


def test_toggle_sound(tmp_path):
    settings = GameSettings(path=str(tmp_path / "settings.json"))
    settings.toggle_sound()
    assert settings.data["sound_enabled"] is False
    settings.toggle_sound()
    assert settings.data["sound_enabled"] is True


def test_set_volume_clamped_between_zero_and_one(tmp_path):
    settings = GameSettings(path=str(tmp_path / "settings.json"))
    settings.set_volume(1.5)
    assert settings.data["volume"] == 1.0
    settings.set_volume(-0.5)
    assert settings.data["volume"] == 0.0


def test_persists_and_reloads(tmp_path):
    path = str(tmp_path / "settings.json")
    settings = GameSettings(path=path)
    settings.set_volume(0.8)
    settings.toggle_sound()

    reloaded = GameSettings(path=path)
    assert reloaded.data["volume"] == 0.8
    assert reloaded.data["sound_enabled"] is False
