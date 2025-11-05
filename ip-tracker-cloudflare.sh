#!/bin/bash
echo "🌐 Starting IP Tracker for Cloudflare..."

# Function to check if command exists
command_exists() {
    command -v "$1" >/dev/null 2>&1
}

# Check if ip-tracker is available
if ! command_exists "ip-tracker"; then
    echo "📦 ip-tracker not found. Installing..."
    
    # Try to install
    if command_exists "npm"; then
        npm install -g ip-tracker
    else
        echo "❌ npm not found. Please install Node.js and npm first."
        exit 1
    fi
fi

# Run ip-tracker
ip-tracker --server cloudflare --port 5000
