#!/bin/bash

# Detect package manager and install espeak/espeak-ng
if command -v apt &> /dev/null; then
    echo "Detected Debian/Ubuntu. Installing espeak..."
    sudo apt update
    sudo apt install -y espeak
elif command -v dnf &> /dev/null; then
    echo "Detected Fedora. Installing espeak-ng..."
    sudo dnf install -y espeak-ng
elif command -v yum &> /dev/null; then
    echo "Detected RHEL/CentOS. Installing espeak-ng..."
    sudo yum install -y espeak-ng
elif command -v pacman &> /dev/null; then
    echo "Detected Arch Linux. Installing espeak-ng..."
    sudo pacman -Sy --noconfirm espeak-ng
elif command -v zypper &> /dev/null; then
    echo "Detected openSUSE. Installing espeak-ng..."
    sudo zypper install -y espeak-ng
else
    echo "Unsupported Linux distribution. Please install espeak manually."
    exit 1
fi

echo "✅ eSpeak installation complete!"
pip3 install -r requirements.txt
python3 main.py
