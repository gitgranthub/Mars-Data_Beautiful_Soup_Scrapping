from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests
import pandas as pd

def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():

    #run above function 'init_browser'
    browser = init_browser()

    # Scrape the NASA Mars News Site and collect the latest News
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the News Info Section
    news_info = soup.find('div', class_='list_text')
    #print(news_info.text)

    # collect the latest News Title
    news_sec1 = news_info.find('div', class_='content_title')
    news_title = news_sec1.a.text
    #print(news_title)

    # news article Paragraph Text
    news_p = news_info.find('div', class_="article_teaser_body").text
    #print(news_p)

    # Close the browser after scraping
    browser.quit()

    
    
    
    ### LETS GET THE JPL IMAGE!!
    # Visit the url for JPL Featured Space Image here

    # run above function 'init_browser'
    browser = init_browser()

    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    time.sleep(5)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")


    # Use splinter to click on main 'full image' button
    image_button = browser.find_by_id('full_image')

    image_button.click()
    time.sleep(1)

    # Clicking 'more info' button. Making way to large image info
    browser.find_by_css(".buttons .button").click()
    time.sleep(1)

    # image url for the current Featured Mars Image
    browser.find_by_css(".lede").click()
    time.sleep(1)

    # assign the url string to a variable called featured_image_url
    featured_image_url = browser.url

    # Close the browser after scraping
    browser.quit()

    
    
    ### LETS GET THE MARS FUN FACTS!!

    #run above function 'init_browser'
    browser = init_browser()

    url = "https://space-facts.com/mars/"
    browser.visit(url)

    time.sleep(5)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Turn any site table into a pandas object
    tables = pd.read_html(url)

    # Close the browser after scraping
    browser.quit()

    # make the pandas table object a dataframe and make sure it's the 1st table
    df = tables[0]
    ## remove index
    #df.set_index([0], inplace=True)
    #df

    # Just making sure there are non column labels
    df.columns = ['Facts', 'Data']
    df

    ## HTML tables from DataFrames
    mars_facts = df.to_html(justify='left',index=False)
    mars_facts



    ## LETS GET THE MARS hemisphere images

    browser = init_browser()

    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # main_url 
    main_url = 'https://astrogeology.usgs.gov'

    # the section of the page with all the mars hemi's
    items = soup.find_all('div', class_='item')

    # The empty list of to-be dictionaries 
    hemi_urls = []

    ## Loop through the section of mars images and titles
    #interesting that 'i' in the loop acts like 'soup' but as the iterator. Took me awhile to get my
    #head around that concept.
    for i in items: 
        # Store title
        title = i.find('h3').text

        # Just the full image url
        just_img_url = i.find('a', class_='itemLink product-item')['href']

        # go to full image url
        browser.visit(main_url + just_img_url)

        time.sleep(1)

        # store html 
        img_html = browser.html

        soup = bs( img_html, 'html.parser')

        # get full image
        img_url = main_url + soup.find('img', class_='wide-image')['src']

        # Append the retreived information into a list of dictionaries 
        hemi_urls.append({"title" : title, "img_url" : img_url})

        time.sleep(1)

    browser.quit()
    # see list

        
        
        
    ## This section is connected in the app.py
    
    # Store data in a dictionary
    
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url,
        "mars_facts": mars_facts,
        "hemi_urls": hemi_urls
    }



    return mars_data