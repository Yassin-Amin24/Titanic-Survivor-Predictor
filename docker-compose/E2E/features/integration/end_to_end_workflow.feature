@integration @e2e
Feature: End-to-End Titanic Survival Prediction Workflow
  As a user
  I want to complete a full prediction workflow
  So that I can analyze passenger survival probability

  Background:
    Given all services are running
    And I am a registered user

  Scenario: Complete user registration and prediction workflow
    When I register a new user account
    And I login to the application
    And I navigate to the calculator page
    And I enter passenger data for prediction
    And I select multiple models for comparison
    And I submit the prediction request
    Then I should see prediction results from all models
    And the prediction should be saved in my history
    And I can view my prediction history

  Scenario: Admin workflow for model management
    Given I am logged in as an admin user
    When I access the admin panel
    And I view the current models list
    And I train a new custom model
    And I verify the new model is available
    And I delete the custom model
    Then the model should be removed from the system
    And the model should not appear in the models list

  Scenario: Cross-service prediction workflow
    When I make a prediction through the web frontend
    Then the web backend should receive the request
    And the web backend should forward the request to model backend
    And the model backend should process the prediction
    And the results should be returned through the web backend
    And the results should be displayed in the web frontend

  Scenario: User authentication across services
    When I login through the web frontend
    Then my session should be valid for web backend API calls
    And I should be able to access protected endpoints
    And my user information should be consistent across requests

  Scenario: Model training and prediction integration
    Given I am logged in as an admin user
    When I train a new model through the admin panel
    And I wait for the training to complete
    And I make a prediction using the new model
    Then the prediction should use the newly trained model
    And the prediction results should be accurate

  Scenario: Error handling across services
    When the model backend service is unavailable
    And I attempt to make a prediction
    Then I should receive an appropriate error message
    And the web frontend should handle the error gracefully
    And the user should be informed of the service issue

  Scenario: Data consistency across services
    When I make multiple predictions with the same data
    Then all predictions should return consistent results
    And the prediction history should be accurate
    And the data should be properly stored in the database

  Scenario: Performance under load
    When multiple users make predictions simultaneously
    Then all predictions should complete successfully
    And the response times should be reasonable
    And no data should be lost or corrupted

  Scenario: Service recovery after restart
    When I restart the model backend service
    And I wait for the service to be healthy
    And I make a prediction request
    Then the prediction should complete successfully
    And the results should be accurate 