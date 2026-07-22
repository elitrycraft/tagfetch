#!/bin/bash
set -e

echo "Detecting system architecture..."

ARCH=$(uname -m)
if [[ "$ARCH" == "x86_64" ]]; then
    BINARY="TagFetch_linux_x86_64"
    URL="https://github.com/elitrycraft/tagfetch/releases/download/1.0.3R/$BINARY"
elif [[ "$ARCH" == "aarch64" || "$ARCH" == "arm64" ]]; then
    BINARY="TagFetch_linux_arm64"
    URL="https://github.com/elitrycraft/tagfetch/releases/download/1.0.1R/$BINARY"
else
    echo "Unsupported architecture: $ARCH"
    exit 1
fi

echo "Detected: $ARCH"
echo "Installing TagFetch for Linux..."

if command -v wget &> /dev/null; then
    echo "Using wget for download..."
    sudo wget -q --show-progress -O "/usr/bin/tagfetch" "$URL"
elif command -v curl &> /dev/null; then
    echo "Using curl for download..."
    sudo curl -L --progress-bar -o "/usr/bin/tagfetch" "$URL"
else
    echo "Neither wget nor curl is installed. Please install one of them."
    exit 1
fi

sudo chmod +x /usr/bin/tagfetch

echo "TagFetch has been successfully installed to /usr/bin/tagfetch!"
