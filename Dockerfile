FROM python:3.12-slim

WORKDIR /app

# Install system dependencies for OpenCV (correct package names for Debian bookworm/bullseye)
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1 \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Default command – change to match your app's entry point
CMD ["python", "main.py"]