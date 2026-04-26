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

    result = predict_digit(None, "mnist", mnist, custom)

    assert result["final_digit"] == 3
    assert result["final_confidence"] == 0.90
    assert result["source"] == "MNIST"
    assert result["mnist_digit"] == 3
    assert result["custom_digit"] is None


def test_custom_mode_uses_custom():
    mnist = FakeModel(3, 0.90)
    custom = FakeModel(7, 0.99)

    result = predict_digit(None, "custom", mnist, custom)

    assert result["final_digit"] == 7
    assert result["final_confidence"] == 0.99
    assert result["source"] == "CUSTOM"
    assert result["mnist_digit"] == 3
    assert result["custom_digit"] == 7


def test_dual_mode_uses_custom_when_confident():
    mnist = FakeModel(3, 0.90)
    custom = FakeModel(7, 0.95)

    result = predict_digit(None, "dual", mnist, custom)

    assert result["final_digit"] == 7
    assert result["final_confidence"] == 0.95
    assert result["source"] == "CUSTOM"
    assert result["mnist_digit"] == 3
    assert result["custom_digit"] == 7


def test_dual_mode_falls_back_to_mnist_when_custom_uncertain():
    mnist = FakeModel(3, 0.90)
    custom = FakeModel(7, 0.20)

    result = predict_digit(None, "dual", mnist, custom)

    assert result["final_digit"] == 3
    assert result["final_confidence"] == 0.90
    assert result["source"] == "MNIST"
    assert result["mnist_digit"] == 3
    assert result["custom_digit"] == 7
