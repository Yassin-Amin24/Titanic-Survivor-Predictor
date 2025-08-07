# Quick Start Guide - E2E Testing

This guide will help you get started with the end-to-end testing suite in under 5 minutes.

## Prerequisites

- Docker and Docker Compose installed
- Python 3.8+ installed
- Git (to clone the repository)

## Step 1: Start the Services

```bash
# Navigate to the docker-compose directory
cd docker-compose

# Start all services
docker-compose up -d

# Wait for services to be healthy (check with docker-compose ps)
```

## Step 2: Install Test Dependencies

```bash
# Navigate to the E2E directory
cd E2E

# Install Python dependencies
pip install -r requirements.txt
```

## Step 3: Run Your First Test

### Option A: Use the Test Runner Script (Recommended)

```bash
# Make the script executable (first time only)
chmod +x run_tests.sh

# Run all tests
./run_tests.sh

# Run only UI tests
./run_tests.sh ui

# Run only API tests
./run_tests.sh web-backend
./run_tests.sh model-backend

# Run with verbose output
./run_tests.sh -v ui
```

### Option B: Use Behave Directly

```bash
# Run all tests
behave

# Run specific test category
behave features/web-frontend/ --tags=@web-frontend
behave features/web-backend/ --tags=@web-backend
behave features/model-backend/ --tags=@model-backend
behave features/integration/ --tags=@integration

# Run with specific tags
behave --tags=@auth
behave --tags=@prediction
behave --tags=@admin
```

## Step 4: View Test Results

Test results are saved to `test_results.txt` by default. You can also:

```bash
# View results in real-time
behave --format=pretty

# Generate HTML report
behave --format=html --outfile=report.html
```

## Common Commands

### Run Specific Test Categories

```bash
# UI Tests (Web Frontend)
./run_tests.sh ui

# API Tests (Web Backend)
./run_tests.sh web-backend

# ML Tests (Model Backend)
./run_tests.sh model-backend

# Integration Tests
./run_tests.sh integration

# Authentication Tests (across all services)
./run_tests.sh -t @auth

# Prediction Tests (across all services)
./run_tests.sh -t @prediction
```

### Debug and Development

```bash
# Run with verbose output
./run_tests.sh -v ui

# Run single feature file
behave features/web-frontend/authentication.feature

# Run single scenario
behave features/web-frontend/authentication.feature:15

# Run with custom output file
./run_tests.sh -o my_results.txt ui
```

### Troubleshooting

```bash
# Check if services are running
docker-compose ps

# Check service logs
docker-compose logs web-frontend
docker-compose logs web-backend
docker-compose logs model-backend

# Restart services
docker-compose restart

# Clean up and restart
docker-compose down
docker-compose up -d
```

## Test Structure Overview

```
features/
├── web-frontend/          # UI tests using Selenium
│   ├── landing_page.feature
│   ├── authentication.feature
│   ├── calculator.feature
│   └── admin_panel.feature
├── web-backend/           # API tests using requests
│   ├── authentication_api.feature
│   ├── prediction_api.feature
│   └── admin_api.feature
├── model-backend/         # ML API tests
│   ├── prediction_api.feature
│   └── training_api.feature
└── integration/           # Cross-service tests
    ├── end_to_end_workflow.feature
    └── data_flow.feature
```

## What Each Test Category Covers

### UI Tests (@web-frontend)
- User interface interactions
- Form submissions and validation
- Navigation and routing
- Error message display
- Responsive design testing

### Web Backend Tests (@web-backend)
- REST API endpoints
- Authentication and authorization
- Data validation
- Database operations
- Error handling

### Model Backend Tests (@model-backend)
- Machine learning model predictions
- Model training workflows
- Feature validation
- Model management
- Performance metrics

### Integration Tests (@integration)
- End-to-end user workflows
- Cross-service communication
- Data consistency
- Error propagation
- System recovery

## Next Steps

1. **Read the full documentation**: See `README.md` for detailed information
2. **Explore test files**: Look at the `.feature` files to understand test scenarios
3. **Add new tests**: Follow the existing patterns to add your own test cases
4. **Set up CI/CD**: Use the provided GitHub Actions example in the README

## Need Help?

- Check the troubleshooting section in `README.md`
- Review test logs in `test_results.txt`
- Ensure all services are healthy with `docker-compose ps`
- Verify prerequisites are installed correctly

Happy testing! 🧪 