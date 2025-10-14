# Test Suite Documentation

This directory contains all test files for the Django E-commerce project, organized by category for better maintainability.

## Directory Structure

### 📋 Functional Tests (`functional/`)
Tests for authentication, permissions, login flows, checkout processes, and user workflows.

### 🔧 Unit Tests (`unit/`)
Individual component and model tests that verify specific functionality in isolation.

### 🔗 Integration Tests (`integration/`)
End-to-end tests that verify complete workflows and system interactions.

### 🛠️ Utilities (`utilities/`)
Debug scripts, quick tests, and diagnostic tools for development.

### 📊 Data Setup (`data_setup/`)
Scripts for creating test data, demo functionality, and test environment setup.

## Running Tests

### Run All Tests
```bash
# From project root
python manage.py test

# Or run individual test files
python test_filename.py
```

### Run Tests by Category
```bash
# Functional tests
python -m pytest tests/functional/

# Unit tests  
python -m pytest tests/unit/

# Integration tests
python -m pytest tests/integration/
```

### Run Specific Test Files
```bash
# Authentication tests
python tests/functional/test_login_flow.py

# Cart functionality
python tests/functional/test_add_to_cart.py

# Complete workflow tests
python tests/integration/test_all_functionality.py

> Note: test files were moved to the top-level `tests/` directory during cleanup. The examples above were updated to point at the new locations.
```

## Test Environment Setup

Before running tests, ensure you have:

1. **Django Environment**: `python manage.py check`
2. **Test Database**: Tests use SQLite by default
3. **Required Packages**: Install from `requirements.txt`

## Development Workflow

1. **Writing New Tests**: Place new tests in the appropriate category folder
2. **Running During Development**: Use quick tests from `utilities/` for rapid feedback
3. **Pre-commit Testing**: Run integration tests before major commits
4. **Data Setup**: Use scripts from `data_setup/` to prepare test environments

## Test Categories Explained

### Functional Tests
- `test_login_flow.py`: User authentication workflows
- `test_add_to_cart.py`: Shopping cart functionality
- `test_checkout_flow.py`: Purchase process testing
- `test_vendor_dashboard.py`: Vendor-specific features
- `test_password_reset.py`: Password recovery workflows

### Integration Tests  
- `test_all_functionality.py`: Complete system workflow testing
- `test_real_functionality.py`: Real-world scenario testing
- `test_web_form.py`: Form submission and validation testing

### Utilities
- `debug_add_to_cart.py`: Cart debugging tools
- `quick_cart_test.py`: Rapid cart functionality verification

### Data Setup
- `create_test_order.py`: Generate test orders and data
- `setup_demo_functionality.py`: Prepare demonstration environment
- `fix_tshirt_test_images.py`: Test data image management

## Important Notes

⚠️ **No Webpage Functionality Changed**: This reorganization only moves test files and does not affect any website functionality.

🔒 **Backwards Compatibility**: All test files maintain their original functionality and can be run independently.

📁 **Backup Available**: Original file locations are backed up in `archived/test_backup_[timestamp]/`

## Troubleshooting

If you encounter import issues after reorganization:

1. Check your Python path includes the project root
2. Verify Django settings are properly configured  
3. Ensure all required test dependencies are installed
4. Run `python manage.py check` to verify Django configuration

For questions or issues, refer to the main project documentation.
