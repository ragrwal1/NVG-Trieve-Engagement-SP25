from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set up WebDriver
driver = webdriver.Chrome()

try:
    # Open your Shopify password page
    store_url = "https://ehn5xs-sa.myshopify.com/collections"
    driver.get(store_url)

    # Wait for page to load
    time.sleep(2)

    # Click on the password entry modal
    password_button = driver.find_element(By.CSS_SELECTOR, ".password-link")
    password_button.click()

    # Wait for modal to appear
    time.sleep(1)

    # Locate the password input field
    password_input = driver.find_element(By.ID, "Password")

    # Enter password and submit
    password = "trieve"
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)

    # Wait for login to process
    time.sleep(3)

    print("Password entered successfully!")

finally:
    driver.quit()  # Close the browser