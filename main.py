#!/usr/bin/env python3
"""
Main entry point for Binance Trading Bots
Choose which bot to run: Flask web interface, Enhanced CLI, or Basic CLI
"""

import sys
import subprocess
from config import FLASK_HOST, FLASK_PORT

def show_menu():
    print("\n=== Binance Trading Bot Launcher ===")
    print("1. Flask Web Interface (Recommended)")
    print("2. Enhanced CLI Bot")
    print("3. Basic CLI Bot")
    print("4. Exit")
    print("=" * 35)

def run_flask_bot():
    print(f"\nStarting Flask web interface...")
    print(f"Web interface will be available at: http://{FLASK_HOST}:{FLASK_PORT}")
    print("Press Ctrl+C to stop the server")
    try:
        subprocess.run([sys.executable, "flask_trading_bot.py"])
    except KeyboardInterrupt:
        print("\nFlask server stopped.")

def run_enhanced_bot():
    print("\nStarting Enhanced CLI Bot...")
    try:
        subprocess.run([sys.executable, "enhanced_trading_bot.py"])
    except KeyboardInterrupt:
        print("\nEnhanced bot stopped.")

def run_basic_bot():
    print("\nStarting Basic CLI Bot...")
    try:
        subprocess.run([sys.executable, "bot.py"])
    except KeyboardInterrupt:
        print("\nBasic bot stopped.")

def main():
    while True:
        show_menu()
        choice = input("Select an option (1-4): ").strip()
        
        if choice == '1':
            run_flask_bot()
        elif choice == '2':
            run_enhanced_bot()
        elif choice == '3':
            run_basic_bot()
        elif choice == '4':
            print("Goodbye!")
            break
        else:
            print("Invalid option. Please select 1-4.")

if __name__ == "__main__":
    main() 