FROM python:3.10

# Install necessary dependencies
RUN apt-get update && apt-get install -y \
    fonts-liberation libappindicator3-1 libasound2 libatk-bridge2.0-0 \
    libnspr4 libnss3 lsb-release xdg-utils libxss1 libdbus-glib-1-2 \
    curl unzip wget vim \
    xvfb libgbm1 libu2f-udev libvulkan1 \
    # Additional dependencies
    libx11-6 libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 \
    libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 \
    ca-certificates fonts-liberation libappindicator1 libnss3 libx11-6 \
    libx11-xcb1 libxcb1 libxcomposite1 libxcursor1 libxdamage1 \
    libxext6 libxfixes3 libxi6 libxrandr2 libxrender1 libxss1 libxtst6 \
    lsb-release xdg-utils

# Install Google Chrome
RUN wget -O google-chrome.deb "https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb" && \
    dpkg -i google-chrome.deb || apt-get install -fy && \
    rm google-chrome.deb

RUN which google-chrome

# Set environment variables
ENV LANG=C.UTF-8
ENV LC_ALL=C.UTF-8
ENV PYTHONUNBUFFERED=1
ENV PATH="$PATH:/bin:/usr/bin"

# Set work directory
WORKDIR /app

# Copy application code
COPY . /app

# Install Python dependencies
RUN --mount=type=cache,target=/root/.cache/pip \
    pip3 install --upgrade pip && \
    pip3 install -r requirements.txt

# Define the default command to run the application
CMD ["python3", "app.py"]
