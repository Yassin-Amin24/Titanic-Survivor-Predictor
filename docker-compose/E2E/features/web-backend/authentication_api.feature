@api @web-backend @auth
Feature: Web Backend Authentication API
  As a client application
  I want to authenticate users through the API
  So that I can access protected resources

  Background:
    Given the web backend service is running

  Scenario: Register a new user successfully
    When I send a POST request to "/api/auth/register" with:
      | email              | password        |
      | test@example.com   | testpassword123 |
    Then the response status should be 201
    And the response should contain user details
    And the user should be created in the database

  Scenario: Register with invalid email format
    When I send a POST request to "/api/auth/register" with:
      | email           | password        |
      | invalid-email   | testpassword123 |
    Then the response status should be 422
    And the response should contain validation error

  Scenario: Register with existing email
    Given a user with email "existing@example.com" exists
    When I send a POST request to "/api/auth/register" with:
      | email                | password        |
      | existing@example.com | testpassword123 |
    Then the response status should be 400
    And the response should contain "email already registered"

  Scenario: Login with valid credentials
    Given a user with email "test@example.com" and password "testpassword123" exists
    When I send a POST request to "/api/auth/login" with:
      | email              | password        |
      | test@example.com   | testpassword123 |
    Then the response status should be 200
    And the response should contain an access token
    And the response should contain user information

  Scenario: Login with invalid credentials
    When I send a POST request to "/api/auth/login" with:
      | email              | password        |
      | test@example.com   | wrongpassword   |
    Then the response status should be 401
    And the response should contain "invalid credentials"

  Scenario: Get current user information with valid token
    Given I have a valid authentication token
    When I send a GET request to "/api/auth/me"
    Then the response status should be 200
    And the response should contain user information

  Scenario: Get current user information with invalid token
    When I send a GET request to "/api/auth/me" with invalid token
    Then the response status should be 401
    And the response should contain "invalid or expired token"

  Scenario: Logout with valid token
    Given I have a valid authentication token
    When I send a POST request to "/api/auth/logout"
    Then the response status should be 200
    And the session should be invalidated

  Scenario: Access protected endpoint without authentication
    When I send a GET request to "/api/history" without authentication
    Then the response status should be 401
    And the response should contain "not authenticated" 