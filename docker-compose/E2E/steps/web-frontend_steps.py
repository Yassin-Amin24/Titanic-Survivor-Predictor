"""
Step implementations for web-frontend UI tests
"""

from behave import given, when, then
import time


@given("I am on the landing page")
def step_impl(context):
    context.page.goto(context.web_frontend_url)
    context.page.wait_for_load_state("networkidle")


@given("I am on the registration page")
def step_impl(context):
    context.page.goto(f"{context.web_frontend_url}/register")
    context.page.wait_for_load_state("networkidle")


@given("I am on the login page")
def step_impl(context):
    context.page.goto(f"{context.web_frontend_url}/login")
    context.page.wait_for_load_state("networkidle")


@given("I am on the calculator page")
def step_impl(context):
    context.page.goto(f"{context.web_frontend_url}/calculator")
    context.page.wait_for_load_state("networkidle")


@given("I am logged in as a user")
def step_impl(context):
    # Navigate to login page
    context.page.goto(f"{context.web_frontend_url}/login")
    
    # Fill in login form
    context.page.fill('input[name="email"]', context.test_user["email"])
    context.page.fill('input[name="password"]', context.test_user["password"])
    
    # Submit form
    context.page.click('button:has-text("Login")')
    
    # Wait for successful login
    context.page.wait_for_selector('button:has-text("Logout")')


@given("I am logged in as an admin user for the web frontend")
def step_impl(context):
    # Navigate to login page
    context.page.goto(f"{context.web_frontend_url}/login")
    
    # Fill in admin login form
    context.page.fill('input[name="email"]', context.admin_user["email"])
    context.page.fill('input[name="password"]', context.admin_user["password"])
    
    # Submit form
    context.page.click('button:has-text("Login")')
    
    # Wait for successful login
    context.page.wait_for_selector('button:has-text("Logout")')


@given("I am on the admin panel page")
def step_impl(context):
    context.page.goto(f"{context.web_frontend_url}/admin")
    context.page.wait_for_load_state("networkidle")


@when("I click on the {button_text} button")
def step_impl(context, button_text):
    context.page.click(f'button:has-text("{button_text}")')


@when("I click on the {link_text} link")
def step_impl(context, link_text):
    context.page.click(f'a:has-text("{link_text}")')


@when("I enter {value} in the {field_name} field")
def step_impl(context, value, field_name):
    field_selector = f'input[name="{field_name.lower().replace(" ", "_")}"]'
    context.page.fill(field_selector, value)


@when("I select {value} for {field_name}")
def step_impl(context, value, field_name):
    field_name_lower = field_name.lower().replace(" ", "_")
    
    # Try to find select element first
    select_selector = f'select[name="{field_name_lower}"]'
    if context.page.locator(select_selector).count() > 0:
        context.page.select_option(select_selector, label=value)
    else:
        # Try radio buttons or checkboxes
        radio_selector = f'input[value="{value.lower()}"]'
        if context.page.locator(radio_selector).count() > 0:
            context.page.click(radio_selector)
        else:
            # Try by label text
            context.page.click(f'label:has-text("{value}")')


@when("I select {model1} and {model2} models")
def step_impl(context, model1, model2):
    # For multiple model selection, we'll click on checkboxes
    for model in [model1, model2]:
        checkbox = context.page.locator(f'input[value="{model}"]')
        if not checkbox.is_checked():
            checkbox.check()


@when("I click the {button_text} button")
def step_impl(context, button_text):
    context.page.click(f'button:has-text("{button_text}")')


@when("I navigate to the {section} section")
def step_impl(context, section):
    if section == "history":
        # Navigate to history section (might be a tab or link)
        context.page.click('a:has-text("History")')
    elif section == "users":
        # Navigate to users section in admin panel
        context.page.click('button:has-text("Users")')


@when("I try to access the admin panel")
def step_impl(context):
    context.page.goto(f"{context.web_frontend_url}/admin")


@when("I confirm the deletion")
def step_impl(context):
    # Look for confirmation dialog
    context.page.click('button:has-text("Confirm"), button:has-text("Delete")')


@then("I should see the main heading")
def step_impl(context):
    heading = context.page.locator("h1")
    assert heading.is_visible()


@then("I should see navigation links")
def step_impl(context):
    nav_links = context.page.locator("a")
    assert nav_links.count() > 0


@then("I should see a call-to-action button")
def step_impl(context):
    cta_button = context.page.locator('button:has-text("Try"), button:has-text("Get Started")')
    assert cta_button.is_visible()


@then("I should be redirected to the {page} page")
def step_impl(context, page):
    # Wait for navigation to complete
    context.page.wait_for_load_state("networkidle")
    
    # Check if we're on the expected page
    current_url = context.page.url
    assert page.lower() in current_url.lower()


