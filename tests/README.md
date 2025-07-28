# Smart Gardening Dashboard - Test Suite

This directory contains comprehensive tests for the Smart Gardening Dashboard application.

## Test Overview

The test suite covers all major components of the application:

- **Database Tests** - Database models, relationships, and operations
- **Core Tests** - Zone management and business logic
- **Sensor Tests** - Moisture and pH sensor functionality
- **Actuator Tests** - Water pump control and monitoring
- **Simulator Tests** - Sensor data simulation
- **Dashboard Tests** - Dashboard data operations and validation
- **Integration Tests** - Full system workflow testing
- **Configuration Tests** - Configuration management and validation

## Quick Start

### Run All Tests

```bash
# Run all tests with verbose output
python tests/run_tests.py

# Run tests quietly
python tests/run_tests.py --quiet

# Generate JSON report
python tests/run_tests.py --output test_report.json
```

### Run Specific Test Categories

```bash
# Run only database tests
python tests/run_tests.py --category database

# Run only sensor tests
python tests/run_tests.py --category sensors

# Run only integration tests
python tests/run_tests.py --category integration
```

### List Available Test Categories

```bash
python tests/run_tests.py --list
```

## Test Structure

```
tests/
├── __init__.py                 # Test package initialization
├── test_database.py           # Database model tests
├── test_core.py              # Core functionality tests
├── test_sensors.py           # Sensor tests
├── test_actuators.py         # Actuator tests
├── test_simulator.py         # Simulator tests
├── test_dashboard.py         # Dashboard tests
├── test_integration.py       # Integration tests
├── test_config.py            # Configuration tests
├── run_tests.py              # Test runner script
├── requirements-test.txt     # Testing dependencies
└── README.md                 # This file
```

## Test Categories

### Database Tests (`test_database.py`)

- **Zone Creation** - Test zone model creation and validation
- **Plant Management** - Test plant model operations
- **Sensor Readings** - Test sensor data storage and retrieval
- **Pump Logs** - Test pump activity logging
- **Relationships** - Test model relationships and foreign keys
- **Data Integrity** - Test data consistency and constraints

### Core Tests (`test_core.py`)

- **Zone Operations** - Test zone creation, updates, and status
- **Data Validation** - Test input validation and business rules
- **Status Logic** - Test moisture and pH status calculations
- **Plant Management** - Test plant addition and tracking

### Sensor Tests (`test_sensors.py`)

- **Moisture Sensor** - Test moisture sensor readings and validation
- **pH Sensor** - Test pH sensor readings and validation
- **Sensor Integration** - Test multiple sensors in same zone
- **Reading Validation** - Test sensor reading ranges and types

### Actuator Tests (`test_actuators.py`)

- **Pump Control** - Test pump activation and deactivation
- **Status Tracking** - Test pump status monitoring
- **Timing** - Test pump activation timestamps
- **Zone Association** - Test pump-zone relationships

### Simulator Tests (`test_simulator.py`)

- **Data Generation** - Test realistic sensor data simulation
- **Multi-zone Support** - Test simulation across multiple zones
- **Value Ranges** - Test simulated values within valid ranges
- **Randomization** - Test random value generation

### Dashboard Tests (`test_dashboard.py`)

- **Data Retrieval** - Test dashboard data fetching
- **Zone Status** - Test zone status calculations
- **Data Validation** - Test data integrity and types
- **Chart Data** - Test data preparation for visualizations

### Integration Tests (`test_integration.py`)

- **Complete Workflow** - Test end-to-end garden management
- **Sensor Monitoring** - Test continuous monitoring cycles
- **Automated Watering** - Test automated watering system
- **Error Handling** - Test system recovery and error handling
- **Performance** - Test system scalability

### Configuration Tests (`test_config.py`)

- **Default Values** - Test default configuration
- **Environment Variables** - Test environment variable overrides
- **Validation** - Test configuration value validation
- **Type Consistency** - Test configuration data types

## Test Configuration

### Environment Setup

```bash
# Install testing dependencies
pip install -r tests/requirements-test.txt

# Set up test environment
export TESTING=True
export DATABASE_URL=sqlite:///test.db
```

### Test Database

