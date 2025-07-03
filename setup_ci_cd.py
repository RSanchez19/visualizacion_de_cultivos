#!/usr/bin/env python3
"""
CI/CD Setup Script for Visualización de Cultivos QGIS Plugin

This script helps set up the complete CI/CD pipeline with testing and coverage.
It verifies dependencies, runs tests, and provides feedback on the setup.
"""

import os
import sys
import subprocess
import shutil
from pathlib import Path


def print_banner():
    """Print setup banner."""
    print("=" * 70)
    print("🚀 CI/CD Setup - Visualización de Cultivos QGIS Plugin")
    print("=" * 70)
    print("Setting up production-ready CI/CD pipeline with 60% coverage minimum")
    print()


def check_python_version():
    """Check Python version compatibility."""
    print("🐍 Checking Python version...")
    
    version = sys.version_info
    if version.major == 3 and version.minor >= 9:
        print(f"✅ Python {version.major}.{version.minor} is supported")
        return True
    else:
        print(f"❌ Python {version.major}.{version.minor} is not supported")
        print("   Minimum required: Python 3.9")
        return False


def install_dependencies():
    """Install development dependencies."""
    print("📦 Installing development dependencies...")
    
    try:
        # Check if requirements-dev.txt exists
        if not Path('requirements-dev.txt').exists():
            print("❌ requirements-dev.txt not found")
            return False
        
        # Install dependencies
        result = subprocess.run([
            sys.executable, '-m', 'pip', 'install', '-r', 'requirements-dev.txt'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Development dependencies installed successfully")
            return True
        else:
            print("❌ Failed to install dependencies")
            print(f"   Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error installing dependencies: {e}")
        return False


def run_test_suite():
    """Run the test suite to verify setup."""
    print("🧪 Running test suite...")
    
    try:
        # Run core tests first
        result = subprocess.run([
            sys.executable, 'run_tests.py', '--type', 'core', '--fast'
        ], capture_output=True, text=True)
        
        if result.returncode == 0:
            print("✅ Core tests passed")
            return True
        else:
            print("❌ Core tests failed")
            print(f"   Error: {result.stderr}")
            return False
            
    except Exception as e:
        print(f"❌ Error running tests: {e}")
        return False


def main():
    """Main setup function."""
    print_banner()
    
    # Step 1: Check prerequisites
    if not check_python_version():
        print("⚠️  Please upgrade Python to 3.9 or higher")
        sys.exit(1)
    
    # Step 2: Install dependencies
    print("\n" + "-" * 50)
    if not install_dependencies():
        print("⚠️  Dependency installation failed")
        print("   Try: pip install -r requirements-dev.txt")
    
    # Step 3: Run tests
    print("\n" + "-" * 50)
    if run_test_suite():
        print("🎉 Setup complete! Your CI/CD pipeline is ready.")
    else:
        print("⚠️  Setup completed with issues. Check the output above.")
    
    print("\n📚 Next Steps:")
    print("   make test           # Full tests with coverage")
    print("   make format         # Auto-format code")
    print("   open htmlcov/index.html  # View coverage report")
    print("   See CI_CD_SETUP.md for detailed guide")


if __name__ == '__main__':
    main() 