from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, NoSuchElementException
import time

def parse_price(price_str):
    """
    Parse price string that might be a range and return a single float value.
    For ranges, returns the average of the min and max prices.
    """
    price_str = price_str.replace('$', '').replace(',', '').strip()
    
    if ' to ' in price_str:
        # Handle price range
        try:
            low, high = map(float, price_str.split(' to '))
            return (low + high) / 2
        except ValueError as e:
            print(f"Error parsing price range '{price_str}': {e}")
            return None
    else:
        # Handle single price
        try:
            return float(price_str)
        except ValueError as e:
            print(f"Error parsing single price '{price_str}': {e}")
            return None

def scrape_ebay(item_names, search_limit=10):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")
    driver = webdriver.Chrome(options=chrome_options)
    wait = WebDriverWait(driver, 10)

    all_items = []

    try:
        for item_name in item_names:
            base_url = f"https://www.ebay.com/sch/i.html?_nkw={item_name['title'].replace(' ', '+')}&_ipg=100&_sop=13&LH_Sold=1&LH_Complete=1"
            print(f'base_url: {base_url}')

            driver.get(base_url)
            time.sleep(3)  # Allow page to load fully

            # Wait for the main container to load
            try:
                results_container = wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "#srp-river-results > ul"))
                )
            except TimeoutException:
                print(f"Timeout waiting for results container for {item_name['title']}")
                continue

            # Find all product containers
            try:
                # Using both the new container selector and the traditional class name as backup
                item_containers = results_container.find_elements(By.CSS_SELECTOR, "li.s-item")
                count = 0

                for item in item_containers:
                    if count >= search_limit:
                        break
                    try:
                        # Try multiple selectors for title
                        try:
                            title_element = item.find_element(By.CSS_SELECTOR, ".s-item__title")
                            title = title_element.text.strip() if title_element else None
                        except NoSuchElementException:
                            continue

                        # Try multiple selectors for price
                        try:
                            price_element = item.find_element(By.CSS_SELECTOR, ".s-item__price")
                            if not price_element:
                                # Try the specific XPath as backup
                                price_element = item.find_element(By.XPATH, ".//div[contains(@class, 's-item__details')]//span[contains(@class, 's-item__price')]")
                            price_str = price_element.text.strip() if price_element else None
                            price = parse_price(price_str) if price_str else None
                        except NoSuchElementException:
                            continue

                        # Get sold date
                        try:
                            sold_date_element = item.find_element(By.CSS_SELECTOR, ".s-item__caption--signal, .POSITIVE")
                            sold_date = sold_date_element.text.strip() if sold_date_element else None
                        except NoSuchElementException:
                            sold_date = None

                        # Get shipping cost
                        try:
                            shipping_element = item.find_element(By.CSS_SELECTOR, ".s-item__shipping, .s-item__logisticsCost")
                            shipping_text = shipping_element.text.strip()
                            if 'Free' in shipping_text:
                                shipping = '0'
                            else:
                                shipping = ''.join(filter(str.isdigit, shipping_text.replace('.', '')))
                                shipping = shipping[:-2] + '.' + shipping[-2:] if shipping else '0'
                        except NoSuchElementException:
                            shipping = '0'

                        if title and price and price is not None:
                            try:
                                shipping_float = float(shipping)
                                
                                print(f"Found item: {title} - ${price} (+ ${shipping_float} shipping)")
                                all_items.append({
                                    'title': title,
                                    'price': price + shipping_float,
                                    'sold_date': sold_date,
                                    'shipping': shipping_float,
                                    'searched_item': item_name['title']
                                })
                                count += 1
                            except ValueError as e:
                                print(f"Error converting shipping to float: {e}")
                                continue
                                
                    except Exception as e:
                        print(f"Error while scraping an eBay item: {e}")
                        continue

            except Exception as e:
                print(f"Error while scraping all eBay items: {e}")
                continue

    except Exception as e:
        print(f"Error during eBay scraping: {e}")
    finally:
        driver.quit()

    if all_items:
        print(f"Successfully scraped {len(all_items)} items")
    else:
        print("No items were successfully scraped")
    
    return all_items


## testing function

# item_names = [{'title': 'macbook pro'}, {'title': 'iphone 12'}]

# all_items = scrape_ebay(item_names, search_limit=10)

# print(all_items)