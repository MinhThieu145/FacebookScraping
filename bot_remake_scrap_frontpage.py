# scraping
import pandas as pd
import csv
import os
import re # to clean the post link

from datetime import datetime
import time


from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

# config file
from config import *
import config

# discord sending message script
import bot_remake_discord


# ---------------------------------------------------------------------------- **Scraping** ----------------------------------------------------------------------------

# clean post link
async def clean_post_link(post_link):
    # Clean post link, as now the post link is a bit messy
    try:
        match = re.search(r'\/item\/(\d+)\/', post_link)
        item_id = match.group(1)
        # clean the post link
        post_link = f"https://www.facebook.com/marketplace/item/{item_id}/"
    except:
        pass # if the post link is already clean, then pass
    return post_link

# scrap some items in the front page (as it seems simpler)
async def scrap_info_front_page(item, driver):
    # get img link
    img_link = WebDriverWait(item, 5).until(EC.presence_of_element_located((By.XPATH, './/img'))).get_attribute("src")

    # find the post link
    post_link = WebDriverWait(driver, 5).until(EC.visibility_of(item)).get_attribute("href")
    # clean post link, convert post link to string
    post_link = await clean_post_link(str(post_link))

    # find the price
    price = WebDriverWait(item, 5).until(EC.presence_of_element_located((By.XPATH, './/span[@class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 x1s688f xzsf02u"]'))).text

    # find the title 
    title = WebDriverWait(item, 5).until(EC.presence_of_element_located((By.XPATH, './/span[@class="x1lliihq x6ikm8r x10wlt62 x1n2onr6"]'))).text

    # find the location 
    location = WebDriverWait(item, 5).until(EC.presence_of_element_located((By.XPATH, './/span[@class="x1lliihq x6ikm8r x10wlt62 x1n2onr6 xlyipyv xuxw1ft x1j85h84"]'))).text

    return img_link, post_link, title, price, location


# compare data
async def compare_data(img_link, post_link, title, price, location):
    # check if the data is already in the csv file

    # read the csv file
    df = pd.read_csv("data.csv",encoding="utf-8")
    # check if the data is already in the csv file, if the post link has already been scraped, then skip

    # get the current time
    now = datetime.now()
    current_time = now.strftime("%Y-%m-%d %H:%M:%S")

    # if the item id is not in the csv file, then add the data to the csv file
    if post_link not in df["post_link"].values:
        # if the data is not in the csv file, add the data to the csv file support encoding "utf-8"
        with open("data.csv", "a", newline="", encoding='utf-8') as f:
            writer = csv.writer(f )
            writer.writerow([current_time,img_link, post_link, title, price, location])

        # print out new items for debugging
        debug = f'{current_time} New item: {title}, {price}, {location}'
        print(debug)


        # return the data
        return img_link, post_link, title, price, location
    else:
        
        # print out old items for debugging
        debug = f'{current_time} Old item: {title}, {price}, {location}'
        print(debug)

        # if the data is in the csv file, return None for all the data
        return None, None, None, None, None

def at_least_n_visible_elements(n, driver):
    elements = driver.find_elements(By.XPATH, '//div[@class="x3ct3a4"]//a')
    visible_elements = [element for element in elements if element.is_displayed()]
    if len(visible_elements) >= n:
        return visible_elements
    else:
        for i in range(config.scroll_number):
            driver.execute_script(f"window.scrollTo(0,document.body.scrollHeight)")
            time.sleep(config.sleep_time_each_scroll)
            elements = driver.find_elements(By.XPATH, '//div[@class="x3ct3a4"]//a')
            visible_elements = [element for element in elements if element.is_displayed()]
            if len(visible_elements) >= n:
                return visible_elements
        raise TimeoutException(f"Could not find at least {n} visible elements")



# Scraping core
async def scraping_core(url, channel, driver):

    # go to site
    driver.get(url)
    time.sleep(2)

    # scroll down a bit
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight/2);")
    # get the list of items
    items = at_least_n_visible_elements(n=config.item_scrap_number, driver=driver)
    # limit to first 10 items
    items = items[:10]
    print('number of items:', len(items)) 

    # limit the number of items to scrap
    
    # loop through the items
    for item in items:
        try:

            # scrap the info
            img_link, post_link, title, price, location = await scrap_info_front_page(item=item, driver=driver)

            # before sending the info, compare the data to see if there is any new item
            img_link, post_link, title, price, location = await compare_data(img_link, post_link, title, price, location)
            

            # send the  info to the channel if it is not None
            if title != None:
                await bot_remake_discord.send_embeded(img_link= img_link,post_link= post_link,title= title,price= price, location= location, channel = channel)



        except Exception as e:
            print(e)
            print('item error, move on with next item') # move on to the next item, this error was caused by the sponsor items
            continue 

def prepared_driver():
    # global selenium driver setup
    options = Options()

    # for the chrome data folder
    dir_path = os.path.abspath(os.getcwd())
    data_dir = os.path.join(dir_path, 'Chromedata')

    # set the chrome data folder
    options.add_argument(f"--user-data-dir={data_dir}")

    # maximize window
    options.add_argument("--start-maximized")

    driver = webdriver.Chrome(options=options, executable_path="chromedriver.exe")
    return driver


async def started_scraping(channel):
    # call the scraping function
    try:
        driver = prepared_driver()
        await scraping_core(url=config.url,channel=channel,driver=driver)
    except:
        print('error, restart the script')
        # restart the script






