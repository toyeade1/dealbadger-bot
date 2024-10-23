from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import re
import time
import json

def parse_time_left(time_left_str):
    """
    Parses a time string in multiple possible formats:
    '01D: 19H:22M:37S', '11H:26M:25S', '26M:25S', '25S'
    and returns the total time left in hours.
    """
    # Initialize variables
    days = hours = minutes = seconds = 0

    # Patterns to match the different formats
    day_pattern = r'(\d+)D'
    hour_pattern = r'(\d+)H'
    minute_pattern = r'(\d+)M'
    second_pattern = r'(\d+)S'

    # Extract days, hours, minutes, and seconds if they exist
    days_match = re.search(day_pattern, time_left_str)
    hours_match = re.search(hour_pattern, time_left_str)
    minutes_match = re.search(minute_pattern, time_left_str)
    seconds_match = re.search(second_pattern, time_left_str)

    # Parse each matched group if present
    if days_match:
        days = int(days_match.group(1))
    if hours_match:
        hours = int(hours_match.group(1))
    if minutes_match:
        minutes = int(minutes_match.group(1))
    if seconds_match:
        seconds = int(seconds_match.group(1))

    # Convert the total time to hours
    total_hours = days * 24 + hours + minutes / 60 + seconds / 3600
    if total_hours:
        return total_hours
    return None

def scrape_dealbadger(base_url, time_limit=3):

    chrome_options = Options()
    chrome_options.add_argument("--headless")  # Enables headless mode
    chrome_options.add_argument("--disable-gpu")  # Disable GPU acceleration (optional, but recommended)
    driver = webdriver.Chrome(options=chrome_options)

    driver.get(base_url)
    items = []

    while True:
        try:
            print(f"Scraping current page...")
            time.sleep(3)  # Wait for the page to load

            print('Filtering Decatur and Electronics...')
            all_locations = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[1]/div[1]/button/span[1]').click()
            categories_header = driver.find_element(By.XPATH, '//*[@id="megaMenu"]/div[3]/div/div/ul/li[1]')
            categories_header.click()
            time.sleep(3)
            categories = driver.find_element(By.XPATH, '//*[@id="root"]/div/div[1]/div[1]/div[2]/button/span[1]').click()
            time.sleep(1)
            electronics = driver.find_element(By.XPATH, '//*[@id="megaMenu"]/div[3]/div/div/div[3]/div[2]/ul/li[2]').click()
            time.sleep(3)

            # Find all product containers (assuming each product is in a div with a common class like 'productCardGrid')
            item_containers = driver.find_elements(By.CLASS_NAME, 'productCardGrid')
            if not item_containers:
                print(f"No items found on the current page. Ending scrape.")
                break

            for item in item_containers:
                try:
                    # Extract product title (h2 element with class 'gridProdTitle')
                    title_element = item.find_element(By.CLASS_NAME, 'gridProdTitle')
                    title = title_element.text.strip() if title_element else None

                    # Extract price (span inside the 'price' class div)
                    price_element = item.find_element(By.CLASS_NAME, 'price').find_element(By.TAG_NAME, 'span')
                    price = price_element.text.strip().replace('$', '').replace(',', '') if price_element else None

                    # Extract remaining time (h6 element inside 'pvTimerView' class div)
                    time_element = item.find_element(By.CLASS_NAME, 'pvTimerView').find_element(By.TAG_NAME, 'h6')
                    time_left = time_element.text.strip() if time_element else None

                    total_hours = parse_time_left(time_left)
                    if total_hours is not None and total_hours < time_limit:
                        if title and price and time_left:
                            print(f"Found item: {title} - ${price} - Time left: {time_left}")
                            items.append({
                                'title': title,
                                'price': float(price),
                                'price_with_premium': float(price) * 1.17,
                                'time_left': time_left
                            })
                        else:
                            print("Could not find all details for an item.")
                    else:
                        # Break the loop if the time left is more than x hours (since items are ordered by time)
                        print(f"Encountered an item with more than {time_limit} hours left: {time_left}. Stopping further scraping.")
                        break

                except Exception as e:
                    print(f"Error while scraping an item: {e}")
                    continue

            # Stop scraping further pages if we already encountered an item with more than x hours left
            if total_hours is not None and total_hours >= time_limit:
                break

            # Check if there's a next page by looking for the "next" button
            next_button = WebDriverWait(driver, 10).until(EC.element_to_be_clickable((By.XPATH, '//button[@aria-label="Go to next page"]')))
            print('Next button found!!')

            if next_button:
                print("Moving to the next page...")
                
                # Scroll to the next button
                driver.execute_script("arguments[0].scrollIntoView(true);", next_button)
                time.sleep(1)  # Wait for the scrolling to finish

                # Click the button using JavaScript
                driver.execute_script("arguments[0].click();", next_button)
                time.sleep(3)  # Wait for the next page to load

            else:
                print("No next page found. Scraping complete.")
                break

        except Exception as e:
            print(f"Error during scraping: {e}")
            break

    driver.quit()
    return items