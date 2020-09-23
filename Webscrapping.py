
"""

Created on Thu Oct  3 22:37:11 2019

@author: AlexandreWongwanit
The script below is strictly for educational purposes only
I am not responsible for any wrong use of the script.

"""


import requests
from bs4 import BeautifulSoup
from scrapy import Selector
import datetime
import argparse
import re
import urllib.request
import time
import requests
from random import choice
import pandas as pd
import time
timestr = time.strftime("%Y%m%d")

#Optional : make a backup just in case
import shutil
shutil.copy(r'C:\Users\Alexandre\Desktop\Immo\Webscrapping.py', r'C:\Users\Alexandre\Desktop\Immo\Backup_Scripts\Webscrapping_'+timestr+'.py')


#create a class which will store all the data you want, for example, a house, a car, a smartphone, if you plan to scrap data on it.
#I only put 3 Features, which store for example: link, price, surface ,etc...
class OneScrappedUnit():
    
    def __init__(self,Feature1, Feature2,Feature3):
    
        self.Feature1 =Feature1
        self.Feature2 = Feature2
        self.Feature3 = Feature3

    def extract_data(soup) :
        #each information has its own extract function from the soup
        Feature1= BienImmo.extract_Feature1 (soup)
        Feature2 = BienImmo.extract_Feature2 (soup)
        Feature3 = BienImmo.extract_Feature3 (soup)
        # it returns one instance of the class
        return OneScrappedUnit(Feature1, Feature2,Feature3)
       
    #for each feature, you will need one extract function, which probably will require its own parsing method (eg different regex formula or else)
    #it heavily depends on the websites you parse. You will have to study their html architecture.
    def extract_Feature1(soup):
        Feature1 = "Feature1 infos not found"
        for element in soup.find_all(re.compile("strong")):
            #your own regular expressions
            #will check if any (if len(x) >0)
            if len(re.findall(r'[0-9]\sFeature1', str(element))) > 0 :
              # get only the characters
                Feature1 = str(element.get_text())
        return Feature1
      
     def extract_Feature2(soup):
        Feature1 = "Feature2 infos not found"
        for element in soup.find_all(re.compile("strong")):
            #your own regular expressions
            #will check if any (if len(x) >0)
            if len(re.findall(r'[0-9]\sFeature2', str(element))) > 0 :
              # get only the characters
                Feature1 = str(element.get_text())
        return Feature1
      
     def extract_Feature3(soup):
        Feature1 = "Feature3 infos not found"
        for element in soup.find_all(re.compile("strong")):
            #your own regular expressions
            #will check if any (if len(x) >0)
            if len(re.findall(r'[0-9]\sFeature3', str(element))) > 0 :
              # get only the characters
                Feature1 = str(element.get_text())
        return Feature1

    def extract_Feature2(soup):
        Feature2 = "Feature2 not found"
        for element in soup.find_all("div", class_="margin-bottom-30"):
          
              #you can test your regex formulas online on websites such as regexter 
                if len(re.findall(r'<div.class=.margin-bottom-30.>\n{1,2}(.*\n{1,2})*</div>', str(element))) > 0:
                    Feature2= str(element.get_text())
                    Feature2 = "".join(Feature2)
        return Feature2
    
    def extract_Feature3(soup):
        Feature3 = "Feature3 phone not found"
        #it depends on the HTML tags you want
        for element in soup.find_all("span", class_="txt-indigo"):
            if len(soup.find_all("span", class_ = "txt-indigo")) > 0 :
                Feature3= str(element.get_text())
            return Feature3
  
    #you can also get urls in a webpage , with the "a" tags.
    def getURLs(soup):
        #a list to store all the urls you scrap
        URLs= []
        count= 1
        for element in soup.find_all("a", class_="item-title",href= True):
            if len(re.findall(r'/ads_list/.*r\d{1,12}', str(element))) > 0 :
                #depends on the architecture of the website, if its only one number which change for the next pages.
                #you may need to study deeper how the target websites works.
                url = 'https://www.the_website_you_want_to_scrap.com' + ''.join(re.findall(r'/ads_list/.*r\d{1,12}', str(element)))
                URLs.append(url) 
                #for convenience
                print("ELEMENT FOUND n°",count," : ", url)
            else:
                print("ELEMENT FOUND n°",count," : None")
  
            count +=1
        return URLs


