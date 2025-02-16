from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set up WebDriver
driver = webdriver.Chrome()

try:
    # Step 1: Open Shopify password page and unlock store
    store_url = "https://ehn5xs-sa.myshopify.com/password"
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

    # Step 2: Perform search operation after unlocking store
    store_url = "https://ehn5xs-sa.myshopify.com/collections/all?"
    driver.get(store_url)

    # Wait for page to load
    time.sleep(2)

    # Open the search modal
    search_button = driver.find_element(By.CSS_SELECTOR, ".header__icon--search")
    search_button.click()

    # Wait for search input to be available
    time.sleep(1)

    # Locate the search input field
    search_box = driver.find_element(By.ID, "Search-In-Modal")

    # Enter search term and press Enter
    search_term = "t-shirt"
    search_box.send_keys(search_term)
    search_box.send_keys(Keys.RETURN)

    # Wait for results to load
    time.sleep(3)

    # Extract product titles from search results
    product_titles = driver.find_elements(By.CSS_SELECTOR, ".card__heading a")

    print("Search Results:")
    for title in product_titles:
        print(title.text)

finally:
    driver.quit()  # Close the browser