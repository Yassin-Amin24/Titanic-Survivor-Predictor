@api @model-backend @prediction
Feature: Model Backend Prediction API
  As a client application
  I want to make survival predictions through the model backend
  So that I can get accurate ML model predictions

  Background:
    Given the model backend service is running

  Scenario: Make a prediction with valid passenger data
    When I send a POST request to "/api/predict" with passenger data:
      | pclass | sex   | age | sibsp | parch | fare | embarked | title | cabin_letter |
      | 1      | male  | 30  | 0     | 0     | 50.0 | C        | Mr    | A            |
    And I select models "random_forest"
    Then the response status should be 200
    And the response should contain prediction results
    And the prediction should include survival probability

  Scenario: Make a prediction with multiple models
    When I send a POST request to "/api/predict" with passenger data:
      | pclass | sex     | age | sibsp | parch | fare | embarked | title | cabin_letter |
      | 2      | female  | 25  | 1     | 0     | 75.0 | S        | Miss  | B            |
    And I select models "random_forest", "svm", "logistic_regression"
    Then the response status should be 200
    And the response should contain predictions from all models
    And each model should have different prediction results

  Scenario: Make a prediction with missing optional fields
    When I send a POST request to "/api/predict" with passenger data:
      | pclass | sex   | age | sibsp | parch | fare | embarked | title | cabin_letter |
      | 3      | male  | 35  | 0     | 0     | 25.0 | S        | Mr    |              |
    And I select models "random_forest"
    Then the response status should be 200
    And the response should contain prediction results

  Scenario: Make a prediction with invalid passenger data
    When I send a POST request to "/api/predict" with invalid passenger data:
      | pclass | sex   | age | sibsp | parch | fare | embarked | title | cabin_letter |
      | 5      | male  | 30  | 0     | 0     | 50.0 | C        | Mr    | A            |
    And I select models "random_forest"
    Then the response status should be 422
    And the response should contain validation error

  Scenario: Make a prediction with missing required fields
    When I send a POST request to "/api/predict" with incomplete data:
      | pclass | sex   | age | sibsp | parch | fare | embarked | title |
      | 1      | male  | 30  | 0     | 0     | 50.0 | C        | Mr    |
    And I select models "random_forest"
    Then the response status should be 422
    And the response should contain "field required"

  Scenario: Make prediction with non-existent model
    When I send a POST request to "/api/predict" with passenger data:
      | pclass | sex   | age | sibsp | parch | fare | embarked | title | cabin_letter |
      | 1      | male  | 30  | 0     | 0     | 50.0 | C        | Mr    | A            |
    And I select models "non_existent_model"
    Then the response status should be 400
    And the response should contain "model not found"

  Scenario: Get available models
    When I send a GET request to "/api/models"
    Then the response status should be 200
    And the response should contain a list of available models
    And each model should have algorithm and accuracy information

  Scenario: Get model details by ID
    Given a model with ID "random_forest" exists
    When I send a GET request to "/api/models/random_forest"
    Then the response status should be 200
    And the response should contain model details
    And the model details should include algorithm and features

  Scenario: Get non-existent model details
    When I send a GET request to "/api/models/non_existent_model"
    Then the response status should be 404
    And the response should contain "model not found"

  Scenario: Get available features
    When I send a GET request to "/api/features"
    Then the response status should be 200
    And the response should contain a list of available features
    And the features should include passenger attributes 