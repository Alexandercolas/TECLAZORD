import os

from core import paths


def test_not_frozen_by_default():
    # Corriendo bajo pytest (o "python main.py"), nunca deberia reportarse
    # como empaquetado.
    assert paths.is_frozen() is False


def test_user_data_dir_is_project_data_folder_when_not_frozen():
    expected = os.path.join(paths.get_base_dir(), "data")
    assert paths.get_user_data_dir() == expected


def test_user_data_dir_uses_localappdata_when_frozen(monkeypatch):
    monkeypatch.setattr(paths.sys, "frozen", True, raising=False)
    monkeypatch.setenv("LOCALAPPDATA", r"C:\Users\Someone\AppData\Local")
    monkeypatch.setattr(paths.sys, "platform", "win32")

    result = paths.get_user_data_dir()

    assert result == r"C:\Users\Someone\AppData\Local\TeclazoRD"


def test_get_user_data_path_creates_directory(tmp_path, monkeypatch):
    monkeypatch.setattr(paths, "get_user_data_dir", lambda: str(tmp_path / "nested"))

    result = paths.get_user_data_path("player.json")

    assert result == str(tmp_path / "nested" / "player.json")
    assert os.path.isdir(tmp_path / "nested")


def test_get_asset_path_joins_base_dir_and_assets():
    result = paths.get_asset_path("sounds", "type_correct.wav")
    assert result == os.path.join(paths.get_base_dir(), "assets", "sounds", "type_correct.wav")


def test_base_dir_is_project_root_when_not_frozen():
    base_dir = paths.get_base_dir()
    # La raiz del proyecto debe contener main.py.
    assert os.path.isfile(os.path.join(base_dir, "main.py"))
