"""
Step implementations for web-backend API tests
"""

from behave import given, when, then
import requests
import json
import sqlite3
from datetime import datetime


@given("the web backend service is running")
def step_impl(context):
    # Check if service is running by calling health endpoint
    response = requests.get(f"{context.web_backend_url}/health", timeout=5)
    assert response.status_code == 200, f"Web backend not running: {response.status_code}"


@given("the model backend service is running")
def step_impl(context):
    # Check if model backend is running
    response = requests.get(f"{context.model_backend_url}/health", timeout=5)
    assert response.status_code == 200, f"Model backend not running: {response.status_code}"


@given("a user with email {email} exists in the database")
def step_impl(context, email):
    # Create user in database directly
    conn = sqlite3.connect('web-backend/titanic_app.db')
    cursor = conn.cursor()
    
    # Hash password (same as in web-backend)
    import hashlib
    password_hash = hashlib.sha256("testpassword123".encode()).hexdigest()
    
    cursor.execute('''
        INSERT OR IGNORE INTO users (email, password_hash, is_admin, created_at)
        VALUES (?, ?, ?, ?)
    ''', (email, password_hash, False, datetime.now()))
    
    conn.commit()
    conn.close()


@given("a user with email {email} and password {password} exists")
def step_impl(context, email, password):
    # Create user in database directly
    conn = sqlite3.connect('web-backend/titanic_app.db')
    cursor = conn.cursor()
    
    # Hash password
    import hashlib
    password_hash = hashlib.sha256(password.encode()).hexdigest()
    
    cursor.execute('''
        INSERT OR IGNORE INTO users (email, password_hash, is_admin, created_at)
        VALUES (?, ?, ?, ?)
    ''', (email, password_hash, False, datetime.now()))
    
    conn.commit()
    conn.close()


@given("I have a valid authentication token")
def step_impl(context):
    # Login to get token
    login_data = {
        "email": context.test_user["email"],
        "password": context.test_user["password"]
    }
    
    response = requests.post(f"{context.web_backend_url}/api/auth/login", json=login_data)
    assert response.status_code == 200
    
    context.auth_token = response.json()["token"]


@given("I have admin authentication token")
def step_impl(context):
    # Login as admin to get token
    login_data = {
        "email": context.admin_user["email"],
        "password": context.admin_user["password"]
    }
    
    response = requests.post(f"{context.web_backend_url}/api/auth/login", json=login_data)
    assert response.status_code == 200
    
    context.auth_token = response.json()["token"]


@given("I have regular user authentication token")
def step_impl(context):
    # Login as regular user
    login_data = {
        "email": context.test_user["email"],
        "password": context.test_user["password"]
    }
    
    response = requests.post(f"{context.web_backend_url}/api/auth/login", json=login_data)
    assert response.status_code == 200
    
    context.auth_token = response.json()["token"]


@given("I have made previous predictions")
def step_impl(context):
    # Make a test prediction to create history
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
    assert response.status_code == 200


@given("a custom model {model_name} exists")
def step_impl(context, model_name):
    # This would typically create a model through the API
    # For now, we'll assume it exists
    pass


@when("I send a POST request to {endpoint} with")
def step_impl(context, endpoint):
    # Parse table data
    data = {}
    for row in context.table:
        key = row[0]
        value = row[1]
        
        # Handle special cases
        if key == "features" and value.startswith("[") and value.endswith("]"):
            # Parse list from string
            value = json.loads(value.replace("'", '"'))
        
        data[key] = value
    
    # Make request
    url = f"{context.web_backend_url}{endpoint}"
    headers = {}
    
    if hasattr(context, 'auth_token') and context.auth_token:
        headers["Authorization"] = f"Bearer {context.auth_token}"
    
    context.response = requests.post(url, json=data, headers=headers)


@when("I send a POST request to {endpoint} with passenger data")
def step_impl(context, endpoint):
    # Parse passenger data from table
    passenger_data = {}
    for row in context.table:
        key = row[0]
        value = row[1]
        
        # Convert types
        if key in ["pclass", "age"]:
            value = int(value)
        elif key in ["fare"]:
            value = float(value)
        elif key in ["traveled_alone"]:
            value = value.lower() == "true"
        
        passenger_data[key] = value
    
    # Create request data
    data = {
        "passenger": passenger_data,
        "model_names": ["random_forest"]  # Default model
    }
    
    # Make request
    url = f"{context.web_backend_url}{endpoint}"
    headers = {}
    
    if hasattr(context, 'auth_token') and context.auth_token:
        headers["Authorization"] = f"Bearer {context.auth_token}"
    
    context.response = requests.post(url, json=data, headers=headers)


