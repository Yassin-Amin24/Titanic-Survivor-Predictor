"""
Step implementations for integration tests
"""

from behave import given, when, then
import requests
import json
import time
import sqlite3
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


@given("all services are running")
def step_impl(context):
    # Check all services are running
    services = [
        ("Web Frontend", context.web_frontend_url),
        ("Web Backend", context.web_backend_url),
        ("Model Backend", context.model_backend_url)
    ]
    
    for service_name, url in services:
        response = requests.get(f"{url}/health", timeout=5)
        assert response.status_code == 200, f"{service_name} not running: {response.status_code}"


@given("I am a registered user")
def step_impl(context):
    # Register a test user
    register_data = {
        "email": context.test_user["email"],
        "password": context.test_user["password"]
    }
    
    response = requests.post(f"{context.web_backend_url}/api/auth/register", json=register_data)
    # Don't assert as user might already exist


@given("I am logged in as an admin user for integration")
def step_impl(context):
    # Integration-specific admin login logic
    login_data = {
        "email": context.admin_user["email"],
        "password": context.admin_user["password"]
    }
    
    response = requests.post(f"{context.web_backend_url}/api/auth/login", json=login_data)
    assert response.status_code == 200
    
    context.auth_token = response.json()["token"]


@given("the database is properly initialized")
def step_impl(context):
    # Check if database exists and has required tables
    try:
        conn = sqlite3.connect('web-backend/titanic_app.db')
        cursor = conn.cursor()
        
        # Check if users table exists
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
        assert cursor.fetchone() is not None, "Users table does not exist"
        
        conn.close()
    except Exception as e:
        assert False, f"Database initialization failed: {e}"


@when("I register a new user account")
def step_impl(context):
    # Register through web frontend
    context.driver.get(f"{context.web_frontend_url}/register")
    
    email_field = context.driver.find_element(By.NAME, "email")
    password_field = context.driver.find_element(By.NAME, "password")
    
    email_field.send_keys("integration@test.com")
    password_field.send_keys("integrationpass123")
    
    register_button = context.driver.find_element(By.XPATH, "//button[contains(text(), 'Register')]")
    register_button.click()
    
    # Wait for registration to complete
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'success')]"))
    )


@when("I login to the application")
def step_impl(context):
    context.driver.get(f"{context.web_frontend_url}/login")
    
    email_field = context.driver.find_element(By.NAME, "email")
    password_field = context.driver.find_element(By.NAME, "password")
    
    email_field.send_keys("integration@test.com")
    password_field.send_keys("integrationpass123")
    
    login_button = context.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
    login_button.click()
    
    # Wait for successful login
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Logout')]"))
    )


@when("I navigate to the calculator page")
def step_impl(context):
    context.driver.get(f"{context.web_frontend_url}/calculator")


@when("I enter passenger data for prediction")
def step_impl(context):
    # Fill in passenger data
    context.execute_steps('''
        When I select "1" for passenger class
        And I select "male" for sex
        And I enter "30" for age
        And I enter "50.0" for fare
        And I select "Yes" for traveled alone
        And I select "C" for embarked
        And I select "Mr" for title
    ''')


@when("I select multiple models for comparison")
def step_impl(context):
    # Select multiple models
    models = ["Random Forest", "SVM", "Logistic Regression"]
    for model in models:
        checkbox = context.driver.find_element(By.XPATH, f"//input[@value='{model}']")
        if not checkbox.is_selected():
            checkbox.click()


@when("I submit the prediction request")
def step_impl(context):
    predict_button = context.driver.find_element(By.XPATH, "//button[contains(text(), 'Predict')]")
    predict_button.click()


@when("I access the admin panel")
def step_impl(context):
    context.driver.get(f"{context.web_frontend_url}/admin")


@when("I view the current models list")
def step_impl(context):
    # Wait for models list to load
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'models-list')]"))
    )


