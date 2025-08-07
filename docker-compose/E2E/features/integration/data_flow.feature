@integration @data-flow
Feature: Data Flow and Consistency Across Services
  As a system administrator
  I want to ensure data flows correctly between services
  So that the system maintains data integrity

  Background:
    Given all services are running
    And the database is properly initialized

  Scenario: User data consistency across services
    When I create a user through the web backend API
    And I login through the web frontend
    And I access user profile information
    Then the user data should be consistent across all requests
    And the user session should be properly maintained

  Scenario: Prediction data flow validation
    When I submit a prediction request through the web frontend
    And I check the web backend database
    And I verify the model backend processed the request
    Then the prediction data should be consistent across all services
    And the prediction history should be properly recorded

  Scenario: Model data synchronization
    When I train a new model through the model backend
    And I check the model availability in web backend
    And I verify the model appears in web frontend
    Then the model information should be synchronized across services
    And the model should be accessible for predictions

  Scenario: Database transaction integrity
    When I make a prediction request
    And the request is processed by multiple services
    And I check the database state
    Then all database transactions should be completed successfully
    And no partial data should be left in the database

  Scenario: Error propagation across services
    When the model backend returns an error
    And the error propagates through the web backend
    And the error reaches the web frontend
    Then the error should be properly handled at each layer
    And the user should receive a meaningful error message

  Scenario: Data validation across service boundaries
    When I submit invalid data through the web frontend
    And the data is validated by the web backend
    And the data reaches the model backend
    Then validation should occur at appropriate service boundaries
    And invalid data should be rejected with proper error messages

  Scenario: Concurrent data access
    When multiple users access the same data simultaneously
    And they perform conflicting operations
    Then the system should handle concurrent access properly
    And data integrity should be maintained

  Scenario: Data backup and recovery
    When I backup the current system state
    And I simulate a system failure
    And I restore from the backup
    Then all data should be properly restored
    And the system should function normally

  Scenario: API version compatibility
    When I use an older version of the API
    And I interact with newer service versions
    Then the system should handle version differences gracefully
    And backward compatibility should be maintained

  Scenario: Service discovery and health checks
    When I check the health of all services
    And I verify service dependencies
    And I test service communication
    Then all services should be discoverable
    And health checks should accurately reflect service status 