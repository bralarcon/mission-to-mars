#import dependencies
from bs4 import BeautifulSoup
import requests
import pymongo
from splinter import Browser
import tweepy
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.keys import Keys


def init_browser():
    executable_path = {"executable_path":"C:\Webdrivers\chromedriver_win32\chromedriver"}
    return Browser("chrome", **executable_path, headless=False)

def scrape(): 
    browser = init_browser()
    mars_data = {} 

    api = "https://mars.nasa.gov/news/"
    driver = webdriver.Chrome()
    driver.get(api)  
#Mars News
    soup =  BeautifulSoup(driver.page_source, "html.parser")
    news_title = soup.find_all("div", {"class": "content_title"})
    news_title[0].find("a").get_text()
    news_p = soup.find_all("div", {"class": "rollover_description_inner"})
    news_p[0].get_text() 
# JPL Mars Space image
    space_url = "https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"

    executable_path = {'executable_path': 'chromedriver.exe'}
    browser = Browser('chrome', **executable_path)
    browser.visit(space_url)

    time.sleep(3)
    browser.click_link_by_partial_text('FULL IMAGE')
    time.sleep(3)
    browser.click_link_by_partial_text('more info')
    time.sleep(3)

    html = browser.html
    soup = BeautifulSoup(html, 'html.parser')
# Get featured image
    results = soup.find('article')
    extension = results.find('figure', 'lede').a['href']
    link = "https://www.jpl.nasa.gov"
    featured_image_url = link + extension
    print(featured_image_url)
# Twitter-Weather
    consumer_key ="qN0U90cXCQTIV57XZRYOD0Znr"
    consumer_secret = "UiyILUuUOzkNnTTyvubQePtahZiFQ8XzTTGWH34ekrKQEigbdQ"
    access_token = "1009210970554576896-tONBAz2Dw4lqGaLj3QbDB5wZVOR0yR"
    access_token_secret = "nRqUtNUSbltiz9Kkkz35R9mg0l186jRLOHsHlsekxsvgO"

# Use Tweepy to Authenticate our access
    auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    api = tweepy.API(auth, parser=tweepy.parsers.JSONParser())

# Target User
    target_user = "@MarsWxReport"
    tweet = api.user_timeline(target_user, count=1)[0]
    mars_weather = tweet['text']
    print(mars_weather)
#Mars Facts
    mf_url = "https://space-facts.com/mars/"
    table = pd.read_html(mf_url)
    table[0]   
#mars hemispheres
    hemispheres_url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(hemispheres_url)
    html = browser.html
    soup = BeautifulSoup(html, "html.parser")
    mars_hemisphere = []
    products = soup.find("div", class_ = "result-list" )
    hemispheres = products.find_all("div", class_="item")

    for hemisphere in hemispheres:
        title = hemisphere.find("h3").text
        title = title.replace("Enhanced", "")
        end_link = hemisphere.find("a")["href"]
        image_link = "https://astrogeology.usgs.gov/" + end_link    
        browser.visit(image_link)
        html = browser.html
        soup=BeautifulSoup(html, "html.parser")
        downloads = soup.find("div", class_="downloads")
        image_url = downloads.find("a")["href"]
        mars_hemisphere.append({"title": title, "img_url": image_url})
    
    print(mars_hemisphere)


    return mars_data