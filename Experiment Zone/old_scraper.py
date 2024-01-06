# Selenium Scraper
# import scraping stuff
import pandas as pd
import numpy as np
import csv

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
# import time
from time import sleep
import time

import config


# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# Search in each item and get info
def search_info(items):
    # create a dataframe to store the data
    df = pd.DataFrame(columns=['title','time', 'location','photo_link','post_link'])

    for item in items:
        # photo link 
        photo_link = item.find_element(By.XPATH, './/div[@class="x1n2onr6"]//img').get_attribute('src')
        print(photo_link)

        # 3 things: title, price, location
        title_price_location = item.find_elements(By.XPATH, './/div[@class="x1gslohp xkh6y0r"]')
        price = title_price_location[0].text

        title = title_price_location[1].text
        # remove any character that is not a number or a letter
        title = ''.join(e for e in title if e.isalnum() or e == ' ')

        # if the title is longer than 20 characters, cut it down
        if len(title) > 20:
            title = title[:20] + "..."


        location = title_price_location[2].text

        print(price + " " + title + " " + location)

        # link to the item
        item_link = item.find_element(By.XPATH, './/a').get_attribute('href')
        print(item_link)

        print(" ----------------- ") 

        # add to the dataframe
        df = df.append({'title': title, 'time': price, 'location': location, 'photo_link': photo_link, 'post_link': item_link}, ignore_index=True)

    # return the dataframe
    return df

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# Get the items list
def GetItemList():
    
    # just for the waiting
    WebDriverWait(driver, 5).\
            until(EC.presence_of_element_located((By.XPATH,'//div[@class="xkrivgy x1gryazu x1n2onr6"]'))).text

    items = driver.find_elements(By.XPATH, '//div[@class="x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e xnpuxes x291uyu x1uepa24 x1iorvi4 xjkvuk6"]//div[@class="xjp7ctv"]')
    print(len(items))

    # Now scrap data
    df =  search_info(items)

    return df

# Compare and return new item
def CompareData():
    try:
        # get data and compare to see any new ite
        df_new = GetItemList()

        # compare the data
        # get the old df from the csv file
        df = pd.read_csv('data.csv')

        # get the rows from the new df that are not in the old df. Compare all the title, price, location, photo_link, post_link
        df_new = df_new[~df_new[['title', 'time', 'location', 'photo_link', 'post_link']].apply(tuple,1).isin(df[['title', 'time', 'location', 'photo_link', 'post_link']].apply(tuple,1))]
        
        # if there is no new item, return None
        if df_new.empty:
            print("No new item")
            return None
        # if there is new item, return the new dataframe
        else:
            # return the dictionary of new items
            print("New item")

            # overwrite the old csv file with the new dataframe that has all the items of the old dataframe and the new items
            df = df.append(df_new, ignore_index=True)
            df.to_csv('data.csv', index=False)

            return df_new.to_dict('records')
    except:
        return None
    
def stop():
    driver.quit()

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
# start function
def start():
    # initialize Selenium
    # Set up Chrome Options
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")

    global driver
    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)

    # Open the website
    driver.get(config.url)
    # wait for the page to load
    time.sleep(5)

    # initialize the dataframe
    df = GetItemList()

    # save that dataframe to a csv file
    df.to_csv('data.csv', index=False)

