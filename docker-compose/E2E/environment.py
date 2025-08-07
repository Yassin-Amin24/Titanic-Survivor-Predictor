"""
Behave environment configuration for E2E testing
Handles setup and teardown for all test scenarios
"""

import os
import time
import requests
from playwright.sync_api import sync_playwright


def before_all(context):
    """Setup before all tests run"""
    context.config.setup_logging()
    
    # Base URLs for services
    context.web_frontend_url = os.getenv("WEB_FRONTEND_URL", "http://localhost:3000")
    context.web_backend_url = os.getenv("WEB_BACKEND_URL", "http://localhost:8000")
    context.model_backend_url = os.getenv("MODEL_BACKEND_URL", "http://localhost:5001")
    
    # Test data
    context.test_user = {
        "email": "test@example.com",
        "password": "testpassword123"
    }
    
    context.admin_user = {
        "email": "admin@titanic.com",
        "password": "admin123"
    }
    
    # Wait for services to be ready
    wait_for_services(context)


def before_scenario(context, scenario):
    """Setup before each scenario"""
    context.browser = None
    context.page = None
    context.session = requests.Session()
    context.auth_token = None
    
    # Initialize Playwright browser for UI tests
    if "ui" in scenario.tags:
        setup_playwright(context)


def after_scenario(context, scenario):
    """Cleanup after each scenario"""
    if context.page:
        context.page.close()
    
    if context.browser:
        context.browser.close()
    
    if context.session:
        context.session.close()


def after_all(context):
    """Cleanup after all tests"""
    if hasattr(context, 'playwright'):
        context.playwright.stop()


def wait_for_services(context):
    """Wait for all services to be ready"""
    services = [
        ("Web Frontend", context.web_frontend_url),
        ("Web Backend", context.web_backend_url),
        ("Model Backend", context.model_backend_url)
    ]
    
    for service_name, url in services:
        print(f"Waiting for {service_name} at {url}...")
        max_retries = 30
        retry_count = 0
        
        while retry_count < max_retries:
            try:
                response = requests.get(f"{url}/health", timeout=5)
                if response.status_code == 200:
                    print(f"✓ {service_name} is ready")
                    break
            except requests.exceptions.RequestException:
                pass
            
            retry_count += 1
            time.sleep(2)
        
        if retry_count >= max_retries:
            print(f"✗ {service_name} failed to start within timeout")


def setup_playwright(context):
    """Setup Playwright browser for UI testing"""
    context.playwright = sync_playwright().start()
    
    # Launch browser with headless mode
    headless = os.getenv("HEADLESS", "true").lower() == "true"
    context.browser = context.playwright.chromium.launch(
        headless=headless,
        args=[
            "--no-sandbox",
            "--disable-dev-shm-usage",
            "--disable-gpu"
        ]
    )
    
    # Create browser context and page
    context.browser_context = context.browser.new_context(
        viewport={"width": 1920, "height": 1080}
    )
    context.page = context.browser_context.new_page()
    
    # Set default timeout
    context.page.set_default_timeout(10000)  # 10 seconds 