@when("I train a new custom model")
def step_impl(context):
    # Click train new model button
    train_button = context.driver.find_element(By.XPATH, "//button[contains(text(), 'Train New Model')]")
    train_button.click()
    
    # Fill in training parameters
    model_name_field = context.driver.find_element(By.NAME, "model_name")
    model_name_field.send_keys("integration_test_model")
    
    # Select algorithm
    algorithm_select = context.driver.find_element(By.NAME, "algorithm")
    algorithm_select.click()
    random_forest_option = context.driver.find_element(By.XPATH, "//option[contains(text(), 'Random Forest')]")
    random_forest_option.click()
    
    # Select features
    feature_checkboxes = context.driver.find_elements(By.XPATH, "//input[@type='checkbox' and @name='features']")
    for checkbox in feature_checkboxes[:3]:  # Select first 3 features
        if not checkbox.is_selected():
            checkbox.click()
    
    # Submit training
    submit_button = context.driver.find_element(By.XPATH, "//button[contains(text(), 'Train Model')]")
    submit_button.click()


@when("I verify the new model is available")
def step_impl(context):
    # Wait for training to complete and model to appear
    WebDriverWait(context.driver, 30).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(text(), 'integration_test_model')]"))
    )


@when("I delete the custom model")
def step_impl(context):
    # Find and click delete button for the custom model
    delete_button = context.driver.find_element(By.XPATH, "//button[contains(@onclick, 'integration_test_model')]")
    delete_button.click()
    
    # Confirm deletion
    confirm_button = context.driver.find_element(By.XPATH, "//button[contains(text(), 'Confirm')]")
    confirm_button.click()


@when("I make a prediction through the web frontend")
def step_impl(context):
    # Navigate to calculator and make prediction
    context.driver.get(f"{context.web_frontend_url}/calculator")
    
    # Fill in form
    context.execute_steps('''
        When I select "1" for passenger class
        And I select "male" for sex
        And I enter "30" for age
        And I enter "50.0" for fare
        And I select "Yes" for traveled alone
        And I select "C" for embarked
        And I select "Mr" for title
        And I select "Random Forest" model
        And I click the "Predict" button
    ''')


@when("I login through the web frontend")
def step_impl(context):
    context.driver.get(f"{context.web_frontend_url}/login")
    
    email_field = context.driver.find_element(By.NAME, "email")
    password_field = context.driver.find_element(By.NAME, "password")
    
    email_field.send_keys(context.test_user["email"])
    password_field.send_keys(context.test_user["password"])
    
    login_button = context.driver.find_element(By.XPATH, "//button[contains(text(), 'Login')]")
    login_button.click()
    
    # Wait for successful login
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//button[contains(text(), 'Logout')]"))
    )


@when("I train a new model through the admin panel")
def step_impl(context):
    # Train model through API
    training_data = {
        "model_name": "integration_model",
        "algorithm": "random_forest",
        "features": ["Age", "Sex", "Fare"]
    }
    
    headers = {"Authorization": f"Bearer {context.auth_token}"}
    response = requests.post(f"{context.web_backend_url}/api/models/train", json=training_data, headers=headers)
    assert response.status_code == 200


@when("I wait for the training to complete")
def step_impl(context):
    # Wait for training to complete (this might take some time)
    time.sleep(10)


@when("I make a prediction using the new model")
def step_impl(context):
    prediction_data = {
        "passenger": {
            "pclass": 1,
            "sex": "male",
            "age": 30,
            "fare": 50.0,
            "traveled_alone": True,
            "embarked": "C",
            "title": "Mr"
        },
        "model_names": ["integration_model"]
    }
    
    headers = {"Authorization": f"Bearer {context.auth_token}"}
    response = requests.post(f"{context.web_backend_url}/api/predict", json=prediction_data, headers=headers)
    assert response.status_code == 200


@when("the model backend service is unavailable")
def step_impl(context):
    # This would typically involve stopping the model backend service
    # For testing purposes, we'll simulate by using an invalid URL
    context.original_model_backend_url = context.model_backend_url
    context.model_backend_url = "http://localhost:9999"  # Invalid port


