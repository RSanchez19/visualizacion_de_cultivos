#!/usr/bin/env python3
"""
Complete verification script for visualizacion_de_cultivos plugin

This script runs all necessary checks to ensure the plugin and tests
work correctly both locally and in CI environments.
"""
import os
import sys
import subprocess
import time
from pathlib import Path
from typing import List, Tuple, Dict


class Colors:
    """ANSI color codes for terminal output"""
    GREEN = '\033[92m'
    RED = '\033[91m'
    YELLOW = '\033[93m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    BOLD = '\033[1m'
    END = '\033[0m'


class VerificationRunner:
    """Main verification runner class"""
    
    def __init__(self):
        self.project_root = Path(__file__).parent
        self.results = []
        self.start_time = time.time()
        
    def print_header(self, title: str, emoji: str = "🔍") -> None:
        """Print a formatted header"""
        print(f"\n{Colors.CYAN}{Colors.BOLD}")
        print("=" * 70)
        print(f"{emoji} {title}")
        print("=" * 70)
        print(f"{Colors.END}")
        
    def print_step(self, step: str, emoji: str = "🔄") -> None:
        """Print a step description"""
        print(f"\n{Colors.BLUE}{emoji} {step}...{Colors.END}")
        
    def print_success(self, message: str) -> None:
        """Print success message"""
        print(f"{Colors.GREEN}✅ {message}{Colors.END}")
        
    def print_error(self, message: str) -> None:
        """Print error message"""
        print(f"{Colors.RED}❌ {message}{Colors.END}")
        
    def print_warning(self, message: str) -> None:
        """Print warning message"""
        print(f"{Colors.YELLOW}⚠️  {message}{Colors.END}")
        
    def run_command(self, cmd: List[str], description: str, critical: bool = True) -> Tuple[bool, str]:
        """Run a command and return success status and output"""
        try:
            result = subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                cwd=self.project_root,
                timeout=300  # 5 minute timeout
            )
            
            success = result.returncode == 0
            output = result.stdout + result.stderr
            
            if success:
                self.print_success(f"{description} - PASSED")
                self.results.append((description, True, ""))
            else:
                if critical:
                    self.print_error(f"{description} - FAILED")
                else:
                    self.print_warning(f"{description} - FAILED (non-critical)")
                self.results.append((description, False, output))
                
            return success, output
            
        except subprocess.TimeoutExpired:
            self.print_error(f"{description} - TIMEOUT")
            self.results.append((description, False, "Timeout"))
            return False, "Timeout"
        except Exception as e:
            self.print_error(f"{description} - ERROR: {e}")
            self.results.append((description, False, str(e)))
            return False, str(e)
    
    def check_environment(self) -> bool:
        """Check if the environment is properly set up"""
        self.print_header("Environment Check", "🌍")
        
        # Check Python version
        python_version = sys.version_info
        if python_version.major == 3 and python_version.minor >= 8:
            self.print_success(f"Python {python_version.major}.{python_version.minor}.{python_version.micro}")
        else:
            self.print_error(f"Python {python_version.major}.{python_version.minor} (requires 3.8+)")
            return False
            
        # Check if we're in the right directory
        if not (self.project_root / "config.py").exists():
            self.print_error("Not in the correct project directory")
            return False
        else:
            self.print_success("Project directory structure")
            
        # Check if tests directory exists
        if not (self.project_root / "tests").exists():
            self.print_error("Tests directory not found")
            return False
        else:
            self.print_success("Tests directory found")
            
        return True
    
    def install_dependencies(self) -> bool:
        """Install required dependencies"""
        self.print_header("Dependencies Installation", "📦")
        
        # Install pytest and related packages
        pytest_packages = [
            "pytest", "pytest-cov", "pytest-mock", "pytest-timeout", 
            "coverage", "black", "isort", "flake8"
        ]
        
        for package in pytest_packages:
            success, _ = self.run_command(
                [sys.executable, "-m", "pip", "install", "--user", package],
                f"Installing {package}",
                critical=False
            )
            
        # Try to install project requirements
        if (self.project_root / "requirements.txt").exists():
            success, _ = self.run_command(
                [sys.executable, "-m", "pip", "install", "--user", "-r", "requirements.txt"],
                "Installing project requirements",
                critical=False
            )
            
        return True
    
    def test_mocking_system(self) -> bool:
        """Test the intelligent mocking system"""
        self.print_header("Mocking System Test", "🎭")
        
        # Test import of mocking system
        test_code = '''
import sys
import os
sys.path.insert(0, ".")

# Set CI environment to test mocking
os.environ["CI"] = "true"
os.environ["GITHUB_ACTIONS"] = "true"
os.environ["ENVIRONMENT"] = "test"

try:
    from tests import is_ci_environment, is_qgis_available, MOCKS_ENABLED
    print(f"CI Environment: {is_ci_environment()}")
    print(f"QGIS Available: {is_qgis_available()}")
    print(f"Mocks Enabled: {MOCKS_ENABLED}")
    
    if MOCKS_ENABLED:
        print("✅ Mocking system working correctly")
    else:
        print("⚠️  Mocking system not enabled (real QGIS available)")
        
except Exception as e:
    print(f"❌ Mocking system failed: {e}")
    sys.exit(1)
'''
        
        success, output = self.run_command(
            [sys.executable, "-c", test_code],
            "Testing mocking system"
        )
        
        if success and "Mocking system" in output:
            return True
        else:
            self.print_error(f"Mocking system test failed: {output}")
            return False
    
    def run_code_quality_checks(self) -> bool:
        """Run code quality checks"""
        self.print_header("Code Quality Checks", "🧹")
        
        all_passed = True
        
        # Black formatting check
        success, _ = self.run_command(
            [sys.executable, "-m", "black", "--check", "--diff", "."],
            "Code formatting (Black)",
            critical=False
        )
        if not success:
            all_passed = False
            
        # isort import sorting check
        success, _ = self.run_command(
            [sys.executable, "-m", "isort", "--check-only", "--diff", "."],
            "Import sorting (isort)",
            critical=False
        )
        if not success:
            all_passed = False
            
        # Flake8 linting
        success, _ = self.run_command(
            [sys.executable, "-m", "flake8", ".", "--count", "--select=E9,F63,F7,F82", "--show-source", "--statistics"],
            "Critical linting (Flake8)",
            critical=False
        )
        if not success:
            all_passed = False
            
        return all_passed
    
    def run_core_tests(self) -> bool:
        """Run core tests that should always pass"""
        self.print_header("Core Tests", "🧪")
        
        # Set environment for testing
        env = os.environ.copy()
        env.update({
            "CI": "true",
            "GITHUB_ACTIONS": "true", 
            "ENVIRONMENT": "test",
            "PYTHONPATH": str(self.project_root)
        })
        
        all_passed = True
        
        # Test config module
        success, _ = self.run_command(
            [sys.executable, "-m", "pytest", "tests/unit/test_config.py", "-v", "--tb=short"],
            "Config module tests"
        )
        if not success:
            all_passed = False
            
        # Test crop model
        success, _ = self.run_command(
            [sys.executable, "-m", "pytest", "tests/unit/test_crop_model.py", "-v", "--tb=short"],
            "Crop model tests"
        )
        if not success:
            all_passed = False
            
        return all_passed
    
    def run_comprehensive_tests(self) -> bool:
        """Run comprehensive test suite"""
        self.print_header("Comprehensive Tests", "🎯")
        
        # Create coverage configuration
        coveragerc_content = '''[run]
source = .
omit = 
    */tests/*
    */test_*
    */venv/*
    */htmlcov/*
    setup.py
    run_tests.py
    verify_tests.py
    views/crop_view.py
    consulta_dialog.py
    ui_consulta_dialog.py
    compile_resources.py

[report]
exclude_lines =
    pragma: no cover
    def __repr__
    raise AssertionError
    raise NotImplementedError
    if __name__ == .__main__.:
'''
        
        with open(self.project_root / ".coveragerc", "w") as f:
            f.write(coveragerc_content)
        
        # Run comprehensive tests with coverage
        success, output = self.run_command([
            sys.executable, "-m", "pytest",
            "tests/unit/test_config.py",
            "tests/unit/test_crop_model.py", 
            "tests/unit/test_crop_controller.py",
            "tests/unit/test_plugin.py",
            "-v", "--tb=short", "--timeout=60",
            "--cov=.", "--cov-report=term-missing", "--cov-report=html",
            "--cov-fail-under=60"
        ], "Comprehensive test suite with coverage")
        
        if success:
            # Check if coverage report was generated
            if (self.project_root / "htmlcov").exists():
                self.print_success("Coverage report generated in htmlcov/")
        
        return success
    
    def run_import_tests(self) -> bool:
        """Test that all modules can be imported"""
        self.print_header("Import Tests", "📥")
        
        modules_to_test = [
            "config",
            "models.crop_model",
            "controllers.crop_controller",
            "plugin"
        ]
        
        all_passed = True
        
        for module in modules_to_test:
            test_code = f'''
import sys
import os
sys.path.insert(0, ".")
os.environ["ENVIRONMENT"] = "test"

try:
    import {module}
    print("✅ {module} imported successfully")
except Exception as e:
    print(f"❌ {module} import failed: {{e}}")
    sys.exit(1)
'''
            
            success, _ = self.run_command(
                [sys.executable, "-c", test_code],
                f"Importing {module}"
            )
            
            if not success:
                all_passed = False
                
        return all_passed
    
    def simulate_ci_environment(self) -> bool:
        """Simulate CI environment and run tests"""
        self.print_header("CI Simulation", "🤖")
        
        # Set CI environment variables
        ci_env = os.environ.copy()
        ci_env.update({
            "CI": "true",
            "GITHUB_ACTIONS": "true",
            "ENVIRONMENT": "test",
            "PYTHONPATH": str(self.project_root)
        })
        
        # Run tests as they would run in CI
        success, output = self.run_command([
            sys.executable, "-m", "pytest",
            "tests/unit/test_config.py",
            "tests/unit/test_crop_model.py",
            "-v", "--tb=short", "--timeout=30"
        ], "CI simulation tests")
        
        return success
    
    def generate_summary(self) -> None:
        """Generate and print final summary"""
        self.print_header("Summary Report", "📊")
        
        total_tests = len(self.results)
        passed_tests = sum(1 for _, success, _ in self.results if success)
        failed_tests = total_tests - passed_tests
        
        print(f"\n{Colors.BOLD}Overall Results:{Colors.END}")
        print(f"  Total checks: {total_tests}")
        print(f"  {Colors.GREEN}Passed: {passed_tests}{Colors.END}")
        print(f"  {Colors.RED}Failed: {failed_tests}{Colors.END}")
        
        if failed_tests > 0:
            print(f"\n{Colors.RED}{Colors.BOLD}Failed checks:{Colors.END}")
            for description, success, error in self.results:
                if not success:
                    print(f"  ❌ {description}")
                    if error and len(error) < 200:
                        print(f"     {error.strip()}")
        
        execution_time = time.time() - self.start_time
        print(f"\n{Colors.CYAN}Execution time: {execution_time:.1f} seconds{Colors.END}")
        
        if failed_tests == 0:
            print(f"\n{Colors.GREEN}{Colors.BOLD}🎉 ALL CHECKS PASSED!{Colors.END}")
            print(f"{Colors.GREEN}Ready for CI/CD pipeline! 🚀{Colors.END}")
            return True
        else:
            print(f"\n{Colors.RED}{Colors.BOLD}❌ Some checks failed{Colors.END}")
            print(f"{Colors.YELLOW}Please fix the issues before pushing to CI{Colors.END}")
            return False


