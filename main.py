
from scripts import profitable_item
from web_scrapers import scrape_dealbadger, scrapers
import json
import argparse


def main():

    parser = argparse.ArgumentParser(description='Scrape DealBadger with a time limit.')
    parser.add_argument('--tl', type=float, default=3, help='Max time left in hours to scrape an item.')
    
    args = parser.parse_args()
    time_limit = args.tl

    print(f"*********** Scraping DealBadger with a time limit of {time_limit} hours *************/n")

    base_url = "https://dealbadger.com/search"
    all_items = scrape_dealbadger(base_url, time_limit)

    print(f"Scraped a total of {len(all_items)} items.\n")
    print(" *********** Saving items to dealbadger_items.json *************\n")

    with open('search_results/dealbadger_items.json', 'w') as f:
        json.dump(all_items, f, indent=2)
    
    print(" *********** Scraping seller sites for profit margin *************\n")

    scrapers(all_items)

    print(" *********** Calculating Profit Margins *************\n")
    print(" *********** Ebay *************\n")

    profitable_item('ebay', profit_margin_min=30)


    print("Done scraping all items.")


if __name__ == "__main__":
    main()