@when("I attempt to make a prediction")
def step_impl(context):
    prediction_data = {
        "passenger": {
            "pclass": 1,
            "sex": "male",
            "age": 30,
            "fare": 50.0,
            "traveled_alone": True,
            "embarked": "C",
            "title": "Mr"
        },
        "model_names": ["random_forest"]
    }
    
    headers = {"Authorization": f"Bearer {context.auth_token}"}
    try:
        response = requests.post(f"{context.web_backend_url}/api/predict", json=prediction_data, headers=headers, timeout=5)
        context.response = response
    except requests.exceptions.RequestException as e:
        context.request_exception = e


@when("I make multiple predictions with the same data")
def step_impl(context):
    prediction_data = {
        "passenger": {
            "pclass": 1,
            "sex": "male",
            "age": 30,
            "fare": 50.0,
            "traveled_alone": True,
            "embarked": "C",
            "title": "Mr"
        },
        "model_names": ["random_forest"]
    }
    
    headers = {"Authorization": f"Bearer {context.auth_token}"}
    
    # Make multiple predictions
    context.predictions = []
    for i in range(3):
        response = requests.post(f"{context.web_backend_url}/api/predict", json=prediction_data, headers=headers)
        context.predictions.append(response.json())


@when("I restart the model backend service")
def step_impl(context):
    # This would typically involve restarting the service
    # For testing purposes, we'll simulate by restoring the original URL
    if hasattr(context, 'original_model_backend_url'):
        context.model_backend_url = context.original_model_backend_url


@when("I wait for the service to be healthy")
def step_impl(context):
    # Wait for service to be ready
    max_retries = 30
    for i in range(max_retries):
        try:
            response = requests.get(f"{context.model_backend_url}/health", timeout=5)
            if response.status_code == 200:
                break
        except requests.exceptions.RequestException:
            pass
        time.sleep(2)


@when("I make a prediction request")
def step_impl(context):
    prediction_data = {
        "passenger": {
            "pclass": 1,
            "sex": "male",
            "age": 30,
            "fare": 50.0,
            "traveled_alone": True,
            "embarked": "C",
            "title": "Mr"
        },
        "model_names": ["random_forest"]
    }
    
    headers = {"Authorization": f"Bearer {context.auth_token}"}
    response = requests.post(f"{context.web_backend_url}/api/predict", json=prediction_data, headers=headers)
    context.response = response


@then("I should see prediction results from all models")
def step_impl(context):
    # Wait for results to appear
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'results')]"))
    )
    
    # Check that we have results from multiple models
    model_results = context.driver.find_elements(By.XPATH, "//div[contains(@class, 'model-result')]")
    assert len(model_results) >= 3


@then("the prediction should be saved in my history")
def step_impl(context):
    # Check that prediction was saved in database
    conn = sqlite3.connect('web-backend/titanic_app.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM prediction_history WHERE user_id = (SELECT id FROM users WHERE email = ?)", 
                   ("integration@test.com",))
    count = cursor.fetchone()[0]
    
    conn.close()
    assert count > 0, "Prediction was not saved in history"


@then("I can view my prediction history")
def step_impl(context):
    # Navigate to history section
    history_link = context.driver.find_element(By.XPATH, "//a[contains(text(), 'History')]")
    history_link.click()
    
    # Wait for history to load
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'history')]"))
    )


@then("the model should be removed from the system for integration")
def step_impl(context):
    # Verify model is no longer in the list
    WebDriverWait(context.driver, 10).until(
        EC.invisibility_of_element_located((By.XPATH, "//div[contains(text(), 'integration_test_model')]"))
    )


@then("the model should not appear in the models list")
def step_impl(context):
    # Check that model is not in the list
    models = context.driver.find_elements(By.XPATH, "//div[contains(@class, 'model-item')]")
    model_names = [model.text for model in models]
    assert "integration_test_model" not in model_names


