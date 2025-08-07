@api @web-backend @admin
Feature: Web Backend Admin API
  As an admin user
  I want to manage models and users through the API
  So that I can maintain the system

  Background:
    Given the web backend service is running
    And I have admin authentication token

  Scenario: Train a new model with valid parameters
    When I send a POST request to "/api/models/train" with:
      | model_name      | algorithm       | features                    |
      | custom_rf_model | random_forest   | ["Age", "Sex", "Fare"]     |
    Then the response status should be 200
    And the response should contain training results
    And the new model should be available in the models list

  Scenario: Train a model with invalid algorithm
    When I send a POST request to "/api/models/train" with:
      | model_name      | algorithm       | features                    |
      | invalid_model   | invalid_algo    | ["Age", "Sex", "Fare"]     |
    Then the response status should be 400
    And the response should contain "unsupported algorithm"

  Scenario: Train a model with invalid features
    When I send a POST request to "/api/models/train" with:
      | model_name      | algorithm       | features                    |
      | custom_model    | random_forest   | ["InvalidFeature"]         |
    Then the response status should be 400
    And the response should contain "invalid features"

  Scenario: Delete an existing model
    Given a custom model "test_model" exists
    When I send a DELETE request to "/api/models/test_model"
    Then the response status should be 200
    And the model should be removed from the system

  Scenario: Delete a non-existent model
    When I send a DELETE request to "/api/models/non_existent_model"
    Then the response status should be 404
    And the response should contain "model not found"

  Scenario: Get all users as admin
    When I send a GET request to "/api/users"
    Then the response status should be 200
    And the response should contain a list of all users
    And each user should have email and registration date

  Scenario: Delete a user as admin
    Given a user with email "test@example.com" exists
    When I send a DELETE request to "/api/users/1"
    Then the response status should be 200
    And the user should be removed from the system

  Scenario: Delete a non-existent user
    When I send a DELETE request to "/api/users/999"
    Then the response status should be 404
    And the response should contain "user not found"

  Scenario: Access admin endpoints without admin privileges
    Given I have regular user authentication token
    When I send a GET request to "/api/users"
    Then the response status should be 403
    And the response should contain "admin privileges required"

  Scenario: Access admin endpoints without authentication
    When I send a GET request to "/api/users" without authentication
    Then the response status should be 401
    And the response should contain "not authenticated"

  Scenario: Train model without admin privileges
    Given I have regular user authentication token
    When I send a POST request to "/api/models/train" with:
      | model_name      | algorithm       | features                    |
      | custom_model    | random_forest   | ["Age", "Sex", "Fare"]     |
    Then the response status should be 403
    And the response should contain "admin privileges required" 