@api @web-backend @prediction
Feature: Web Backend Prediction API
  As a client application
  I want to make survival predictions through the API
  So that I can analyze passenger data

  Background:
    Given the web backend service is running
    And the model backend service is running

  Scenario: Make a prediction with valid passenger data
    When I send a POST request to "/api/predict" with passenger data:
      | pclass | sex   | age | fare | traveled_alone | embarked | title |
      | 1      | male  | 30  | 50.0 | true          | C        | Mr    |
    And I select models "random_forest"
    Then the response status should be 200
    And the response should contain prediction results
    And the prediction should include survival probability

  Scenario: Make a prediction with multiple models
    When I send a POST request to "/api/predict" with passenger data:
      | pclass | sex     | age | fare | traveled_alone | embarked | title |
      | 2      | female  | 25  | 75.0 | false         | S        | Miss  |
    And I select models "random_forest", "svm", "logistic_regression"
    Then the response status should be 200
    And the response should contain predictions from all models
    And each model should have different prediction results

  Scenario: Make a prediction with invalid passenger data
    When I send a POST request to "/api/predict" with invalid passenger data:
      | pclass | sex   | age | fare | traveled_alone | embarked | title |
      | 5      | male  | 30  | 50.0 | true          | C        | Mr    |
    Then the response status should be 422
    And the response should contain validation error

  Scenario: Make a prediction with missing required fields
    When I send a POST request to "/api/predict" with incomplete data:
      | pclass | sex   | age | fare | embarked | title |
      | 1      | male  | 30  | 50.0 | C        | Mr    |
    Then the response status should be 422
    And the response should contain "field required"

  Scenario: Get available models
    When I send a GET request to "/api/models"
    Then the response status should be 200
    And the response should contain a list of available models
    And each model should have algorithm and accuracy information

  Scenario: Get available features
    When I send a GET request to "/api/features"
    Then the response status should be 200
    And the response should contain a list of available features
    And the features should include passenger attributes

  Scenario: Get prediction history for authenticated user
    Given I have a valid authentication token
    And I have made previous predictions
    When I send a GET request to "/api/history"
    Then the response status should be 200
    And the response should contain prediction history
    And each history item should have passenger data and predictions

  Scenario: Get prediction history without authentication
    When I send a GET request to "/api/history" without authentication
    Then the response status should be 401
    And the response should contain "not authenticated"

  Scenario: Make prediction with non-existent model
    When I send a POST request to "/api/predict" with passenger data:
      | pclass | sex   | age | fare | traveled_alone | embarked | title |
      | 1      | male  | 30  | 50.0 | true          | C        | Mr    |
    And I select models "non_existent_model"
    Then the response status should be 400
    And the response should contain "model not found" 