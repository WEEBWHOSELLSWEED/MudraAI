import os 
import csv
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOCAB_FILE = os.path.join(BASE_DIR, "data", "vocab_list.csv")   
LANDMARK_DIR = os.path.join(BASE_DIR, "data", "landmarks")

def load_vocabulary(csv_file):
    """Load vocabulary entries from the CSV file."""
    vocabulary = []

    with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            vocabulary.append(row)

    return vocabulary

def load_dataset(vocabulary):

    X = []
    y = []

    label_map = {}

    for label, item in enumerate(vocabulary):

        word = item["word"]

        label_map[word] = label

        folder = os.path.join(LANDMARK_DIR, word)

        if not os.path.exists(folder):
            continue

        files = sorted(
            f for f in os.listdir(folder)
            if f.endswith(".npy")
        )

        for file in files:

            path = os.path.join(folder, file)

            sequence = np.load(path)

            X.append(sequence)

            y.append(label)

    return (
        np.array(X),
        np.array(y),
        label_map
    )

def main():

    vocabulary = load_vocabulary(VOCAB_FILE)

    X, y, label_map = load_dataset(vocabulary)

    print("Dataset Loaded\n")

    print("X shape:", X.shape)

    print("y shape:", y.shape)

    print("\nLabel Map")

    print(label_map)


if __name__ == "__main__":

    main()
