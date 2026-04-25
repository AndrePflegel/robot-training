import sys
import os
import numpy as np

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from modules.digit_utils import preprocess_digit_image


def test_preprocess_shape():
    fake = np.ones((480, 640, 3), dtype=np.uint8) * 255
    result = preprocess_digit_image(fake, 100, 100, 300, 300)

    assert result.shape == (28, 28)


def test_preprocess_range():
    fake = np.ones((480, 640, 3), dtype=np.uint8) * 255
    result = preprocess_digit_image(fake, 100, 100, 300, 300)

    assert result.min() >= 0.0
    assert result.max() <= 1.0
