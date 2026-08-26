from core.timer import GameTimer


def test_not_started_has_zero_elapsed():
    timer = GameTimer(10, clock=lambda: 999)
    assert timer.elapsed() == 0.0
    assert not timer.is_expired()


def test_counts_down_with_injected_clock():
    fake_now = [0]
    timer = GameTimer(10, clock=lambda: fake_now[0])
    timer.start()

    fake_now[0] = 4
    assert timer.elapsed() == 4
    assert timer.remaining() == 6
    assert not timer.is_expired()

    fake_now[0] = 10
    assert timer.is_expired()


def test_remaining_never_negative():
    fake_now = [0]
    timer = GameTimer(5, clock=lambda: fake_now[0])
    timer.start()
    fake_now[0] = 50
    assert timer.remaining() == 0.0
