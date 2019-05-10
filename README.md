# “The Wall” Project: Crime and Border
Created on 6/20/2017

## What is it about?
There is a continuous discussion about whether or not the [illegal]
immigrants infiltrating the USA from Mexico positively affect the
crime rate in the border neighborhoods. This program's purpose is to cast
some light on the situation using data from Wikipedia. Check out our [report](https://github.com/tphuong141607/Cime-and-Border-Correlation/blob/master/document/Project%201%20-%20Report.pdf) in the document folder for more detailed information. 

The program was built using Python, matplotlib, and CSV and BeautifulSoup module.

## What we did:
1. Download and extract crime-related data (namely, the total violent crime rate per 100,000 people) from the major US cities
from the List of US cities by crime rate. (cache was used) [here](https://en.wikipedia.org/wiki/List_of_United_States_cities_by_crime_rate)

2. For each city, follow the link to its Wikipedia page and extract its coordinates. Calculate the distance to the border as the smallest distance from each city to San Ysidro, Yuma, Tucson, El
Paso, Laredo, Del Rio, and Brownsville, TX. 

3. Save the city names, crime rates, and smallest distances to the border in a 3-column CSV file for further analysis

## How to run this program on your computer locally?
1. Download Anaconda Navigator [here](https://www.anaconda.com/distribution/#download-section)
2. Install Spider within Anaconda Navigator
3. Launch Spider and import the source code (File --> Open --> select the CrimeBorder.py)
4. Run the program

## NOTE: The behavior of the program might change or not work due to changes applied to the Websites.