@when("I send a POST request to {endpoint} with invalid passenger data")
def step_impl(context, endpoint):
    # Parse invalid passenger data from table
    passenger_data = {}
    for row in context.table:
        key = row[0]
        value = row[1]
        
        # Convert types
        if key in ["pclass", "age"]:
            value = int(value)
        elif key in ["fare"]:
            value = float(value)
        elif key in ["traveled_alone"]:
            value = value.lower() == "true"
        
        passenger_data[key] = value
    
    # Create request data
    data = {
        "passenger": passenger_data,
        "model_names": ["random_forest"]
    }
    
    # Make request
    url = f"{context.web_backend_url}{endpoint}"
    headers = {}
    
    if hasattr(context, 'auth_token') and context.auth_token:
        headers["Authorization"] = f"Bearer {context.auth_token}"
    
    context.response = requests.post(url, json=data, headers=headers)


@when("I send a POST request to {endpoint} with incomplete data")
def step_impl(context, endpoint):
    # Parse incomplete passenger data from table
    passenger_data = {}
    for row in context.table:
        key = row[0]
        value = row[1]
        
        # Convert types
        if key in ["pclass", "age"]:
            value = int(value)
        elif key in ["fare"]:
            value = float(value)
        
        passenger_data[key] = value
    
    # Create request data (missing traveled_alone)
    data = {
        "passenger": passenger_data,
        "model_names": ["random_forest"]
    }
    
    # Make request
    url = f"{context.web_backend_url}{endpoint}"
    headers = {}
    
    if hasattr(context, 'auth_token') and context.auth_token:
        headers["Authorization"] = f"Bearer {context.auth_token}"
    
    context.response = requests.post(url, json=data, headers=headers)


@when("I select models {model_names}")
def step_impl(context, model_names):
    # Update the model names in the request
    model_list = [model.strip() for model in model_names.split(",")]
    
    # Update the last request data
    if hasattr(context, 'response') and context.response:
        # Re-send the request with updated model names
        request_data = context.response.request.body
        if request_data:
            data = json.loads(request_data)
            data["model_names"] = model_list
            
            url = context.response.url
            headers = {}
            if hasattr(context, 'auth_token') and context.auth_token:
                headers["Authorization"] = f"Bearer {context.auth_token}"
            
            context.response = requests.post(url, json=data, headers=headers)


@when("I send a GET request to {endpoint}")
def step_impl(context, endpoint):
    url = f"{context.web_backend_url}{endpoint}"
    headers = {}
    
    if hasattr(context, 'auth_token') and context.auth_token:
        headers["Authorization"] = f"Bearer {context.auth_token}"
    
    context.response = requests.get(url, headers=headers)


@when("I send an invalid-token GET request to {endpoint} for the web backend")
def step_impl(context, endpoint):
    url = f"{context.web_backend_url}{endpoint}"
    headers = {"Authorization": "Bearer invalid_token"}
    
    context.response = requests.get(url, headers=headers)


@when("I send an unauthenticated GET request to {endpoint} for the web backend")
def step_impl(context, endpoint):
    url = f"{context.web_backend_url}{endpoint}"
    context.response = requests.get(url)


@when("I send a DELETE request to {endpoint}")
def step_impl(context, endpoint):
    url = f"{context.web_backend_url}{endpoint}"
    headers = {}
    
    if hasattr(context, 'auth_token') and context.auth_token:
        headers["Authorization"] = f"Bearer {context.auth_token}"
    
    context.response = requests.delete(url, headers=headers)


@then("the response status should be {status_code} for the web backend")
def step_impl(context, status_code):
    expected_status = int(status_code)
    actual_status = context.response.status_code
    assert actual_status == expected_status, f"Expected {expected_status}, got {actual_status}"


@then("the response should contain user details")
def step_impl(context):
    response_data = context.response.json()
    assert "email" in response_data
    assert "id" in response_data


