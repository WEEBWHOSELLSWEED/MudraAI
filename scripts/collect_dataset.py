"""Collect hand landmark samples for the MudraAI dataset."""

import csv
import os
import time
import numpy as np

import cv2
import mediapipe as mp


# -----------------------------------------------------------------------------
# Configuration
# -----------------------------------------------------------------------------
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
VOCAB_FILE = os.path.join(BASE_DIR, "data", "vocab_list.csv")
LANDMARK_DIR = os.path.join(BASE_DIR, "data", "landmarks")
COUNTDOWN_SECONDS = 3
SEQUENCE_LENGTH = 45
TARGET_SAMPLES = 30

# -----------------------------------------------------------------------------
# Helper Functions
# -----------------------------------------------------------------------------
def load_vocabulary(csv_file):
    """Load vocabulary entries from the CSV file."""
    vocabulary = []

    with open(csv_file, mode="r", newline="", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        for row in reader:
            vocabulary.append(row)

    return vocabulary


def create_word_folders(vocabulary):
    """Create a folder for each word in the vocabulary."""
    os.makedirs(LANDMARK_DIR, exist_ok=True)

    for word in vocabulary:
        folder = os.path.join(LANDMARK_DIR, word["word"])
        os.makedirs(folder, exist_ok=True)



def print_instructions():
    """Print keyboard instructions for the user."""
    print("\nMudraAI Dataset Collector")
    print("SPACE : Record sample")
    print("N     : Next word")
    print("B     : Previous word")
    print("ESC   : Exit")


def initialize_media_pipe():
    """Set up MediaPipe hand detection."""
    mp_hands = mp.solutions.hands
    mp_draw = mp.solutions.drawing_utils

    hands = mp_hands.Hands(
        static_image_mode=False,
        max_num_hands=2,
        min_detection_confidence=0.7,
        min_tracking_confidence=0.5,
    )

    return mp_hands, mp_draw, hands

def extract_landmarks(results):
    """Extract both hands into a consistent 126-value feature vector."""

    landmarks = [0.0] * 126

    if not results.multi_hand_landmarks:
        return landmarks

    for hand_landmarks, handedness in zip(
        results.multi_hand_landmarks,
        results.multi_handedness,
    ):

        label = handedness.classification[0].label

        if label == "Left":
            offset = 0
        else:
            offset = 63

        for i, landmark in enumerate(hand_landmarks.landmark):

            landmarks[offset + i * 3] = landmark.x
            landmarks[offset + i * 3 + 1] = landmark.y
            landmarks[offset + i * 3 + 2] = landmark.z

    return landmarks

def save_sequence(sequence, word):
    """Save a recorded landmark sequence as a .npy file."""

    word_folder = os.path.join(LANDMARK_DIR, word)

    existing = [
        f for f in os.listdir(word_folder)
        if f.endswith(".npy")
    ]

    highest=0

    for file in existing:
        try:
            number = int(file.split("_")[-1].split(".")[0])
            if number > highest:
                highest = number
        except ValueError:
            continue

    sample_number = highest + 1

    filename = os.path.join(
        word_folder,
        f"{word}_{sample_number:03d}.npy"
    )

    np.save(filename, np.array(sequence))

    return filename

def update_sample_count(word):
    """Update the sample count for a word in vocab_list.csv."""

    rows = []

    with open(VOCAB_FILE, "r", newline="") as file:
        reader = csv.DictReader(file)

        for row in reader:

            if row["word"] == word:

                folder = os.path.join(LANDMARK_DIR, word)

                count = len(
                    [
                        f
                        for f in os.listdir(folder)
                        if f.endswith(".npy")
                    ]
                )

                row["samples"] = str(count)

            rows.append(row)

    with open(VOCAB_FILE, "w", newline="") as file:

        writer = csv.DictWriter(
            file,
            fieldnames=["id", "word", "category", "samples"],
        )

        writer.writeheader()
        writer.writerows(rows)


# -----------------------------------------------------------------------------
# Main Workflow
# -----------------------------------------------------------------------------
def main():
    vocabulary = load_vocabulary(VOCAB_FILE)
    create_word_folders(vocabulary)

    mp_hands, mp_draw, hands = initialize_media_pipe()

    current_word = 0
    countdown = False
    countdown_start = 0
    recording = False
    sequence = []

    print(f"Loaded {len(vocabulary)} words.\n")
    print_instructions()

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        raise SystemExit("Error: Could not open webcam.")

    while True:
        success, frame = cap.read()
        if not success:
            print("Failed to read frame.")
            break

        # Mirror the camera for a natural view
        frame = cv2.flip(frame, 1)

        # Convert BGR → RGB for MediaPipe
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect hands and draw landmarks
        results = hands.process(rgb)
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                mp_draw.draw_landmarks(
                    frame,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                )

        current = vocabulary[current_word]
        word = current["word"]
        category = current["category"]
        samples = int(current["samples"])

        remaining = COUNTDOWN_SECONDS
        status = "ready"

        if countdown:
            elapsed = time.time() - countdown_start
            remaining = max(0, COUNTDOWN_SECONDS - int(elapsed))

            if remaining > 0:
                status = f"starting in {remaining} seconds"
            else:
                countdown = False
                recording = True
                print("Recording starts!")
                status = f"recording {len(sequence)}/{SEQUENCE_LENGTH}"

        elif recording:
            status = f"recording {len(sequence)}/{SEQUENCE_LENGTH}"

        cv2.putText(frame,
            f"Word: {word}",
            (20,40),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0,255,0),
            2)

        cv2.putText(frame,
            f"Category: {category}",
            (20,70),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,255,255),
            2)

        cv2.putText(frame,
            f"Samples: {samples}",
            (20,100),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,255,255),
            2)

        cv2.putText(frame,
            f"Target: {samples}/{TARGET_SAMPLES}",
            (20,130),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,255,255),
            2)

        cv2.putText(frame,
            f"Progress: {current_word + 1}/{len(vocabulary)}",
            (20,160),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (255,255,255),
            2)  

        cv2.putText(frame,
            f"Status: {status}",
            (20,190),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.7,
            (0,255,255),
            2)

        # Handle countdown timer
        if countdown:
            if remaining > 0:
                cv2.putText(
                    frame,
                    str(remaining),
                    (frame.shape[1] // 2 - 20, frame.shape[0] // 2),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    4,
                    (0, 0, 255),
                    6,
                )

        # Handle recording state
        if recording:

            sequence.append(extract_landmarks(results))

            cv2.putText(
                frame,
                f"Recording: {len(sequence)}/{SEQUENCE_LENGTH}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 0, 255),
                2,
            )
                
            if len(sequence) >= SEQUENCE_LENGTH:
                recording = False
                print("Recording finished!")
                sequence = np.array(sequence)
                filename=save_sequence(sequence, word)
                update_sample_count(word)
                vocabulary[current_word]["samples"] = str(
                int(vocabulary[current_word]["samples"]) + 1)
                print(f"Saved sequence to {filename}")
                sequence = []
                recording = False

    

        cv2.imshow("MudraAI Dataset Collector", frame)

        # Handle keyboard events
        key = cv2.waitKey(1) & 0xFF

        if key == ord("n"):
            current_word = (current_word + 1) % len(vocabulary)
        elif key == ord("b"):
            current_word = (current_word - 1) % len(vocabulary)
        elif key == ord(" "):
            if not countdown and not recording:
                countdown = True
                countdown_start = time.time()
        elif key == 27:
            break

    cap.release()
    cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
