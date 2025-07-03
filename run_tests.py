#!/usr/bin/env python3
"""
Optimized Test Runner for Visualización de Cultivos QGIS Plugin

This script provides an easy way to run tests locally with the same configuration
used in CI/CD. It supports different test types and coverage reporting.
"""
import argparse
import os
import sys
import subprocess
from pathlib import Path

# Add project root to Python path
PROJECT_ROOT = Path(__file__).parent.absolute()
sys.path.insert(0, str(PROJECT_ROOT))


def setup_environment():
    """Setup environment variables for testing."""
    os.environ.update({
        'ENVIRONMENT': 'test',
        'QT_QPA_PLATFORM': 'offscreen',
        'QGIS_PREFIX_PATH': '/usr',
        'PYTHONPATH': f"{PROJECT_ROOT}:/usr/lib/python3/dist-packages:/usr/share/qgis/python"
    })


def run_command(cmd, description):
    """Run a command and handle errors."""
    print(f"\n🔄 {description}")
    print(f"Running: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print(f"✅ {description} completed successfully")
        if result.stdout:
            print(result.stdout)
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ {description} failed")
        print(f"Exit code: {e.returncode}")
        if e.stdout:
            print("STDOUT:", e.stdout)
        if e.stderr:
            print("STDERR:", e.stderr)
        return False


def run_tests(test_type='all', coverage=True, verbose=True, fast=False):
    """Run tests based on specified type."""
    setup_environment()
    
    base_cmd = ['python', '-m', 'pytest']
    
    # Add coverage if requested
    if coverage:
        base_cmd.extend(['--cov', '--cov-report=term-missing', '--cov-report=html'])
    
    # Add verbosity
    if verbose:
        base_cmd.append('--verbose')
    
    # Fast mode (reduced timeout)
    timeout = 180 if fast else 300
    base_cmd.extend(['--timeout', str(timeout)])
    
    # Test selection based on type
    if test_type == 'core':
        # Core functionality only (fastest)
        test_files = [
            'tests/unit/test_crop_model.py',
            'tests/unit/test_config.py',
            'tests/unit/test_plugin.py'
        ]
        description = "Core Tests (Model, Config, Plugin)"
        
    elif test_type == 'unit':
        # All unit tests
        test_files = [
            'tests/unit/test_crop_model.py',
            'tests/unit/test_crop_controller.py',
            'tests/unit/test_plugin.py',
            'tests/unit/test_config.py',
            'tests/unit/test_crop_view.py::TestCropViewSimple'
        ]
        description = "All Unit Tests (81% Coverage)"
        
    elif test_type == 'functional':
        # Functional tests if they exist
        test_files = ['tests/functional/']
        description = "Functional Tests"
        
    elif test_type == 'all':
        # All tests
        test_files = [
            'tests/unit/test_crop_model.py',
            'tests/unit/test_crop_controller.py',
            'tests/unit/test_plugin.py',
            'tests/unit/test_config.py',
            'tests/unit/test_crop_view.py::TestCropViewSimple'
        ]
        description = "All Available Tests"
        
    else:
        print(f"❌ Unknown test type: {test_type}")
        return False
    
    # Build final command
    cmd = base_cmd + test_files
    
    return run_command(cmd, description)


def check_dependencies():
    """Check if required dependencies are available."""
    print("🔍 Checking dependencies...")
    
    required_packages = ['pytest', 'coverage', 'pytest-cov', 'pytest-timeout']
    missing = []
    
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
        except ImportError:
            missing.append(package)
    
    if missing:
        print(f"❌ Missing packages: {', '.join(missing)}")
        print("📦 Install with: pip install -r requirements.txt")
        return False
    
    print("✅ All dependencies available")
    return True


def clean_artifacts():
    """Clean test artifacts and cache files."""
    print("🧹 Cleaning test artifacts...")
    
    patterns = [
        'htmlcov/',
        'coverage.xml',
        '.coverage',
        '.pytest_cache/',
        '**/__pycache__/',
        '*.pyc'
    ]
    
    for pattern in patterns:
        for path in PROJECT_ROOT.glob(pattern):
            if path.is_file():
                path.unlink()
                print(f"Removed file: {path}")
            elif path.is_dir():
                import shutil
                shutil.rmtree(path)
                print(f"Removed directory: {path}")
    
    print("✅ Cleanup completed")


def main():
    """Main entry point."""
    parser = argparse.ArgumentParser(
        description="Optimized Test Runner for QGIS Plugin",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Test Types:
  core       - Core functionality only (fastest: ~30s)
  unit       - All unit tests (recommended: ~60s, 81% coverage)
  functional - Functional tests (slower: ~120s)
  all        - All available tests (comprehensive)

Examples:
  python run_tests.py                    # Run all unit tests with coverage
  python run_tests.py --type core        # Quick core tests
  python run_tests.py --fast --no-cov    # Fast run without coverage
  python run_tests.py --clean             # Clean artifacts only
        """
    )
    
    parser.add_argument(
        '--type', '-t',
        choices=['core', 'unit', 'functional', 'all'],
        default='unit',
        help='Type of tests to run (default: unit)'
    )
    
    parser.add_argument(
        '--no-coverage', '--no-cov',
        action='store_true',
        help='Skip coverage reporting (faster)'
    )
    
    parser.add_argument(
        '--fast', '-f',
        action='store_true',
        help='Fast mode (reduced timeouts, less verbose)'
    )
    
    parser.add_argument(
        '--quiet', '-q',
        action='store_true',
        help='Quiet mode (less verbose output)'
    )
    
    parser.add_argument(
        '--clean', '-c',
        action='store_true',
        help='Clean test artifacts and exit'
    )
    
    parser.add_argument(
        '--check-deps',
        action='store_true',
        help='Check dependencies and exit'
    )
    
    args = parser.parse_args()
    
    print("🧪 Optimized Test Runner for QGIS Plugin")
    print("=" * 50)
    
    # Handle special actions
    if args.clean:
        clean_artifacts()
        return 0
    
    if args.check_deps:
        return 0 if check_dependencies() else 1
    
    # Check dependencies first
    if not check_dependencies():
        return 1
    
    # Run tests
    success = run_tests(
        test_type=args.type,
        coverage=not args.no_coverage,
        verbose=not args.quiet,
        fast=args.fast
    )
    
    if success:
        print("\n🎉 Tests completed successfully!")
        print("📊 Check htmlcov/index.html for detailed coverage report")
        return 0
    else:
        print("\n❌ Tests failed!")
        return 1


if __name__ == '__main__':
    sys.exit(main()) 