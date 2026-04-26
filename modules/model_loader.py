import os
import tensorflow as tf


MODEL_PATHS = {
    "mnist": "models/digit_model.keras",
    "custom": "models/digit_model_custom.keras",
}


def model_exists(model_name):
    if model_name not in MODEL_PATHS:
        return False

    return os.path.exists(MODEL_PATHS[model_name])


def load_digit_model(model_name="mnist"):
    if model_name not in MODEL_PATHS:
        raise ValueError(f"Unbekanntes Modell: {model_name}")

    model_path = MODEL_PATHS[model_name]

    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Modell nicht gefunden: {model_path}")

    return tf.keras.models.load_model(model_path)
