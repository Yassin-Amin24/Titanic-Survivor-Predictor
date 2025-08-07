#!/bin/bash

# Add virtual environment to PATH if it exists
if [ -d "venv/bin" ]; then
    export PATH="venv/bin:$PATH"
fi

# E2E Test Runner Script
# This script provides convenient commands to run different categories of tests

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Default values
TEST_TYPE="all"
VERBOSE=false
OUTPUT_FILE="test_results.txt"
TAGS=""

# Function to print colored output
print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Function to show usage
show_usage() {
    echo "Usage: $0 [OPTIONS] [TEST_TYPE]"
    echo ""
    echo "TEST_TYPE options:"
    echo "  all              Run all tests (default)"
    echo "  ui               Run web frontend UI tests"
    echo "  web-backend      Run web backend API tests"
    echo "  model-backend    Run model backend API tests"
    echo "  integration      Run integration tests"
    echo "  auth             Run authentication tests"
    echo "  prediction       Run prediction tests"
    echo "  admin            Run admin tests"
    echo ""
    echo "OPTIONS:"
    echo "  -v, --verbose    Enable verbose output"
    echo "  -o, --output     Specify output file (default: test_results.txt)"
    echo "  -t, --tags       Run tests with specific tags"
    echo "  -h, --help       Show this help message"
    echo ""
    echo "Examples:"
    echo "  $0 ui                    # Run UI tests"
    echo "  $0 web-backend -v        # Run web backend tests with verbose output"
    echo "  $0 -t @auth              # Run all authentication tests"
    echo "  $0 integration -o results.txt  # Run integration tests with custom output"
}

# Function to check prerequisites
check_prerequisites() {
    print_status "Checking prerequisites..."
    
    # Check if Python is installed
    if ! command -v python3 &> /dev/null; then
        print_error "Python 3 is not installed"
        exit 1
    fi
    
    # Check for pip
    if ! command -v pip &> /dev/null; then
        print_error "pip is not installed"
        exit 1
    fi
    
    # Check if behave is installed
    if ! python3 -c "import behave" &> /dev/null; then
        print_warning "behave is not installed. Installing dependencies..."
        pip install --upgrade pip > /dev/null 2>&1
        pip install -r requirements.txt > /dev/null 2>&1
    fi
    
    # Check if Docker is running
    if ! docker info &> /dev/null; then
        print_error "Docker is not running"
        exit 1
    fi
    
    print_success "Prerequisites check passed"
}

# Function to check if services are running
check_services() {
    print_status "Checking if services are running..."
    
    # Check web frontend
    if ! curl -s http://localhost:3000/health &> /dev/null; then
        print_warning "Web frontend is not responding. Starting services..."
        cd .. && docker-compose up -d && cd E2E
        sleep 30
    fi
    
    # Check web backend
    if ! curl -s http://localhost:8000/health &> /dev/null; then
        print_error "Web backend is not responding"
        exit 1
    fi
    
    # Check model backend
    if ! curl -s http://localhost:5001/health &> /dev/null; then
        print_error "Model backend is not responding"
        exit 1
    fi
    
    print_success "All services are running"
}

# Function to run tests
run_tests() {
    local test_type=$1
    local behave_args=""
    
    # Set up behave arguments
    if [ "$VERBOSE" = true ]; then
        behave_args="$behave_args --verbose"
    fi
    
    if [ -n "$TAGS" ]; then
        behave_args="$behave_args --tags=$TAGS"
    fi
    
    behave_args="$behave_args --format=pretty --outfile=$OUTPUT_FILE"
    
    print_status "Running $test_type tests..."
    
    case $test_type in
        "all")
            behave $behave_args
            ;;
        "ui")
            behave features/web-frontend/ --tags=@web-frontend $behave_args
            ;;
        "web-backend")
            behave features/web-backend/ --tags=@web-backend $behave_args
            ;;
        "model-backend")
            behave features/model-backend/ --tags=@model-backend $behave_args
            ;;
        "integration")
            behave features/integration/ --tags=@integration $behave_args
            ;;
        "auth")
            behave --tags=@auth $behave_args
            ;;
        "prediction")
            behave --tags=@prediction $behave_args
            ;;
        "admin")
            behave --tags=@admin $behave_args
            ;;
        *)
            print_error "Unknown test type: $test_type"
            show_usage
            exit 1
            ;;
    esac
    
    if [ $? -eq 0 ]; then
        print_success "$test_type tests completed successfully"
        print_status "Results saved to: $OUTPUT_FILE"
    else
        print_error "$test_type tests failed"
        exit 1
    fi
}

# Function to show test summary
show_summary() {
    if [ -f "$OUTPUT_FILE" ]; then
        echo ""
        print_status "Test Summary:"
        echo "=============="
        tail -20 "$OUTPUT_FILE"
    fi
}

# Parse command line arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -v|--verbose)
            VERBOSE=true
            shift
            ;;
        -o|--output)
            OUTPUT_FILE="$2"
            shift 2
            ;;
        -t|--tags)
            TAGS="$2"
            shift 2
            ;;
        -h|--help)
            show_usage
            exit 0
            ;;
        ui|web-backend|model-backend|integration|auth|prediction|admin|all)
            TEST_TYPE="$1"
            shift
            ;;
        *)
            print_error "Unknown option: $1"
            show_usage
            exit 1
            ;;
    esac
done

# Main execution
main() {
    echo "=========================================="
    echo "    E2E Test Runner for Titanic System"
    echo "=========================================="
    echo ""
    
    check_prerequisites
    check_services
    
    echo ""
    print_status "Starting test execution..."
    echo "Test Type: $TEST_TYPE"
    if [ "$VERBOSE" = true ]; then
        echo "Verbose: Yes"
    fi
    if [ -n "$TAGS" ]; then
        echo "Tags: $TAGS"
    fi
    echo "Output File: $OUTPUT_FILE"
    echo ""
    
    run_tests "$TEST_TYPE"
    show_summary
    
    echo ""
    print_success "Test execution completed!"
}

# Run main function
main 