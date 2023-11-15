# Automated Facebook Marketplace Scraper and Discord Notification Bot

## Project Overview
This project involves the development of an automated data pipeline designed to scrape Facebook Marketplace listings on a daily basis. The key feature of this pipeline is its integration with a Discord bot, which notifies users on a server about new listings. The project leverages various AWS services, Selenium for web scraping, and Python for scripting and bot interaction.

## Features

### Facebook Marketplace Data Scraping
- **Technology Used:** Selenium.
- **Functionality:** Dynamically scrapes Facebook Marketplace for specific listings based on predefined criteria.
- **Automation:** Script runs on a scheduled basis, facilitated by AWS CloudWatch.

### AWS Lambda and CloudWatch Integration
- **Serverless Execution:** Utilizes AWS Lambda for running the scraping script without the need for a dedicated server, optimizing resource usage.
- **Scheduled Script Execution:** Employs AWS CloudWatch to manage the scheduling of the scraping script, ensuring daily data collection.

### Data Storage on AWS S3
- **CSV Data Storage:** Scraped data is stored in a structured CSV format on AWS S3, allowing for easy data retrieval and analysis.

### Discord Bot Integration
- **Hosted on AWS EC2:** The bot is hosted on an EC2 instance, ensuring reliable and continuous operation.
- **Notification System:** Users on the Discord server receive real-time notifications via the bot about new listings from Facebook Marketplace.
- **Webhook Integration:** Utilizes Discord bot webhook for seamless communication and notifications.

### Interactive Bot Features
- **User Registration for New Items:** Allows users to register their interest in new items, customizing the data they receive.
- **Customizable Notification Schedule:** Users can set and modify the schedule for receiving notifications about new listings.
- **Data Management Commands:** Users can issue commands to the bot to manage data, such as deleting files or changing notification settings.

### Boto3 and Python Integration
- **AWS Service Interaction:** Utilizes boto3 library in Python for interacting with various AWS services, enhancing the bot's capabilities in data management and scheduling.

### Demo Video
