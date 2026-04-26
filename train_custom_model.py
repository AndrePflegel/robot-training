import os
import numpy as np
import cv2
import tensorflow as tf

DATA_DIR = "data/corrections"
MODEL_OUTPUT = "models/digit_model_custom.keras"


def load_data():
    images = []
    labels = []

    for label in range(10):
        label_dir = os.path.join(DATA_DIR, str(label))

        if not os.path.exists(label_dir):
            continue

        for file in os.listdir(label_dir):
            path = os.path.join(label_dir, file)

            img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

            if img is None:
                continue

            img = img / 255.0

            images.append(img)
            labels.append(label)

    return np.array(images), np.array(labels)


def build_model():
    model = tf.keras.Sequential([
        tf.keras.layers.Flatten(input_shape=(28, 28)),
        tf.keras.layers.Dense(128, activation="relu"),
        tf.keras.layers.Dense(64, activation="relu"),
        tf.keras.layers.Dense(10, activation="softmax")
    ])

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    return model


def main():
    x, y = load_data()

    if len(x) == 0:
        print("Keine Trainingsdaten gefunden.")
        return

    print(f"{len(x)} Bilder geladen.")

    model = build_model()

    model.fit(x, y, epochs=10, validation_split=0.2)

    model.save(MODEL_OUTPUT)

    print(f"Modell gespeichert unter: {MODEL_OUTPUT}")


if __name__ == "__main__":
    main()
