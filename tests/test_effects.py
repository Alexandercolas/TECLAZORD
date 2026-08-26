from core.effects import EffectManager


def test_trigger_adds_active_effect():
    fake_now = [0.0]
    manager = EffectManager(clock=lambda: fake_now[0])
    manager.trigger("flash_error", 0.2)
    assert len(manager.get("flash_error")) == 1


def test_update_removes_expired_effects():
    fake_now = [0.0]
    manager = EffectManager(clock=lambda: fake_now[0])
    manager.trigger("flash_error", 0.2)

    fake_now[0] = 0.1
    manager.update()
    assert len(manager.get("flash_error")) == 1

    fake_now[0] = 0.3
    manager.update()
    assert manager.get("flash_error") == []


def test_progress_goes_from_zero_to_one():
    fake_now = [0.0]
    manager = EffectManager(clock=lambda: fake_now[0])
    manager.trigger("fade", 1.0)
    effect = manager.get("fade")[0]

    assert manager.progress(effect) == 0.0

    fake_now[0] = 0.5
    assert manager.progress(effect) == 0.5

    fake_now[0] = 2.0
    assert manager.progress(effect) == 1.0  # se limita a 1.0, no sigue creciendo


def test_data_is_stored_and_retrievable():
    fake_now = [0.0]
    manager = EffectManager(clock=lambda: fake_now[0])
    manager.trigger("combo_popup", 0.5, {"combo": 40})
    effect = manager.get("combo_popup")[0]
    assert effect["data"]["combo"] == 40


def test_different_effect_types_do_not_mix():
    fake_now = [0.0]
    manager = EffectManager(clock=lambda: fake_now[0])
    manager.trigger("fade", 0.2)
    manager.trigger("flash_error", 0.2)
    assert len(manager.get("fade")) == 1
    assert len(manager.get("flash_error")) == 1
    assert len(manager.get("combo_popup")) == 0
