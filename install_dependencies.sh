#!/bin/bash
# Installation script for download_lyrics.py dependencies

echo "Installing Python dependencies for lyrics downloader..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed."
    echo "Please install Python 3 first:"
    echo "  Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "  Fedora: sudo dnf install python3 python3-pip"
    echo "  Arch: sudo pacman -S python python-pip"
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed."
    echo "Please install pip3 first:"
    echo "  Ubuntu/Debian: sudo apt install python3-pip"
    echo "  Fedora: sudo dnf install python3-pip"
    exit 1
fi

# Install required packages
echo "Installing mutagen (for MP3 metadata reading)..."
pip3 install mutagen

echo "Installing beautifulsoup4 (for web scraping)..."
pip3 install beautifulsoup4

echo "Installing requests (for HTTP requests)..."
pip3 install requests

echo ""
echo "✅ Installation complete!"
echo ""
echo "Usage:"
echo "  python3 download_lyrics.py /path/to/your/music/folder"
echo ""
echo "Options:"
echo "  --force    Download LRC files even if they already exist"
echo ""
echo "Example:"
echo "  python3 download_lyrics.py ~/Music"
echo "  python3 download_lyrics.py ~/Music --force"

