import base64
import pickle
import cv2
import mediapipe as mp
import numpy as np
import warnings
from flask import Flask, render_template
from flask_socketio import SocketIO, emit

# Suppress specific warnings
warnings.filterwarnings("ignore", message="SymbolDatabase.GetPrototype() is deprecated. Please use message_factory.GetMessageClass() instead.")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

import os
# Load model (Prefer improved, fallback to baseline)
try:
    if os.path.exists('./improved_model.p'):
        model_dict = pickle.load(open('./improved_model.p', 'rb'))
        print("Loaded improved_model.p")
    else:
        model_dict = pickle.load(open('./model.p', 'rb'))
        print("Loaded baseline model.p")
    model = model_dict['model']
except Exception as e:
    print("Error loading the model:", e)
    model = None

# Initialize MediaPipe Tasks API
BaseOptions = mp.tasks.BaseOptions
HandLandmarker = mp.tasks.vision.HandLandmarker
HandLandmarkerOptions = mp.tasks.vision.HandLandmarkerOptions
VisionRunningMode = mp.tasks.vision.RunningMode

options = HandLandmarkerOptions(
    base_options=BaseOptions(model_asset_path='./hand_landmarker.task'),
    running_mode=VisionRunningMode.IMAGE,
    num_hands=2,
    min_hand_detection_confidence=0.3
)
landmarker = HandLandmarker.create_from_options(options)

labels_dict = {
    0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F', 6: 'G', 7: 'H', 8: 'I', 9: 'J',
    10: 'K', 11: 'L', 12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R', 18: 'S',
    19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X', 24: 'Y', 25: 'Z', 26: 'Hello',
    27: 'Done', 28: 'Thank You', 29: 'I Love you', 30: 'Sorry', 31: 'Please',
    32: 'You are welcome.'
}

@app.route('/')
def index():
    return render_template('index.html')

@socketio.on('connect')
def handle_connect():
    print('Client connected')

@socketio.on('image')
def handle_image(data_url):
    try:
        encoded_data = data_url.split(',')[1]
        nparr = np.frombuffer(base64.b64decode(encoded_data), np.uint8)
        frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        frame = cv2.flip(frame, 1)

        H, W, _ = frame.shape
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)
        results = landmarker.detect(mp_image)

        if results.hand_landmarks:
            for hand_landmarks in results.hand_landmarks:
                x_ = []
                y_ = []
                data_aux = []

                for i in range(len(hand_landmarks)):
                    x = hand_landmarks[i].x
                    y = hand_landmarks[i].y
                    x_.append(x)
                    y_.append(y)

                for i in range(len(hand_landmarks)):
                    x = hand_landmarks[i].x
                    y = hand_landmarks[i].y
                    data_aux.append(x - min(x_))
                    data_aux.append(y - min(y_))

                x1 = int(min(x_) * W) - 10
                y1 = int(min(y_) * H) - 10
                x2 = int(max(x_) * W) - 10
                y2 = int(max(y_) * H) - 10

                if model is not None:
                    try:
                        prediction = model.predict([np.asarray(data_aux)])
                        prediction_proba = model.predict_proba([np.asarray(data_aux)])
                        confidence = max(prediction_proba[0])
                        predicted_character = labels_dict[int(prediction[0])]
                        emit('prediction', {'text': predicted_character, 'confidence': float(confidence)})
                    except Exception as e:
                        print("Prediction Error:", e)

    except Exception as e:
        print("Error processing image:", e)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    socketio.run(app, host='0.0.0.0', port=port, debug=False, allow_unsafe_werkzeug=True)
