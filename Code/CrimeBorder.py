#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Feb  1 17:53:43 2019

@author: Thao Phuong, Bakhosh
"""
import os
import csv
import math
import scipy
import requests
from bs4 import BeautifulSoup
    
"""The "main" program starts here"""

def main():
    #Variables
    DATA_DIRECTORY = "../data/" 
    CACHE_DIRECTORY = "../cache/" 
    CITY_FILE = "mainPage"
    MAIN_WEB_PATH = CACHE_DIRECTORY + CITY_FILE + ".html"

    WEB_DOMAIN_NAME = 'https://en.wikipedia.org'
    WEB_PATH = '/wiki/List_of_United_States_cities_by_crime_rate'  
    SITE = WEB_DOMAIN_NAME + WEB_PATH

    cities = []
    urlList = []
    crimeRate = []
    border_cities = [] 
    distanceToBorder = []
    correlation = []
     
    #List of pre-defined default border-cities              
    border_cities.append({'name':'San Diego', 'lat':32.71500, 'lon': -117.16250})
    border_cities.append({'name':'Yuma', 'lat':32.69222, 'lon': -114.61528})
    border_cities.append({'name':'Tucson', 'lat':32.22167, 'lon': -110.92639})
    border_cities.append({'name':'El Paso', 'lat':31.7592056, 'lon': -106.4901750})
    border_cities.append({'name':'Laredo', 'lat':27.52444, 'lon': -99.49056})
    border_cities.append({'name':'Del Rio', 'lat':29.370833, 'lon': -100.89583})
    border_cities.append({'name':'Brownsville', 'lat':25.93028, 'lon': -97.48444})
    
    # Check if the needed html page is stored locally, if not download them
    getDocument(MAIN_WEB_PATH, SITE, CACHE_DIRECTORY)
    
    # Get the soup from local file
    with open(MAIN_WEB_PATH, encoding = 'utf8') as url:
        soup = BeautifulSoup (url, "lxml")
        
    # Pinpoint the cities' name and its crime rate within the local html file
    table = soup.find('table', {'class': 'wikitable sortable'})
    table_body = table.find('tbody')
    rows = table_body.find_all('tr')
    
    # Extract the name of countries from the link and append it to the list of countries.
    links = table_body.find_all('a')
    cities = [link.text.strip() for link in links]
    
    # Extract the total crime rate per 100,000 people and append it to the list of crime rate.
    for row in rows:
        cells = row.find_all('td')
        if len(cells)!= 0:
            crimeRate.append(cells[3].find(text=True))
    
    # For each city, get the link to its own Wikipedia html page
    urlList = [link.get('href') for link in links]
    
    # Download the html page of each city if you don't have it in your local workspace
    indx = 0 
    while (indx < len(cities)):
        localURL = CACHE_DIRECTORY + cities[indx] + ".html"
        website = WEB_DOMAIN_NAME + urlList[indx]
        getDocument(localURL, website, CACHE_DIRECTORY)
        indx += 1
    
    # Calcuating the distance to the closet city border 
    distance_indx = 0 
    while (distance_indx < len(cities)):
        localURL = CACHE_DIRECTORY + cities[distance_indx] + ".html"
        with open(localURL, encoding = 'utf8') as url:
            city_soup = BeautifulSoup (url, "lxml")
            coordinates = (city_soup.find('span', class_ = 'geo').text).split(';')
            distanceToBorder.append(smallest_distance(coordinates, border_cities))
            distance_indx += 1
      

    # Save the city names, crime rates, and smallest distances to the border in a 3-column CSV file
    try: 
        with open(DATA_DIRECTORY + 'CrimeBorder.csv', 'w') as CSV_file:
            CSVwriter(CSV_file, cities, crimeRate, distanceToBorder)
    except:
        if not os.path.exists(DATA_DIRECTORY):
                os.makedirs(DATA_DIRECTORY)
        with open(DATA_DIRECTORY + 'CrimeBorder.csv', 'w') as CSV_file:
            CSVwriter(CSV_file, cities, crimeRate, distanceToBorder)
     
        
    # Get the correlation
    crimeRateFloat = [float(i) for i in crimeRate]
    correlation = coefficient_of_correlation(crimeRateFloat, distanceToBorder)
    print("The correlation between"
          + " the city's crime rate and the city's distance to border: \n"
          + " {}".format(round(correlation, 3)))
    

# Supporting functions
"""
The function getDocument(LocalURL) first check if the local file exists on your computer. 
If the file exists, the function will parse the LOCAL html page using beautiful soup 
if the file does not exist, the function will automatically download the file for you
"""       
def getDocument(localURL, site, directory):
    try:
        file = open(localURL, 'r')
        file.close()

    except: 
        if not os.path.exists(directory):
            os.makedirs(directory)
            
        requestHTML = requests.get(site)
        with open(localURL, 'wb') as file:  
            file.write(requestHTML.content)
    
    
""" 
The function smallest_distance(link_to_city, border_cities) calculates 
the greate circle distance from 1 location to many border cities. Then it will 
return the smallest distance among all. The parameter takes 2 values: 
    • a link to the city
    • a list of border citites.
The value is returned in kilometers. 
Calculations were performed using the Haversine formula.
"""
def smallest_distance(coordinate1, coordinate2):
    radius_of_earth_in_km = 6371
    convert_degree_to_radians = math.pi/180
    list_of_distances = list()
    
    for city in coordinate2:
        lat_1 = float(coordinate1[1])*convert_degree_to_radians
        lat_2 = city['lat']*convert_degree_to_radians
        lon_1 = float(coordinate1[1])*convert_degree_to_radians
        lon_2 = city['lon']*convert_degree_to_radians
        
        dlon = lon_2 - lon_1 
        dlat = lat_2 - lat_1 
        a = math.sin(dlat/2)**2 + math.cos(lat_1) * math.cos(lat_2) * math.sin(dlon/2)**2
        c = 2 * math.asin(math.sqrt(a)) 
        
        smallestDistance_km = round(radius_of_earth_in_km * c, 3)
        
        list_of_distances.append(smallestDistance_km)
        
        return(min(list_of_distances))
    
    
"""The function calculates the correlation between 2 input data"""   
def coefficient_of_correlation(x, y):
    return scipy.corrcoef(x, y)[0, 1]


"""The function writes data into CSV file"""  
def CSVwriter(file, cityList, crimeRateList, distanceList):
    CSV_file = csv.writer(file)
    CSV_file.writerow(['City Names', 'Crime Rates', 'Smallest Distances'])
    CSV_indx = 0 
    while (CSV_indx < len(cityList)):
        CSV_file.writerow([cityList[CSV_indx], crimeRateList[CSV_indx], distanceList[CSV_indx]])
        CSV_indx += 1
  
    
"""Call the main function"""      
if __name__ == '__main__':
    main()
     
           
