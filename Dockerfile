# Use official Python image
FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    wget gnupg curl unzip fonts-liberation libnss3 libatk-bridge2.0-0 libxss1 \
    libasound2 libgtk-3-0 libx11-xcb1 libxcb-dri3-0 libdrm2 libxcomposite1 \
    libxrandr2 libgbm1 libxdamage1 libpango-1.0-0 libpangocairo-1.0-0 \
    libatspi2.0-0 libxinerama1 libxext6 libxfixes3 libxi6 libgl1 \
    && rm -rf /var/lib/apt/lists/*

# Install Playwright and Python bindings
RUN pip install playwright && playwright install chromium

# Copy requirements.txt from root
COPY requirements.txt /app
# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY app/ /app

# Expose port
EXPOSE 5000

# Run the Flask app
CMD ["python", "main.py"]
