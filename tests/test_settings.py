from config import settings


def test_red_lower_1_shape():
    assert settings.RED_LOWER_1.shape == (3,)


def test_red_upper_1_shape():
    assert settings.RED_UPPER_1.shape == (3,)


def test_red_lower_2_shape():
    assert settings.RED_LOWER_2.shape == (3,)


def test_red_upper_2_shape():
    assert settings.RED_UPPER_2.shape == (3,)


def test_color_min_area_positive():
    assert settings.COLOR_MIN_AREA > 0
