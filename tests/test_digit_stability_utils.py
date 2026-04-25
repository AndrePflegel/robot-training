from modules.digit_stability_utils import get_stable_digit


def test_simple_majority():
    digits = [1, 1, 1, 2, 3]
    assert get_stable_digit(digits) == 1


def test_empty_list():
    assert get_stable_digit([]) is None


def test_all_different():
    digits = [1, 2, 3]
    assert get_stable_digit(digits) in digits


def test_clear_winner():
    digits = [5, 5, 5, 5, 2]
    assert get_stable_digit(digits) == 5
