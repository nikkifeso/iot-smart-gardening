#!/usr/bin/env python3
"""
Test runner for advanced automation logic tests
"""

import unittest
import sys
import os

# Add the project root to the path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from test_automation_logic import TestAdvancedAutomationLogic
from test_main_automation import TestMainAutomationLogic


def run_automation_tests():
    """Run all automation logic tests"""
    print("🧪 Running Advanced Automation Logic Tests")
    print("=" * 50)
    
    test_suite = unittest.TestSuite()
    
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestAdvancedAutomationLogic))
    test_suite.addTest(unittest.TestLoader().loadTestsFromTestCase(TestMainAutomationLogic))
    
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    print("\n" + "=" * 50)
    print("TEST SUMMARY")
    print("=" * 50)
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print("\n FAILURES:")
        for test, traceback in result.failures:
            print(f"  - {test}: {traceback.split('AssertionError:')[-1].strip()}")
    
    if result.errors:
        print("\n ERRORS:")
        for test, traceback in result.errors:
            print(f"  - {test}: {traceback.split('Exception:')[-1].strip()}")
    
    if not result.failures and not result.errors:
        print("\n ALL TESTS PASSED!")
        print("Advanced automation logic is working correctly!")
    
    return result.wasSuccessful()


if __name__ == '__main__':
    success = run_automation_tests()
    sys.exit(0 if success else 1) 