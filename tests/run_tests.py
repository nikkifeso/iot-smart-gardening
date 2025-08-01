#!/usr/bin/env python3
"""
Test runner for Smart Gardening Dashboard
Runs all tests and generates a comprehensive test report
"""

import unittest
import sys
import os
import time
import json
from datetime import datetime
from io import StringIO

# Add the project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

# Import all test modules
from tests.test_database import TestDatabase
from tests.test_core import TestZone
from tests.test_simulator import TestSensorSimulator
from tests.test_actuators import TestWaterPump
# from tests.test_sensors import TestMoistureSensor, TestPHSensor, TestSensorIntegration
from tests.test_dashboard import TestDashboardData, TestZoneStatus, TestDataValidation
from tests.test_integration import TestSmartGardenIntegration
from tests.test_config import TestConfig
from tests.test_remove_plant_ui import TestRemovePlantUI



class TestRunner:
    """Test runner with reporting capabilities"""
    
    def __init__(self):
        self.test_results = {}
        self.start_time = None
        self.end_time = None
    
    def run_all_tests(self, verbose=True, output_file=None):
        """Run all tests and generate a report"""
        print("Smart Gardening Dashboard - Test Suite")
        print("=" * 50)
        
        self.start_time = time.time()
        
        # Create test suite
        test_suite = unittest.TestSuite()
        
        # Add all test classes
        test_classes = [
            TestDatabase,
            TestZone,
            TestSensorSimulator,
            TestWaterPump,
            TestDashboardData,
            TestZoneStatus,
            TestDataValidation,
            TestSmartGardenIntegration,
            TestConfig,
            TestRemovePlantUI
        ]
        
        for test_class in test_classes:
            test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_class))
        
        # Run tests
        runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
        result = runner.run(test_suite)
        
        self.end_time = time.time()
        
        # Generate report
        self.generate_report(result, output_file)
        
        return result.wasSuccessful()
    
    def generate_report(self, result, output_file=None):
        """Generate a comprehensive test report"""
        print("\n" + "=" * 50)
        print("TEST REPORT")
        print("=" * 50)
        
        # Calculate statistics
        total_tests = result.testsRun
        failed_tests = len(result.failures)
        error_tests = len(result.errors)
        skipped_tests = len(result.skipped) if hasattr(result, 'skipped') else 0
        passed_tests = total_tests - failed_tests - error_tests - skipped_tests
        
        # Calculate execution time
        execution_time = self.end_time - self.start_time
        
        # Print summary
        print(f"Test Summary:")
        print(f"   Total Tests: {total_tests}")
        print(f"   Passed: {passed_tests}")
        print(f"   Failed: {failed_tests}")
        print(f"   Errors: {error_tests}")
        print(f"   Skipped: {skipped_tests}")
        print(f"   Success Rate: {(passed_tests/total_tests*100):.1f}%")
        print(f"   Execution Time: {execution_time:.2f} seconds")
        
        # Print detailed results
        if result.failures:
            print(f"\nFailed Tests:")
            for test, traceback in result.failures:
                print(f"   - {test}: {traceback.split('AssertionError:')[-1].strip()}")
        
        if result.errors:
            print(f"\nTest Errors:")
            for test, traceback in result.errors:
                print(f"   - {test}: {traceback.split('Exception:')[-1].strip()}")
        
        # Generate JSON report if output file specified
        if output_file:
            self.save_json_report(result, output_file, execution_time)
        
        # Print final status
        if result.wasSuccessful():
            print(f"\nAll tests passed successfully!")
        else:
            print(f"\nSome tests failed. Please review the errors above.")
    
    def save_json_report(self, result, output_file, execution_time):
        """Save test results as JSON report"""
        report_data = {
            "timestamp": datetime.now().isoformat(),
            "execution_time": execution_time,
            "summary": {
                "total_tests": result.testsRun,
                "passed": result.testsRun - len(result.failures) - len(result.errors),
                "failed": len(result.failures),
                "errors": len(result.errors),
                "success_rate": (result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100
            },
            "failures": [
                {
                    "test": str(test),
                    "error": traceback.split('AssertionError:')[-1].strip() if 'AssertionError:' in traceback else traceback
                }
                for test, traceback in result.failures
            ],
            "errors": [
                {
                    "test": str(test),
                    "error": traceback.split('Exception:')[-1].strip() if 'Exception:' in traceback else traceback
                }
                for test, traceback in result.errors
            ]
        }
        
        with open(output_file, 'w') as f:
            json.dump(report_data, f, indent=2)
        
        print(f"\nJSON report saved to: {output_file}")
    
    def run_specific_test_category(self, category, verbose=True):
        """Run tests for a specific category"""
        print(f"Running {category} tests...")
        
        test_map = {
            "database": TestDatabase,
            "core": TestZone,
            "simulator": TestSensorSimulator,
            "actuators": TestWaterPump,
            # "sensors": [TestMoistureSensor, TestPHSensor, TestSensorIntegration],
            "dashboard": [TestDashboardData, TestZoneStatus, TestDataValidation],
            "integration": TestSmartGardenIntegration,
            "config": TestConfig
        }
        
        if category not in test_map:
            print(f"Unknown test category: {category}")
            return False
        
        test_suite = unittest.TestSuite()
        test_classes = test_map[category]
        
        if isinstance(test_classes, list):
            for test_class in test_classes:
                test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_class))
        else:
            test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(test_classes))
        
        runner = unittest.TextTestRunner(verbosity=2 if verbose else 1)
        result = runner.run(test_suite)
        
        return result.wasSuccessful()


def main():
    """Main function to run tests"""
    import argparse
    
    parser = argparse.ArgumentParser(description="Run Smart Gardening Dashboard tests")
    parser.add_argument("--category", "-c", 
                       choices=["database", "core", "simulator", "actuators", "dashboard", "integration", "config"],
                       help="Run tests for a specific category")
    parser.add_argument("--output", "-o", 
                       help="Save JSON report to specified file")
    parser.add_argument("--quiet", "-q", 
                       action="store_true", 
                       help="Run tests quietly")
    parser.add_argument("--list", "-l", 
                       action="store_true", 
                       help="List all available test categories")
    
    args = parser.parse_args()
    
    runner = TestRunner()
    
    if args.list:
        print("Available test categories:")
        print("  database     - Database models and operations")
        print("  core         - Core zone functionality")
        print("  simulator    - Sensor simulation")
        print("  actuators    - Water pump functionality")
        print("  sensors      - Moisture and pH sensors")
        print("  dashboard    - Dashboard data operations")
        print("  integration  - Full system integration")
        print("  config       - Configuration management")
        return
    
    if args.category:
        success = runner.run_specific_test_category(args.category, verbose=not args.quiet)
    else:
        success = runner.run_all_tests(verbose=not args.quiet, output_file=args.output)
    
    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main() 