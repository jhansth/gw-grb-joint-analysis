#!/bin/bash
# WSL2 Setup Script for gw-grb-joint-analysis

echo "===== GW-GRB Joint Analysis - WSL2 Setup ====="
echo ""

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Update system packages
echo "Updating system packages..."
sudo apt-get update
sudo apt-get upgrade -y

# Install Python dev tools
echo "Installing Python development tools..."
sudo apt-get install -y python3 python3-venv python3-dev build-essential

# Create virtual environment
VENV_PATH="$HOME/venv_linux"
if [ ! -d "$VENV_PATH" ]; then
  echo "Creating Python virtual environment at $VENV_PATH..."
  python3 -m venv "$VENV_PATH"
else
  echo "Using existing virtual environment at $VENV_PATH..."
fi

# Activate virtual environment
echo "Activating virtual environment..."
source "$VENV_PATH/bin/activate"

# Install pip upgrade
echo "Upgrading pip..."
pip install --upgrade pip

# Install requirements
echo "Installing project dependencies..."
pip install -r "$ROOT_DIR/requirements.txt"

echo ""
echo "===== Setup Complete ====="
echo ""
echo "To activate the environment in future sessions, run:"
echo "  source ~/venv_linux/bin/activate"
echo ""
echo "To deactivate, run:"
echo "  deactivate"
