# DealBadger Bot

DealBadger Bot is a Python application that scrapes the website dealbadger.com and matches the items with sold items on eBay, Facebook Marketplace, and Craigslist to find profitable arbitrage opportunities. The bot can be set up to run at regular intervals and send email notifications with potential profitable items.

## Features

- Scrapes dealbadger.com for items with a specified time limit.
- Matches scraped items with sold items on eBay, Facebook Marketplace, and Craigslist.
- Calculates profit margins and identifies arbitrage opportunities.
- Sends email and SMS notifications with profitable items.
- Can be run as a GitHub Actions workflow or on an EC2 instance.

## Requirements

- Python 3.x
- The following Python packages (listed in `requirements.txt`):
  - requests
  - ebaysdk
  - beautifulsoup4
  - selenium
  - twilio
  - python-dotenv
  - sendgrid
  - certifi

## Installation

1. Clone the repository:
   ```sh
   git clone https://github.com/yourusername/dealbadger-bot.git
   cd dealbadger-bot


# Steps to run

Install dependencies: pip install -r requirements.txt

main.py --tl [time_limit]

time_limit: It will check bids up to this cutoff point ( i.e 3 will check all of the bids ongoing that are less than 3 hours)
  - might consider adding minutes as wel
