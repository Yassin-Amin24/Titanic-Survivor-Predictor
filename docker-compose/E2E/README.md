# End-to-End Testing Suite

This directory contains comprehensive end-to-end tests for the Titanic Survival Prediction System using Behave (Python BDD framework) and Gherkin syntax.

## Project Structure

```
E2E/
├── features/                    # Gherkin feature files
│   ├── web-frontend/           # UI tests for web frontend
│   │   ├── landing_page.feature
│   │   ├── authentication.feature
│   │   ├── calculator.feature
│   │   └── admin_panel.feature
│   ├── web-backend/            # API tests for web backend
│   │   ├── authentication_api.feature
│   │   ├── prediction_api.feature
│   │   └── admin_api.feature
│   ├── model-backend/          # API tests for model backend
│   │   ├── prediction_api.feature
│   │   └── training_api.feature
│   └── integration/            # Cross-service integration tests
│       ├── end_to_end_workflow.feature
│       └── data_flow.feature
├── steps/                      # Python step implementations
│   ├── web-frontend_steps.py
│   ├── web-backend_steps.py
│   ├── model-backend_steps.py
│   └── integration_steps.py
├── environment.py              # Test setup and teardown
├── requirements.txt            # Python dependencies
└── README.md                   # This file
```

## Prerequisites

1. **Docker and Docker Compose**: Ensure all services are running
2. **Python 3.8+**: For running Behave tests
3. **Chrome/Chromium**: For UI testing (WebDriver will be managed automatically)

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Ensure all services are running:
```bash
cd docker-compose
docker-compose up -d
```

3. Wait for all services to be healthy (check with `docker-compose ps`)

## Running Tests

### 1. Web Frontend Tests (UI Flows)

Test user interface interactions and user flows:

```bash
# Run all web frontend tests
behave features/web-frontend/ --tags=@web-frontend

# Run specific feature
behave features/web-frontend/landing_page.feature

# Run authentication tests only
behave features/web-frontend/ --tags=@auth

# Run calculator tests only
behave features/web-frontend/ --tags=@calculator

# Run admin panel tests only
behave features/web-frontend/ --tags=@admin
```

**Test Coverage:**
- Landing page navigation and content
- User registration and login flows
- Survival calculator functionality
- Admin panel model and user management
- Form validation and error handling

### 2. Web Backend Tests (API Endpoints)

Test API endpoints and business logic:

```bash
# Run all web backend tests
behave features/web-backend/ --tags=@web-backend

# Run authentication API tests
behave features/web-backend/ --tags=@auth

# Run prediction API tests
behave features/web-backend/ --tags=@prediction

# Run admin API tests
behave features/web-backend/ --tags=@admin
```

**Test Coverage:**
- User authentication (register, login, logout)
- Prediction endpoints with validation
- Model management (list, train, delete)
- User management (list, delete)
- Error handling and validation

### 3. Model Backend Tests (API Endpoints)

Test machine learning model endpoints:

```bash
# Run all model backend tests
behave features/model-backend/ --tags=@model-backend

# Run prediction API tests
behave features/model-backend/ --tags=@prediction

# Run training API tests
behave features/model-backend/ --tags=@training
```

**Test Coverage:**
- Survival prediction with various models
- Model training with different algorithms
- Model management (list, delete, details)
- Feature validation and error handling
- Cross-validation and accuracy metrics

### 4. Integration Tests (Cross-Service Workflows)

Test end-to-end workflows across all services:

```bash
# Run all integration tests
behave features/integration/ --tags=@integration

# Run end-to-end workflow tests
behave features/integration/end_to_end_workflow.feature

# Run data flow tests
behave features/integration/data_flow.feature
```

**Test Coverage:**
- Complete user registration and prediction workflow
- Admin model management workflow
- Cross-service communication
- Data consistency across services
- Error handling and recovery
- Performance under load

### 5. Run All Tests

```bash
# Run all tests
behave

# Run with verbose output
behave --verbose

# Run with colored output
behave --color

# Run specific tags
behave --tags=@ui
behave --tags=@api
behave --tags=@integration
```

## Test Tags

Use tags to run specific test categories:

- `@ui` - All UI tests
- `@api` - All API tests
- `@integration` - All integration tests
- `@web-frontend` - Web frontend tests
- `@web-backend` - Web backend tests
- `@model-backend` - Model backend tests
- `@auth` - Authentication tests
- `@prediction` - Prediction functionality tests
- `@admin` - Admin functionality tests
- `@calculator` - Calculator functionality tests
- `@training` - Model training tests

## Configuration

### Environment Variables

Set these environment variables to customize test behavior:

```bash
export WEB_FRONTEND_URL=http://localhost:3000
export WEB_BACKEND_URL=http://localhost:8000
export MODEL_BACKEND_URL=http://localhost:5001
```

### Test Data

Default test users are configured in `environment.py`:

- **Regular User**: `test@example.com` / `testpassword123`
- **Admin User**: `admin@titanic.com` / `admin123`

## Test Reports

### HTML Reports

Generate HTML test reports:

```bash
# Install pytest-html if not already installed
pip install pytest-html

# Run tests with HTML report
behave --format=pretty --outfile=test_results.txt
```

### Allure Reports (Advanced)

For detailed test reports with Allure:

```bash
# Install allure-behave
pip install allure-behave

# Run tests with Allure
behave --format=allure_behave.formatter:AllureFormatter --outfile=allure-results

# Generate and open report
allure serve allure-results
```

## Troubleshooting

### Common Issues

1. **Services not running**: Ensure all Docker containers are up and healthy
2. **WebDriver issues**: Chrome/Chromium should be installed
3. **Database connection**: Ensure web-backend database is accessible
4. **Port conflicts**: Check that ports 3000, 8000, and 5001 are available

### Debug Mode

Run tests with debug output:

```bash
behave --verbose --no-capture
```

### Single Test Execution

Run a single scenario for debugging:

```bash
behave features/web-frontend/authentication.feature:15
```

## Continuous Integration

### GitHub Actions Example

```yaml
name: E2E Tests
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
          pip install -r docker-compose/E2E/requirements.txt
      - name: Start services
        run: |
          cd docker-compose
          docker-compose up -d
      - name: Wait for services
        run: |
          sleep 30
      - name: Run E2E tests
        run: |
          cd docker-compose/E2E
          behave --format=pretty --outfile=test_results.txt
      - name: Upload test results
        uses: actions/upload-artifact@v2
        with:
          name: test-results
          path: docker-compose/E2E/test_results.txt
```

## Best Practices

1. **Test Isolation**: Each test should be independent and not rely on other tests
2. **Data Cleanup**: Tests should clean up after themselves
3. **Realistic Data**: Use realistic test data that represents actual usage
4. **Error Scenarios**: Test both happy path and error scenarios
5. **Performance**: Monitor test execution time and optimize slow tests

## Contributing

When adding new tests:

1. Follow the existing naming conventions
2. Use appropriate tags for categorization
3. Add step implementations in the correct files
4. Update this README if adding new test categories
5. Ensure tests are independent and repeatable

## Support

For issues with the test suite:

1. Check the troubleshooting section
2. Review the test logs for specific error messages
3. Ensure all prerequisites are met
4. Verify service health before running tests 