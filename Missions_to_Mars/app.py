import pandas as pd 
from bs4 import BeautifulSoup as bs
from webdriver_manager.chrome import ChromeDriverManager
from selenium import webdriver
import nbconvert
import requests
import time
from splinter import Browser
import json
from flask import Flask,render_template,render_template_string
from mission_to_mars import scrape
import pymongo


myclient = pymongo.MongoClient("mongodb://localhost:27017/")
scrape_db = myclient["scrape_db"]
data = scrape_db['data'] 
scrape_db.data.update({}, scrape(), upsert=True)


mars = scrape_db.data.find_one()

app = Flask(__name__)
@app.route('/scrape')
def echo():
    return str(scrape())


@app.route('/')
def index_html():
    return render_template('index.html',mars = mars)

if __name__ =="__main__":
    app.run()

# use {mars_facts | safe} for non literal in html file
# create mars = mars as the dictionary it is and then call with mars.Title_p in html file 
# https://www.geeksforgeeks.org/python-using-for-loop-in-flask/