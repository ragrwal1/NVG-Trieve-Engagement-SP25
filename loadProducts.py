import csv
import re
import ijson
import os
from thefuzz import fuzz
from tqdm import tqdm

FILE_PATH = "/Users/ragrwal/Downloads/kith.json"
CSV_OUTPUT_DIR = "/Users/ragrwal/Downloads/products_csvs"

def process_products(file_path, csv_output_dir):
    total_matching = 0
    product_list = []

    # Open the file and use ijson to stream each product item
    with open(file_path, 'r', encoding='utf-8') as f:
        products = ijson.items(f, 'item')
        for product in products:
            product_name = product.get("title", "Unknown Product")

            # Extract price from the first variant (if available)
            price = "Unknown Price"
            if "variants" in product and isinstance(product["variants"], list) and product["variants"]:
                price = product["variants"][0].get("price", "Unknown Price")

            # Convert price to a float value for comparison.
            try:
                price_value = float(price)
            except (ValueError, TypeError):
                price_value = 0.0

            # Clean product description: remove HTML and extra spaces.
            raw_description = product.get("body_html", "")
            clean_description = re.sub(r'<[^>]+>', ' ', raw_description)
            clean_description = re.sub(r'\s+', ' ', clean_description).strip()

            # Count words in the cleaned description.
            description_word_count = len(clean_description.split())

            # Check conditions: description must have more than 5 words and price > 0.50.
            if description_word_count > 5 and price_value > 0.50:
                total_matching += 1
                product_list.append({
                    "title": product_name,
                    "price": price,
                    "description": clean_description
                })

    # Remove duplicate names using fuzzy matching (93% similarity threshold)
    unique_products = []
    seen_titles = []
    
    print("Filtering duplicates...")
    for product in tqdm(product_list, desc="Processing Products", unit="product"):
        title = product["title"]
        is_duplicate = False

        for seen_title in seen_titles:
            if fuzz.ratio(title.lower(), seen_title.lower()) >= 90:
                is_duplicate = True
                break

        if not is_duplicate:
            unique_products.append(product)
            seen_titles.append(title)

    # Ensure output directory exists
    os.makedirs(csv_output_dir, exist_ok=True)

    # Split data into 6 equal parts
    chunk_size = len(unique_products) // 6
    if chunk_size == 0:
        chunk_size = 1  # Ensure at least one file is created if the dataset is small
    
    for i in range(6):
        start_idx = i * chunk_size
        end_idx = (i + 1) * chunk_size if i < 5 else len(unique_products)
        chunk = unique_products[start_idx:end_idx]
        csv_output_path = os.path.join(csv_output_dir, f'products_part_{i+1}.csv')
        
        with open(csv_output_path, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.DictWriter(file, fieldnames=["Title", "Price", "Description"])
            writer.writeheader()
            for product in chunk:
                writer.writerow({
                    "Title": product["title"],
                    "Price": product["price"],
                    "Description": product["description"]
                })

    print(f"CSV files saved in directory: {csv_output_dir}")

if __name__ == "__main__":
    process_products(FILE_PATH, CSV_OUTPUT_DIR)