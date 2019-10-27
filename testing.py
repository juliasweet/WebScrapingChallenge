import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import time

hemisphere_dictionary = []
hemisphere_data = {"Image": [] , "URL": []}

USGS_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
browser = Browser("chrome", headless = False)
browser.visit(USGS_url)
time.sleep(3)

home = browser.html
USGSsoup = bs(home, "html.parser")
headings = USGSsoup.find_all("h3")

for heading in headings:
    title = heading.text
    print(title)
    browser.click_link_by_partial_text(title)
    time.sleep(3)
    img_url = browser.find_link_by_partial_href("download")["href"]
    print(img_url)
    hemisphere_data = {"Image": title, "URL": img_url}
    hemisphere_dictionary.append(hemisphere_data)
    time.sleep(3)
    browser.visit(USGS_url)

print(hemisphere_dictionary)