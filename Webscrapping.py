
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


