from bs4 import BeautifulSoup as bs
from splinter import Browser
import requests
import pymongo
import time
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd

def scrape(): 
    executable_path = {'executable_path': ChromeDriverManager().install()}
    browser = Browser('chrome', **executable_path, headless=False)
    
    data = {
        "news_t": news_t(browser),
        "news_p": news_p(browser),
        "featured_image": featured(browser),
        "mars_facts": facts(browser),
        'mars_hemispheres': hemispheres(browser)
    }

    print(data)

    return data


def news_t(browser):
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    soup_news = bs(html, 'html.parser')

    title_results = soup_news.find_all('div', class_='content_title')

    first_title=title_results[0].text

    return first_title

def news_p(browser):
    url = 'https://redplanetscience.com/'
    browser.visit(url)

    html = browser.html
    soup_news = bs(html, 'html.parser')

    text_results = soup_news.find_all('div', class_='article_teaser_body')

    first_text=text_results[0].text

    return first_text 


def featured(browser): 
    url = 'https://spaceimages-mars.com/'
    browser.visit(url)

    html = browser.html
    soup_image = bs(html, 'html.parser')

    browser.click_link_by_partial_text('FULL IMAGE')

    time.sleep(2)

    results = soup_image.select_one('img.headerimage.fade-in').get('src')
    featured_image_url = 'https://spaceimages-mars.com/' + results

    return featured_image_url

def facts(browser):
    url = 'https://galaxyfacts-mars.com/'

    table_0 = pd.read_html(url)[0]
    table_0.columns = ['Description', 'Mars', 'Earth']
    table_0.set_index('Description', inplace=True)
    html_table_0 = table_0.to_html(classes="data table table-striped")

    return html_table_0


def hemispheres(browser):
    url = 'https://marshemispheres.com'
    browser.visit(url)

    hemisphere_image_urls = []

    results = browser.find_by_css('a.product-item img')

    hemisphere_image_urls = []

    for item in range(len(results)):
        hemisphere = {}
    
        hemisphere['title'] = browser.find_by_css('a.itemLink h3')[item].text
        browser.find_by_css('a.itemLink img')[item].click()
        
        raw_image = browser.find_by_text('Sample').first
        hemisphere['img_url'] = raw_image['href']
        
        hemisphere_image_urls.append(hemisphere)
        
        browser.back()

    print(hemisphere_image_urls) 
    return hemisphere_image_urls


if __name__ == "__main__": 
    print(scrape())