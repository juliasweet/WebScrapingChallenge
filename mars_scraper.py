import pandas as pd
from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import time

def scrape_mars():

  # NASA News
  executable_path = {'executable_path': 'chromedriver.exe'}
  browser = Browser('chrome', **executable_path, headless=False)
  NASAurl = 'https://mars.nasa.gov/news/'
  browser.visit(NASAurl)
  html = browser.html
  NASAsoup = bs(html, 'html.parser')
  NASAtitle1 = NASAsoup.find('div', class_ = 'content_title').text
  NASAparagraph1 = NASAsoup.find('div', class_ = 'article_teaser_body').text

  # ### Scrape JPL Mars Space Images -- Featured Image
  # Set the URL and visit the page. 
  JPLurl = 'https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars'
  browser.visit(JPLurl)
  # Navigate to the full image using a button.
  browser.click_link_by_partial_text('FULL IMAGE')
  time.sleep(3)
  # And again
  browser.click_link_by_partial_text('more info')
  time.sleep(3)
  # Make some Jet Propulsion soup
  html = browser.html
  JPLsoup = bs(html, 'html.parser')
  # Get the URL
  # Get the relative first
  # Get the lede figure
  # # Get the src (relative path)
  relative_path = JPLsoup.select_one('figure.lede a').get('href')
  # Add it to the end of the full path
  full_path = f'https://www.jpl.nasa.gov{relative_path}'
  print(full_path)

  # ### Scrape Mars Weather Twitter account. 
  #     # 
  # Use Splinter.
  # Set URL path and visit
  MWRurl = 'https://twitter.com/marswxreport?lang=en'
  browser.visit(MWRurl)
  # Make Twitter soup
  html=browser.html
  MWRsoup= bs(html, 'html.parser')
  # Get the weather info by scraping
  mars_weather = MWRsoup.find('p', class_="TweetTextSize TweetTextSize--normal js-tweet-text tweet-text").text
  print(mars_weather)
  ### Scrape Space Facts Mars page
  # Use Pandas

  # Set path and visit
  SFMurl = 'https://space-facts.com/mars/'
  # Set tables
  Marstable= pd.read_html(SFMurl)
  # Make a DF. Need second table (index 1)
  MarsDF = Marstable[1]
  # Give the table descriptive column names
  MarsDF.columns = ['Description', 'Value']
  # Set the index to Description column
  MarsDF.set_index('Description')
  # # Convert to html and export as an html file
  MarsDF.to_html('MarsFacts_table.html')
  print(Marstable)

  # # ### Scrape USGS Astrogeology site for images of Mars' hemispheres
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
    time.sleep(3)
    title = heading.text
    print(title)
    browser.click_link_by_partial_text(title)
    time.sleep(3)
    full_url = browser.find_link_by_partial_href("download")["href"]
    print(full_url)
    hemisphere_data = {"Image": title, "URL": full_url}
    hemisphere_dictionary.append(hemisphere_data)
    time.sleep(3)
    browser.visit(USGS_url)

  ## Make results dictionary

  Mars_dict = {"Headline": NASAtitle1, "Summary": NASAparagraph1, "ImageURL": full_path, "Weather": mars_weather, "HD": hemisphere_dictionary}


  return Mars_dict