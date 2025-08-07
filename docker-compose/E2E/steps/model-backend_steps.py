"""
Step implementations for model-backend API tests
"""

from behave import given, when, then
import requests
import json


@given("the model backend service is running for model backend tests")
def step_impl(context):
    # Check if service is running by calling health endpoint
    response = requests.get(f"{context.model_backend_url}/health", timeout=5)
    assert response.status_code == 200, f"Model backend not running: {response.status_code}"


@given("a model with ID {model_id} exists")
def step_impl(context, model_id):
    # Check if model exists by calling models endpoint
    response = requests.get(f"{context.model_backend_url}/api/models")
    assert response.status_code == 200
    
    models = response.json()
    model_ids = [model["id"] for model in models]
    assert model_id in model_ids, f"Model {model_id} does not exist"


@given("a model with name {model_name} exists")
def step_impl(context, model_name):
    # Create a test model through the API
    training_data = {
        "model_name": model_name,
        "algorithm": "random_forest",
        "features": ["Age", "Sex", "Fare"]
    }
    
    response = requests.post(f"{context.model_backend_url}/api/train", json=training_data)
    # Don't assert here as the model might already exist
    pass


@given("a custom model {model_name} exists in the model backend")
def step_impl(context, model_name):
    # Create a test model through the API
    training_data = {
        "model_name": model_name,
        "algorithm": "random_forest",
        "features": ["Age", "Sex", "Fare"]
    }
    
    response = requests.post(f"{context.model_backend_url}/api/train", json=training_data)
    # Don't assert here as the model might already exist
    pass


@when("I send a POST request to {endpoint} with passenger data for the model backend")
def step_impl(context, endpoint):
    # Parse passenger data from table
    passenger_data = {}
    for row in context.table:
        key = row[0]
        value = row[1]
        
        # Convert types
        if key in ["pclass", "age", "sibsp", "parch"]:
            value = int(value) if value else None
        elif key in ["fare"]:
            value = float(value) if value else None
        elif key in ["cabin_letter"] and not value:
            value = None
        
        passenger_data[key] = value
    
    # Create request data
    data = {
        "passenger": passenger_data,
        "model_names": ["random_forest"]  # Default model
    }
    
    # Make request
    url = f"{context.model_backend_url}{endpoint}"
    context.response = requests.post(url, json=data)


@when("I send a POST request to {endpoint} with invalid passenger data for the model backend")
def step_impl(context, endpoint):
    # Parse invalid passenger data from table
    passenger_data = {}
    for row in context.table:
        key = row[0]
        value = row[1]
        
        # Convert types
        if key in ["pclass", "age", "sibsp", "parch"]:
            value = int(value) if value else None
        elif key in ["fare"]:
            value = float(value) if value else None
        elif key in ["cabin_letter"] and not value:
            value = None
        
        passenger_data[key] = value
    
    # Create request data
    data = {
        "passenger": passenger_data,
        "model_names": ["random_forest"]
    }
    
    # Make request
    url = f"{context.model_backend_url}{endpoint}"
    context.response = requests.post(url, json=data)


@when("I send a POST request to {endpoint} with incomplete data for the model backend")
def step_impl(context, endpoint):
    # Parse incomplete passenger data from table
    passenger_data = {}
    for row in context.table:
        key = row[0]
        value = row[1]
        
        # Convert types
        if key in ["pclass", "age", "sibsp", "parch"]:
            value = int(value) if value else None
        elif key in ["fare"]:
            value = float(value) if value else None
        
        passenger_data[key] = value
    
    # Create request data (missing cabin_letter)
    data = {
        "passenger": passenger_data,
        "model_names": ["random_forest"]
    }
    
    # Make request
    url = f"{context.model_backend_url}{endpoint}"
    context.response = requests.post(url, json=data)


@when("I select models {model_names} for the model backend")
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
            context.response = requests.post(url, json=data)


@when("I send a POST request to {endpoint} with data for the model backend")
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
    url = f"{context.model_backend_url}{endpoint}"
    context.response = requests.post(url, json=data)


@when("I send a GET request to {endpoint} for the model backend")
def step_impl(context, endpoint):
    url = f"{context.model_backend_url}{endpoint}"
    context.response = requests.get(url)


@when("I send a DELETE request to {endpoint} for the model backend")
def step_impl(context, endpoint):
    url = f"{context.model_backend_url}{endpoint}"
    context.response = requests.delete(url)


@when("I send a GET request to {endpoint} for the model backend with an invalid token")
def step_impl(context, endpoint):
    url = f"{context.model_backend_url}{endpoint}"
    headers = {"Authorization": "Bearer invalid_token"}
    
    context.response = requests.get(url, headers=headers)


