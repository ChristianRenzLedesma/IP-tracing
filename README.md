# IP Tracker Tool

Facebook-style IP tracker for Termux and Linux.

## Installation

### Termux
```bash
pkg install python git
git clone https://github.com/your-repo/ip-tracker.git
cd ip-tracker
chmod +x install.sh
./install.sh

## Linux

sudo apt update
sudo apt install python3 python3-pip git
git clone https://github.com/your-repo/ip-tracker.git
cd ip-tracker
chmod +x install.sh
./install.sh


### Usage

# Basic usage
ip-tracker

# Custom port
ip-tracker --port 8080

# Network access
ip-tracker --host 0.0.0.0 --port 8080

# Debug mode
ip-tracker --debug