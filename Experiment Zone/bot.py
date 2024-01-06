from discord.ext import commands, tasks
import discord

BOT_TOKEN = "MTA4MzYzNzk2ODk1MjExNTI0MA.GpgqT8.aSyh6KDmo4xaLcu5nrcicpuCvGQWjXMcPgp_bg"
CHANNEL_ID = 1083640013180387352

# scraping libraries
import pandas as pd
import csv
import time

from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

from config import *
import config

# set up some discord
bot = commands.Bot(command_prefix="!", intents=discord.Intents.default())


# Scraping core
def core_scraping(driver, link):
    driver.get(link) # open link
    #TITLE
    title = (WebDriverWait(driver, 5).until(
            EC.presence_of_element_located(
                (By.XPATH, '//div[@class="xyamay9 x1pi30zi x18d9i69 x1swvt13"]//h1')
            )
        )
        .text
    )
    #TIME POSTED
    time_location = driver.find_element(
        By.XPATH,
        '//span[@class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x4zkp8e x676frb x1nxh6w3 x1sibtaa xo1l8bm xi81zsa"]',
    ).text
    #PRICE
    price = driver.find_element(
        By.XPATH,
        '//div[@class="x1xmf6yo"]//span[@class="x193iq5w xeuugli x13faqbe x1vvkbs x1xmvt09 x1lliihq x1s928wv xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x xudqn12 x676frb x1lkfr7t x1lbecb7 xk50ysn xzsf02u"]',
    ).text
    #PICTURE LINKS
    picture_links = driver.find_elements(By.XPATH, '//div[@class="x1a0syf3 x1ja2u2z"]//img')
    picture_links_list = []
    for i in range(len(picture_links)):
        picture_links_list.append(picture_links[i].get_attribute("src"))

    current_time = time.strftime("%Y-%m-%d %H:%M:%S")
    return current_time, title, time_location, picture_links_list, price

def loop_over_item(driver, df, item_links):

    new_item_list = []

    for item_link in item_links:
        try:
            (
                current_time,
                title,
                time_location,
                picture_links_list,
                price,
            ) = core_scraping(driver, item_link)
        except Exception as e:
            print(e)
            print("Error at: ", item_link)
            continue

        #Check existence
        if len(df[(df['title']==title) & (df['price'] == price)]) >0:
            print("Old listing")
            print(current_time, title, time_location, price)
        else:
            print("New listing")
            print(current_time, title, time_location, price)
            #SAVE and SEND NOTIFICATION
            row = pd.DataFrame({
                "current_time": [current_time],
                "title": [title],
                "time_location": [time_location],
                "price": [price],
                "item_link": [item_link],
            })
            df = pd.concat([row, df])
            df.to_csv(config.output_dir, index = False)

            # add to new item list
            new_item_list.append({
                "title": title,
                "time": time_location,
                "location": "",
                "photo_link": picture_links_list,
                "post_link": item_link,
            })
    return new_item_list
            
            

def scroll(driver, n_loads):
    for i in range(n_loads):
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(1)

def get_item_links(driver, url, n_loads):
    driver.get(url) # go to the url
    time.sleep(5) # wait for the page to load
    scroll(driver, n_loads) # scroll down to load all items
    items = driver.find_elements(
        By.XPATH,
        '//a[@class="x1i10hfl xjbqb8w x6umtig x1b1mbwd xaqea5y xav7gou x9f619 x1ypdohk xt0psk2 xe8uvvx xdj266r x11i5rnm xat24cr x1mh8g0r xexx8yu x4uap5 x18d9i69 xkhd6sd x16tdsg8 x1hl2dhg xggy1nq x1a2a7pz x1heor9g x1lku1pv"]',
    ) 

    item_links = []
    print(f"Found {len(items)} items class" )
    
    for item in items: # loop through all items
        item_links.append(item.get_attribute("href"))
    return item_links



# Markdown format before sending
def format_data_to_markdown(data):
    title = data['title']
    time = data['time']
    location = data['location']
    post_link = data['post_link']

    markdown = f"""
- Title: {title}
- Price: {time}
- Location: {location}
- Post link: {post_link}
"""
    return markdown

@tasks.loop(seconds=config.refresh_rate)
async def repeatedCheck(driver, df, url, count):
    print("Num iteration:", count)
    item_links = get_item_links(driver, url, n_loads)  # get all items
    
    new_item_list =  loop_over_item(driver, df, item_links) #Check each item and update

    # Send notification
    for new_item in new_item_list:
        markdown = format_data_to_markdown(new_item)
        await channel.send(markdown)
        print("Sent notification")
        print(markdown)
    time.sleep(config.refresh_rate)
    count+=1


def execution():
    # Set up WEBDRIVER
    chrome_options = Options()  # Set up Chrome Options
    chrome_options.add_argument("start-maximized")
    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)

    df = pd.read_csv(output_dir, encoding="iso-8859-1") #Load data
    url = config.url
    count = 1
    
    # Start the loop
    repeatedCheck.start(driver, df, url, count)


@bot.event
async def on_ready():
    print("Bot is ready")
    global channel
    channel = bot.get_channel(CHANNEL_ID)

    await channel.send("Bot is ready")
    # sleep a little
    time.sleep(5)

    # start the execution of the task
    execution()



bot.run(BOT_TOKEN)
