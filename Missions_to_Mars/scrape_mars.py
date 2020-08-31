from splinter import Browser
from bs4 import BeautifulSoup as bs
import time
import requests

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

    #run above function 'init_browser'
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

    #image url for the current Featured Mars Image
    browser.find_by_css(".lede").click()
    time.sleep(1)

    #assign the url string to a variable called featured_image_url
    featured_image_url = browser.url

    #featured_image_url

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url
    }

    # Close the browser after scraping
    browser.quit()

    return mars_data