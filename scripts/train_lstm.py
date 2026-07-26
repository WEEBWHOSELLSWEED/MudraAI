import os

import tensorflow as tf
from sklearn.model_selection import train_test_split

from dataset_loader import (
    load_dataset,
    load_vocabulary,
    VOCAB_FILE
)


def main():

    # Load dataset
    vocabulary = load_vocabulary(VOCAB_FILE)

    X, y, label_map = load_dataset(vocabulary)

    print("Dataset:", X.shape)
    print("Labels :", y.shape)

    # Train/Test split
    X_train, X_test, y_train, y_test = train_test_split(
        X,
        y,
        test_size=0.2,
        random_state=42,
        stratify=y
    )

    input_shape = X.shape[1:]

    # Build model
    model = tf.keras.Sequential([
        tf.keras.layers.Input(shape=input_shape),
        tf.keras.layers.LSTM(64),
        tf.keras.layers.Dropout(0.3),
        tf.keras.layers.Dense(32, activation="relu"),
        tf.keras.layers.Dense(len(label_map), activation="softmax")
    ])

    model.compile(
        optimizer="adam",
        loss="sparse_categorical_crossentropy",
        metrics=["accuracy"]
    )

    early_stop = tf.keras.callbacks.EarlyStopping(
        monitor="val_loss",
        patience=5,
        restore_best_weights=True
    )

    history = model.fit(
        X_train,
        y_train,
        validation_split=0.2,
        epochs=30,
        batch_size=8,
        callbacks=[early_stop]
    )

    loss, accuracy = model.evaluate(X_test, y_test)

    print(f"\nTest Accuracy: {accuracy:.2%}")

    MODEL_DIR = os.path.join(
        os.path.dirname(os.path.dirname(__file__)),
        "models"
    )

    os.makedirs(MODEL_DIR, exist_ok=True)

    model.save(os.path.join(MODEL_DIR, "isl_lstm.keras"))

    print("Model saved!")


if __name__ == "__main__":
    main()
