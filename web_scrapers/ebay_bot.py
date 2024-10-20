from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time

def scrape_ebay(item_names, search_limit=10):
    chrome_options = Options()
    chrome_options.add_argument("--headless")
    driver = webdriver.Chrome(options=chrome_options)

    all_items = []


    try:
        for item_name in item_names:
            base_url = f"https://www.ebay.com/sch/i.html?_nkw={item_name['title'].replace(' ', '+')}&_ipg=100&_sop=13&LH_Sold=1&LH_Complete=1"
            print(f'base_url: {base_url}')

            driver.get(base_url)

            print(f"Scraping eBay for {item_name['title']}...")
            time.sleep(3)

            # Find all product containers
            try:
                item_containers = driver.find_elements(By.CLASS_NAME, 's-item')
                count = 0

                for item in item_containers:
                    if count >= search_limit:
                        break
                    try:
                        title_element = item.find_element(By.CLASS_NAME, 's-item__title')
                        title = title_element.text.strip() if title_element else None

                        try:
                            sold_date_element = item.find_element(By.CLASS_NAME, 's-item__caption--signal')
                            sold_date = sold_date_element.text.strip() if sold_date_element else None
                        except:
                            sold_date = None

                        try:
                            shipping_element = item.find_element(By.CLASS_NAME, 's-item__logisticsCost')
                            shipping = shipping_element.text.strip().replace('+$', '').replace(' shipping', '') if shipping_element else None
                            if shipping == 'Free':
                                shipping = 0

                        except:
                            shipping = None

                        price_element = item.find_element(By.CLASS_NAME, 's-item__price')
                        price = price_element.text.strip().replace('$', '').replace(',', '') if price_element else None

                        if title and price:
                            print(f"Found item: {title} - ${price}")
                            all_items.append({
                                'title': title,
                                'price': float(price) + float(shipping),
                                'sold_date': sold_date,
                                'shipping': shipping,
                                'searched_item': item_name['title']
                            })

                            count += 1
                                
                    except Exception as e:
                        print(f"Error while scraping an eBay item: {e}")
                        continue
            except Exception as e:
                print(f"Error while scraping all eBay items: {e}")
                continue

    except Exception as e:
        print(f"Error during eBay scraping: {e}")
    
    driver.quit()

    if count == search_limit:
        print("Search limit reached. Exiting.")
    
    return all_items


## testing function

# item_names = [{'title': 'macbook pro'}, {'title': 'iphone 12'}]

# all_items = scrape_ebay(item_names, search_limit=10)

# print(all_items)