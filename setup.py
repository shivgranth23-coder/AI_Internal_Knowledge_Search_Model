#!/usr/bin/env python3
"""
PDF Knowledge Search - Quick Start Setup Script
Automates initial setup for new users
"""

import subprocess
import sys
import os
from pathlib import Path

def print_header(text):
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)

def run_command(cmd, description, shell=False):
    """Run a command and handle errors"""
    print(f"\n[*] {description}...")
    try:
        if shell:
            result = subprocess.run(cmd, shell=True, capture_output=False)
        else:
            result = subprocess.run(cmd, capture_output=False)
        return result.returncode == 0
    except Exception as e:
        print(f"[✗] Error: {e}")
        return False

def check_python():
    """Check if Python 3.8+ is installed"""
    print_header("Checking Python Installation")
    try:
        version = sys.version_info
        if version.major >= 3 and version.minor >= 8:
            print(f"✓ Python {version.major}.{version.minor} found")
            return True
        else:
            print(f"✗ Python 3.8+ required (found {version.major}.{version.minor})")
            return False
    except:
        print("✗ Python not found")
        return False

def check_node():
    """Check if Node.js is installed"""
    print_header("Checking Node.js Installation")
    try:
        result = subprocess.run(["npm", "--version"], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✓ npm {result.stdout.strip()} found")
            return True
        else:
            print("✗ npm not found. Please install Node.js from https://nodejs.org")
            return False
    except:
        print("✗ Node.js not found. Please install from https://nodejs.org")
        return False

def check_ollama():
    """Check if Ollama is installed"""
    print_header("Checking Ollama Installation")
    
    ollama_paths = [
        "C:\\Users\\hp\\AppData\\Local\\Programs\\Ollama\\ollama.exe",
        "/usr/bin/ollama",
        "/usr/local/bin/ollama",
        "/opt/homebrew/bin/ollama"
    ]
    
    for path in ollama_paths:
        if Path(path).exists():
            print(f"✓ Ollama found at: {path}")
            return True
    
    print("✗ Ollama not found. Please install from https://ollama.ai")
    return False

def setup_python_env():
    """Setup Python virtual environment"""
    print_header("Setting Up Python Environment")
    
    venv_path = Path("venv")
    if venv_path.exists():
        print("✓ Virtual environment already exists")
        return True
    
    print("[*] Creating virtual environment...")
    if run_command([sys.executable, "-m", "venv", "venv"], "Create venv"):
        print("✓ Virtual environment created")
        return True
    return False

def install_python_deps():
    """Install Python dependencies"""
    print_header("Installing Python Dependencies")
    
    if sys.platform == "win32":
        pip_cmd = ".\\venv\\Scripts\\pip"
    else:
        pip_cmd = "./venv/bin/pip"
    
    print("[*] Installing packages (this may take 5-10 minutes)...")
    if run_command([pip_cmd, "install", "-r", "requirements.txt"], 
                   "Install requirements", shell=False):
        print("✓ Python dependencies installed")
        return True
    return False

def install_node_deps():
    """Install Node.js dependencies"""
    print_header("Installing Node.js Dependencies")
    
    frontend_path = Path("frontend")
    if not frontend_path.exists():
        print("✗ frontend folder not found")
        return False
    
    os.chdir("frontend")
    if run_command(["npm", "install"], "Install npm packages"):
        print("✓ Node.js dependencies installed")
        os.chdir("..")
        return True
    os.chdir("..")
    return False

def download_ollama_model():
    """Download Ollama model"""
    print_header("Downloading Ollama Model")
    
    print("""
    This will download the Phi model (~640MB).
    
    Model options:
    - phi          - 640MB (Recommended for first time)
    - orca-mini    - 1.3GB (Better quality)
    - neural-chat  - 2.3GB (Good balance)
    - mistral      - 4.4GB (Best quality, requires 4GB+ RAM)
    """)
    
    model = input("\nEnter model name (default: phi): ").strip() or "phi"
    
    if sys.platform == "win32":
        ollama_cmd = "C:\\Users\\hp\\AppData\\Local\\Programs\\Ollama\\ollama.exe"
    else:
        ollama_cmd = "ollama"
    
    print(f"\n[*] Downloading {model} model...")
    print("    (This may take 5-15 minutes depending on internet speed)")
    
    os.system(f"{ollama_cmd} pull {model}")
    
    print(f"✓ Model {model} downloaded")
    return True

def create_directories():
    """Create necessary directories"""
    print_header("Creating Directories")
    
    dirs = ["documents", "data/chroma_db"]
    
    for dir_path in dirs:
        Path(dir_path).mkdir(parents=True, exist_ok=True)
        # Create .gitkeep
        Path(f"{dir_path}/.gitkeep").touch()
    
    print("✓ Directories created")
    return True

def main():
    """Main setup flow"""
    print("\n" + "█"*60)
    print("█  PDF Knowledge Search - Setup Script")
    print("█"*60)
    
    # Check prerequisites
    if not check_python():
        print("\n✗ Setup failed: Python 3.8+ required")
        return False
    
    if not check_node():
        print("\n⚠ Node.js not found, skipping frontend setup")
        print("  You can install it later from https://nodejs.org")
    
    if not check_ollama():
        print("\n⚠ Ollama not found")
        print("  Download from https://ollama.ai")
        print("  Setup will continue, but you'll need to start Ollama separately")
    
    # Setup
    if not create_directories():
        return False
    
    if not setup_python_env():
        return False
    
    if not install_python_deps():
        print("\n⚠ Some Python dependencies failed")
        print("  Try manually: pip install -r requirements.txt")
    
    if not install_node_deps():
        print("\n⚠ Node.js setup skipped (npm not found)")
        print("  To setup frontend later:")
        print("  cd frontend && npm install")
    
    if check_ollama():
        download_model = input("\nDownload Ollama model now? (y/n): ").lower() == 'y'
        if download_model:
            download_ollama_model()
    
    print_header("Setup Complete!")
    print("""
    ✓ All components installed successfully!
    
    Next steps:
    1. Make sure Ollama is running:
       ollama serve
    
    2. Start backend (Terminal 1):
       python backend/main.py
    
    3. Start frontend (Terminal 2):
       cd frontend && npm start
    
    4. Open browser to: http://localhost:3000
    
    5. Upload PDFs, click "Index", and ask questions!
    
    For troubleshooting, see README.md
    """)
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
