import random

url = "https://www.facebook.com/marketplace/houston/search?daysSinceListed=1&sortBy=creation_time_descend&query=couch&exact=false"
n_loads = 1  # Number of time to scroll
refresh_rate = 15 #Number of time to wait for each iteration
output_dir = "data.csv"

# Discord bot
BOT_TOKEN = "MTA4MzYzNzk2ODk1MjExNTI0MA.GR13si.U4fHTPkybCx3DtxbEzCr7yu5o_XjzlAPnd-Kqc"
CHANNEL_ID = 1083640013180387352

# Scraping Front Page 
sleep_time_each_scroll = 0.5 # thời gian chờ sau mỗi lần scroll xuống
item_scrap_number = 50 # số lượng item tối thiểu cần tìm thấy trên mỗi trang
scroll_number = 10

# generate 5 random hex code for color
def generate_random_color():
    return random.randint(0, 0xffffff)