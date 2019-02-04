# -*- coding: utf-8 -*-
"""
Created on Mon Feb  4 02:54:45 2019

@author: Bakhosh
"""

import requests
import os
from bs4 import BeautifulSoup
import math
import scipy
import csv




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
        with open(localURL, 'r', encoding = 'utf8') as file:
            return BeautifulSoup(file, 'lxml')
        
    except: 
        if not os.path.exists(CACHE_DIRECTORY):
            os.makedirs(CACHE_DIRECTORY)
        
        requestHTML = requests.get(site)
        with open(localURL, 'wb') as file:  
            file.write(requestHTML.content)
            return BeautifulSoup(open(HTML_PATH), 'lxml')

"""Alternative for calculation 1. Calculate the great circle distance between two points on the earth. The value is returned in
kilometers. Calculations were performed using the Haversine formula."""
def smallest_distance(link_to_city, border_cities):
    """The following line we need to make in such a way that soup will have a link to city"""
    soup = getDocument(link_to_city)
    coordinates_from_link = (soup.find('span', class_ = 'geo').text).split(';')
    radius_of_earth_in_km = 6371
    convert_degree_to_radians = math.pi/180
    list_of_distances = list()
    
    for city in border_cities:
        lat_1 = float(coordinates_from_link[1])*convert_degree_to_radians
        lat_2 = city['lat']*convert_degree_to_radians
        lon_1 = float(coordinates_from_link[1])*convert_degree_to_radians
        lon_2 = city['lon']*convert_degree_to_radians
        
        dlon = lon_2 - lon_1 
        dlat = lat_2 - lat_1 
        a = math.sin(dlat/2)**2 + math.cos(lat_1) * math.cos(lat_2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a)) 
        
        km = radius_of_earth_in_km * c
        
        print(km)
        list_of_distances.append(km)
    return(min(list_of_distances))


"""Alternative for calculation 2
def getSmallestDistance(city_link, borders): 
    soup = getDocument(localURL, site)  
    coordinates = (soup.find('span', class_='geo').text).split(';')
    distance = []
    EARTH_RADIUS = 6367
    RADIANS = math.pi/180
    
    for border in borders:
        lat1 = float(coordinates[0])*RADIANS
        lat2 = border['lat']*RADIANS
        lon1 = float(coordinates[1])*RADIANS
        lon2 = border['lon']*RADIANS
        a = (math.sin((lat1-lat2)/2))**2 + math.cos(lat1) * math.cos(lat2) * (math.sin((lon1-lon2)/2))**2
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        d = EARTH_RADIUS * c
        print(d)
        distance.append(d)
    return(min(distance))
"""  
    
"""Calculation of correlation"""   
def coefficient_of_correlation(x, y):
    return scipy.corrcoef(x, y)[0][1]




"""List of pre-defined default border-cities"""
border_cities = []               
border_cities.append({'name':'San Diego', 'lat':32.71500, 'lon': -117.16250})
border_cities.append({'name':'Yuma', 'lat':32.69222, 'lon': -114.61528})
border_cities.append({'name':'Tucson', 'lat':32.22167, 'lon': -110.92639})
border_cities.append({'name':'El Paso', 'lat':31.7592056, 'lon': -106.4901750})
border_cities.append({'name':'Laredo', 'lat':27.52444, 'lon': -99.49056})
border_cities.append({'name':'Del Rio', 'lat':29.370833, 'lon': -100.89583})
border_cities.append({'name':'Brownsville', 'lat':25.93028, 'lon': -97.48444})


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
    
    
"""Anna, above you can see the implemented formula for calculating the smallest distance between cities
and getting the coefficient of correlation. Now, we need to come up with some sort of loop which will iterate through
the soup, open each link of city, use the smallest_distance formula and return to us the minimum.

A friend of mine who is also taking this class gave me a hint. They have used the following loop:
   The following is copy from his code:
       
       city_list = list()
       count = 0
        
       soup = getDocument(SITE)
       for i in soup.find('table', class_='wikitable').find_all('td'):
           if count == 1:
               city_name = i.text
               print(city_name)
               smallest = round(getSmallestDistance(i.a['href'], borders), 4)
           elif count == 3:
               crime_rate = float(i.text)
               d = {'city':city_name, 'crime rate':crime_rate, 'distance':smallest}
               city_list.append(d)
           elif count == 13:
               count = 0
           count += 1   
           
           
        As the result of this loop they have list_of_cities (city_list) which then can be used for creating a csv file and calculating the correlation coeffcient
           
   I have tried to implement similar method but that totally SUCKED.
   
   Once we come up with our loop the rest is will be following.
   
"""


"""

for csv:

import csv
#check if directory result exists, if not create a new one
with open('../crime_data.csv', 'w') as csvfile:
    fieldname = ['city', 'crime rate', 'distance']
    filew = csv.DictWriter(csvfile, fieldnames = fieldname)
    filew.writeheader()
    filew.writerows(list_of_cities which we will get from the loop created)
    


for correlation results: 

 #create list with smallest distance and crime rate
smallestDistance=[]
crimeRate=[]
for i in list_of_cities:
    smallestDistance.append(i['distance'])
    crimeRate.append(i['crime rate'])
print(getCorrelation(smallestDistance, crimeRate))         
"""



           
           
           
           
           
           
           
           
           
           
