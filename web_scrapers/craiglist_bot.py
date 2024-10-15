from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def scrape_craigslist(item_names, search_limit=10):
    count = 0
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    all_items = []

    try:
        for item_name in item_names:

            base_url = f"https://www.craigslist.org/search/sss?query={item_name['title'].replace(' ', '+')}&sort=rel"
            print(f'base_url: {base_url}')
            driver.get(base_url)

            print(f"Scraping Craigslist for {item_name['title']}...")
            time.sleep(3)

            # Find all product containers
            item_containers = driver.find_elements(By.CLASS_NAME, 'result-row')

            for item in item_containers:
                while count < search_limit:
                    try:
                        title_element = item.find_element(By.CLASS_NAME, 'result-title')
                        title = title_element.text.strip() if title_element else None

                        price_element = item.find_element(By.CLASS_NAME, 'result-price')
                        price = price_element.text.strip().replace('$', '').replace(',', '') if price_element else None

                        if title and price:
                            print(f"Found item: {title} - ${price}")
                            all_items.append({
                                'title': title,
                                'price': float(price),
                                'searched_item': item_name['title']
                            })
                        count += 1
                    except Exception as e:
                        print(f"Error while scraping a Craigslist item: {e}")
                        continue

    except Exception as e:
        print(f"Error during Craigslist scraping: {e}")
    
    driver.quit()

    if count == 10:
        print("Search limit reached. Exiting.")
    
    return all_items
