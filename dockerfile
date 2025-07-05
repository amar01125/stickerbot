# Base image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt update && \
    apt install -y ffmpeg && \
    rm -rf /var/lib/apt/lists/*

# Copy code and install Python deps
COPY . .
RUN pip install --no-cache-dir -r requirements.txt

# Expose port
EXPOSE 8080

# Run app
CMD ["python", "main.py"]
