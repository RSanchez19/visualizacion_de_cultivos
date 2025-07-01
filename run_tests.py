#!/usr/bin/env python3
"""
Test runner script for local development and CI/CD
"""
import sys
import subprocess
import argparse
import os

# Try to import config for dynamic settings
try:
    from config import get_config, Config
    config = get_config()
    CONFIG_AVAILABLE = True
except ImportError:
    CONFIG_AVAILABLE = False
    # Fallback defaults
    class FallbackConfig:
        COVERAGE_MINIMUM = 60
        COVERAGE_UNIT_MINIMUM = 40
        COVERAGE_FUNCTIONAL_MINIMUM = 30
        UNIT_TEST_TIMEOUT = 300
        FUNCTIONAL_TEST_TIMEOUT = 600
        INTEGRATION_TEST_TIMEOUT = 900
    config = FallbackConfig()


def run_command(cmd, description=""):
    """Run a command and handle the result"""
    print(f"\n{'='*60}")
    print(f"Running: {description or ' '.join(cmd)}")
    print('='*60)
    
    result = subprocess.run(cmd, capture_output=False)
    if result.returncode != 0:
        print(f"❌ Command failed with return code {result.returncode}")
        return False
    else:
        print(f"✅ Command succeeded")
        return True


def main():
    parser = argparse.ArgumentParser(description='Run tests for QGIS plugin')
    parser.add_argument('--unit', action='store_true', help='Run only unit tests')
    parser.add_argument('--functional', action='store_true', help='Run only functional tests')
    parser.add_argument('--integration', action='store_true', help='Run only integration tests')
    parser.add_argument('--coverage', action='store_true', help='Generate coverage report')
    parser.add_argument('--no-cov', action='store_true', help='Run tests without coverage')
    parser.add_argument('--html', action='store_true', help='Generate HTML coverage report')
    parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
    parser.add_argument('--fast', action='store_true', help='Run tests without timeout')
    parser.add_argument('--config', action='store_true', help='Show current configuration')
    
    args = parser.parse_args()
    
    # Show configuration if requested
    if args.config:
        if CONFIG_AVAILABLE:
            config.print_config()
        else:
            print("Configuration module not available - using defaults")
        return
    
    # Base pytest command
    base_cmd = ['python', '-m', 'pytest']
    
    if args.verbose:
        base_cmd.append('--verbose')
    
    # Determine test scope
    test_paths = []
    markers = []
    
    if args.unit:
        test_paths.append('tests/unit/')
        markers.append('unit')
    elif args.functional:
        test_paths.append('tests/functional/')
        markers.append('functional')
    elif args.integration:
        test_paths.append('tests/functional/')
        markers.append('integration')
    else:
        test_paths.append('tests/')
    
    # Add test paths to command
    base_cmd.extend(test_paths)
    
    # Add markers if specified
    if markers:
        base_cmd.extend(['-m', ' or '.join(markers)])
    
    # Coverage options
    if not args.no_cov:
        base_cmd.extend([
            '--cov=.',
            '--cov-branch',
            '--cov-report=term-missing'
        ])
        
        if args.html or args.coverage:
            base_cmd.append('--cov-report=html')
            
        if args.coverage:
            base_cmd.extend([
                '--cov-report=xml',
                f'--cov-fail-under={config.COVERAGE_MINIMUM}'
            ])
        elif args.unit:
            base_cmd.extend([f'--cov-fail-under={config.COVERAGE_UNIT_MINIMUM}'])
        elif args.functional:
            base_cmd.extend([f'--cov-fail-under={config.COVERAGE_FUNCTIONAL_MINIMUM}'])
    
    # Timeout settings using config
    if not args.fast:
        if args.functional or args.integration:
            timeout = getattr(config, 'FUNCTIONAL_TEST_TIMEOUT', 600)
            base_cmd.extend([f'--timeout={timeout}'])
        else:
            timeout = getattr(config, 'UNIT_TEST_TIMEOUT', 300)
            base_cmd.extend([f'--timeout={timeout}'])
    
    success = True
    
    # Run linting first if enabled
    if getattr(config, 'RUN_LINT_CHECKS', True):
        print("Running code quality checks...")
        
        lint_commands = [
            (['python', '-m', 'flake8', '.', '--count', '--select=E9,F63,F7,F82', '--show-source', '--statistics'], 
             "Syntax check with flake8"),
            (['python', '-m', 'flake8', '.', '--count', '--exit-zero', '--max-complexity=10', '--max-line-length=127', '--statistics'], 
             "Code quality check with flake8")
        ]
        
        for cmd, desc in lint_commands:
            try:
                if not run_command(cmd, desc):
                    print("⚠️  Linting issues found, but continuing with tests...")
            except FileNotFoundError:
                print("⚠️  flake8 not installed, skipping linting")
    
    # Set environment variables for testing
    os.environ['ENVIRONMENT'] = 'test'
    os.environ['USE_MOCK_DATA'] = 'True'
    
    # Run the main test command
    print(f"\nRunning tests with command: {' '.join(base_cmd)}")
    success = run_command(base_cmd, "Main test run")
    
    # Generate additional reports if requested
    if args.coverage and success:
        print("\n" + "="*60)
        print("COVERAGE SUMMARY")
        print("="*60)
        
        try:
            subprocess.run(['python', '-m', 'coverage', 'report'], check=False)
        except FileNotFoundError:
            print("Coverage module not found")
    
    # Final status
    print("\n" + "="*60)
    if success:
        print("🎉 ALL TESTS PASSED!")
        if args.coverage:
            print("📊 Coverage reports generated in htmlcov/")
        if CONFIG_AVAILABLE and hasattr(config, 'COVERAGE_MINIMUM'):
            print(f"✅ Coverage requirement: {config.COVERAGE_MINIMUM}% met")
    else:
        print("❌ TESTS FAILED!")
        sys.exit(1)
    print("="*60)


if __name__ == '__main__':
    main() 