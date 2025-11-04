#!/bin/bash

echo ""
echo "╔═══════════════════════════════════════════╗"
echo "║           🚀 IP TRACKER INSTALL 🚀        ║"
echo "║         Facebook Style IP Logger          ║
echo "║              For Termux/Linux             ║
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
pip3 install flask

# Install the package
echo ""
echo "🚀 Installing IP Tracker..."
python3 setup.py install

# Create desktop entry for Linux (if not Termux)
if [ "$IS_TERMUX" = false ]; then
    echo ""
    echo "🖥️ Creating desktop entry..."
    cat > ~/.local/share/applications/ip-tracker.desktop << EOF
[Desktop Entry]
Version=1.0
Type=Application
Name=IP Tracker
Comment=Facebook-style IP Tracker
Exec=ip-tracker
Icon=network-wired
Terminal=true
Categories=Network;
EOF
fi

# Create termux shortcut script
if [ "$IS_TERMUX" = true ]; then
    echo ""
    echo "📱 Creating Termux shortcut..."
    cat > $PREFIX/bin/ip-tracker-start << 'EOF'
#!/bin/bash
cd ~/ip-tracker
ip-tracker
EOF
    chmod +x $PREFIX/bin/ip-tracker-start
    
    # Create termux-url-opener integration
    echo ""
    echo "🔗 Setting up URL opener..."
    cat > ~/bin/termux-url-opener << 'EOF'
#!/bin/bash
if [[ $1 == *"ip-tracker"* ]]; then
    echo "Opening IP Tracker..."
    ip-tracker-start
fi
EOF
    chmod +x ~/bin/termux-url-opener
fi

echo ""
echo "✅ Installation complete!"
echo ""
echo "📖 USAGE:"
echo "   ip-tracker                    # Start with full UI"
echo "   ip-tracker --port 8080        # Custom port"
echo "   ip-tracker --simple           # Simple mode"
echo "   ip-tracker --help             # Show help"
echo ""

if [ "$IS_TERMUX" = true ]; then
    echo "📱 TERMUX SPECIFIC:"
    echo "   termux-open-url http://127.0.0.1:5000    # Open in browser"
    echo "   termux-clipboard-set http://YOUR_IP:5000 # Copy URL"
    echo "   ip-tracker-start                         # Quick start"
    echo ""
fi

echo "🌐 Access URLs:"
echo "   Local:    http://127.0.0.1:5000"
echo "   Network:  http://$(hostname -I | awk '{print $1}'):5000"
echo ""
echo "📊 Logs saved to: logs.txt"
echo ""