#a function to connect to the website to scrap
def ConnectTo(url):
    desktop_agents = ['Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:68.0) Gecko/20100101 Firefox/68.0']
    
    #you might want to take a random header among the ones above
    def random_headers():
        return {'User-Agent': choice(desktop_agents),'Accept':'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8'}
    try:
        r =requests.get(url,headers=random_headers())
    #print the blocked url in case. You might want to store it to a .txt or .csv file
    except "blocked" in r.text:
        print("ACCESS BLOCKED to: ", url)
    except "Forbidden" in r.text:
        print("FORBIDDEN ACCESS to: ", url)
    else:
        soup = BeautifulSoup(r.content, "lxml")
        print("-"*100)
        print("Successfully connected to: ", url)  
        return soup


#here the fun begins

#list of the urls to scrap
baseurls = [r"https://www.website_to_scrap.com/page/1"]
          
#loop to all urls, and use function
t0 = time.time()

#to store all the contents
BDD = []

#load a link, get the sublinks
for baseurl in baseurls:
    # i put many timers for curiosity and monitor the efficiency.
    baseurltime = time.time()
    soup = ConnectTo(baseurl)
    response_delay = time.time() - baseurltime
    print("Waiting ",round(10*response_delay,2), " seconds...")
    time.sleep(10*response_delay)
    
    URLlist=OneScrappedUnit.getURLs(soup)                        
    compteur_page = 1
    
    sheettime = time.time()
    
    #loop through links
    for link in URLlist:
        sublinktime = time.time()
        #if there is a link
        if len(link) > 0: 
            #connect to the link
            soup = ConnectTo(link)
            #extract data
            OneScrappedUnit = OneScrappedUnit.extract_data(soup)
            #append data to BDD list
            BDD.append(OneScrappedUnit)
            print("Waiting ",round(15*response_delay,2), " seconds...")
            
            #because its important to avoid too many requests
            time.sleep(15*response_delay)
            sublinktime = time.time() - sublinktime
            print("Sublink:",link," : ",round(sublinktime,2), "secs")
            
    sheettime = time.time() - sheettime
    print("-"*100)
    print("First sheet completion time: ",round(sheettime,2), "secs")
    #since we started page 1, I want also to scrap page 2 to 21
    #the below part is similar and could have been merged with the previous one
    for compteur_page in range(2,21):
        
        url= baseurl +"-"+str(compteur_page)
        sheettime = time.time()
        
        soup = ConnectTo(url)
        response_delay = time.time() - sheettime
        print("Waiting ",round(12*response_delay,2), " seconds...")
        time.sleep(12*response_delay)
        URLlist=OneScrappedUnit.getURLs(soup)
        
        for link in URLlist:
            if len(link) > 0:
                sublinkstart = time.time()
                soup = ConnectTo(link)
                sublinktime = time.time() - sublinkstart        
                OneScrappedUnit = OneScrappedUnit.extract_data(soup)
                BDD.append(OneScrappedUnit)
                print("Waiting ",round(20*sublinktime,2), " seconds...")
                time.sleep(15*sublinktime)
        
        sheettime = time.time() - sheettime
        print("-"*100)
        print("Sheet n°" + str(compteur_page)+"/20"+ " completion time: ",round(sheettime,2), "secs ie ",round(sheettime/60,2), " minutes." )
        
    baseurltime = time.time() - baseurltime
    
    print("url completion time: ",round(baseurltime,2), "secs")
    
    #once data are retrived, for each instance of the class  OneScrappedUnit filled with data, put it in a dataframe
    d = []
    for OneScrappedUnit in BDD:
        d.append({'Feature1': OneScrappedUnit.Feature1, 'Feature2': OneScrappedUnit.Feature2,'Feature3': OneScrappedUnit.Feature3})     
    
    fichier = pd.DataFrame(d)

    #put the whole dataframe in an excel file
    fichier.to_excel(r"C:\Users\Alexandre\Project\OneScrappedUnit_" + timestr + ".xlsx", index= False)  

#for the curiosity sake
totalTime = time.time() - t0
print("Total time of scanning: ",round(totalTime,2), "secs i.ee : ",round(totalTime/60,2), " minutes." )
print("Total time of scanning: ",round((totalTime/60)/60,2), " hours.")
