from modules.line_contour_utils import get_biggest_valid_contour


def test_no_contours():
    assert get_biggest_valid_contour([]) is None


def test_small_contour_filtered():
    contours = [
        ("c1", 200),
        ("c2", 300)
    ]

    assert get_biggest_valid_contour(contours, min_area=500) is None


def test_biggest_contour_selected():
    contours = [
        ("c1", 500),
        ("c2", 1000),
        ("c3", 800)
    ]

    result = get_biggest_valid_contour(contours, min_area=500)

    assert result == "c2"
