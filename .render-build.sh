#!/usr/bin/env bash
set -x

# Install dependencies
apt-get update
apt-get install -y wget gnupg unzip xvfb libxi6 libgconf-2-4

# Install Google Chrome
wget -q -O - https://dl.google.com/linux/linux_signing_key.pub | apt-key add -
sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
apt-get update
apt-get install -y google-chrome-stable

# Install Chromedriver
CHROME_DRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`
wget -N http://chromedriver.storage.googleapis.com/$CHROME_DRIVER_VERSION/chromedriver_linux64.zip -P /tmp/
unzip /tmp/chromedriver_linux64.zip -d /usr/local/bin/
rm /tmp/chromedriver_linux64.zip
chmod +x /usr/local/bin/chromedriver

# Install Python dependencies
pip install -r requirements.txt
