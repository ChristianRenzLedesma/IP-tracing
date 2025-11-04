#!/bin/bash

echo ""
echo "╔═══════════════════════════════════════════╗"
echo "║           🚀 IP TRACKER INSTALL 🚀        ║
echo "║         With Server Selection            ║
echo "║        Local 🆚 Cloudflare Tunnels       ║
echo "╚═══════════════════════════════════════════╝"
echo ""

# Check if Termux
if [ -d "/data/data/com.termux" ]; then
    IS_TERMUX=true
    echo "📱 Termux environment detected"
else
    IS_TERMUX=false
    echo "💻 Linux environment detected"
fi

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3 is not installed."
    if [ "$IS_TERMUX" = true ]; then
        echo "📦 Installing Python for Termux..."
        pkg install python -y
    else
        echo "📦 Please install Python3: sudo apt install python3 python3-pip"
        exit 1
    fi
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed."
    if [ "$IS_TERMUX" = true ]; then
        echo "📦 Installing pip for Termux..."
        pkg install python-pip -y
    else
        echo "📦 Please install pip3: sudo apt install python3-pip"
        exit 1
    fi
fi

echo "✅ Python and pip are installed"

# Install required packages
echo ""
echo "📦 Installing dependencies..."
pip3 install flask requests

# Install the package
echo ""
echo "🚀 Installing IP Tracker..."
python3 setup.py install

# Install Cloudflared if requested
if [ "$1" = "--with-cloudflare" ]; then
    echo ""
    echo "🌐 Installing Cloudflared for tunnels..."
    if [ "$IS_TERMUX" = true ]; then
        pkg install cloudflared -y
    else
        wget -q https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64 -O /usr/local/bin/cloudflared
        chmod +x /usr/local/bin/cloudflared
    fi
    echo "✅ Cloudflared installed"
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "🎯 SERVER OPTIONS:"
echo "   ip-tracker --server local          # Local network only"
echo "   ip-tracker --server cloudflare     # Ready for Cloudflare tunnel"
echo ""
echo "📖 BASIC USAGE:"
echo "   ip-tracker                         # Local server with full UI"
echo "   ip-tracker --port 8080             # Custom port"
echo "   ip-tracker --simple                # Simple mode"
echo ""

if [ "$IS_TERMUX" = true ]; then
    echo "📱 TERMUX COMMANDS:"
    echo "   ip-tracker-local                # Quick local start"
    echo "   ip-tracker-cloudflare           # Quick cloudflare setup"
    echo "   termux-open-url http://127.0.0.1:5000"
    echo ""
fi

echo "🌐 Access URLs:"
echo "   Local:    http://127.0.0.1:5000"
echo "   Network:  http://$(hostname -I | awk '{print $1}'):5000"
echo ""
echo "📊 Logs saved to: logs.txt"
echo ""
