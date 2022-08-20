# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
from bs4  import BeautifulSoup
import pandas as pd
from selenium.webdriver import Chrome

import requests

header = ['Product Category Level1', 'Product Category Level 2', 'Part #', 'Product Name', 
          'Product Description', 'UPC', 'Image1', 'Image 2', 'Image 3', 'Country Of Origin',
          'Color', 'Length', 'Number', 'Joint Type', '1000 Volt InSulated', 'Data Sheet(PDF)']
totalData = []
 
driver = Chrome(executable_path='C:\\Users\\Admin\\.spyder-py3\\chromedriver.exe')
driver.get('https://www.knipex-tools.com/products/pipe-wrenches-and-water-pump-pliers/pliers-wrenches/pliers-wrench/8602180')

results = []
content = driver.page_source
soup = BeautifulSoup(content,"lxml")

details = ''
detail_Object = soup.findAll('li', attrs={'class': 'field__item'})
for element in detail_Object:
    details = details + element.text.strip() +'\n'

#print(details)
UPC = ''
country = ''
length = ''
jointType = ''
VoltInsulated = ''
color = ''
number = ''
UPC_Object = soup.findAll('div', attrs={'class': 'key-value-class-item'})

for element in UPC_Object:
    key = element.find('div', attrs={'class': 'key'}).find('span').text
    if key.strip() == 'UPC':
        UPC = element.find('div', attrs={'class': 'value'}).find('span').text
    if key.strip() == 'Country of Origin':
        country = element.find('div', attrs={'class': 'value'}).find('span').text
    if key.strip() == 'Length':
        length = element.find('div', attrs={'class': 'value'}).find('span').text
    if key.strip() == 'Joint Type':
        jointType = element.find('div', attrs={'class': 'value'}).find('span').text
    if key.strip() == '1000 Volt Insulated':
        VoltInsulated = element.find('div', attrs={'class': 'value'}).find('span').text
    if key.strip() == 'Color':
      color = element.find('div', attrs={'class': 'value'}).find('span').text
    if key.strip() == 'Number of Adjustment Positions':
      number = element.find('div', attrs={'class': 'value'}).find('span').text

print(UPC)
print(country)
print(length)
print(jointType)
print(VoltInsulated)
print(color)

Nabigation_Object = soup.find('ol').find_all('li')

level1 = ''
level1 = Nabigation_Object[2].find('a').text
print(level1)

level2 = ''
level2 = Nabigation_Object[3].find('a').text
print(level2)

product1 = soup.find('div', attrs={'class': 'computed_detail_title_nominal_length_inches_and_name'}).text
product2 = soup.find('div', attrs={'class': 'computed_detail_title_sku_en_us'}).text
print(product1)
print(product2)

image1_object = soup.find('div', attrs={'data-slick-index': '0'})
image2_object = soup.find('div', attrs={'data-slick-index': '1'})
image3_object = soup.find('div', attrs={'data-slick-index': '2'})

image1 =  'https://www.knipex-tools.com' + image1_object.find('img').get('src')
image2 =  'https://www.knipex-tools.com' + image2_object.find('img').get('src')
image3 =  'https://www.knipex-tools.com' + image3_object.find('img').get('src')
print(image1)
print(image2)
print(image3)


dataSheet = soup.find('span', attrs={'class': 'file--mime-application-pdf'}).find('a').get('href')
print(dataSheet)

rowData = [level1, level2, product2, product1, details,  UPC, image1, image2, image3, country,
           color,length,number, jointType ,VoltInsulated, dataSheet]

totalData.append(rowData)

allDataFrame = pd.DataFrame()
allDataFrame = pd.DataFrame(totalData,columns = header)
print(allDataFrame)

filename = 'ResultData.csv'
allDataFrame.to_csv(filename,index=False )
driver.quit() # closing the browser
