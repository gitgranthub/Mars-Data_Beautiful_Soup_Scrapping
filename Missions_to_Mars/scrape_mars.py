from splinter import Browser
from bs4 import BeautifulSoup as bs
import time


def init_browser():
    # @NOTE: Replace the path with your actual path to the chromedriver
    executable_path = {"executable_path": "/usr/local/bin/chromedriver"}
    return Browser("chrome", **executable_path, headless=False)


def scrape_info():
    browser = init_browser()

    # Scrape the NASA Mars News Site and collect the latest News
    url = "https://mars.nasa.gov/news/?page=0&per_page=40&order=publish_date+desc%2Ccreated_at+desc&search=&category=19%2C165%2C184%2C204&blank_scope=Latest"
    browser.visit(url)

    time.sleep(1)

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Get the News Info Section
    news_info = soup.find('div?????', id='title????')

    # collect the latest News Title
    news_title = news_info.find_all('strong?????')[0].text

    # news article Paragraph Text
    news_p = news_info.find_all('p?????')[1].text

    
    # Visit the url for JPL Featured Space Image here
    url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)

    time.sleep(1)

    browser.find_by_name('button fancybox').first.click()
    browser.find_by_name('button').first.click()

    # Scrape page into Soup
    html = browser.html
    soup = bs(html, "html.parser")

    # Use splinter to navigate the site and find the 
    #image url for the current Featured Mars Image and 
    #assign the url string to a variable called featured_image_url
    relative_image_path = soup.find_all('main_img')[2]["src"]
    featured_image_url = url + relative_image_path

    # Store data in a dictionary
    mars_data = {
        "news_title": news_title,
        "news_p": news_p,
        "featured_image_url": featured_image_url
    }

    # Close the browser after scraping
    browser.quit()

    # Return results
    return mars_data
