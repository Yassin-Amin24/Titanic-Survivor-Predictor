@ui @web-frontend @calculator
Feature: Survival Calculator
  As a user
  I want to predict Titanic survival probability
  So that I can analyze passenger data

  Background:
    Given I am on the calculator page

  Scenario: Calculate survival with valid passenger data
    When I select "1" for passenger class
    And I select "male" for sex
    And I enter "30" for age
    And I enter "50.0" for fare
    And I select "Yes" for traveled alone
    And I select "C" for embarked
    And I select "Mr" for title
    And I select "Random Forest" model
    And I click the "Predict" button
    Then I should see the prediction results
    And I should see the survival probability

  Scenario: Calculate survival with multiple models
    When I select "2" for passenger class
    And I select "female" for sex
    And I enter "25" for age
    And I enter "75.0" for fare
    And I select "No" for traveled alone
    And I select "S" for embarked
    And I select "Miss" for title
    And I select "Random Forest" and "SVM" models
    And I click the "Predict" button
    Then I should see predictions from both models
    And I should see different probabilities for each model

  Scenario: Validate required fields
    When I leave the age field empty
    And I click the "Predict" button
    Then I should see an error message about required fields

  Scenario: View prediction history
    Given I am logged in as a user
    And I have made a prediction
    When I navigate to the history section
    Then I should see my previous predictions
    And I should see the passenger details and results

  Scenario: Clear calculator form
    When I fill in all the passenger data
    And I click the "Clear" button
    Then all form fields should be reset to default values 