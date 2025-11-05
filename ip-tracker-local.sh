#!/bin/bash
echo "🚀 Starting Local IP Tracker..."
echo "📡 Starting Python IP Tracker on port 5000..."

# Check if Python is available
if command -v python3 &> /dev/null; then
    # Run the Python script directly
    exec python3 -c "
from flask import Flask, request, jsonify
import datetime
import os

app = Flask(__name__)

@app.route('/')
def track_ip():
    client_ip = request.environ.get('HTTP_X_REAL_IP', request.remote_addr)
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print(f'📍 IP Accessed: {client_ip}')
    print(f'🕒 Time: {timestamp}')
    print('-' * 40)
    
    return f'<h1>IP Tracker</h1><p>Your IP: {client_ip}</p><p>Time: {timestamp}</p>'

if __name__ == '__main__':
    print('🚀 IP Tracker running on http://0.0.0.0:5000')
    print('📍 Access from other devices to see their IPs')
    print('⏹️  Press Ctrl+C to stop')
    app.run(host='0.0.0.0', port=8000, debug=False)
"
else
    echo "❌ Python3 is required but not installed."
    echo "💡 Install it with: sudo apt install python3 python3-pip"
fi
