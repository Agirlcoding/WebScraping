#WebScraping for real beginners (Like me) from the website www.officialcharts.com from Mai 2003 to Mai 2018

#Import Libraries
import requests
from bs4 import BeautifulSoup
from datetime import timedelta, date
import pandas as pd
import numpy as np


def createList(r1, r2): 
    return list(range(r1, r2+1))
    
#Choose the timeframe I'm interested in to get the Top40 Charts
datum=[]
numbers=np.arange(-6382, -900, 7)
numbers_clean=numbers.tolist()
for n in numbers_clean:
    datum.append((date.today() + timedelta(days=n)).strftime('%Y%m%d'))
    
chart=createList(1,40)*len(numbers_clean)
musicWebsite=[]
for n in datum:
    musicWebsite.append('https://www.officialcharts.com/charts/rock-and-metal-singles-chart/'+str(n))
    
artists_clean=[]
title_clean=[]

for url in musicWebsite:
    src = requests.get(url).text
    soup = BeautifulSoup(src, 'html.parser')
    artists=[]
    for row in soup.findAll('div',attrs={"class" : "artist"}):
        artists.append(row.text)
    for i in artists:
        artists_clean.append((i.rstrip('\n'))[1:])
    title=[]
    for row in soup.findAll('div',attrs={"class" : "title"}):
        title.append(row.text)
    for i in title:
        title_clean.append((i.rstrip('\n'))[1:])
        
iteration=createList(0,783)
    
dateRelease=[]
for i in iteration:
    dateRelease.append([(datum[i])]*40)

flat_datum=[]
for sublist in dateRelease:
    for item in sublist:
        flat_datum.append(item)

Year=[]
for i in flat_datum:
   Year.append(i[:4])
   
#Create the DataFrame
df = pd.DataFrame(list(zip(chart, artists_clean, title_clean, flat_datum, Year)), 
               columns =['Position', 'Artist', 'Song', 'ChartDate', 'Year'])
