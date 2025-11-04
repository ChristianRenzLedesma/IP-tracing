#!/bin/bash

echo "🔧 Installing IP Tracker for Termux/Linux..."

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed. Please install it first."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install it first."
    exit 1
fi

# Install required packages
echo "📦 Installing dependencies..."
pip3 install flask

# Install the package
echo "🚀 Installing IP Tracker..."
python3 setup.py install

echo ""
echo "✅ Installation complete!"
echo ""
echo "📖 Usage:"
echo "   ip-tracker                    # Start on default port 5000"
echo "   ip-tracker --port 8080        # Start on custom port"
echo "   ip-tracker --host 0.0.0.0     # Allow network access"
echo ""
echo "🌐 Then open: http://localhost:5000"
echo "📊 Logs will be saved to: logs.txt"
echo ""