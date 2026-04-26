import numpy as np

from modules.digit_preprocess_utils import threshold_digit_roi, resize_to_mnist
from modules.digit_preprocess_utils import extract_largest_digit


def test_threshold_digit_roi_shape():
    fake_roi = np.ones((220, 220, 3), dtype=np.uint8) * 255

    result = threshold_digit_roi(fake_roi)

    assert result.shape == (220, 220)


def test_threshold_digit_roi_values_are_binary():
    fake_roi = np.ones((220, 220, 3), dtype=np.uint8) * 255

    result = threshold_digit_roi(fake_roi)

    unique_values = set(np.unique(result))

    assert unique_values.issubset({0, 255})


def test_resize_to_mnist_shape():
    fake_image = np.ones((220, 220), dtype=np.uint8) * 255

    result = resize_to_mnist(fake_image)

    assert result.shape == (28, 28)


def test_resize_to_mnist_value_range():
    fake_image = np.ones((220, 220), dtype=np.uint8) * 255

    result = resize_to_mnist(fake_image)

    assert result.min() >= 0.0
    assert result.max() <= 1.0
    
def test_extract_largest_digit_returns_none_for_empty():
    img = np.zeros((100, 100), dtype=np.uint8)
    
    result = extract_largest_digit(img)
    
    assert result is None
    
    
def test_extract_largest_digit_finds_object():
    img = np.zeros((100, 100), dtype=np.uint8)
    
    img[30:70, 30:70] = 255
    
    result = extract_largest_digit(img)
    
    assert result is not None
    assert result.shape[0] > 0
    assert result.shape[1] > 0
