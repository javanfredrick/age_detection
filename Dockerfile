
# Use a slim Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Install system dependencies for PIL/OpenCV
RUN apt-get update && apt-get install -y --no-install-recommends \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy model and code
COPY best_age_model.pth .
COPY app/ ./app/

# Expose the port Railway uses
EXPOSE 8080

# Command to run the API
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8080"]
