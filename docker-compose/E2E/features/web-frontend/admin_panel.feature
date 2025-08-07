@ui @web-frontend @admin
Feature: Admin Panel
  As an admin user
  I want to manage models and users
  So that I can maintain the system

  Background:
    Given I am logged in as an admin user
    And I am on the admin panel page

  Scenario: View available models
    Then I should see a list of available models
    And I should see model details including algorithm and accuracy
    And I should see options to manage each model

  Scenario: Train a new model
    When I click on "Train New Model"
    And I select "Random Forest" algorithm
    And I select features "Age", "Sex", "Fare"
    And I click the "Train Model" button
    Then I should see a success message
    And the new model should appear in the models list

  Scenario: Delete an existing model
    Given there is a custom model available
    When I click the "Delete" button for the custom model
    And I confirm the deletion
    Then the model should be removed from the list
    And I should see a success message

  Scenario: View user management
    When I navigate to the users section
    Then I should see a list of all registered users
    And I should see user details including email and registration date

  Scenario: Delete a user
    Given there is a test user in the system
    When I click the "Delete" button for the test user
    And I confirm the deletion
    Then the user should be removed from the list
    And I should see a success message

  Scenario: Access admin panel without admin privileges
    Given I am logged in as a regular user
    When I try to access the admin panel
    Then I should be denied access
    And I should see an error message 