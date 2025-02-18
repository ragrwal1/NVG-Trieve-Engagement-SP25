from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time

# ----- Configuration -----
search_queries = ["t-shirt", "hoodie", "jeans"]

search_bars = {
    1: {"element_id": "Search-In-Template", "type": "real", "description": "Primary search bar"},
    2: {"element_id": None, "type": "dummy", "description": "Secondary search bar (dummy)"},
    3: {"element_id": None, "type": "dummy", "description": "Tertiary search bar (dummy)"}
}

# Dictionary to store all logs and results
results_log = {
    "website_open_time": None,
    "search_bars": {1: [], 2: [], 3: []}
}

# ----- Helper Functions -----
def run_search(driver, search_bar, query):
    """
    Runs a search for the given query using the specified search bar.
    Captures detailed timing information.

    Returns:
        run_time (float): Total duration of the search action.
        search_latency (float): Time from hitting Enter to getting results.
        results (list): List of search results.
    """
    start_time = time.time()
    
    if search_bar["type"] == "real":
        search_box = driver.find_element(By.ID, search_bar["element_id"])
        search_box.clear()
        search_box.send_keys(query)

        # Log time when Enter is pressed
        enter_pressed_time = time.time()
        search_box.send_keys(Keys.RETURN)

        # Wait for search results to load
        time.sleep(3)  
        
        # Log time when results are retrieved
        results_loaded_time = time.time()

        results_elements = driver.find_elements(By.CSS_SELECTOR, ".card__heading a")
        results = [elem.text for elem in results_elements if elem.text]
    else:
        time.sleep(0.00001)  # Simulated near-instant search
        results = [f"Dummy result for '{query}'"]
        enter_pressed_time = start_time  # For logging consistency
        results_loaded_time = start_time + 0.00001  # Minimal time delay

    # Calculate times
    run_time = results_loaded_time - start_time
    search_latency = results_loaded_time - enter_pressed_time

    return run_time, search_latency, results


def print_results_log(log, search_bars_config, overall_time):
    """Prints out the full log of times and results."""
    print("=== Test Results Log ===")
    print(f"Website Open Time: {log['website_open_time']:.4f} seconds")
    
    for bar_id, entries in log["search_bars"].items():
        description = search_bars_config[bar_id]["description"]
        print(f"\nSearch Bar {bar_id} ({description}):")
        for entry in entries:
            print(f" Query: {entry['query']}")
            print(f"  Total Run Time: {entry['run_time']:.4f} sec")
            print(f"  Search Latency (Enter to Results): {entry['search_latency']:.4f} sec")
            print(f"  Results: {entry['results']}")
    
    print(f"\nOverall Test Run Time: {overall_time:.4f} seconds")


# ----- Main Test Flow -----
driver = webdriver.Chrome()

try:
    overall_start = time.time()

    # --- Step 1: Unlock the Shopify store ---
    store_url = "https://ehn5xs-sa.myshopify.com/password"
    driver.get(store_url)
    time.sleep(2)

    password_button = driver.find_element(By.CSS_SELECTOR, ".password-link")
    password_button.click()
    time.sleep(1)

    password_input = driver.find_element(By.ID, "Password")
    password = "trieve"
    password_input.send_keys(password)
    password_input.send_keys(Keys.RETURN)
    time.sleep(3)
    print("Password entered successfully!")

    # --- Step 2: Open collection page & prepare search ---
    collection_url = "https://ehn5xs-sa.myshopify.com/collections/all?"
    collection_start = time.time()
    driver.get(collection_url)
    time.sleep(2)

    search_button = driver.find_element(By.CSS_SELECTOR, ".header__icon--search")
    search_button.click()
    time.sleep(1)

    dummy_search_box = driver.find_element(By.ID, "Search-In-Modal")
    dummy_search_box.clear()
    dummy_search_box.send_keys("dummy")
    dummy_search_box.send_keys(Keys.RETURN)
    time.sleep(3)

    results_log["website_open_time"] = time.time() - collection_start

    # --- Perform searches ---
    for query in search_queries:
        for bar_id, bar_config in search_bars.items():
            run_time, search_latency, search_results = run_search(driver, bar_config, query)
            results_log["search_bars"][bar_id].append({
                "query": query,
                "run_time": run_time,
                "search_latency": search_latency,
                "results": search_results
            })

    overall_run_time = time.time() - overall_start

finally:
    driver.quit()

# Print out the results log to the console.
print_results_log(results_log, search_bars, overall_run_time)