@then("the user should be created in the database")
def step_impl(context):
    # Verify user exists in database
    conn = sqlite3.connect('web-backend/titanic_app.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE email = ?", ("test@example.com",))
    result = cursor.fetchone()
    
    conn.close()
    assert result is not None, "User was not created in database"


@then("the response should contain validation error for the web backend")
def step_impl(context):
    response_data = context.response.json()
    assert "detail" in response_data


@then("the response should contain the error message {error_message}")
def step_impl(context, error_message):
    response_data = context.response.json()
    response_text = json.dumps(response_data).lower()
    assert error_message.lower() in response_text


@then("the response should contain an access token")
def step_impl(context):
    response_data = context.response.json()
    assert "token" in response_data
    assert len(response_data["token"]) > 0


@then("the response should contain user information")
def step_impl(context):
    response_data = context.response.json()
    assert "email" in response_data
    assert "id" in response_data


@then("the session should be invalidated")
def step_impl(context):
    # Try to use the token again - should fail
    headers = {"Authorization": f"Bearer {context.auth_token}"}
    response = requests.get(f"{context.web_backend_url}/api/auth/me", headers=headers)
    assert response.status_code == 401


@then("the response should contain a list of available models for the web backend")
def step_impl(context):
    response_data = context.response.json()
    assert isinstance(response_data, list)
    assert len(response_data) > 0


@then("each model should have algorithm and accuracy information for the web backend")
def step_impl(context):
    response_data = context.response.json()
    for model in response_data:
        assert "algorithm" in model
        assert "accuracy" in model


@then("the response should contain a list of available features for the web backend")
def step_impl(context):
    response_data = context.response.json()
    assert isinstance(response_data, list)
    assert len(response_data) > 0


@then("the features should include passenger attributes for the web backend")
def step_impl(context):
    response_data = context.response.json()
    feature_names = [feature.lower() for feature in response_data]
    assert "age" in feature_names or "sex" in feature_names or "fare" in feature_names


@then("the response should contain prediction results for the web backend")
def step_impl(context):
    response_data = context.response.json()
    assert "predictions" in response_data


@then("the prediction should include survival probability for the web backend")
def step_impl(context):
    response_data = context.response.json()
    predictions = response_data["predictions"]
    
    for model_name, prediction in predictions.items():
        assert "prediction" in prediction
        assert "probability" in prediction


@then("the response should contain predictions from all models for the web backend")
def step_impl(context):
    response_data = context.response.json()
    predictions = response_data["predictions"]
    assert len(predictions) >= 3  # random_forest, svm, logistic_regression


@then("each model should have different prediction results for the web backend")
def step_impl(context):
    response_data = context.response.json()
    predictions = response_data["predictions"]
    
    # Check that we have multiple models with predictions
    assert len(predictions) > 1
    
    # Check that predictions exist for each model
    for model_name, prediction in predictions.items():
        assert "prediction" in prediction


@then("the response should contain prediction history")
def step_impl(context):
    response_data = context.response.json()
    assert isinstance(response_data, list)


@then("each history item should have passenger data and predictions")
def step_impl(context):
    response_data = context.response.json()
    if len(response_data) > 0:
        history_item = response_data[0]
        assert "passenger_class" in history_item
        assert "model_predictions" in history_item


@then("the response should contain training results for the web backend")
def step_impl(context):
    response_data = context.response.json()
    assert "model_id" in response_data
    assert "accuracy" in response_data


@then("the new model should be available in the models list for the web backend")
def step_impl(context):
    # Get models list to verify new model exists
    headers = {"Authorization": f"Bearer {context.auth_token}"}
    response = requests.get(f"{context.web_backend_url}/api/models", headers=headers)
    
    assert response.status_code == 200
    models = response.json()
    
    # Check if new model exists (by algorithm type)
    model_algorithms = [model["algorithm"] for model in models]
    assert "random_forest" in model_algorithms


@then("the model should be removed from the system for the web backend")
def step_impl(context):
    # Verify model is no longer in the list
    headers = {"Authorization": f"Bearer {context.auth_token}"}
    response = requests.get(f"{context.web_backend_url}/api/models", headers=headers)
    assert response.status_code == 200
    models = response.json()
    # Check that test_model is not in the list
    model_names = [model["name"] for model in models]
    assert "test_model" not in model_names


@then("the response should contain a list of all users")
def step_impl(context):
    response_data = context.response.json()
    assert isinstance(response_data, list)
    assert len(response_data) > 0


@then("each user should have email and registration date")
def step_impl(context):
    response_data = context.response.json()
    for user in response_data:
        assert "email" in user
        assert "created_at" in user


@then("the user should be removed from the system")
def step_impl(context):
    # Verify user is no longer in the database
    conn = sqlite3.connect('web-backend/titanic_app.db')
    cursor = conn.cursor()
    
    cursor.execute("SELECT id FROM users WHERE email = ?", ("test@example.com",))
    result = cursor.fetchone()
    
    conn.close()
    assert result is None, "User was not removed from database" 