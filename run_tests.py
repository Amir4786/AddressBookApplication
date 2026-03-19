#!/usr/bin/env python3
"""
Test runner script for Address Book API
Run all tests with: python run_tests.py
Run specific test: python run_tests.py -k test_name
Run with coverage: python run_tests.py --cov=src --cov-report=html
"""

import sys
import subprocess

def run_tests():
    """Run pytest with appropriate arguments"""
    cmd = [
        sys.executable, "-m", "pytest",
        "tests/",
        "-v",
        "--tb=short",
        "--color=yes"
    ]

    # Add any additional arguments passed to this script
    if len(sys.argv) > 1:
        cmd.extend(sys.argv[1:])

    print("Running tests...")
    print("Command:", " ".join(cmd))
    print("-" * 50)

    result = subprocess.run(cmd)
    return result.returncode

if __name__ == "__main__":
    exit_code = run_tests()
    sys.exit(exit_code)