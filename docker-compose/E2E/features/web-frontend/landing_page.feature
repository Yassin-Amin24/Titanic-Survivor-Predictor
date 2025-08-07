@ui @web-frontend
Feature: Landing Page
  As a user
  I want to access the landing page
  So that I can learn about the Titanic survival prediction service

  Background:
    Given I am on the landing page

  Scenario: View landing page content
    Then I should see the main heading
    And I should see navigation links
    And I should see a call-to-action button

  Scenario: Navigate to calculator from landing page
    When I click on the "Try Calculator" button
    Then I should be redirected to the calculator page

  Scenario: Navigate to login from landing page
    When I click on the "Login" link
    Then I should be redirected to the login page

  Scenario: Navigate to register from landing page
    When I click on the "Register" link
    Then I should be redirected to the registration page 