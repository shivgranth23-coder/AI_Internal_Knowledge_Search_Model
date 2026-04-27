#!/usr/bin/env python3
"""
PDF Knowledge Search - System Launcher
Starts all components: Backend, Frontend, and opens browser
"""

import os
import sys
import subprocess
import time
import webbrowser
import platform
from pathlib import Path

def print_header():
    print("\n" + "="*60)
    print("  PDF Knowledge Search - System Launcher")
    print("="*60 + "\n")

def check_venv():
    """Check if virtual environment exists"""
    venv_path = Path("venv")
    if not venv_path.exists():
        print("ERROR: Virtual environment not found!")
        print("Please run: python -m venv venv")
        sys.exit(1)
    print("[OK] Virtual environment found")

def check_node_modules():
    """Check if npm dependencies are installed"""
    node_modules = Path("frontend/node_modules")
    if node_modules.exists():
        print("[OK] Frontend dependencies already installed")
        return True
    
    print("\n[!] Frontend dependencies NOT installed")
    print("    Installing npm packages (this takes 2-3 minutes)...\n")
    
    try:
        os.chdir("frontend")
        result = subprocess.run([sys.executable, "-m", "pip", "install", "-q", "npm"], 
                              capture_output=True, timeout=30)
        result = subprocess.run("npm install", shell=True, capture_output=False, timeout=300)
        os.chdir("..")
        
        if node_modules.exists():
            print("\n[OK] Frontend dependencies installed successfully!")
            return True
        else:
            print("\n[ERROR] Failed to install frontend dependencies")
            print("Try manually: cd frontend && npm install")
            return False
    except Exception as e:
        print(f"\n[ERROR] Failed to install: {e}")
        return False

def get_python_cmd():
    """Get the correct Python command for the venv"""
    if platform.system() == "Windows":
        return str(Path("venv/Scripts/python.exe"))
    else:
        return str(Path("venv/bin/python"))

def start_backend():
    """Start the FastAPI backend"""
    print("\n[1/3] Starting Backend (port 8000)...")
    python_cmd = get_python_cmd()
    
    if platform.system() == "Windows":
        subprocess.Popen(f'start "Backend" cmd /k "{python_cmd} backend/main.py"', shell=True)
    else:
        subprocess.Popen([python_cmd, "backend/main.py"])
    
    print("      Backend starting... waiting for it to be ready")
    time.sleep(5)
    print("      [OK] Backend window opened")

def start_frontend():
    """Start the React frontend"""
    print("\n[2/3] Starting Frontend (port 3000)...")
    
    if platform.system() == "Windows":
        subprocess.Popen('start "Frontend" cmd /k "cd frontend && npm start"', shell=True)
    else:
        os.chdir("frontend")
        subprocess.Popen(["npm", "start"])
        os.chdir("..")
    
    print("      Frontend starting...")
    time.sleep(3)
    print("      [OK] Frontend window opened")

def open_browser():
    """Open the React app in browser"""
    print("\n[3/3] Opening browser...")
    time.sleep(2)
    
    try:
        webbrowser.open("http://localhost:3000")
        print("      [OK] Browser opened to http://localhost:3000")
    except Exception as e:
        print(f"      [!] Could not open browser automatically: {e}")
        print("      Please open manually: http://localhost:3000")

def print_summary():
    """Print system information"""
    print("\n" + "="*60)
    print("  System Started Successfully!")
    print("="*60)
    print("\n  Frontend:  http://localhost:3000")
    print("  API Docs:  http://localhost:8000/docs")
    print("  Backend:   http://localhost:8000")
    print("  Ollama:    http://127.0.0.1:11434")
    print("\n  Note: Keep all terminal windows open")
    print("        To stop: Close windows or press Ctrl+C")
    print("\n" + "="*60 + "\n")

def main():
    """Main launcher function"""
    print_header()
    
    # Check prerequisites
    print("[*] Checking prerequisites...\n")
    check_venv()
    
    if not check_node_modules():
        print("\n[!] Warning: Frontend dependencies may not be fully installed")
        response = input("    Continue anyway? (y/n): ").lower()
        if response != 'y':
            sys.exit(1)
    
    # Start all components
    print("\n[*] Starting all components...\n")
    
    try:
        start_backend()
        start_frontend()
        open_browser()
        print_summary()
        
        print("[*] System is running!")
        print("[*] Press Ctrl+C to stop the launcher")
        print("    (Backend and Frontend will continue running)\n")
        
        # Keep the script running
        while True:
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\n\n[*] Launcher stopped (systems still running)")
        print("[*] Close the Backend and Frontend windows to stop them\n")
        sys.exit(0)
    except Exception as e:
        print(f"\n[ERROR] {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
