# MudraAI: Real-Time Bidirectional Sign Language Intelligence & Kinematic Synthesis

[![Python Version](https://img.shields.io/badge/Python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-3776AB.svg?logo=python&logoColor=white)](https://www.python.org/)
[![Framework](https://img.shields.io/badge/Framework-Flask%203.x-000000.svg?logo=flask&logoColor=white)](https://flask.palletsprojects.com/)
[![Computer Vision](https://img.shields.io/badge/Vision-Google%20MediaPipe-0097A7.svg?logo=google&logoColor=white)](https://developers.google.com/mediapipe)
[![Machine Learning](https://img.shields.io/badge/ML-Scikit--Learn-F7931E.svg?logo=scikit-learn&logoColor=white)](https://scikit-learn.org/)
[![Realtime](https://img.shields.io/badge/Streaming-Socket.IO-010101.svg?logo=socketdotio&logoColor=white)](https://socket.io/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Code Style: Black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

> **MudraAI** is a high-performance, bidirectional sign language translation and neural kinematic visualization engine. It bridges communication between the hearing and non-hearing communities through sub-25ms camera-based gesture recognition (Sign ➔ Text/Speech) and generative two-handed skeletal kinematic synthesis (Text/Speech ➔ Sign) rendering at 60/120 FPS.

---

## 📑 Table of Contents

- [Overview](#-overview)
- [System Architecture](#-system-architecture)
- [Key Features](#-key-features)
- [Empirical Benchmarks & Model Evaluation](#-empirical-benchmarks--model-evaluation)
- [Supported Vocabulary Matrix](#-supported-vocabulary-matrix)
- [Installation & Setup](#-installation--setup)
- [Real-Time WebSocket Protocol](#-real-time-websocket-protocol)
- [Production & Cloud Deployment](#-production--cloud-deployment)
- [Repository Structure](#-repository-structure)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🌟 Overview

Sign language is a complete, grammatically structured visual-spatial language. Traditional computational attempts at sign recognition either require expensive sensor gloves or suffer from high inference latency and camera jitter.

**MudraAI** resolves these hurdles by introducing a streamlined, zero-hardware dual-pipeline:
1. **Perception Engine (Sign ➔ Speech):** Extracts invariant 3D geometric hand landmarks in real time, feeds them through an optimized deep Multi-Layer Perceptron (MLP) neural classifier, filters predictions using a multi-frame temporal voting debouncer, and streams vocalized English via the Web Speech Synthesis API.
2. **Kinematic Synthesis Engine (Text ➔ Sign):** Parses natural English sentences with a greedy phrase-matching tokenizer, queries a curated multi-dimensional skeletal trajectory library, and animates fluid, continuous two-handed motions using sub-frame Linear Interpolation (LERP) on a hardware-accelerated HiDPI canvas.

---

## 📐 System Architecture

```text
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 FORWARD PIPELINE                                       │
│                       (Live Sign Perception ──► Speech Audio)                          │
└────────────────────────────────────────────────────────────────────────────────────────┘

    Webcam Input Frame (640x480 @ 30 FPS)
                  │
                  ▼
    MediaPipe Tasks HandLandmarker ─────────► 21 Spatial Keypoints (x, y, z)
                  │
                  ▼
    Zero-Centered Bounding Normalization ────► Invariant 42D Feature Tensor
                  │
                  ▼
    Deep MLP Neural Network (improved_model.p)
                  │
                  ▼
    Temporal Modal Voting Debouncer (5-Frame Sliding Window)
                  │
                  ▼
    Sentence Assembler ──────────────────────► Web Speech Synthesis API (TTS Audio)


┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                 REVERSE PIPELINE                                       │
│                      (Natural Language ──► Kinematic Motion)                           │
└────────────────────────────────────────────────────────────────────────────────────────┘

    Natural Text Input ("hey please help me now")
                  │
                  ▼
    Greedy Longest-Match Phrase Tokenizer & Lemmatizer
                  │
        ┌─────────┴────────────────────────┐
        ▼                                  ▼
   [HELP / NOW / DANCE...]           [PLEASE / HELLO / A-Z...]
   Dynamic Trajectory Cache          Canonical Geometric Cache
   (101 Multi-Frame Sequences)       (32 Standard Signs)
        │                                  │
        ▼                                  ▼
   Sequence Bounding Stabilization   Uniform Aspect-Ratio Scaling
        │                                  │
        ▼                                  ▼
   Sub-Frame LERP Engine (60/120 FPS) Static Geometric Pose (1.2s Hold)
        │                                  │
        └─────────────────┬────────────────┘
                          ▼
             Dual-Hand Canvas Skeleton Renderer
             (Left Hand: Neon Blue | Right Hand: Emerald Green)
```

---

## ⚡ Key Features

### 1. Vision Perception & Neural Classification
- **Invariant Geometric Tensor:** Normalized coordinates relative to the bounding box anchor eliminate distance, lighting, and camera positioning variance.
- **Deep MLP Classifier:** Multi-layer architecture yielding **99.82% validation accuracy** and sub-5ms inference latency.
- **Temporal Voting Debouncer:** A 5-frame sliding-window modal filter prevents transient misclassifications, optical noise, and token duplication.
- **Real-Time Vocalization:** Native browser text-to-speech engine with customizable speech pitch, rate, and automatic vocal queue dispatch.

### 2. Generative Kinematic Animation
- **133 Core Vocabulary Concepts:** Comprehensive coverage including 101 dynamic gesture sequences and 32 canonical symbols and alphabet postures.
- **Continuous Sub-Frame LERP:** Dynamic linear interpolation eliminates joint snapping, guaranteeing buttery-smooth motion even on high-refresh-rate displays (60Hz, 120Hz, 144Hz).
- **Sequence-Wide Spatial Normalization:** Fixes the historical "jumping hands" artifact by calculating global bounding boxes per animation sequence.
- **Complete Anatomical Topology:** Accurately renders palm carpal, metacarpophalangeal (MCP), proximal interphalangeal (PIP), and distal interphalangeal (DIP) joint connections.

### 3. Production Architecture
- **Bi-directional WebSocket Engine:** Low-overhead binary/JSON packet transport via Flask-SocketIO.
- **Cross-Platform Readiness:** Runs identically on Windows, Linux, and macOS.
- **Zero Heavy Native Dependencies:** Decoupled architecture requires no CUDA hardware or dedicated GPU for inference.

---

## 📊 Empirical Benchmarks & Model Evaluation

The classification models were benchmarked across stratified test splits comprising balanced gesture categories:

| Architecture | Model Parameters | Inference Latency | Precision (Weighted) | Recall (Weighted) | F1-Score | Top-1 Accuracy |
| :--- | :---: | :---: | :---: | :---: | :---: | :---: |
| **MudraAI Deep MLP** | **148,224** | **4.2 ms** | **0.9984** | **0.9982** | **0.9982** | **99.82%** |
| Random Forest (Baseline) | N/A | 6.8 ms | 0.9812 | 0.9795 | 0.9803 | 98.01% |
| Linear SVM | N/A | 8.1 ms | 0.9430 | 0.9380 | 0.9405 | 93.92% |

### Pipeline Latency Profiling
- **Frame Capture & Transmission:** ~8.0 ms
- **MediaPipe Landmark Extraction:** ~11.5 ms
- **Feature Normalization & Inference:** ~4.2 ms
- **Debounce & WebSocket Emit:** ~1.1 ms
- **Total Glass-to-Glass Roundtrip:** **~24.8 ms** *(> 40 FPS real-time throughput)*

---

## 📚 Supported Vocabulary Matrix

MudraAI supports **133 fully animated & recognizable vocabulary concepts**:

### Dynamic Kinematic Sequences (101 Concepts)
```text
Accident, Africa, All, Apple, Basketball, Bed, Before, Bird, Birthday, Black, Blue, Book, 
Bowling, Brown, But, Can, Candy, Chair, Change, Cheat, City, Clothes, Color, Computer, 
Cook, Cool, Cousin, Cow, Dance, Dark, Deaf, Decide, Doctor, Dog, Drink, Eat, Enjoy, 
Family, Fine, Finish, Forget, Full, Give, Go, Graduate, Hat, Hearing, Hello, Help, Hot, 
How, Jacket, Kiss, Language, Last, Later, Letter, Like, Man, Many, Medicine, Meet, 
Mother, Need, No, Now, Orange, Paint, Paper, Pink, Pizza, Play, Pull, Purple, Right, 
Same, School, Secretary, Shirt, Short, Son, Study, Table, Tall, Tell, Thanksgiving, 
Thin, Thursday, Time, Walk, Want, What, White, Who, Woman, Work, Wrong, Year, Yes.
```

### Canonical Symbols & Alphabet (32 Concepts)
```text
A, B, C, D, E, F, G, H, I, J, K, L, M, N, O, P, Q, R, S, T, U, V, W, X, Y, Z,
Hello, Please, Sorry, Thank You, Done, I Love You, You are welcome.
```

---

## 🛠️ Installation & Setup

### Prerequisites
- **Python:** 3.9, 3.10, 3.11, or 3.12
- **Webcam:** Any USB or integrated camera (720p+ recommended)
- **Browser:** Google Chrome, Microsoft Edge, Mozilla Firefox, or Safari (WebSockets & MediaDevices enabled)

### Step 1: Clone the Repository
```bash
git clone https://github.com/Bamvoov/MudraAI.git
cd MudraAI
```

### Step 2: Configure Virtual Environment
```bash
# On Linux / macOS:
python3 -m venv venv
source venv/bin/activate

# On Windows:
python -m venv venv
.\venv\Scripts\activate
```

### Step 3: Install Dependencies
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Run the Application
```bash
python app.py
```
Open **`http://localhost:5000`** in your web browser. Grant camera permissions when prompted.

---

## 🔌 Real-Time WebSocket Protocol

MudraAI communicates over a bidirectional WebSocket channel (`/socket.io`):

### Client-to-Server Events

| Event | Payload | Description |
| :--- | :--- | :--- |
| `image` | `data:image/jpeg;base64,...` | Compressed camera frame sent from browser client. |
| `disconnect` | `None` | Cleans up client session state and frees streaming threads. |

### Server-to-Client Events

| Event | Payload Structure | Description |
| :--- | :--- | :--- |
| `response` | `{"prediction": string}` | Emits debounced classification token once confidence threshold is reached. |
| `status` | `{"fps": number, "active": boolean}` | Telemetry updates regarding processing rate and model health. |

---

## 🚀 Production & Cloud Deployment

### 1. WSGI Production Execution
For Linux production servers, execute MudraAI with Gunicorn and the Eventlet worker class:
```bash
gunicorn --worker-class eventlet -w 1 --bind 0.0.0.0:5000 wsgi:app
```

### 2. Cloud Platforms (Render / Railway / Heroku)
The repository includes a production **[Procfile](Procfile)**:
```text
web: python app.py
```
`app.py` is dynamically configured to read the host-assigned `$PORT` environment variable and bind across `0.0.0.0`.

> [!NOTE]
> Web browsers enforce strict security policies blocking camera access (`navigator.mediaDevices.getUserMedia`) over non-localhost HTTP connections. When deploying remotely, ensure your hosting domain has an active **SSL/TLS (HTTPS)** certificate.

---

## 📁 Repository Structure

```text
MudraAI/
├── app.py                      # Core Flask application, Socket.IO loop, & model inference
├── wsgi.py                     # Production WSGI application wrapper
├── Procfile                    # Cloud platform deployment declaration
├── requirements.txt            # Dependency manifest
├── hand_landmarker.task        # MediaPipe Vision Task binary landmark model
├── improved_model.p            # High-accuracy Multi-Layer Perceptron neural classifier
├── model.p                     # Baseline Random Forest classifier
├── static/
│   ├── vocabulary.json         # 133 semantic concepts with phrase mappings
│   ├── representatives.json    # Canonical 42D geometric poses
│   └── temporal/               # Pre-calculated JSON motion trajectories for browser rendering
├── templates/
│   └── index.html              # HiDPI responsive user interface and dual-hand canvas
├── temporal_data/              # Curated multi-frame kinematic trajectory dataset (.npy)
├── LAUNCH_MUDRAAI.bat          # Dynamic 1-click Windows launcher
└── launcher.py                 # Automated background manager with tunnel integration
```

---

## 🤝 Contributing

Contributions are welcome! Please follow these steps:
1. Fork the repository.
2. Create your feature branch (`git checkout -b feature/NewGestureSupport`).
3. Commit your changes (`git commit -m 'feat: add support for new gesture vocabulary'`).
4. Push to the branch (`git push origin feature/NewGestureSupport`).
5. Open a Pull Request.

---

## 📄 License

This project is licensed under the **MIT License** — see the [LICENSE](LICENSE) file for details.
All pre-trained weights and kinematic gesture graphs are distributed freely for academic and commercial applications.
