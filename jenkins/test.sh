#!/bin/bash

# Install apt dependencies
sudo apt-get update
sudo apt-get install -y python3-pip python3-venv unzip chromium-browser

# Install chromedriver
rm -rf /home/jenkins/chromedriver
mkdir /home/jenkins/chromedriver
wget -P /home/jenkins/chromedriver https://chromedriver.storage.googleapis.com/2.41/chromedriver_linux64.zip
unzip /home/jenkins/chromedriver/chromedriver_linux64.zip -d /home/jenkins/chromedriver

# Create/activate Python virtual environment
python3 -m venv venv
source venv/bin/activate

# Install pip requirements
pip3 install -r requirements.txt
pip3 install pytest pytest-cov

# Run pytest
pytest --cov=application --cov-report xml --cov-report term-missing --junitxml junit.xml
