from bs4 import BeautifulSoup as bs
import requests
import pymongo
from splinter import Browser
from selenium import webdriver
from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import pandas as pd

def init_browser():
    executable_path = {"executable_path": "chromedriver.exe"}
    return Browser("chrome", **executable_path, headless=False)

def scrape():
    browser = intit_browser()
    mars_dict = {}

    ##MARS NEWS##
    news_url = 'https://mars.nasa.gov/news/'
    browser.vist(news_url)
    html = browser.html
    news_soup = bs(html, 'html.parser')
    news_title = news_soup.find_all('div', class_='content_title')[0].text
    news_body = news_soup.find_all('div', class_='article_teaser_body')[0].text

    ##JPL MARS IMAGES##
    def featured():
        url = "https://spaceimages-mars.com"
        browser.visit(url)
        html_img = browser.html
        soup = bs(html_img,"html.parser")
        featured_img_url = soup.find('div', class_='header')
        jpg = featured_img_url.find('a', class_="showimg fancybox-thumbs")
        jpg = jpg['href']
        featured_img_url = (f'{url}/{jpg}')
        featured_img_url
        return(featured_img_url)

    ##MARS FACTS##
    url = 'https://galaxyfacts-mars.com/'
    tables = pd.read_html(url)
    mars_fact = tables[0]
    mars_fact.columns = mars_fact.iloc[0]
    mars_fact = mars_fact.reindex(mars_fact.index.drop(0)).reset_index(drop=True)
    mars_fact.columns.name = None
    fact_table = mars_fact.to_html()
    fact_table.replace('\n','')

    ##MARS HEMISPHERES##
    mars_hem_url = 'https://marshemispheres.com/'
    browser.visit(mars_hem_url)
    html = browser.html
    soup = bs(html,'html.parser')
    mars_hems = soup.find('div',class_='collapsible results')
    mars_item = mars_hems.find_all('div',class_='item')
    hemisphere_image_urls = []
    for item in mars_item:
    try:
        ##TITLE##
        hem = item.find('div',class_ = 'description')
        title = hem.h3.text
        ##IMAGE URL##
        hem_url = hem.a['href']
        browser.visit(mars_hem_url + hem_url)
        html = browser.html
        soup = bs(html,'html.parser')
        image_src = soup.find('li').a['href']
        img_url = mars_hem_url + hem_url
        if (title and image_src):        
        ##CREATE DICTIONARY##
        hem_dict = {
            'title':title,
            'image_url':img_url
        }
        hemisphere_image_urls.append(hem_dict)

if __name__ == "__main__": 
    print(scrape())