# # dealbadger-bot

bot that scrapes the website dealbadger.com and matches the items with sold items on ebay, facebook and craigslist to find out it they are profitable for arbitrage opportunities.

will setup as either a github actions workflow or host on a VM with intervals of 12 hours and connect to a mailing service to send me emails twice a day of potential profitable items.

# TODOS:

- Set up mailing service
- Add links to the json object to make it easier to navigate each product when i get the email
- fix profit margin calculations ( currently backwards - comparing ebay to dealbadger )
- host on machine other than local
- make fasterrr

# Steps to run

Install dependencies: pip install -r requirements.txt

main.py -t [time_limit]

time_limit: It will check bids up to this cutoff point ( i.e 3 will check all of the bids ongoing that are less than 3 hours)
  - might consider adding minutes as wel