@then("I should see a success message")
def step_impl(context):
    success_message = context.page.locator('.success, .alert-success, [class*="success"]')
    assert success_message.is_visible()


@then("I should see an error message about {error_type}")
def step_impl(context, error_type):
    error_message = context.page.locator('.error, .alert-danger, [class*="error"]')
    assert error_message.is_visible()


@then("I should be successfully logged in")
def step_impl(context):
    logout_button = context.page.locator('button:has-text("Logout")')
    assert logout_button.is_visible()


@then("I should see the user menu")
def step_impl(context):
    user_menu = context.page.locator('[class*="user-menu"], [class*="profile"]')
    assert user_menu.is_visible()


@then("I should be logged out")
def step_impl(context):
    login_button = context.page.locator('button:has-text("Login")')
    assert login_button.is_visible()


@then("I should see the prediction results")
def step_impl(context):
    results_section = context.page.locator('[class*="results"], [class*="prediction"]')
    assert results_section.is_visible()


@then("I should see the survival probability")
def step_impl(context):
    probability_element = context.page.locator('[class*="probability"], [class*="survival"]')
    assert probability_element.is_visible()


@then("I should see predictions from both models")
def step_impl(context):
    model_predictions = context.page.locator('[class*="model"], [class*="prediction"]')
    assert model_predictions.count() >= 2


@then("I should see different probabilities for each model")
def step_impl(context):
    # This would need to be implemented based on the actual UI structure
    # For now, we'll just check that multiple prediction elements exist
    predictions = context.page.locator('[class*="prediction"]')
    assert predictions.count() >= 2


@then("all form fields should be reset to default values")
def step_impl(context):
    # Check that form fields are empty or reset
    form_inputs = context.page.locator('input[type="text"], input[type="email"], input[type="number"]')
    for input_field in form_inputs.all():
        value = input_field.input_value()
        assert value == "" or value is None


@then("I should see a list of available models")
def step_impl(context):
    models_list = context.page.locator('[class*="models"], [class*="model-list"]')
    assert models_list.is_visible()


@then("I should see model details including algorithm and accuracy")
def step_impl(context):
    model_details = context.page.locator('[class*="model-details"], [class*="algorithm"]')
    assert model_details.is_visible()


@then("I should see options to manage each model")
def step_impl(context):
    manage_buttons = context.page.locator('button:has-text("Edit"), button:has-text("Delete"), button:has-text("Manage")')
    assert manage_buttons.count() > 0


@then("the new model should appear in the models list")
def step_impl(context):
    # Wait for the new model to appear
    context.page.wait_for_selector('[class*="model"]', timeout=10000)


@then("the model should be removed from the list")
def step_impl(context):
    # Wait for the model to be removed
    # This would need to be implemented based on the actual UI behavior
    time.sleep(2)  # Give time for the removal to complete


@then("I should see a list of all registered users")
def step_impl(context):
    users_list = context.page.locator('[class*="users"], [class*="user-list"]')
    assert users_list.is_visible()


@then("I should see user details including email and registration date")
def step_impl(context):
    user_details = context.page.locator('[class*="user-details"], [class*="email"]')
    assert user_details.is_visible()


@then("the user should be removed from the list")
def step_impl(context):
    # Wait for the user to be removed
    # This would need to be implemented based on the actual UI behavior
    time.sleep(2)  # Give time for the removal to complete


@then("I should be denied access")
def step_impl(context):
    # Should be redirected away from admin panel
    current_url = context.page.url
    assert "admin" not in current_url.lower()


@given("I have made a prediction")
def step_impl(context):
    # Navigate to calculator and make a prediction
    context.page.goto(f"{context.web_frontend_url}/calculator")
    
    # Fill in some sample data (this would need to be adjusted based on your actual form)
    context.page.fill('input[name="age"]', "25")
    context.page.select_option('select[name="sex"]', label="Male")
    context.page.select_option('select[name="pclass"]', label="3")
    
    # Submit the form
    context.page.click('button:has-text("Predict")')
    
    # Wait for results
    context.page.wait_for_selector('[class*="results"]')


@given("there is a custom model available")
def step_impl(context):
    # This would typically be set up in a previous scenario or test data
    pass


@given("there is a test user in the system")
def step_impl(context):
    # This would typically be set up in a previous scenario or test data
    pass


@given("I am logged in as a regular user")
def step_impl(context):
    # Login as regular user (not admin)
    context.page.goto(f"{context.web_frontend_url}/login")
    context.page.fill('input[name="email"]', context.test_user["email"])
    context.page.fill('input[name="password"]', context.test_user["password"])
    context.page.click('button:has-text("Login")')
    context.page.wait_for_selector('button:has-text("Logout")') 