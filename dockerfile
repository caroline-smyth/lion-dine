# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Install necessary dependencies and Chromium
RUN apt-get update && apt-get install -y \
    chromium \
    wget \
    --no-install-recommends \
    && rm -rf /var/lib/apt/lists/*

# Set environment variables for Chromium
ENV CHROME_BIN=/usr/bin/chromium
ENV PATH=$PATH:/usr/bin/chromium

# Install ChromeDriver
RUN CHROME_DRIVER_VERSION=$(wget -qO- https://chromedriver.storage.googleapis.com/LATEST_RELEASE) && \
    wget -O /tmp/chromedriver.zip https://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip && \
    unzip /tmp/chromedriver.zip -d /usr/local/bin/ && \
    rm /tmp/chromedriver.zip && \
    chmod +x /usr/local/bin/chromedriver

# Set work directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Expose port (if applicable)
EXPOSE 5000

# Command to run the application
CMD ["python", "app.py"]
