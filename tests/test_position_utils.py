from modules.position_utils import get_horizontal_position


def test_position_left():
    assert get_horizontal_position(50, 300) == "Links"


def test_position_middle():
    assert get_horizontal_position(150, 300) == "Mitte"


def test_position_right():
    assert get_horizontal_position(250, 300) == "Rechts"


def test_left_boundary_is_middle():
    assert get_horizontal_position(100, 300) == "Mitte"


def test_right_boundary_is_middle():
    assert get_horizontal_position(200, 300) == "Mitte"