Tests use temporary SQLite databases that are automatically created and cleaned up:

- Each test class gets its own temporary database
- Databases are automatically deleted after tests complete
- No interference with production data

### Mocking and Stubbing

Tests use Python's `unittest.mock` for:

- Simulating sensor readings
- Mocking external dependencies
- Controlling test data generation
- Isolating components for unit testing

## Test Reports

### Console Output

Tests provide detailed console output including:

- Test execution progress
- Pass/fail status for each test
- Detailed error messages and tracebacks
- Execution time and statistics

### JSON Reports

Generate detailed JSON reports with:

```bash
python tests/run_tests.py --output test_report.json
```

Report includes:

- Test execution timestamp
- Summary statistics (total, passed, failed, errors)
- Success rate percentage
- Execution time
- Detailed failure and error information

### Coverage Reports

Generate code coverage reports:

```bash
# Install coverage tool
pip install coverage

# Run tests with coverage
coverage run tests/run_tests.py

# Generate coverage report
coverage report
coverage html  # Generate HTML report
```

## Debugging Tests

### Running Individual Tests

```bash
# Run specific test method
python -m unittest tests.test_database.TestDatabase.test_zone_creation

# Run specific test class
python -m unittest tests.test_database.TestDatabase
```

### Verbose Output

```bash
# Get detailed test output
python tests/run_tests.py --verbose

# See test discovery
python -m unittest discover tests -v
```

### Debug Mode

Add debugging to tests:

```python
import pdb; pdb.set_trace()  # Add breakpoint
```

## Common Issues

### Import Errors

If you encounter import errors:

1. Ensure you're in the project root directory
2. Check that `PYTHONPATH` includes the project root
3. Verify all dependencies are installed

### Database Errors

If database tests fail:

1. Check SQLite is available
2. Ensure write permissions in test directory
3. Verify database models are properly imported

### Mock Issues

If mocking doesn't work:

1. Check import paths for mocked objects
2. Verify mock patches target correct modules
3. Ensure mocks are applied before object instantiation

## Continuous Integration

### GitHub Actions

The test suite is designed to work with CI/CD pipelines:

```yaml
# .github/workflows/test.yml
name: Tests
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Set up Python
        uses: actions/setup-python@v2
        with:
          python-version: 3.9
      - name: Install dependencies
        run: |
          pip install -r requirements.txt
          pip install -r tests/requirements-test.txt
      - name: Run tests
        run: python tests/run_tests.py --output test_results.json
      - name: Upload test results
        uses: actions/upload-artifact@v2
        with:
          name: test-results
          path: test_results.json
```

### Pre-commit Hooks

Set up pre-commit hooks to run tests automatically:

```bash
# Install pre-commit
pip install pre-commit

# Create .pre-commit-config.yaml
repos:
  - repo: local
    hooks:
      - id: tests
        name: Run Tests
        entry: python tests/run_tests.py --quiet
        language: system
        pass_filenames: false
```

## Contributing

### Adding New Tests

1. Create test file following naming convention: `test_<module>.py`
2. Inherit from `unittest.TestCase`
3. Use descriptive test method names
4. Include docstrings explaining test purpose
5. Add tests to `run_tests.py` test suite

### Test Guidelines

- **Isolation**: Each test should be independent
- **Cleanup**: Always clean up test data
- **Descriptive**: Use clear test names and descriptions
- **Comprehensive**: Test both success and failure cases
- **Realistic**: Use realistic test data

### Test Data

- Use `setUp()` and `tearDown()` methods for test data
- Create realistic test scenarios
- Test edge cases and error conditions
- Use factories for complex test data

## Additional Resources

- [Python unittest documentation](https://docs.python.org/3/library/unittest.html)
- [pytest documentation](https://docs.pytest.org/)
- [Coverage.py documentation](https://coverage.readthedocs.io/)
- [Mock documentation](https://docs.python.org/3/library/unittest.mock.html)

## Support

If you encounter issues with the test suite:

1. Check the console output for detailed error messages
2. Review the test documentation above
3. Check that all dependencies are installed
4. Verify your Python environment is set up correctly
5. Create an issue with detailed error information

---

**Happy Testing!**
