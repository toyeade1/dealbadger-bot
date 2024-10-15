from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def scrape_facebook_marketplace(item_names, search_limit=10):
    count = 0
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    all_items = []

    try:
        for item_name in item_names:
            base_url = f"https://www.facebook.com/marketplace/search/?query={item_name['title'].replace(' ', '+')}"
            print(f'base_url: {base_url}')

            driver.get(base_url)

            print(f"Scraping Facebook Marketplace for {item_name['title']}...")
            time.sleep(5)  # Wait for content to load

            # exit from the login popup
            try:
                close_button = driver.find_element(By.XPATH, '//div[@aria-label="Close" and @role="button"]')
                close_button.click()
            except Exception as e:
                print("No login popup found or error clicking the close button:", e)
                pass

            # Find all product containers
            try:
                item_containers = driver.find_elements(By.CLASS_NAME, '_4b3n')

                for item in item_containers:
                    while count < search_limit:
                        try:
                            title_element = item.find_element(By.CLASS_NAME, '_7h3e')
                            title = title_element.text.strip() if title_element else None

                            price_element = item.find_element(By.CLASS_NAME, '_4c1k')
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
                            print(f"Error while scraping a Facebook Marketplace item: {e}")
                            continue
            except Exception as e:
                print(f"Error while scraping all Facebook Marketplace items: {e}")
                continue
            

    except Exception as e:
        print(f"Error during Facebook Marketplace scraping: {e}")
    
    driver.quit()

    if count == 10:
        print("Search limit reached. Exiting.")

    return all_items


## trail run

# item_names = [{'title': 'macbook pro'}, {'title': 'iphone 12'}]

# all_items = scrape_facebook_marketplace(item_names, search_limit=10)

# print(all_items)