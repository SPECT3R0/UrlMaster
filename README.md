# UrlMaster

**UrlMaster** is a Python-based tool that automates Google search queries using Playwright, collects `.pk` domain URLs, and saves them into a CSV file. It is useful for gathering website URLs from search results efficiently and can handle multiple search queries over multiple pages.

## Features
- Perform automated Google searches for specified queries.
- Extract `.pk` domain URLs from search results.
- Save URLs into a CSV file in the same directory as the script.
- Handle multiple queries and scrape multiple result pages.
- Display progress using `tqdm`.

## Prerequisites
Before running this project, ensure you have the following dependencies installed:

- **Python 3.7+**
- **Playwright** for browser automation
- **tqdm** for progress bar display

## Installation

1. Clone the repository:
    ```bash
    git clone https://github.com/tkflash/UrlMaster.git
    cd UrlMaster
    ```

2. Install the required dependencies:
    ```bash
    pip install playwright tqdm
    ```

3. Set up Playwright:
    ```bash
    playwright install
    ```

## Usage

1. Modify the list of search queries in the script to suit your needs. By default, the following queries are included:
    ```python
    queries = [
        "pakistan websites",
        "popular websites in pakistan",
        "pakistan web directories",
        "top websites in pakistan",
    ]
    ```

2. Run the script:
    ```bash
    python urlmaster.py
    ```

3. The script will perform Google searches for the provided queries, scrape `.pk` URLs from the search results, and save them into a CSV file named `urls.csv` in the same directory as the script.

## Output

The output CSV file will have the following structure:
```csv
URL
https://example.pk
https://anotherexample.pk
...

## Customization

- **Number of Pages**: You can control how many Google search result pages are scraped by adjusting the `num_pages_per_query` parameter:
    ```python
    urls = collect_urls(queries, num_pages_per_query=3)
    ```
    Increase or decrease the number of pages based on how much data you want to scrape.

- **Headless Mode**: By default, the script runs in visible browser mode. To run the browser in headless mode (without opening a browser window), change the following line in the `google_search_playwright` function:
    ```python
    browser = p.chromium.launch(headless=True)
    ```
    This is useful for running the script on servers or in environments where you don't need to see the browser.

- **Domain Filtering**: By default, the script collects `.pk` domains. You can modify the domain filter by adjusting this line:
    ```python
    if href and re.search(r'\.pk', href):  # Only collect .pk domains
    ```
    For example, to collect `.com` domains, replace `\.pk` with `\.com`. You can also modify this to match any other top-level domain (TLD) according to your needs.

- **Search Queries**: The list of queries used for scraping can be customized. Modify the `queries` list to include the search terms you are interested in:
    ```python
    queries = [
        "pakistan websites",
        "popular websites in pakistan",
        "pakistan web directories",
        "top websites in pakistan",
    ]
    ```
    Add or remove queries to refine the results based on your preferences.

- **CSV Output File**: By default, the script saves URLs into a file called `urls.csv`. If you'd like to save the output under a different name or location, modify the following line:
    ```python
    with open("urls.csv", "w", newline="") as f:
    ```
    Change `"urls.csv"` to your preferred filename or path.


