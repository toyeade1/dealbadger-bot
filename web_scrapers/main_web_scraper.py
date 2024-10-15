from .craiglist_bot import scrape_craigslist
from .ebay_bot import scrape_ebay
from .fb_marketplace_bot import scrape_facebook_marketplace
import json

import concurrent.futures

def scrapers(item_names):
    with concurrent.futures.ThreadPoolExecutor() as executor:
        future_ebay = executor.submit(scrape_ebay, item_names)

        

        ## Currently deprecated functions for facebook and craigslist will update later

        # future_facebook = executor.submit(scrape_facebook_marketplace, item_names)
        # future_craigslist = executor.submit(scrape_craigslist, item_names)

        ebay_items = future_ebay.result()



        ## Currently deprecated functions for facebook and craigslist will update later

        # facebook_items = future_facebook.result()
        # craigslist_items = future_craigslist.result()

        print(f"eBay Results completed")
        with open('search_results/ebay_items.json', 'w') as f:
            json.dump(ebay_items, f, indent=2)



        ## Currently deprecated functions for facebook and craigslist will update later

        # print(f"Facebook Marketplace Results completed")
        # with open('search_results/facebook_items.json', 'w') as f:
        #     json.dump(facebook_items, f, indent=2)

        # print(f"Craigslist Results completed")
        # with open('search_results/craigslist_items.json', 'w') as f:
        #     json.dump(craigslist_items, f, indent=2)


