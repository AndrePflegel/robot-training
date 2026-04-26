import os
import numpy as np
import pytest

from modules.digit_dataset_utils import save_digit_correction


def test_save_digit_correction_creates_file(tmp_path):
    image = np.zeros((28, 28), dtype=np.uint8)

    file_path = save_digit_correction(
        image,
        "3",
        base_dir=str(tmp_path)
    )

    assert os.path.exists(file_path)
    assert file_path.endswith(".png")
    assert "/3/" in file_path


def test_save_digit_correction_rejects_invalid_label(tmp_path):
    image = np.zeros((28, 28), dtype=np.uint8)

    with pytest.raises(ValueError):
        save_digit_correction(
            image,
            "x",
            base_dir=str(tmp_path)
        )
