#!/bin/bash
echo "🌐 Starting IP Tracker for Cloudflare..."
echo "📡 Starting Cloudflare-aware IP Tracker on port 5000..."

if command -v python3 &> /dev/null; then
    exec python3 -c "
from flask import Flask, request, jsonify
import datetime

app = Flask(__name__)

@app.route('/')
def track_ip():
    # Cloudflare specific headers
    cf_headers = {
        'CF-Connecting-IP': request.headers.get('CF-Connecting-IP'),
        'X-Forwarded-For': request.headers.get('X-Forwarded-For'),
        'X-Real-IP': request.headers.get('X-Real-IP')
    }
    
    real_ip = cf_headers['CF-Connecting-IP'] or request.remote_addr
    timestamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    print('🌐 CLOUDFLARE IP DETECTED:')
    print(f'📍 Real IP: {real_ip}')
    print(f'🛡️  CF-Connecting-IP: {cf_headers[\"CF-Connecting-IP\"]}')
    print(f'🔀 X-Forwarded-For: {cf_headers[\"X-Forwarded-For\"]}')
    print(f'🕒 Time: {timestamp}')
    print('-' * 40)
    
    return f'''
    <h1>🌐 Cloudflare IP Tracker</h1>
    <p><strong>Your Real IP:</strong> {real_ip}</p>
    <p><strong>CF-Connecting-IP:</strong> {cf_headers['CF-Connecting-IP']}</p>
    <p><strong>X-Forwarded-For:</strong> {cf_headers['X-Forwarded-For']}</p>
    <p><strong>Time:</strong> {timestamp}</p>
    <hr>
    <p><a href=\"/cloudflare-headers\">View All Headers</a></p>
    '''

@app.route('/cloudflare-headers')
def show_headers():
    return jsonify(dict(request.headers))

if __name__ == '__main__':
    print('🌐 Cloudflare IP Tracker running on http://0.0.0.0:5000')
    print('🛡️  Designed to detect real IPs behind Cloudflare proxy')
    print('📍 Access from browser or curl to test')
    app.run(host='0.0.0.0', port=8000, debug=False)
"
else
    echo "❌ Python3 is required. Install with: sudo apt install python3 python3-pip"
fi
