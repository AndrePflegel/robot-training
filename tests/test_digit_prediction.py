import numpy as np

from modules.digit_recognition import predict_digit


class FakeModel:
    def __init__(self, digit, confidence):
        self.digit = digit
        self.confidence = confidence

    def predict(self, input_image, verbose=0):
        result = np.zeros((1, 10))
        result[0][self.digit] = self.confidence
        return result


def test_mnist_mode_uses_mnist():
    mnist = FakeModel(3, 0.90)
    custom = FakeModel(7, 0.99)

    digit, confidence, source = predict_digit(
        None,
        "mnist",
        mnist,
        custom
    )

    assert digit == 3
    assert confidence == 0.90
    assert source == "MNIST"


def test_custom_mode_uses_custom():
    mnist = FakeModel(3, 0.90)
    custom = FakeModel(7, 0.99)

    digit, confidence, source = predict_digit(
        None,
        "custom",
        mnist,
        custom
    )

    assert digit == 7
    assert confidence == 0.99
    assert source == "CUSTOM"


def test_dual_mode_uses_custom_when_confident():
    mnist = FakeModel(3, 0.90)
    custom = FakeModel(7, 0.95)

    digit, confidence, source = predict_digit(
        None,
        "dual",
        mnist,
        custom
    )

    assert digit == 7
    assert confidence == 0.95
    assert source == "CUSTOM"


def test_dual_mode_falls_back_to_mnist_when_custom_uncertain():
    mnist = FakeModel(3, 0.90)
    custom = FakeModel(7, 0.20)

    digit, confidence, source = predict_digit(
        None,
        "dual",
        mnist,
        custom
    )

    assert digit == 3
    assert confidence == 0.90
    assert source == "MNIST"
