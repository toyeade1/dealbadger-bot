import json


# load items from json file
def load_items(site):
    with open(f'search_results/{site}_items.json', 'r') as f:
        items = json.load(f)
    return items

# get json dump for items

def get_scraped_average_price(item_name, site):
    average_price = 0
    with open(f'search_results/{site}_items.json', 'r') as f:
        items = json.load(f)
        for item in items:
            if item['searched_item'] == item_name:
                average_price += item['price']
        average_price /= len(items)
    return average_price
    
# calculate profit margin

def profitable_item(site):
    profit_items = []
    dealbadger_items = load_items('dealbadger')

    for item in dealbadger_items:
        try:
            avg_price = get_scraped_average_price(item['title'], site)
            if avg_price:
                profit_margin = (item['price'] - avg_price) / avg_price * 100
                if profit_margin >= 30:
                    print(f"Arbitrage Opportunity: Profit Margin of {profit_margin}%")
                    profit_items.append({
                        'title': item['title'],
                        'dealbadger_price': item['price'],
                        'site_avg_price': avg_price,
                        'profit_margin': profit_margin
                    })

        except Exception as e:
            print(f"Error while calculating profit margin: {e}")
            continue

    with open('search_results/profitable_items.json', "w") as f:
        json.dump(profit_items, f, indent=2)

        
# # Example usage
# dealbadger_price = 50  # Scraped from DealBadger
# avg_sold_price = get_ebay_sold_price("ZINUS Brock Metal And Wood Platform Bed Frame")
# profit_margin = calculate_profit_margin(dealbadger_price, avg_sold_price)

# if profit_margin and profit_margin >= 30:  # Only alert for items with 30% profit margin
#     print(f"Arbitrage Opportunity: Profit Margin of {profit_margin}%")
    


