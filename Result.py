# -*- coding: utf-8 -*-
"""
Spyder Editor

This is a temporary script file.
"""

from selenium import webdriver
from bs4  import BeautifulSoup
import pandas as pd
from selenium.webdriver import Chrome

driver = Chrome(executable_path='C:\\Users\\Admin\\.spyder-py3\\chromedriver.exe')
driver.get('https://www.knipex-tools.com/products?search_api_fulltext=&sort_by=sku&items_per_page=5&page=0')

header = ['Product Category Level1', 'Product Category Level 2', 'Part #', 'Product Name', 
          'Product Description', 'UPC', 'Image1', 'Image 2', 'Image 3', 'Country Of Origin',
          'Color', 'Length', 'Number', 'Joint Type', '1000 Volt InSulated', 'Data Sheet(PDF)',
          'Manufacturer', 'MOQ' , 'Stock Status', 'Stock Status Message', 'Price', 'SKU']
totalData = []





for i in range(0,2):
    #print(item.get('href'))
    driver.get('https://www.knipex-tools.com/products?search_api_fulltext=&sort_by=sku&items_per_page=5&page='+str(i))
    content = driver.page_source
    soup = BeautifulSoup(content,"lxml")
    itemObjects = soup.findAll('div', attrs={'class': 'views-field-field-preview-picture'})
    for layer1Item in itemObjects:

        details = []
        UPC = ''
        country = ''
        length = ''
        jointType = ''
        VoltInsulated = ''
        color = ''
        number = ''
        level = [5]
        product1 = ''
        product2 = ''
        image1 =''
        image2 =''
        image3 =''
        image4 =''
        image5 =''
        image6 =''
        dataSheet = ''
        rowData = []
        driver.get('https://www.knipex-tools.com/'+layer1Item.find('a').get('href'))
        
        mainContent = driver.page_source
        mainSoup = BeautifulSoup(mainContent,"lxml")

        detail_Object = mainSoup.findAll('li', attrs={'class': 'field__item'})
        detail_Object = mainSoup.findAll('li', attrs={'class': 'field__item'})
        for element in detail_Object:
            details.append(element.text.strip())

        UPC_Object = mainSoup.findAll('div', attrs={'class': 'key-value-class-item'})
        for element in UPC_Object:
            key = element.find('div', attrs={'class': 'key'}).find('span').text
            if key.strip() == 'UPC':
                UPC = str(element.find('div', attrs={'class': 'value'}).find('span').text)+" "
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
             
        if mainSoup.find('ol') != None:
            Nabigation_Object = mainSoup.find('ol').find_all('li')

        for navigation in Nabigation_Object:
            level.append(navigation.find('a').text)
        level.append('')
        print(UPC)
        product1 = mainSoup.find('div', attrs={'class': 'computed_detail_title_nominal_length_inches_and_name'}).text
        product2 = mainSoup.find('div', attrs={'class': 'computed_detail_title_sku_en_us'}).text

        image1_object = mainSoup.find('div', attrs={'data-slick-index': '0'})
        image2_object = mainSoup.find('div', attrs={'data-slick-index': '1'})
        image3_object = mainSoup.find('div', attrs={'data-slick-index': '2'})
        image4_object = mainSoup.find('div', attrs={'data-slick-index': '3'})
        image5_object = mainSoup.find('div', attrs={'data-slick-index': '4'})
        image6_object = mainSoup.find('div', attrs={'data-slick-index': '5'})

        if image1_object != None and image1_object.find('img') != None:
            image1 =   'https://www.knipex-tools.com' + image1_object.find('img').get('src')
        if image2_object != None and image2_object.find('img') != None:
            image2 =   'https://www.knipex-tools.com' + image2_object.find('img').get('src')
        if image3_object != None and image3_object.find('img') != None:
            image3 =   'https://www.knipex-tools.com' + image3_object.find('img').get('src')
        if image4_object != None and image4_object.find('img') != None:
            image4 =   'https://www.knipex-tools.com' + image4_object.find('img').get('src')
        if image5_object != None and image5_object.find('img') != None:
            image5 =   'https://www.knipex-tools.com' + image5_object.find('img').get('src')
        if image6_object != None and image6_object.find('img') != None:
            image6 =   'https://www.knipex-tools.com' + image6_object.find('img').get('src')


        if mainSoup.find('span', attrs={'class': 'file--mime-application-pdf'}) != None:
            dataSheet = mainSoup.find('span', attrs={'class': 'file--mime-application-pdf'}).find('a').get('href')

        rowData = [level[3], level[4], product2, product1, details,  UPC, image1, image2, image3, country,
                   color, length, number, jointType ,VoltInsulated, dataSheet, '','','','','', product2]
        totalData.append(rowData)

allDataFrame = pd.DataFrame()
allDataFrame = pd.DataFrame(totalData, columns = header)
filename = 'ResultData.csv'
allDataFrame.to_csv(filename,index=False )
driver.quit()




print('=====================')