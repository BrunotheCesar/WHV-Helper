#!/usr/bin/env python3

import time
from lxml import html
import requests
from os import system, name 

# Settings
MAXRESULTS = 30
WAIT = 3000 # In seconds
# Type of work you're looking for
SEARCH = "receptionist"

# Expected salary, leave as it is if entry-level or low skilled job 
salaryValues = ["0", "30000", "40000", "50000", "60000", "70000", "80000", "100000", "120000", "150000", "200000", "999999"]
SALMIN = salaryValues[0]
SALMAX = salaryValues[-1]

locations = ["All-Auckland", "Queenstown-Otago", "All-Wellington"]
LOCATION = locations[2]

# Page to be scraped
link = "https://www.seek.co.nz/"+SEARCH+"-jobs/in-"+LOCATION+"?salaryrange="+SALMIN+"-"+SALMAX+"&salarytype=annual&sortmode=ListedDate"

def scrapeSeek():
    # Get page data from server, block redirects
    response = requests.get(link)

    dom = html.fromstring(response.content)

    # loop over results
    for advertList in dom.xpath('//*[@data-automation="searchResults"]/div/div[2]'):
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()))
        for advert in advertList.xpath('div')[:MAXRESULTS]:
            # Headline and advertiser
            try:
                advertiser = advert.xpath('article/span[5]/span/a/text()')[0]
            except IndexError:
                advertiser = advert.xpath('article/span[5]/span/span[2]/text()')[0]

            print(advert.xpath('article/span[2]/span/h1/a/text()')[0], " : ",advertiser)

            # Blurb
            print(advert.xpath('article/span[6]/span/text()')[0])

            # Location
            city = advert.xpath('article/div/span[2]/span/strong/span/span/text()')[0]
            city = city.split(":")[1].strip()
            try:
                suburb = advert.xpath('article/div/span[2]/span/span/span/text()')[0]
                suburb = suburb.split(":")[1].strip()
            except IndexError:
                suburb = ""
            print(city+" / " +suburb)
            # Salary
            try:
                print(advert.xpath('article/div/span[3]/span/text()')[0])
            except IndexError:
                print("No salary provided.")
            # Age of ad
            print("Listed: "+advert.xpath('article/span[4]/span/span/text()')[0])
            print("XXXXXXXXXXXXXXX\n")

# Infinite loop
while True:
    scrapeSeek()
    time.sleep(WAIT)