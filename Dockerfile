FROM python:3.10-slim

# Install system dependencies required by OpenCV and MediaPipe Tasks API on Linux
RUN apt-get update && apt-get install -y --no-install-recommends \
    libegl1 \
    libgl1 \
    libgles2 \
    libglib2.0-0 \
    libgomp1 \
    libsm6 \
    libx11-6 \
    libxext6 \
    libxrender1 \
    libxcb1 \
    libxcb-render0 \
    libxcb-shape0 \
    libxcb-xfixes0 \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements and install Python dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application source code and models
COPY . .

# Expose default port
EXPOSE 5000

# Start MudraAI
CMD ["python", "app.py"]
