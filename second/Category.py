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
  
    
driver = Chrome(executable_path='C:\\Users\\Admin\\.spyder-py3\\chromedriver.exe')
driver.get('https://www.unitedabrasives.com')

header = ['SKU#', 'Product Category Level 1', 'Product Category Level 2','Product Category Level 3', 'PRODUCT NAME', 'DESCRIPTION', 
          'MPN', 'UPC', 'Manufacturer', 'Product Image1', 'Product Image 2', 'Product Image 3', 'Data Sheet',
          'DIA', 'THICK', 'ARBOR', 'Type', 'MAX RPM', 'QTV', 'WIDTH', 'TRIM LENGTH', 'OVERALL LENGTH', 'GRIT', 'WIRE SIZE']
totalData = []

results = []
content = driver.page_source
soup = BeautifulSoup(content,"lxml")

details = ''
Owner = soup.find('li', attrs={'id': 'menu-item-25081'})
links  = Owner.findChild('ul').find_all('li', recursive=False)
categoryLevel_1 = ''
categoryLevel_2 = ''
categoryLevel_3 = ''

for link in links:
    categoryLevel_1 = link.find('a').text
    ele = link.find('ul')
    if ele != None:
        element = ele.find_all('li', recursive=False)
        for item in element:
            categoryLevel_2 = item.find('a').text
            if item.find('ul') != None:
                
                subItems = item.find('ul').find_all('li', recursive=False)
                for subItem in subItems:
                    
                    if subItem.find('ul') != None:
                        categoryLevel_3 = subItem.find('a').text
                        finalItems = subItem.find('ul').find_all('li', recursive=False)
                        for finalItem in finalItems:
                            mainLink = finalItem.find('a').get('href')
                            ############## step2 #######################
                            driver.get(mainLink)
                            itemListContent = driver.page_source
                            itemListSoup = BeautifulSoup(itemListContent,"lxml")
                           
                            name_1 = itemListSoup.find('div', attrs={'class': 'category-heading'}).find('h2').text
                            itemList = itemListSoup.findAll('div', attrs={'class': 'category-body'})
                            for temp in itemList:
                                body = temp.find('div', attrs={'class': 'single-cat-prod-header'})
                                if body != None:
                                    detailLink = body.find('h3', attrs={'class': 'single-cat-prod-title'}).find('a').get('href')
                                    name_2 =  body.find('h3').find('a').text
                                    
                                    ###################### step3 ########################
                                    driver.get(detailLink)
                                    itemDetailContent = driver.page_source
                                    itemDetailSoup = BeautifulSoup(itemDetailContent,"lxml")
                                    
                                    name_3 = ''
                                    description_1 = ''
                                    description_2 = ''
                                    dataSheet = ''
                                    images = []
                                    manufacturer = ''
                                    DIA = ''
                                    THICK = ''
                                    ARBOR = ''
                                    TYPE = ''
                                    MAX_RPM = ''
                                    QTY = ''
                                    SKU = ''
                                    WIDTH = ''
                                    TRIM_LENGTH = ''
                                    OVERALL_LENGTH = ''
                                    GRIT = ''
                                    WIRE_SIZE = ''
                                    
                                    rowData = []
                                    
                                    if itemDetailSoup.find('div',attrs={'class': 'summary'}) != None:
                                        description_1 = itemDetailSoup.find('div',attrs={'class': 'summary'}).find('ul').text
                                    if itemDetailSoup.find('div',attrs={'id': 'tech-info'}) != None:
                                        description_2 = itemDetailSoup.find('div',attrs={'id': 'tech-info'}).find('ul').text
                                     
                                    if itemDetailSoup.find('div',attrs={'id': 'sds'}) != None:
                                         dataSheet = itemDetailSoup.find('div',attrs={'id': 'sds'}).find('a').get('href')
                                    
                                    mainImage = itemDetailSoup.find('div',attrs={'class': 'product-sidebar'}).find('img')
                                    if mainImage != None:
                                        images.append(mainImage.get('src'))
                                       
                                    if itemDetailSoup.find('ul',attrs={'class': 'slides'}) != None:    
                                        imageList = itemDetailSoup.find('ul',attrs={'class': 'slides'}).findAll('img')
                                        if imageList != None:
                                            images.clear()
                                            for image in imageList:
                                                if "https" in image.get('src'):
                                                    images.append(image.get('src'))
                                                else:
                                                    images.append("https://www.unitedabrasives.com"+image.get('src'))
                                    images.append('')
                                    images.append('')
                                    images.append('')
                                    
                                    
                                    if itemDetailSoup.find('div',attrs={'class': 'fam-tips'}).find('img') != None :
                                        manufacturer = 'United Abrasives SAIT'
        
                                    informations = itemDetailSoup.findAll('div',attrs={'class': 'panel-default'})
                                    for information in informations:
                                        name_3 = information.find('h4', attrs={'class' : 'panel-title'}).text
                                        if information.find('tbody') != None:
                                            extraDataHead = information.find('tbody').find('tr')
                                            extraDataBody = information.find('tbody').findAll('tr')
                                            if extraDataBody != None:
                                                for i in range(1, len(extraDataBody)):
                                                    extraItems = extraDataHead.findAll('td')
                                                 
                                                    for j in range(0, len(extraItems)):
                                                        if extraItems[j].text.strip() == 'Dia':
                                                            DIA = extraDataBody[i].findAll('td')[j].text
                                                        if extraItems[j].text.strip() == 'Thick':
                                                            THICK = extraDataBody[i].findAll('td')[j].text
                                                        if extraItems[j].text.strip() == 'Arbor':
                                                            ARBOR = extraDataBody[i].findAll('td')[j].text
                                                        if extraItems[j].text.strip() == 'Type':
                                                            TYPE = extraDataBody[i].findAll('td')[j].text
                                                        if extraItems[j].text.strip() == 'Max RPM':
                                                            MAX_RPM = extraDataBody[i].findAll('td')[j].text
                                                        if extraItems[j].text.strip() == 'Qty':
                                                            QTY = extraDataBody[i].findAll('td')[j].text
                                                        if extraItems[j].text.strip() == 'PART #':
                                                            PART = extraDataBody[i].findAll('td')[j].text
                                                        if extraItems[j].text.strip() == 'PART #':
                                                            SKU = extraDataBody[i].findAll('td')[j].text
                                                        if extraItems[j].text.strip() == 'Wire Size':
                                                            WIRE_SIZE = extraDataBody[i].findAll('td')[j].text
                                                        if extraItems[j].text.strip() == 'Trim Length':
                                                            TRIM_LENGTH = extraDataBody[i].findAll('td')[j].text
                                                        if extraItems[j].text.strip() == 'Overall Length':
                                                            TRIM_LENGTH = extraDataBody[i].findAll('td')[j].text
                                                        if extraItems[j].text.strip() == 'Grit':
                                                            GRIT = extraDataBody[i].findAll('td')[j].text 
                                                        if extraItems[j].text.strip() == 'Width':
                                                            WIDTH = extraDataBody[i].findAll('td')[j].text 
                                                            
                                                    print(categoryLevel_1)
                                                    print(categoryLevel_2)
                                                    print(categoryLevel_3)
                                                    print(name_1)
                                                    print(name_2)
                                                    print(name_3)
                                                    print(description_1)
                                                    print(description_2)
                                                    print(images)
                                                    print(dataSheet)
                                                    print(manufacturer)
                                                    print(DIA)
                                                    print(THICK)
                                                    print(ARBOR)
                                                    print(TYPE)
                                                    print(MAX_RPM)
                                                    print(QTY)
                                                    print(SKU)
                                                    
                                                    productName = name_1 + ","+ name_2+","+name_3
                                                    description = description_1 +", " + description_2
                                                    rowData = [SKU, categoryLevel_1, categoryLevel_2, categoryLevel_3, productName,  description, SKU, '', manufacturer, images[0],
                                                               images[1], images[2], dataSheet, DIA ,THICK, ARBOR, TYPE ,MAX_RPM, QTY ]
                                                    totalData.append(rowData)
                                                 
                    else:
                        mainLink = subItem.find('a').get('href')
                        ############## step2 #######################
                        driver.get(mainLink)
                        itemListContent = driver.page_source
                        itemListSoup = BeautifulSoup(itemListContent,"lxml")
                       
                        name_1 = itemListSoup.find('div', attrs={'class': 'category-heading'}).find('h2').text
                        itemList = itemListSoup.findAll('div', attrs={'class': 'category-body'})
                        for temp in itemList:
                            body = temp.find('div', attrs={'class': 'single-cat-prod-header'})
                            if body != None:
                                detailLink = body.find('h3', attrs={'class': 'single-cat-prod-title'}).find('a').get('href')
                                name_2 =  body.find('h3').find('a').text
                                
                                ###################### step3 ########################
                                driver.get(detailLink)
                                itemDetailContent = driver.page_source
                                itemDetailSoup = BeautifulSoup(itemDetailContent,"lxml")
                                
                                name_3 = ''
                                description_1 = ''
                                description_2 = ''
                                dataSheet = ''
                                images = []
                                manufacturer = ''
                                DIA = ''
                                THICK = ''
                                ARBOR = ''
                                TYPE = ''
                                MAX_RPM = ''
                                QTY = ''
                                SKU = ''
                                WIDTH = ''
                                TRIM_LENGTH = ''
                                OVERALL_LENGTH = ''
                                GRIT = ''
                                WIRE_SIZE = ''
                                rowData = []
                                
                                if itemDetailSoup.find('div',attrs={'class': 'summary'}) != None:
                                    description_1_items = itemDetailSoup.find('div',attrs={'class': 'summary'}).find('ul').findAll('li')
                                    for description_1_item in description_1_items:
                                        description_1 = description_1 + description_1_item.text + '.'
                                if itemDetailSoup.find('div',attrs={'id': 'tech-info'}) != None:
                                    description_2_items = itemDetailSoup.find('div',attrs={'id': 'tech-info'}).find('ul').findAll('li')
                                    for description_2_item in description_2_items:
                                        description_2 = description_2 + description_2_item.text + '.'
                                 
                                if itemDetailSoup.find('div',attrs={'id': 'sds'}) != None:
                                     dataSheet = itemDetailSoup.find('div',attrs={'id': 'sds'}).find('a').get('href')
                                
                                mainImage = itemDetailSoup.find('div',attrs={'class': 'product-sidebar'}).find('img')
                                if mainImage != None:
                                    images.append(mainImage.get('src'))
                                   
                                if itemDetailSoup.find('ul',attrs={'class': 'slides'}) != None:    
                                    imageList = itemDetailSoup.find('ul',attrs={'class': 'slides'}).findAll('img')
                                    if imageList != None:
                                        images.clear()
                                        for image in imageList:
                                            if "https" in image.get('src'):
                                                images.append(image.get('src'))
                                            else:
                                                images.append("https://www.unitedabrasives.com"+image.get('src'))
                                images.append('')
                                images.append('')
                                images.append('')
                                
                                
                                if itemDetailSoup.find('div',attrs={'class': 'fam-tips'}).find('img') != None :
                                    manufacturer = 'United Abrasives SAIT'
    
                                informations = itemDetailSoup.findAll('div',attrs={'class': 'panel-default'})
                                for information in informations:
                                    name_3 = information.find('h4', attrs={'class' : 'panel-title'}).text
                                    if information.find('tbody') != None:
                                        extraDataHead = information.find('tbody').find('tr')
                                        extraDataBody = information.find('tbody').findAll('tr')
                                        if extraDataBody != None:
                                            for i in range(1, len(extraDataBody)):
                                                extraItems = extraDataHead.findAll('td')
                                             
                                                for j in range(0, len(extraItems)):
                                                    if extraItems[j].text.strip() == 'Dia':
                                                        DIA = extraDataBody[i].findAll('td')[j].text
                                                    if extraItems[j].text.strip() == 'Thick':
                                                        THICK = extraDataBody[i].findAll('td')[j].text
                                                    if extraItems[j].text.strip() == 'Arbor':
                                                        ARBOR = extraDataBody[i].findAll('td')[j].text
                                                    if extraItems[j].text.strip() == 'Type':
                                                        TYPE = extraDataBody[i].findAll('td')[j].text
                                                    if extraItems[j].text.strip() == 'Max RPM':
                                                        MAX_RPM = extraDataBody[i].findAll('td')[j].text
                                                    if extraItems[j].text.strip() == 'Qty':
                                                        QTY = extraDataBody[i].findAll('td')[j].text
                                                    if extraItems[j].text.strip() == 'PART #':
                                                        PART = extraDataBody[i].findAll('td')[j].text
                                                    if extraItems[j].text.strip() == 'PART #':
                                                        SKU = extraDataBody[i].findAll('td')[j].text
                                                    if extraItems[j].text.strip() == 'Wire Size':
                                                        WIRE_SIZE = extraDataBody[i].findAll('td')[j].text
                                                    if extraItems[j].text.strip() == 'Trim Length':
                                                        TRIM_LENGTH = extraDataBody[i].findAll('td')[j].text
                                                    if extraItems[j].text.strip() == 'Overall Length':
                                                        TRIM_LENGTH = extraDataBody[i].findAll('td')[j].text
                                                    if extraItems[j].text.strip() == 'Grit':
                                                        GRIT = extraDataBody[i].findAll('td')[j].text 
                                                    if extraItems[j].text.strip() == 'Width':
                                                        WIDTH = extraDataBody[i].findAll('td')[j].text 
                                                print(categoryLevel_1)
                                                print(categoryLevel_2)
                                                print(name_1)
                                                print(name_2)
                                                print(name_3)
                                                print(description_1)
                                                print(description_2)
                                                print(images)
                                                print(dataSheet)
                                                print(manufacturer)
                                                print(DIA)
                                                print(THICK)
                                                print(ARBOR)
                                                print(TYPE)
                                                print(MAX_RPM)
                                                print(QTY)
                                                print(SKU)
                                                
                                                productName = name_1 + ","+ name_2+","+name_3
                                                description = description_1 +", " + description_2
                                                rowData = [SKU, categoryLevel_1, categoryLevel_2, categoryLevel_3, productName,  description, SKU, '', manufacturer, images[0],
                                                           images[1], images[2], dataSheet, DIA ,THICK, ARBOR, TYPE ,MAX_RPM, QTY ]
                                                totalData.append(rowData)
                                
            else:   
                mainLink = item.find('a').get('href')
                ############### step2 ######################
                driver.get(mainLink)
                itemListContent = driver.page_source
                itemListSoup = BeautifulSoup(itemListContent,"lxml")
                
                name_1 = itemListSoup.find('div', attrs={'class': 'category-heading'}).find('h2').text
                itemList = itemListSoup.findAll('div', attrs={'class': 'category-body'})
                for temp in itemList:
                    body = temp.find('div', attrs={'class': 'single-cat-prod-header'})
                    if body != None:
                        detailLink = body.find('h3', attrs={'class': 'single-cat-prod-title'}).find('a').get('href')
                        name_2 =  body.find('h3').find('a').text

                        ###################### step3 ########################
                        
                        driver.get(detailLink)
                        itemDetailContent = driver.page_source
                        itemDetailSoup = BeautifulSoup(itemDetailContent,"lxml")
                        
                        name_3 = ''
                        description_1 = ''
                        description_2 = ''
                        dataSheet = ''
                        images = []
                        manufacturer = ''
                        DIA = ''
                        THICK = ''
                        ARBOR = ''
                        TYPE = ''
                        MAX_RPM = ''
                        QTY = ''
                        SKU = ''
                        WIDTH = ''
                        TRIM_LENGTH = ''
                        OVERALL_LENGTH = ''
                        GRIT = ''
                        WIRE_SIZE = ''
                        
                        rowData = []
                        
                        if itemDetailSoup.find('div',attrs={'class': 'summary'}) != None:
                            description_1 = itemDetailSoup.find('div',attrs={'class': 'summary'}).find('ul').text
                        if itemDetailSoup.find('div',attrs={'id': 'tech-info'}) != None:
                            description_2 = itemDetailSoup.find('div',attrs={'id': 'tech-info'}).find('ul').text
                         
                        if itemDetailSoup.find('div',attrs={'id': 'sds'}) != None:
                             dataSheet = itemDetailSoup.find('div',attrs={'id': 'sds'}).find('a').get('href')
                        
                        mainImage = itemDetailSoup.find('div',attrs={'class': 'product-sidebar'}).find('img')
                        if mainImage != None:
                            images.append(mainImage.get('src'))
                           
                        if itemDetailSoup.find('ul',attrs={'class': 'slides'}) != None:    
                            imageList = itemDetailSoup.find('ul',attrs={'class': 'slides'}).findAll('img')
                            if imageList != None:
                                images.clear()
                                for image in imageList:
                                    if "https" in image.get('src'):
                                        images.append(image.get('src'))
                                    else:
                                        images.append("https://www.unitedabrasives.com"+image.get('src'))
                        images.append('')
                        images.append('')
                        images.append('')
                        
                        
                        if itemDetailSoup.find('div',attrs={'class': 'fam-tips'}).find('img') != None :
                            manufacturer = 'United Abrasives SAIT'

                        informations = itemDetailSoup.findAll('div',attrs={'class': 'panel-default'})
                        for information in informations:
                            name_3 = information.find('h4', attrs={'class' : 'panel-title'}).text
                            if information.find('tbody') != None:
                                extraDataHead = information.find('tbody').find('tr')
                                extraDataBody = information.find('tbody').findAll('tr')
                                if extraDataBody != None:
                                    for i in range(1, len(extraDataBody)):
                                        extraItems = extraDataHead.findAll('td')
                                        if extraItems != None:
                                            for j in range(0, len(extraItems)):
                                                if extraItems[j].text.strip() == 'Dia':
                                                    DIA = extraDataBody[i].findAll('td')[j].text
                                                if extraItems[j].text.strip() == 'Thick':
                                                    THICK = extraDataBody[i].findAll('td')[j].text
                                                if extraItems[j].text.strip() == 'Arbor':
                                                    ARBOR = extraDataBody[i].findAll('td')[j].text
                                                if extraItems[j].text.strip() == 'Type':
                                                    TYPE = extraDataBody[i].findAll('td')[j].text
                                                if extraItems[j].text.strip() == 'Max RPM':
                                                    MAX_RPM = extraDataBody[i].findAll('td')[j].text
                                                if extraItems[j].text.strip() == 'Qty':
                                                    QTY = extraDataBody[i].findAll('td')[j].text
                                                if extraItems[j].text.strip() == 'PART #':
                                                    PART = extraDataBody[i].findAll('td')[j].text
                                                if extraItems[j].text.strip() == 'PART #':
                                                    SKU = extraDataBody[i].findAll('td')[j].text
                                                if extraItems[j].text.strip() == 'Wire Size':
                                                    WIRE_SIZE = extraDataBody[i].findAll('td')[j].text
                                                if extraItems[j].text.strip() == 'Trim Length':
                                                    TRIM_LENGTH = extraDataBody[i].findAll('td')[j].text
                                                if extraItems[j].text.strip() == 'Overall Length':
                                                    TRIM_LENGTH = extraDataBody[i].findAll('td')[j].text
                                                if extraItems[j].text.strip() == 'Grit':
                                                    GRIT = extraDataBody[i].findAll('td')[j].text 
                                                if extraItems[j].text.strip() == 'Width':
                                                    WIDTH = extraDataBody[i].findAll('td')[j].text 
                                        print(categoryLevel_1)
                                        print(categoryLevel_2)
                                        print(categoryLevel_3)
                                        print(name_1)
                                        print(name_2)
                                        print(name_3)
                                        print(description_1)
                                        print(description_2)
                                        print(images)
                                        print(dataSheet)
                                        print(manufacturer)
                                        print(DIA)
                                        print(THICK)
                                        print(ARBOR)
                                        print(TYPE)
                                        print(MAX_RPM)
                                        print(QTY)
                                        print(SKU)
                                        
                                        productName = name_1 + ","+ name_2+","+name_3
                                        description = description_1 +", " + description_2
                                        rowData = [SKU, categoryLevel_1, categoryLevel_2, categoryLevel_3, productName,  description, SKU, '', manufacturer, images[0],
                                                   images[1], images[2], dataSheet, DIA ,THICK, ARBOR, TYPE ,MAX_RPM, QTY , WIDTH, TRIM_LENGTH, OVERALL_LENGTH,
                                                   GRIT, WIRE_SIZE]
                                        totalData.append(rowData)
        break 
                       
allDataFrame = pd.DataFrame()
allDataFrame = pd.DataFrame(totalData, columns = header)
filename = 'ResultData.csv'
allDataFrame.to_csv(filename,index=False )

print('=====================')
driver.quit() 
