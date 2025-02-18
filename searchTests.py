from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# Set up WebDriver
driver = webdriver.Chrome()

try:
    # --- Step 1: Unlock the Shopify store ---
    store_url = "https://ehn5xs-sa.myshopify.com/password"
    driver.get(store_url)
    time.sleep(2)

    # Click on the password entry modal
    password_button = driver.find_element(By.CSS_SELECTOR, ".password-link")
    password_button.click()
    time.sleep(1)

    # Locate and fill in the password field
    password_input = driver.find_element(By.ID, "Password")
    password = "trieve"
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(3)
    print("Password entered successfully!")

    # --- Step 2: Open a collection page to start search operations ---
    store_url = "https://ehn5xs-sa.myshopify.com/collections/all?"
    driver.get(store_url)
    time.sleep(2)

    # --- Dummy Search to load the new search screen ---
    search_button = driver.find_element(By.CSS_SELECTOR, ".header__icon--search")
    search_button.click()
    time.sleep(1)

    dummy_search_box = driver.find_element(By.ID, "Search-In-Modal")
    dummy_search_box.clear()
    dummy_search_box.send_keys("dummy")
    dummy_search_box.send_keys(Keys.RETURN)
    time.sleep(3)  # Wait for the new search screen to load

    # --- Now perform actual searches on the new search screen ---
    search_queries = ["t-shirt", "hoodie", "jeans"]

    for search_term in search_queries:
        # Re-locate the search input element (avoid stale element)
        search_box = driver.find_element(By.ID, "Search-In-Template")
        search_box.clear()
        search_box.send_keys(search_term)
        search_box.send_keys(Keys.RETURN)
        time.sleep(3)  # Wait for search results to load

        # Extract product titles from search results
        product_titles = driver.find_elements(By.CSS_SELECTOR, ".card__heading a")
        print(f"Search Results for '{search_term}':")
        for title in product_titles:
            print(title.text)
        print("\n")

        # Optionally, if you need to reopen the search modal before the next query,
        # you can click the search icon and wait briefly
        # search_button = driver.find_element(By.CSS_SELECTOR, ".header__icon--search")
        # search_button.click()
        # time.sleep(1)

finally:
    driver.quit()  # Close the browser