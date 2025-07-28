#!/bin/bash

# Smart Gardening Dashboard - Installation Script
# This script sets up the development environment

set -e  # Exit on any error

echo "Smart Gardening Dashboard - Installation Script"
echo "=============================================="

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is required but not installed."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is required but not installed."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d ".venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .venv
fi

# Activate virtual environment
echo "Activating virtual environment..."
source .venv/bin/activate

# Upgrade pip
echo "Upgrading pip..."
pip install --upgrade pip

# Install dependencies based on argument
if [ "$1" = "dev" ]; then
    echo "Installing development dependencies..."
    pip install -r requirements-dev.txt
elif [ "$1" = "prod" ]; then
    echo "Installing production dependencies..."
    pip install -r requirements-prod.txt
else
    echo "Installing all dependencies..."
    pip install -r requirements.txt
fi

# Initialize database
echo "Initializing database..."
python smart_gardening/init_database.py

echo ""
echo "Installation completed successfully!"
echo ""
echo "To run the dashboard:"
echo "  source .venv/bin/activate"
echo "  streamlit run smart_gardening/dashboard/app.py"
echo ""
echo "To run tests:"
echo "  python tests/run_tests.py"
echo ""
echo "To deactivate virtual environment:"
echo "  deactivate" 