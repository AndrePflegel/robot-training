from modules.line_utils import get_direction_from_center


def test_left_direction():
    assert get_direction_from_center(50, 300) == "Links lenken"


def test_center_direction():
    assert get_direction_from_center(150, 300) == "Geradeaus"


def test_right_direction():
    assert get_direction_from_center(250, 300) == "Rechts lenken"
