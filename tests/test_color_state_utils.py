from modules.color_state_utils import get_color_state


def test_red_returns_stop():
    assert get_color_state(3000, 0) == "STOP"


def test_green_returns_go():
    assert get_color_state(0, 3000) == "GO"


def test_no_color_returns_wait():
    assert get_color_state(0, 0) == "WAIT"


def test_red_has_priority_over_green():
    assert get_color_state(3000, 3000) == "STOP"


def test_equal_threshold_is_not_enough():
    assert get_color_state(2000, 0) == "WAIT"


def test_custom_threshold():
    assert get_color_state(600, 0, threshold=500) == "STOP"
