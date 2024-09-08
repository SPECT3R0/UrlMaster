import os
import csv
import time
from tqdm import tqdm
from playwright.sync_api import sync_playwright, TimeoutError as PlaywrightTimeoutError
import re
import urllib.parse

# Function to perform Google search using Playwright and extract URLs
def google_search_playwright(query, num_pages=3):
    urls = []
    
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Set headless=True to run without a visible browser
        page = browser.new_page()
        
        try:
            print(f"Performing search using URL bar for query: {query}")
            
            # Encode the query for the URL bar
            encoded_query = urllib.parse.quote(query)
            search_url = f"https://www.google.com/search?q={encoded_query}"
            
            # Navigate to the Google search results directly via the URL bar
            page.goto(search_url, timeout=60000)  # Timeout set to 60 seconds
            
            # Wait for the results to load
            print(f"Waiting for search results to load...")
            page.wait_for_selector('h3', timeout=30000)  # Timeout after 30 seconds if results don't load
            
            for page_num in range(num_pages):
                print(f"Scraping page {page_num + 1} for URLs...")
                
                # Extract URLs from search results
                search_results = page.locator('a[href]')
                for i in range(search_results.count()):
                    href = search_results.nth(i).get_attribute('href')
                    if href and re.search(r'\.pk', href):  # Only collect .pk domains
                        urls.append(href)
                
                # Try to go to the next page if available
                next_button = page.locator('a#pnnext')
                if next_button.count() > 0:
                    print(f"Clicking next page button (page {page_num + 1})...")
                    next_button.click()
                    time.sleep(3)  # Pause to load the next page
                else:
                    print(f"No more pages available after page {page_num + 1}.")
                    break
            
        except PlaywrightTimeoutError as e:
            print(f"Timeout error while interacting with Google: {e}")
        except Exception as e:
            print(f"An unexpected error occurred: {e}")
        finally:
            browser.close()
    
    return urls

# Function to collect URLs for multiple queries and show progress
def collect_urls(queries, num_pages_per_query):
    all_urls = set()  # Using a set to avoid duplicate URLs
    total_queries = len(queries)
    
    # Progress bar for queries
    with tqdm(total=total_queries, desc="Collecting URLs", unit="query") as pbar:
        for query in queries:
            print(f"\nSearching: {query}")
            urls = google_search_playwright(query, num_pages_per_query)
            if urls:
                print(f"Found {len(urls)} URLs for query: {query}")
            else:
                print(f"No URLs found for query: {query}")
            
            all_urls.update(urls)
            print(f"Total URLs collected so far: {len(all_urls)}\n")
            pbar.update(1)  # Update the progress bar
            time.sleep(2)  # Slight pause for good measure
    
    return list(all_urls)

# Function to save URLs to a CSV file in the same directory as the Python script
def save_urls_to_csv(urls, file_name):
    # Get the directory where the script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Combine the script directory with the file name to save the file in the same location
    file_path = os.path.join(script_dir, file_name)
    
    # Ensure the file is created if it doesn't exist
    file_exists = os.path.isfile(file_path)
    
    if not file_exists:
        print(f"File {file_path} does not exist. Creating a new one.")
    
    # Open the file in 'w' mode, which creates it if it doesn't exist
    with open(file_path, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["URL"])  # Write the header
        for url in urls:
            writer.writerow([url])
    print(f"URLs have been successfully saved to {file_path}.")

# Example search queries for content
queries = [
    "pakistan websites",
    "popular websites in pakistan",
    "pakistan web directories",
    "top websites in pakistan",
]

# Get URLs spread over multiple queries
urls = collect_urls(queries, num_pages_per_query=3)  # Adjust the number of pages per query

# Specify the file name
csv_file = "urls.csv"

# Save URLs to the CSV file
save_urls_to_csv(urls, csv_file)

print(f"\nCollected {len(urls)} URLs in total.")
