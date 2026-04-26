import os
import cv2
import numpy as np
import tensorflow as tf

DATA_DIR = "data/corrections"
BASE_MODEL = "models/digit_model.keras"
CUSTOM_MODEL = "models/digit_model_custom.keras"


def load_correction_data():
    images = []
    labels = []

    for label in range(10):
        folder = os.path.join(DATA_DIR, str(label))

        if not os.path.exists(folder):
            continue

        for filename in os.listdir(folder):
            path = os.path.join(folder, filename)

            image = cv2.imread(path, cv2.IMREAD_GRAYSCALE)

            if image is None:
                continue

            image = image / 255.0

            images.append(image)
            labels.append(label)

    return np.array(images), np.array(labels)


def main():
    x_train, y_train = load_correction_data()

    if len(x_train) == 0:
        print("Keine Korrekturdaten gefunden.")
        return

    print(f"Korrekturbilder geladen: {len(x_train)}")

    model = tf.keras.models.load_model(BASE_MODEL)

    model.compile(
        optimizer=tf.keras.optimizers.Adam(learning_rate=0.0001),
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    model.fit(
        x_train,
        y_train,
        epochs=5,
        batch_size=8,
        shuffle=True
    )

    model.save(CUSTOM_MODEL)

    print(f"Custom-Modell gespeichert unter: {CUSTOM_MODEL}")


if __name__ == "__main__":
    main()
