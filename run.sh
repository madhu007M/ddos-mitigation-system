#!/bin/bash
# Run Script for DDoS Mitigation System

set -e

echo "🛡️  DDoS Mitigation System - Startup Script"
echo "=========================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✓ Python found: $(python3 --version)"

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo ""
    echo "Creating virtual environment..."
    python3 -m venv venv
    echo "✓ Virtual environment created"
fi

# Activate virtual environment
echo ""
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies if needed
if [ ! -f "venv/.dependencies_installed" ]; then
    echo ""
    echo "Installing dependencies..."
    pip install -q -r requirements.txt
    touch venv/.dependencies_installed
    echo "✓ Dependencies installed"
fi

echo ""
echo "=========================================="
echo "Select an option:"
echo "1. Run Example Usage"
echo "2. Start Dashboard (Web Interface)"
echo "3. Run Attack Simulator"
echo "4. Run Tests"
echo "5. Exit"
echo "=========================================="
read -p "Enter choice [1-5]: " choice

case $choice in
    1)
        echo ""
        echo "Running example usage..."
        python example_usage.py
        ;;
    2)
        echo ""
        echo "Starting dashboard on http://localhost:5000"
        echo "Press Ctrl+C to stop"
        python src/dashboard/app.py
        ;;
    3)
        echo ""
        echo "Starting attack simulator..."
        python simulate_attack.py
        ;;
    4)
        echo ""
        echo "Running tests..."
        python -m unittest discover tests -v
        ;;
    5)
        echo "Goodbye!"
        exit 0
        ;;
    *)
        echo "Invalid choice"
        exit 1
        ;;
esac
