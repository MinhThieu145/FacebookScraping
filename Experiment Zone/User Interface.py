import tkinter
import customtkinter as ctk

# threading stuff
import threading

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

# For email sending 
import smtplib, ssl

## email.mime subclasses
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

# initialize email sender
email_sender = 'facebookmarketbot123@gmail.com'
password_sender = 'boncpceigcggknyp'
running = False # Check if the program is running
driver = None # Selenium driver


# Selenium Scraper
def SeleniumCore(url, email_reciever, text_box):
    # Set up Chrome Options
    chrome_options = Options()
    chrome_options.add_argument("start-maximized")
    chrome_options.add_argument("--disable-notifications")
    chrome_options.add_argument("--disable-infobars")

    global driver # Selenium driver global variable
    driver = webdriver.Chrome(executable_path="chromedriver.exe", options=chrome_options)

    # Open the website
    driver.get(url)
    # wait for the page to load
    time.sleep(5)

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

            # write to the csv file
            with open('data.csv', 'a', newline='') as f:
                writer = csv.writer(f)
                writer.writerow([title, price, location, photo_link, item_link])

            # add to the dataframe
            df = df.append({'title': title, 'time': price, 'location': location, 'photo_link': photo_link, 'post_link': item_link}, ignore_index=True)

        # return the dataframe
        return df
    
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # core of the program
    def Core():
        
        # just for the waiting
        WebDriverWait(driver, 5).\
                until(EC.presence_of_element_located((By.XPATH,'//div[@class="xkrivgy x1gryazu x1n2onr6"]'))).text

        items = driver.find_elements(By.XPATH, '//div[@class="x9f619 x78zum5 x1r8uery xdt5ytf x1iyjqo2 xs83m0k x1e558r4 x150jy0e xnpuxes x291uyu x1uepa24 x1iorvi4 xjkvuk6"]//div[@class="xjp7ctv"]')
        print(len(items))

        # Now scrap data
        df =  search_info(items)

        return df
    
    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Set up HTML email
    def GenerateHTML(new_item_list):
        html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta charset="utf-8">
            <title>New Items</title>
            <style>
            body {
                font-family: Arial, sans-serif;
                font-size: 16px;
                line-height: 1.5;
                background-color: #f4f4f4;
            }

            .card {
                width: 300px;
                height: 400px;
                border: 1px solid #ccc;
                border-radius: 5px;
                overflow: hidden;
                display: inline-block;
                margin-right: 20px;
                margin-bottom: 20px;
                float: left;
            }

            .card img {
                width: 100%;
                height: 60%;
                object-fit: cover;
            }

            .card-body {
                padding: 10px;
                text-align: left;
            }

            .card-title {
                font-size: 20px;
                font-weight: bold;
                margin: 0 0 10px;
                text-align: left;
            }

            .card-text {
                margin: 3px 0;
                text-align: left;
            }

            .card-button {
                display: block;
                margin-top: 10px;
                padding: 5px 10px;
                border: 1px solid #ccc;
                border-radius: 5px;
                background-color: #fff;
                color: #333;
                text-align: center;
                text-decoration: none;
            }

            .card-button:hover {
                background-color: #f4f4f4;
            }
            </style>
        </head>
        <body>
            <h2>Featured Items</h2>
        """

        for item in new_item_list:
            html += f"""
            <div class="card">
            <img src="{item['photo_link']}" alt="{item['title']}">
            <div class="card-body">
                <h3 class="card-title">{item['title']}</h3>
                <p class="card-text">Price: {item['time']}</p>
                <p class="card-text">Location: {item['location']}</p>
                <a href="{item['post_link']}" class="card-button">Go to Post</a>
            </div>
            </div>
            """

        html += """
            </body>
            </html>
            """
        
        return html

    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # Send email
    def SendNotification(new_item):
        # generate the content of the email
        html = GenerateHTML(new_item)

        subject = 'New items on Facebook Marketplace'

        em = MIMEMultipart()
        em.attach(MIMEText(html, 'html'))


        em['From'] = email_sender
        em['To'] = email_reciever
        em['Subject'] = subject

        # connect to server
        context = ssl.create_default_context()

        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as server:
            server.login(email_sender, password_sender)
            server.sendmail(email_sender, email_reciever, em.as_string())

    # ----------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------
    # main function
    df = Core()
    global running
    while True:
        # print a message saying that the program is running
        text_box.insert('0.0', "Scraper is running...\n")

        # get data and compare to see any new ite
        df_new = Core()

        # compare the data
        if df.equals(df_new):
            print("No new item")

            # print out message
            text_box.insert('0.0', "No new item\n")
        else:
            print("New item")

            # print out message
            text_box.insert('0.0', "New item. Sending to mail right now\n")

            # get the new item
            merged = df.merge(df_new, indicator=True, how='outer')
            new_item = merged[merged['_merge']=='right_only']

            # convert to a list of dictionary
            new_item = new_item.to_dict('records')

            # now send the notification to the user
            SendNotification(new_item)

            # update the data
            df = df_new

            # now check if the user wants to stop the program
            if running == False:
                break

        # message saying that the program will be restarted in 30 seconds
        text_box.insert('0.0', "Scraper will be restarted in 30 seconds\n")

        # restart the browser
        driver.refresh()
    
        # sleep for 30 seconds
        time.sleep(30)

       


        




ctk.set_appearance_mode('dark')
ctk.set_default_color_theme('dark-blue')

app = ctk.CTk() # create window
app.geometry('500x500') # set window size
app.title('Facebook Scraper')

# global thread 
selenium_thread = None

# variables to start or stop the program
def scrape():
    global running
    running = True
    url = url_entry.get()
    email=email_entry.get()
    global selenium_thread
    selenium_thread = threading.Thread(target=SeleniumCore, args=(url, email, text_box))
    selenium_thread.start()

    # print a message saying that the thread has started with tkinter
    text_box.insert('0.0', 'Scraping Started. Having fun scraping!\n')
    

def stop():
    global running
    running = False

    # driver close
    driver.close()

    # print a message saying that the thread has finished with tkinter
    text_box.insert('0.0', 'Scraper stopped!\n')



# title
title = ctk.CTkLabel(master=app, text='Facebook Scraper', text_color='white', compound='center', font=('Arial', 20, 'bold'))
title.pack(pady=10)

# 
# Instructions
instructions = ctk.CTkLabel(master=app, text='Enter the URL of the Facebook post you want to scrape', text_color='white', compound='center', font=('Arial', 15))
instructions.pack(pady=10)

# entry box for URL
url_entry = ctk.CTkEntry(master=app, width=400, height=50, font=('Arial', 15))
url_entry.pack(pady=10)

# Instructions 2
instructions = ctk.CTkLabel(master=app, text='Enter the email you want to recive notification', text_color='white', compound='center', font=('Arial', 15))
instructions.pack(pady=10)

# entry box for Email
email_entry = ctk.CTkEntry(master=app, width=400, height=50, font=('Arial', 15))
email_entry.pack(pady=10)

# make 2 buttons next to each other
button_frame = ctk.CTkFrame(master=app)
button_frame.pack(pady=10)

# button to scrape
scrape_button = ctk.CTkButton(master=button_frame, text='Scrape', width=70, height=40, font=('Arial', 15), command=scrape)
scrape_button.pack(side='left', padx=10)

# button to exit
exit_button = ctk.CTkButton(master=button_frame, text='Stop', width=70, height=40, font=('Arial', 15), command=stop)
exit_button.pack(side='right', padx=10)

# text box
text_box = ctk.CTkTextbox(master=app, width=400, height=300, font=('Arial', 15))
text_box.pack(pady=10)



app.mainloop() # run window