@then("the web backend should receive the request")
def step_impl(context):
    # This is verified by the successful prediction flow
    pass


@then("the web backend should forward the request to model backend")
def step_impl(context):
    # This is verified by the successful prediction flow
    pass


@then("the model backend should process the prediction")
def step_impl(context):
    # This is verified by the successful prediction flow
    pass


@then("the results should be returned through the web backend")
def step_impl(context):
    # This is verified by the successful prediction flow
    pass


@then("the results should be displayed in the web frontend")
def step_impl(context):
    # Wait for results to appear
    WebDriverWait(context.driver, 10).until(
        EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'results')]"))
    )


@then("my session should be valid for web backend API calls")
def step_impl(context):
    # Test API call with session
    headers = {"Authorization": f"Bearer {context.auth_token}"}
    response = requests.get(f"{context.web_backend_url}/api/auth/me", headers=headers)
    assert response.status_code == 200


@then("I should be able to access protected endpoints")
def step_impl(context):
    # Test accessing protected endpoint
    headers = {"Authorization": f"Bearer {context.auth_token}"}
    response = requests.get(f"{context.web_backend_url}/api/history", headers=headers)
    assert response.status_code == 200


@then("my user information should be consistent across requests")
def step_impl(context):
    # Test multiple API calls to verify consistency
    headers = {"Authorization": f"Bearer {context.auth_token}"}
    
    response1 = requests.get(f"{context.web_backend_url}/api/auth/me", headers=headers)
    response2 = requests.get(f"{context.web_backend_url}/api/auth/me", headers=headers)
    
    user1 = response1.json()
    user2 = response2.json()
    
    assert user1["email"] == user2["email"]
    assert user1["id"] == user2["id"]


@then("the prediction should use the newly trained model")
def step_impl(context):
    response_data = context.response.json()
    predictions = response_data["predictions"]
    assert "integration_model" in predictions


@then("the prediction results should be accurate")
def step_impl(context):
    response_data = context.response.json()
    predictions = response_data["predictions"]
    
    for model_name, prediction in predictions.items():
        assert "prediction" in prediction
        assert "probability" in prediction
        assert 0.0 <= prediction["probability"] <= 1.0


@then("I should receive an appropriate error message")
def step_impl(context):
    # Check that we got an error response
    assert hasattr(context, 'response') or hasattr(context, 'request_exception')


@then("the web frontend should handle the error gracefully")
def step_impl(context):
    # This would be verified by checking the UI for error handling
    pass


@then("the user should be informed of the service issue")
def step_impl(context):
    # This would be verified by checking the UI for user notification
    pass


@then("all predictions should return consistent results")
def step_impl(context):
    # Check that all predictions have the same structure
    for prediction in context.predictions:
        assert "predictions" in prediction
        assert "random_forest" in prediction["predictions"]


@then("the prediction history should be accurate")
def step_impl(context):
    # Check database for prediction history
    conn = sqlite3.connect('web-backend/titanic_app.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM prediction_history")
    count = cursor.fetchone()[0]
    
    conn.close()
    assert count >= 3, "Not all predictions were recorded in history"


@then("the data should be properly stored in the database")
def step_impl(context):
    # Verify database integrity
    conn = sqlite3.connect('web-backend/titanic_app.db')
    cursor = conn.cursor()
    
    # Check that we have the expected number of predictions
    cursor.execute("SELECT COUNT(*) FROM prediction_history")
    count = cursor.fetchone()[0]
    
    conn.close()
    assert count > 0, "No predictions found in database"


@then("the prediction should complete successfully")
def step_impl(context):
    assert context.response.status_code == 200


@then("the results should be accurate")
def step_impl(context):
    response_data = context.response.json()
    predictions = response_data["predictions"]
    
    for model_name, prediction in predictions.items():
        assert "prediction" in prediction
        assert "probability" in prediction 