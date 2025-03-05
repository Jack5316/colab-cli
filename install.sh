#!/bin/bash

# Exit on error
set -e

# Check if pip is available
if ! command -v pip &> /dev/null; then
    echo "Error: pip is not installed. Please install pip first."
    exit 1
fi

# Install the package
pip install -e .

# Make sure the script is executable
chmod +x colab_cli.py

echo "Installation complete! You can now use the 'colab-cli' command."
echo "Try 'colab-cli --help' to get started."