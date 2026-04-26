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
    
def test_line_roi_start_ratio_valid():
    assert 0 < settings.LINE_ROI_START_RATIO < 1


def test_line_threshold_valid():
    assert 0 <= settings.LINE_THRESHOLD <= 255


def test_line_kernel_size_positive():
    assert settings.LINE_KERNEL_SIZE > 0
    assert settings.LINE_KERNEL_SIZE % 2 == 1


def test_line_min_area_positive():
    assert settings.LINE_MIN_AREA > 0
