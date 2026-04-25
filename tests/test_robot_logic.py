from modules.robot_logic import decide_action


def test_red_has_priority_over_line():
    result = decide_action(3000, 0, "Geradeaus")
    assert result == "STOP"


def test_red_has_priority_over_green():
    result = decide_action(3000, 3000, "Rechts lenken")
    assert result == "STOP"


def test_green_allows_line_direction():
    result = decide_action(0, 3000, "Links lenken")
    assert result == "GO: Links lenken"


def test_no_color_waits_with_direction():
    result = decide_action(0, 0, "Rechts lenken")
    assert result == "WAIT: Rechts lenken"


def test_threshold_is_not_enough_when_equal_2000():
    result = decide_action(2000, 0, "Geradeaus")
    assert result == "WAIT: Geradeaus"


def test_threshold_works_above_2000():
    result = decide_action(2001, 0, "Geradeaus")
    assert result == "STOP"
