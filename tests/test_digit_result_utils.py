from modules.digit_result_utils import format_digit_result


def test_confident_digit_result():
    result = format_digit_result(5, 0.93)
    assert result == "Zahl: 5 (0.93)"


def test_uncertain_digit_result():
    result = format_digit_result(5, 0.42)
    assert result == "Unsicher"


def test_threshold_equal_is_accepted():
    result = format_digit_result(3, 0.70)
    assert result == "Zahl: 3 (0.70)"


def test_custom_threshold():
    result = format_digit_result(8, 0.80, min_confidence=0.90)
    assert result == "Unsicher"
