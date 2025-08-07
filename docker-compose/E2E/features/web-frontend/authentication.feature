@ui @web-frontend @auth
Feature: User Authentication
  As a user
  I want to register and login to the application
  So that I can access personalized features

  Background:
    Given I am on the registration page

  Scenario: Register a new user
    When I enter "test@example.com" in the email field
    And I enter "testpassword123" in the password field
    And I click the "Register" button
    Then I should see a success message
    And I should be redirected to the login page

  Scenario: Register with invalid email
    When I enter "invalid-email" in the email field
    And I enter "testpassword123" in the password field
    And I click the "Register" button
    Then I should see an error message about invalid email

  Scenario: Register with weak password
    When I enter "test@example.com" in the email field
    And I enter "123" in the password field
    And I click the "Register" button
    Then I should see an error message about password requirements

  Scenario: Login with valid credentials
    Given I am on the login page
    When I enter "test@example.com" in the email field
    And I enter "testpassword123" in the password field
    And I click the "Login" button
    Then I should be successfully logged in
    And I should see the user menu

  Scenario: Login with invalid credentials
    Given I am on the login page
    When I enter "wrong@example.com" in the email field
    And I enter "wrongpassword" in the password field
    And I click the "Login" button
    Then I should see an error message about invalid credentials

  Scenario: Logout from application
    Given I am logged in as a user
    When I click on the logout button
    Then I should be logged out
    And I should be redirected to the landing page 