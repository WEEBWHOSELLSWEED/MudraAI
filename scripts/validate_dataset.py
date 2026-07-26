import os
import csv
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOCAB_FILE = os.path.join(BASE_DIR, "data", "vocab_list.csv")
LANDMARK_DIR = os.path.join(BASE_DIR, "data", "landmarks")
SEQUENCE_LENGTH = 45
FEATURES = 126

def load_vocabulary(csv_file):
    """Load vocabulary entries from the CSV file."""
    vocabulary = []

    with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            vocabulary.append(row)

    return vocabulary

def validate_dataset(vocabulary):

    total=0
    errors=0
    print("Validating dataset...")
    for item in vocabulary:
        word = item["word"]
        expected = int(item["samples"])
        folder = os.path.join(LANDMARK_DIR, word)
        if not os.path.exists(folder):
            print(f"Error: Folder for word '{word}' does not exist.")
            errors += 1
            continue
        files = sorted([f for f in os.listdir(folder) if f.endswith('.npy')])
        print(f"\n{word}: {len(files)} files found (expected: {expected})")
        if len(files) != expected:
            print("sample count mismatch!")
            errors += 1
        for file in files:
            path = os.path.join(folder, file)

            try:
                data=np.load(path)
                if data.shape != (SEQUENCE_LENGTH, FEATURES):
                    print(f"Error: File '{file}' has shape {data.shape}, expected {(SEQUENCE_LENGTH, FEATURES)}")
                    errors += 1
                elif np.isnan(data).any():
                    print(f"Error: File '{file}' contains NaN values.")
                    errors += 1
                total += 1
            except Exception as e:
                print(f"Error: Could not load file '{file}'. Exception: {e}")
                errors += 1

    print(f"checked {total} files, found {errors} errors.")
    if errors == 0:
        print("Dataset validation completed successfully. No errors found.")
    else:
        print("Dataset validation completed with errors. Please review the messages above.")

def main():
    vocabulary = load_vocabulary(VOCAB_FILE)
    validate_dataset(vocabulary)
if __name__ == "__main__":
    main()