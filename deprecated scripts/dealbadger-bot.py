import requests
from bs4 import BeautifulSoup
import time
import json

def scrape_dealbadger(base_url):
    items = []
    
    while True:
        try:
            print(f"Scraping page {page}...")

            url = f"{base_url}&page={page}"
            response = requests.get(url)
            if response.status_code != 200:
                print(f"Failed to retrieve page {page}, status code: {response.status_code}")
                break
            
            # Parse the JSON response
            data = json.loads(response.text)
            html_content = data.get('html', '')
            
            if not html_content:
                print(f"No more items found on page {page}. Ending scrape.")
                break

            soup = BeautifulSoup(html_content, 'html.parser')
            
            # Find all product card containers
            product_cards = soup.select('.productCardGrid')

            if not product_cards:
                print(f"No items found on page {page}. Ending scrape.")
                break

            for card in product_cards:
                try:
                    # Extract the product title
                    title_element = card.select_one('h2.gridProdTitle')
                    title = title_element.text.strip() if title_element else "No Title Found"
                    
                    # Extract the product price
                    price_element = card.select_one('.price span')
                    price = price_element.text.strip().replace('$', '').replace(',', '') if price_element else "0.00"

                    # Extract the time left for the auction
                    time_left_element = card.select_one('.pvTimerView h6')
                    time_left = time_left_element.text.strip() if time_left_element else "No Time Left"
                    
                    print(f"Found item: {title} - ${price} - Time left: {time_left}")
                    
                    items.append({
                        'title': title,
                        'price': float(price),
                        'time_left': time_left
                    })
                except Exception as e:
                    print(f"Error while scraping an item: {e}")
                    continue
            
            # Move to the next page
            page += 1
            time.sleep(2)  # Sleep to avoid overwhelming the server
        except Exception as e:
            print(f"Error on page {page}: {e}")
            break

    return items

base_url = "https://dealbadger.com/search"

all_items = scrape_dealbadger(base_url)
print(f"Scraped a total of {len(all_items)} items.")

# Optionally, you can save the results to a file
with open('dealbadger_items.json', 'w') as f:
    json.dump(all_items, f, indent=2)
