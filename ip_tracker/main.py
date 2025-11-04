#!/usr/bin/env python3
import os
import sys
import argparse
import threading
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

def display_server_info(host, port):
    """Display server information"""
    local_ip = get_local_ip()
    
    print("📊 SERVER INFORMATION:")
    print(f"   🌐 Local URL:    http://127.0.0.1:{port}")
    print(f"   📱 Network URL:  http://{local_ip}:{port}")
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

def display_help():
    """Display help information"""
    print("🎯 QUICK COMMANDS:")
    print("   📱 Open in browser: termux-open-url http://127.0.0.1:5000")
    print("   📋 Copy network URL: termux-clipboard-set http://YOUR_IP:5000")
    print("   📊 View logs:        cat logs.txt")
    print("   🗑️  Clear logs:      rm logs.txt")
    print("   ⏹️  Stop server:     Ctrl+C")
    print()

def start_live_dashboard(host, port):
    """Start live dashboard in separate thread"""
    def dashboard_loop():
        import time
        while True:
            try:
                clear_screen()
                display_banner()
                display_server_info(host, port)
                display_real_time_stats()
                display_help()
                print("🔄 Live updating... (Ctrl+C to stop)")
                time.sleep(5)  # Update every 5 seconds
            except KeyboardInterrupt:
                break
            except:
                pass
    
    # Start dashboard in background thread
    dashboard_thread = threading.Thread(target=dashboard_loop, daemon=True)
    dashboard_thread.start()

def start_server(host='0.0.0.0', port=5000, debug=False):
    """Start the Flask server with Termux UI"""
    # Create log file if it doesn't exist
    if not os.path.exists('logs.txt'):
        with open('logs.txt', 'w', encoding='utf-8') as f:
            f.write(f"[{datetime.now().strftime('%Y-%m-%d %H:%M:%S')}] SYNERGY CLAIM TRACKER STARTED\n")
    
    clear_screen()
    display_banner()
    display_server_info(host, port)
    display_real_time_stats()
    display_help()
    
    # Start live dashboard
    start_live_dashboard(host, port)
    
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
    """Main entry point with enhanced UI"""
    parser = argparse.ArgumentParser(description='Facebook-style IP Tracker')
    parser.add_argument('--host', default='0.0.0.0', help='Host to bind to (default: 0.0.0.0)')
    parser.add_argument('--port', type=int, default=5000, help='Port to run on (default: 5000)')
    parser.add_argument('--debug', action='store_true', help='Enable debug mode')
    parser.add_argument('--simple', action='store_true', help='Simple mode without live dashboard')
    
    args = parser.parse_args()
    
    try:
        if args.simple:
            # Simple mode without dashboard
            print("🚀 Starting IP Tracker in simple mode...")
            app.run(host=args.host, port=args.port, debug=args.debug)
        else:
            # Full UI mode
            start_server(host=args.host, port=args.port, debug=args.debug)
    except KeyboardInterrupt:
        print("\n🛑 IP Tracker stopped")
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == '__main__':
    main()