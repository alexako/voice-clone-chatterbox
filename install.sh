#!/bin/bash

# Installer for the Voice Clone project

# Function to check if a command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# --- Dependency Checks ---
echo "🔎 Checking for dependencies..."

# Check for Python 3
if ! command_exists python3; then
    echo "❌ Error: Python 3 is not installed. Please install it to continue." >&2
    exit 1
fi

# Check for pip
if ! command_exists pip; then
    echo "❌ Error: pip is not installed. Please install it to continue." >&2
    exit 1
fi

# Check for sox
if ! command_exists sox; then
    echo "❌ Error: sox is not installed. Please install it to continue." >&2
    echo "   On Debian/Ubuntu: sudo apt-get install sox" >&2
    echo "   On Arch Linux: sudo pacman -S sox" >&2
    echo "   On macOS (Homebrew): brew install sox" >&2
    exit 1
fi

echo "✅ All dependencies are satisfied."

# --- Python Dependencies ---
echo "
🐍 Installing Python packages from requirements.txt..."

pip install -r requirements.txt
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to install Python packages." >&2
    exit 1
fi

echo "✅ Python packages installed successfully."

# --- Script Installation ---
echo "
🚀 Installing the 'alexsay' command..."

# Make alexsay executable
chmod +x alexsay
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to make 'alexsay' executable." >&2
    exit 1
fi

# Create symbolic link
INSTALL_PATH="/usr/local/bin/alexsay"
echo "🔑 This script needs sudo permissions to create a symbolic link at $INSTALL_PATH"

sudo ln -sf "$(pwd)/alexsay" "$INSTALL_PATH"
if [ $? -ne 0 ]; then
    echo "❌ Error: Failed to create symbolic link. Please try running the script with sudo." >&2
    exit 1
fi

echo "✅ 'alexsay' command installed successfully."

echo "
🎉 Installation complete! You can now use the 'alexsay' command from anywhere."