def main():
    """Main verification function"""
    print(f"{Colors.CYAN}{Colors.BOLD}")
    print("🔍 Complete Verification for visualizacion_de_cultivos")
    print("=" * 70)
    print(f"{Colors.END}")
    
    runner = VerificationRunner()
    
    try:
        # Run all verification steps
        steps = [
            ("Environment Check", runner.check_environment),
            ("Dependencies Installation", runner.install_dependencies),
            ("Mocking System Test", runner.test_mocking_system),
            ("Import Tests", runner.run_import_tests),
            ("Code Quality Checks", runner.run_code_quality_checks),
            ("Core Tests", runner.run_core_tests),
            ("CI Simulation", runner.simulate_ci_environment),
            ("Comprehensive Tests", runner.run_comprehensive_tests),
        ]
        
        all_passed = True
        for step_name, step_func in steps:
            try:
                result = step_func()
                if not result:
                    all_passed = False
            except Exception as e:
                runner.print_error(f"{step_name} failed with exception: {e}")
                all_passed = False
        
        # Generate final summary
        summary_passed = runner.generate_summary()
        
        # Exit with appropriate code
        sys.exit(0 if summary_passed else 1)
        
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Verification interrupted by user{Colors.END}")
        sys.exit(130)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.END}")
        sys.exit(1)


if __name__ == "__main__":
    main() 