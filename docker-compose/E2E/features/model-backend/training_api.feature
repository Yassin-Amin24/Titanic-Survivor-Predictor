@api @model-backend @training
Feature: Model Backend Training API
  As a data scientist
  I want to train new ML models through the API
  So that I can improve prediction accuracy

  Background:
    Given the model backend service is running

  Scenario: Train a new model with valid parameters
    When I send a POST request to "/api/train" with:
      | model_name      | algorithm       | features                    |
      | custom_rf_model | random_forest   | ["Age", "Sex", "Fare"]     |
    Then the response status should be 200
    And the response should contain training results
    And the new model should be available in the models list

  Scenario: Train a model with different algorithm
    When I send a POST request to "/api/train" with:
      | model_name      | algorithm       | features                    |
      | custom_svm_model| svm             | ["Age", "Sex", "Pclass"]   |
    Then the response status should be 200
    And the response should contain training results
    And the model accuracy should be reasonable

  Scenario: Train a model with invalid algorithm
    When I send a POST request to "/api/train" with:
      | model_name      | algorithm       | features                    |
      | invalid_model   | invalid_algo    | ["Age", "Sex", "Fare"]     |
    Then the response status should be 400
    And the response should contain "unsupported algorithm"

  Scenario: Train a model with invalid features
    When I send a POST request to "/api/train" with:
      | model_name      | algorithm       | features                    |
      | custom_model    | random_forest   | ["InvalidFeature"]         |
    Then the response status should be 400
    And the response should contain "invalid features"

  Scenario: Train a model with empty features list
    When I send a POST request to "/api/train" with:
      | model_name      | algorithm       | features |
      | custom_model    | random_forest   | []       |
    Then the response status should be 400
    And the response should contain "features list cannot be empty"

  Scenario: Train a model with duplicate name
    Given a model with name "existing_model" exists
    When I send a POST request to "/api/train" with:
      | model_name      | algorithm       | features                    |
      | existing_model  | random_forest   | ["Age", "Sex", "Fare"]     |
    Then the response status should be 400
    And the response should contain "model name already exists"

  Scenario: Delete an existing model
    Given a custom model "test_model" exists
    When I send a DELETE request to "/api/models/test_model"
    Then the response status should be 200
    And the model should be removed from the system

  Scenario: Delete a non-existent model
    When I send a DELETE request to "/api/models/non_existent_model"
    Then the response status should be 404
    And the response should contain "model not found"

  Scenario: Delete a default model
    When I send a DELETE request to "/api/models/random_forest"
    Then the response status should be 400
    And the response should contain "cannot delete default model"

  Scenario: Train model with all available features
    When I send a POST request to "/api/train" with:
      | model_name      | algorithm       | features                    |
      | full_feature_model | random_forest | ["Age", "Sex", "Pclass", "Fare", "Embarked", "Title", "CabinLetter"] |
    Then the response status should be 200
    And the response should contain training results
    And the model should use all specified features

  Scenario: Train model with cross-validation
    When I send a POST request to "/api/train" with:
      | model_name      | algorithm       | features                    |
      | cv_model        | logistic_regression | ["Age", "Sex", "Fare"] |
    Then the response status should be 200
    And the response should contain cross-validation scores
    And the model accuracy should be reasonable 