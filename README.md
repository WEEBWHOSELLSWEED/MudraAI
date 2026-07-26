# MudraAI
MudraAI is a bidirectional interpreter for Indian Sign Language. It uses MediaPipe + LSTM to translate ISL into text or speech, which is then translated back into a real-time 2D skeleton avatar. Developed using a specially selected ISL dataset.

## Requirements

- Python 3.11.9

## Installation

```bash
git clone ...
cd MudraAI

python -m venv .venv

# Windows
.venv\Scripts\activate

pip install -r requirements.txt
```

## Run Dataset Collector

```bash
python scripts/collect_dataset.py
```

## Run Training

```bash
python scripts/train_lstm.py
```
