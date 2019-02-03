#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 17:53:43 2019

@author: thao
"""
import requests
import os
from bs4 import BeautifulSoup

CACHE_DIRECTORY = "../cache/" 
CITY_FILE = "mainPage"
HTML_PATH = CACHE_DIRECTORY + CITY_FILE + ".html"
CELL_LENGTH = 13

WEB_DOMAIN_NAME = 'https://en.wikipedia.org'
WEB_PATH = '/wiki/List_of_United_States_cities_by_crime_rate'  
SITE = WEB_DOMAIN_NAME + WEB_PATH

"""
The function getDocument(LocalURL) first check if the local file exists on your computer. 
If the file exists, the function will parse the LOCAL html page using beautiful soup 
if the file does not exist, the function will automatically download the file for you
""" 
def getDocument(localURL, site):
    try:
        with open(localURL, 'r') as file:
            return BeautifulSoup(file, 'lxml')
        
    except: 
        if not os.path.exists(CACHE_DIRECTORY):
            os.makedirs(CACHE_DIRECTORY)
        
        requestHTML = requests.get(site)
        with open(localURL, 'wb') as file:  
            file.write(requestHTML.content)
            return BeautifulSoup(open(HTML_PATH), 'lxml')


soup = getDocument(HTML_PATH, SITE)
table = soup.find('table', {'class': 'wikitable sortable'})
table_body = table.find('tbody')
rows = table_body.find_all('tr')

"""extract the name of countries from the link and append it to the list of countries."""
links = table_body.find_all('a')
countries = [link.text.strip() for link in links]

"""extract the total crime rate per 100,000 people and append it to the list of crime rate."""
crimeRate = []
for row in rows:
    cells = row.find_all('td')
    if len(cells)== CELL_LENGTH:
        crimeRate.append(cells[3].find(text=True))
        
"""For each city, follow the link to its Wikipedia page and extract its coordinates.""" 
urlList = [link.get('href') for link in links]

# Download the raw data if you don't have it in your local workspace
indx = 0 
while (indx < len(countries)):
    localURL = CACHE_DIRECTORY + countries[indx] + ".html"
    website = WEB_DOMAIN_NAME + urlList[indx]
    getDocument(localURL, website)
    indx += 1

