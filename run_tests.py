#!/usr/bin/env python3
"""
Test runner script for local development and CI/CD
"""
import sys
import subprocess
import argparse
import os


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
    
    args = parser.parse_args()
    
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
                '--cov-fail-under=60'
            ])
    
    # Timeout settings
    if not args.fast:
        if args.functional or args.integration:
            base_cmd.extend(['--timeout=600'])
        else:
            base_cmd.extend(['--timeout=300'])
    
    success = True
    
    # Run linting first
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
    else:
        print("❌ TESTS FAILED!")
        sys.exit(1)
    print("="*60)


if __name__ == '__main__':
    main() 