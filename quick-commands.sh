#!/bin/bash

case $1 in
    "start")
        ip-tracker
        ;;
    "stop")
        pkill -f "ip-tracker"
        echo "🛑 IP Tracker stopped"
        ;;
    "logs")
        cat logs.txt
        ;;
    "status")
        if pgrep -f "ip-tracker" > /dev/null; then
            echo "✅ IP Tracker is running"
        else
            echo "❌ IP Tracker is stopped"
        fi
        ;;
    "open")
        termux-open-url http://127.0.0.1:5000
        ;;
    "share")
        IP=$(hostname -I | awk '{print $1}')
        termux-clipboard-set "http://$IP:5000"
        echo "🔗 Network URL copied to clipboard: http://$IP:5000"
        ;;
    *)
        echo "📱 IP Tracker Quick Commands:"
        echo "   ./quick-commands.sh start    # Start tracker"
        echo "   ./quick-commands.sh stop     # Stop tracker"
        echo "   ./quick-commands.sh logs     # View logs"
        echo "   ./quick-commands.sh status   # Check status"
        echo "   ./quick-commands.sh open     # Open in browser"
        echo "   ./quick-commands.sh share    # Copy network URL"
        ;;
esac