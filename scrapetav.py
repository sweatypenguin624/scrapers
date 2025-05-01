from tavily import TavilyClient
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import os
import csv
import logging
from datetime import datetime
from webdriver_manager.chrome import ChromeDriverManager

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Get or set your Tavily API key
api_key = "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"
if not api_key:
    api_key = input("Please enter your Tavily API key: ")
    os.environ["TAVILY_API_KEY"] = api_key

# Initialize Tavily client
try:
    client = TavilyClient(api_key=api_key)
    logger.info("Tavily client initialized successfully.")
except Exception as e:
    logger.error(f"Failed to initialize Tavily client: {str(e)}")
    raise

# Set up Selenium WebDriver
def setup_driver():
    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Run in headless mode
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.0.0 Safari/537.36")
    driver = webdriver.Chrome(options=chrome_options, service=webdriver.ChromeService(ChromeDriverManager().install()))
    return driver

def scrape_product_details(driver, url):
    """
    Scrape price and rating from a single IndiaMart product page using Selenium.
    """
    try:
        driver.get(url)
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div.prd-card-simple')))

        # Extract price (assuming it's in a class like 'prc.cur')
        price_element = driver.find_elements(By.CLASS_NAME, 'prc.cur')
        price = price_element[0].text.strip() if price_element else "Price not found"

        # Extract rating (assuming it's in a class like 'rtg-val')
        rating_element = driver.find_elements(By.CLASS_NAME, 'rtg-val')
        rating = rating_element[0].text.strip() if rating_element else "Rating not found"

        return {"price": price, "rating": rating}

    except (TimeoutException, NoSuchElementException) as e:
        logger.error(f"Error scraping {url}: {str(e)}")
        return {"price": "Error", "rating": "Error"}
    except Exception as e:
        logger.error(f"Unexpected error scraping {url}: {str(e)}")
        return {"price": "Error", "rating": "Error"}

def scrape_indiamart_with_tavily_and_selenium(search_query, max_results=10):
    """
    Use Tavily to find URLs and Selenium to scrape prices and ratings from IndiaMart.
    """
    logger.info(f"Starting search for '{search_query}' on IndiaMart...")

    # First, use Tavily to get search result URLs
    try:
        response = client.search(
            query=f"{search_query} site:dir.indiamart.com",
            max_results=max_results,
            search_depth="advanced",
            include_domains=["dir.indiamart.com"],
            exclude_domains=[],
        )

        results = response.get("results", [])
        if not results:
            logger.warning("No results found for the query.")
            return []

        products = []
        driver = setup_driver()

        for result in results:
            url = result.get("url", "")
            title = result.get("title", "No title")
            snippet = result.get("content", "No content available")

            # Scrape detailed data using Selenium
            details = scrape_product_details(driver, url)
            
            product_data = {
                "title": title,
                "url": url,
                "snippet": snippet,
                "source": "IndiaMart via Tavily",
                "price": details["price"],
                "rating": details["rating"]
            }
            products.append(product_data)
            logger.info(f"Scraped details for {title}")

        driver.quit()

        # Save to CSV
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"indiamart_{search_query.replace(' ', '_')}_{timestamp}.csv"

        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ["title", "url", "snippet", "source", "price", "rating"]
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

            writer.writeheader()
            for product in products:
                writer.writerow(product)

        logger.info(f"Saved {len(products)} records to {filename}")

        return products

    except Exception as e:
        logger.error(f"Error during scraping process: {str(e)}")
        return []

if __name__ == "__main__":
    search_term = input("Enter product to search on IndiaMart (e.g., 'Apple iPhone'): ")
    products = scrape_indiamart_with_tavily_and_selenium(search_term, max_results=10)

    if products:
        print(f"\nScraped {len(products)} products. Check the CSV file for details.")
    else:
        print("No products found or scraping failed.")