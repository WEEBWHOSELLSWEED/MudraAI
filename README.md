# MudraAI — Bidirectional Sign Language Interpretation Prototype

[![Python 3.9+](https://img.shields.io/badge/python-3.9%20%7C%203.10%20%7C%203.11%20%7C%203.12-blue.svg)](https://www.python.org/downloads/)
[![Flask](https://img.shields.io/badge/framework-Flask%203.x-green.svg)](https://flask.palletsprojects.com/)
[![MediaPipe](https://img.shields.io/badge/vision-Google%20MediaPipe-orange.svg)](https://developers.google.com/mediapipe)
[![Scikit-Learn](https://img.shields.io/badge/ML-Scikit--Learn-yellow.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **MudraAI** is a real-time bidirectional sign language translation and visualization dashboard. It translates live camera sign gestures into English text and synthesized speech, and converts typed English text into fluid, two-handed 2D skeletal sign language motion.

---

## 📌 Architecture & System Flow

```text
┌───────────────────────────────────────────────────────────────────────────┐
│                           FORWARD PIPELINE                                │
│                     (Camera Sign ──► English Speech)                      │
└───────────────────────────────────────────────────────────────────────────┘
   Live Webcam Stream
          │
          ▼
   MediaPipe Vision Tasks (HandLandmarker) ──► 21 Normalized 3D Coordinates
          │
          ▼
   Scikit-Learn MLP Classifier (improved_model.p)
          │
          ▼
   Temporal Sliding-Window Debouncer (5-frame mode filter)
          │
          ▼
   Sentence Builder ──► Web Speech Synthesis API (TTS)


┌───────────────────────────────────────────────────────────────────────────┐
│                           REVERSE PIPELINE                                │
│                      (Text ──► Skeletal Motion)                           │
└───────────────────────────────────────────────────────────────────────────┘
   English Input ("hey pls help me")
          │
          ▼
   Deterministic Normalizer & Greedy Longest-Phrase Matcher
          │
   ┌──────┴──────────────────────────────────────┐
   ▼                                             ▼
[Help / Dance / Book...]                  [Please / Sorry / A-Z...]
Temporal Sequence Available? (101 signs)   Static Baseline Fallback (32 signs)
   │                                             │
   ▼                                             ▼
Load JSON Sequence                            Load representatives.json
   │                                             │
   ▼                                             ▼
Sequence-Wide Bounding Box Normalization      Uniform Aspect-Ratio Scaling
   │                                             │
   ▼                                             ▼
Sub-Frame LERP (60/120 FPS requestAnimationFrame)  Static 2D Pose with 1.2s Hold
   │                                             │
   └──────────────────────┬──────────────────────┘
                          ▼
            HiDPI Canvas Skeleton Renderer
            (Blue = Left Hand, Green = Right Hand)
```

---

## ✨ Key Features

1. **Real-Time Camera Recognition (Sign ➔ Text)**
   - Uses Google MediaPipe Tasks API (`hand_landmarker.task`) running in image stream mode.
   - 42-dimensional geometric feature vector (21 landmarks relative to hand bounding box).
   - High-precision Multi-Layer Perceptron (MLP) neural classifier (`improved_model.p`) with Random Forest baseline fallback (`model.p`).
   - 5-frame temporal sliding-window voting debouncer prevents jitter and duplicate token emissions.
   - Interactive sentence builder with **Delete**, **Clear**, and **Speak (TTS)** capabilities.

2. **Liquid-Smooth 2D Skeletal Animation (Text ➔ Sign)**
   - **101 authentic temporal motion sequences** from the WLASL dataset with two-handed support.
   - **32 static baseline fallback poses** (`Please`, `Sorry`, `Thank You`, alphabet `A-Z`).
   - Continuous sub-frame Linear Interpolation (LERP) rendering at **60/120 FPS**.
   - Sequence-wide bounding box stabilization: hands never jump or resize abruptly between frames.
   - Full MediaPipe skeletal topology (distinct wrist, MCP, PIP, DIP connections).
   - Interactive playback controls: **Play**, **Pause**, **Replay**, and real-time **Frame Progress HUD**.

3. **High-DPI Responsive Dashboard**
   - Built with modern Bootstrap 5 and customized dark/light cards.
   - Native Retina / HiDPI canvas rendering (`window.devicePixelRatio`) with neon luminescence.
   - Searchable **Supported Vocabulary Modal** (133 concepts) with category filters.

4. **1-Click Local & Public Tunnel Launchers**
   - Pre-configured 1-click launchers for **Ngrok** and **Cloudflare Tunnel**.
   - Automatically grabs the public HTTPS link and copies it to your clipboard.

---

## 📊 Supported Vocabulary (133 Concepts)

- **101 Temporal ASL Sequences:** `Hello`, `Help`, `Yes`, `No`, `What`, `Who`, `Want`, `Need`, `Like`, `Time`, `Walk`, `Work`, `Wrong`, `Year`, `Book`, `Eat`, `Drink`, `Dance`, `Play`, `Fine`, `Finish`, `Give`, `Go`, `Hot`, `How`, `Mother`, `Family`, `Right`, `Table`, `Thanksgiving`, `Computer`, `Cook`, `Cool`, `Candy`, `Chair`, `Change`, `City`, `Clothes`, `Color`, `Cousin`, `Cow`, `Dark`, `Deaf`, `Decide`, `Doctor`, `Dog`, `Enjoy`, `Forget`, `Full`, `Graduate`, `Hat`, `Hearing`, `Jacket`, `Kiss`, `Language`, `Last`, `Later`, `Letter`, `Man`, `Many`, `Medicine`, `Meet`, `Now`, `Orange`, `Paint`, `Paper`, `Pink`, `Pizza`, `Pull`, `Purple`, `Same`, `School`, `Secretary`, `Shirt`, `Short`, `Son`, `Study`, `Tall`, `Tell`, `Thin`, `Thursday`, `White`, `Woman`, `Accident`, `Africa`, `All`, `Apple`, `Basketball`, `Bed`, `Before`, `Bird`, `Birthday`, `Black`, `Blue`, `Bowling`, `Brown`, `But`, `Can`, `Cheat`.
- **32 Static Baseline Poses:** `Please`, `Sorry`, `Thank You`, `Done`, `I Love you`, `You are welcome.`, and `A` through `Z`.

---

## 🚀 Quickstart & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/<your-username>/MudraAI.git
cd MudraAI
```

### 2. Create and Activate Virtual Environment (Recommended)
```bash
# Windows
python -m venv venv
.\venv\Scripts\activate

# macOS / Linux
python3 -m venv venv
source venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Run the Application
```bash
python app.py
```
Open **`http://127.0.0.1:5000`** in your browser (Google Chrome, Edge, or Firefox).

---

## ⚡ 1-Click Launchers (Windows)

- **Desktop Launcher:** Double-click `LAUNCH_MUDRAAI.bat`.
- **Cloudflare Tunnel:** Run `start_cloudflare_tunnel.bat` for an instant zero-signup HTTPS link.
- **Ngrok Tunnel:** Run `start_ngrok_tunnel.bat` for high-speed tunnel sharing.

---

## 🌐 24/7 Cloud Hosting (Without Keeping Your Laptop On)

You can host MudraAI online for free on **Render.com** or **Railway.app** so anyone can use it anytime:

### Deploying to Render.com (Free Tier)
1. Push this project to your GitHub account.
2. Sign up at [Render.com](https://render.com) and click **New + ➔ Web Service**.
3. Connect your GitHub repository.
4. Set the following fields:
   - **Environment:** `Python 3`
   - **Build Command:** `pip install -r requirements.txt`
   - **Start Command:** `python app.py`
5. Click **Create Web Service**. Render will assign you a live, free HTTPS URL (e.g. `https://mudraai.onrender.com`).

---

## 📁 Repository Structure

```text
MudraAI/
├── app.py                      # Main Flask application & Socket.IO prediction loop
├── wsgi.py                     # Production WSGI entry point
├── Procfile                    # Cloud platform deployment process file
├── requirements.txt            # Python dependencies
├── hand_landmarker.task        # MediaPipe Vision Task binary model
├── improved_model.p            # Trained MLP neural classifier
├── model.p                     # Baseline Random Forest classifier
├── static/
│   ├── vocabulary.json         # 133 concepts with aliases and phrases
│   ├── representatives.json    # Canonical 42D static poses
│   └── temporal/               # Pre-processed JSON sequences for fast browser rendering
├── templates/
│   └── index.html              # Modern responsive HTML5/Canvas dashboard
├── temporal_data/              # Discovered 101-class WLASL landmark repository
├── temporal_dataset_audit.md   # Dataset audit & validation report
└── LAUNCH_MUDRAAI.bat          # 1-Click launcher script
```

---

## 🔬 Dataset & Linguistic Transparency

- **Camera Dataset:** Trained on burst-captured single-hand static poses.
- **Temporal Sequences:** Derived from the verified WLASL-100 (American Sign Language) landmark dataset.
- **Academic Limitation:** While designed as a student prototype for Indian Sign Language (ISL), the underlying dynamic sequences originate from ASL sources. They are presented honestly as a technical gesture-animation prototype.

---

## 📄 License
This project is licensed under the MIT License — see the [LICENSE](LICENSE) file for details.
