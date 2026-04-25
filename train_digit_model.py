import tensorflow as tf
from tensorflow import keras
from tensorflow.keras import layers

# MNIST laden
(x_train, y_train), (x_test, y_test) = keras.datasets.mnist.load_data()

# Normalisieren (0-255 → 0-1)
x_train = x_train / 255.0
x_test = x_test / 255.0

# Modell definieren
model = keras.Sequential([
    layers.Flatten(input_shape=(28, 28)),
    layers.Dense(128, activation='relu'),
    layers.Dense(10, activation='softmax')
])

# Kompilieren
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Trainieren
model.fit(x_train, y_train, epochs=5)

# Testen
loss, accuracy = model.evaluate(x_test, y_test)
print("Test-Accuracy:", accuracy)

# Speichern
model.save("models/digit_model.keras")
