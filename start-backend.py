#!/usr/bin/env python3
"""
AutoShield Backend Startup Script
Starts the FastAPI backend server with proper configuration
"""

import os
import sys
import subprocess
import time
from pathlib import Path

# Add the backend directory to Python path
backend_dir = Path(__file__).parent / "backend"
sys.path.insert(0, str(backend_dir))

def install_dependencies():
    """Install required Python dependencies"""
    print("Installing Python dependencies...")
    
    # Create requirements.txt if it doesn't exist
    requirements_path = backend_dir / "requirements.txt"
    if not requirements_path.exists():
        requirements_content = """
fastapi==0.104.1
uvicorn[standard]==0.24.0
pydantic==2.5.0
pydantic-settings==2.1.0
sqlalchemy==2.0.23
asyncpg==0.29.0
aioredis==2.0.1
python-multipart==0.0.6
python-jose[cryptography]==3.3.0
passlib[bcrypt]==1.7.4
python-dotenv==1.0.0
web3==6.11.3
eth-account==0.9.0
cryptography==41.0.7
requests==2.31.0
""".strip()
        
        with open(requirements_path, "w") as f:
            f.write(requirements_content)
    
    # Install dependencies
    subprocess.run([sys.executable, "-m", "pip", "install", "-r", str(requirements_path)])

def create_missing_files():
    """Create missing __init__.py files"""
    init_files = [
        backend_dir / "app" / "__init__.py",
        backend_dir / "app" / "api" / "__init__.py",
        backend_dir / "app" / "api" / "v1" / "__init__.py",
        backend_dir / "app" / "api" / "v1" / "endpoints" / "__init__.py",
        backend_dir / "app" / "core" / "__init__.py",
        backend_dir / "app" / "services" / "__init__.py",
        backend_dir / "app" / "models" / "__init__.py",
        backend_dir / "app" / "schemas" / "__init__.py",
        backend_dir / "app" / "utils" / "__init__.py",
        backend_dir / "app" / "middleware" / "__init__.py",
    ]
    
    for init_file in init_files:
        init_file.parent.mkdir(parents=True, exist_ok=True)
        if not init_file.exists():
            init_file.write_text("")

def start_server():
    """Start the FastAPI server"""
    print("Starting AutoShield Backend Server...")
    print("=" * 50)
    
    # Change to backend directory
    os.chdir(backend_dir)
    
    # Start the server
    cmd = [
        sys.executable, "-m", "uvicorn",
        "app.main:app",
        "--host", "0.0.0.0",
        "--port", "8000",
        "--reload",
        "--reload-dir", "app"
    ]
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\nShutting down server...")
    except Exception as e:
        print(f"Error starting server: {e}")

def main():
    """Main function"""
    print("AutoShield Backend Startup")
    print("=" * 30)
    
    # Check if we're in the right directory
    if not backend_dir.exists():
        print("Error: Backend directory not found!")
        sys.exit(1)
    
    # Create missing files
    create_missing_files()
    
    # Install dependencies
    install_dependencies()
    
    # Start server
    start_server()

if __name__ == "__main__":
    main()