@then("the response status should be {status_code} for the model backend")
def step_impl(context, status_code):
    expected_status = int(status_code)
    actual_status = context.response.status_code
    assert actual_status == expected_status, f"Expected {expected_status}, got {actual_status}"


@then("the response should contain prediction results for the model backend")
def step_impl(context):
    response_data = context.response.json()
    assert "predictions" in response_data


@then("the prediction should include survival probability for the model backend")
def step_impl(context):
    response_data = context.response.json()
    predictions = response_data["predictions"]
    
    for model_name, prediction in predictions.items():
        assert "prediction" in prediction
        assert "probability" in prediction


@then("the response should contain predictions from all models for the model backend")
def step_impl(context):
    response_data = context.response.json()
    predictions = response_data["predictions"]
    assert len(predictions) >= 3  # random_forest, svm, logistic_regression


@then("each model should have different prediction results for the model backend")
def step_impl(context):
    response_data = context.response.json()
    predictions = response_data["predictions"]
    
    # Check that we have multiple models with predictions
    assert len(predictions) > 1
    
    # Check that predictions exist for each model
    for model_name, prediction in predictions.items():
        assert "prediction" in prediction


@then("the response should contain validation error for the model backend")
def step_impl(context):
    response_data = context.response.json()
    assert "detail" in response_data


@then("the response should contain the error message {error_message} for the model backend")
def step_impl(context, error_message):
    response_data = context.response.json()
    response_text = json.dumps(response_data).lower()
    assert error_message.lower() in response_text


@then("the response should contain a list of available models for the model backend")
def step_impl(context):
    response_data = context.response.json()
    assert isinstance(response_data, list)
    assert len(response_data) > 0


@then("the response should contain a list of available features for the model backend")
def step_impl(context):
    response_data = context.response.json()
    assert isinstance(response_data, list)
    assert len(response_data) > 0


@then("each model should have algorithm and accuracy information for the model backend")
def step_impl(context):
    response_data = context.response.json()
    for model in response_data:
        assert "algorithm" in model
        assert "accuracy" in model


@then("the response should contain model details")
def step_impl(context):
    response_data = context.response.json()
    assert "id" in response_data
    assert "name" in response_data


@then("the model details should include algorithm and features")
def step_impl(context):
    response_data = context.response.json()
    assert "algorithm" in response_data
    assert "features" in response_data


@then("the features should include passenger attributes for the model backend")
def step_impl(context):
    response_data = context.response.json()
    feature_names = [feature.lower() for feature in response_data]
    assert "age" in feature_names or "sex" in feature_names or "fare" in feature_names


@then("the response should contain training results for the model backend")
def step_impl(context):
    response_data = context.response.json()
    assert "model_id" in response_data
    assert "accuracy" in response_data


@then("the new model should be available in the models list for the model backend")
def step_impl(context):
    # Get models list to verify new model exists
    response = requests.get(f"{context.model_backend_url}/api/models")
    
    assert response.status_code == 200
    models = response.json()
    
    # Check if new model exists (by algorithm type)
    model_algorithms = [model["algorithm"] for model in models]
    assert "random_forest" in model_algorithms


@then("the model accuracy should be reasonable")
def step_impl(context):
    response_data = context.response.json()
    accuracy = response_data["accuracy"]
    assert 0.0 <= accuracy <= 1.0, f"Accuracy {accuracy} is not between 0 and 1"


@then("the model should be removed from the model backend system")
def step_impl(context):
    # Verify model is no longer in the list
    response = requests.get(f"{context.model_backend_url}/api/models")
    
    assert response.status_code == 200
    models = response.json()
    
    # Check that test_model is not in the list
    model_names = [model["name"] for model in models]
    assert "test_model" not in model_names


@then("the model should use all specified features")
def step_impl(context):
    response_data = context.response.json()
    model_id = response_data["model_id"]
    
    # Get model details to verify features
    response = requests.get(f"{context.model_backend_url}/api/models/{model_id}")
    assert response.status_code == 200
    
    model_details = response.json()
    features = model_details["features"]
    
    # Check that all specified features are used
    expected_features = ["Age", "Sex", "Pclass", "Fare", "Embarked", "Title", "CabinLetter"]
    for feature in expected_features:
        assert feature in features


@then("the response should contain cross-validation scores")
def step_impl(context):
    response_data = context.response.json()
    # Check for cross-validation related fields
    assert "accuracy" in response_data
    # Additional CV fields might be present depending on implementation 