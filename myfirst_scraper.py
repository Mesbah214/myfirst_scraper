# File: myfirst_scraper.py
#       A simple app used to scrape data from the given url. It supports pagination, meaning
#       capable of fetching data from multiple pages. It can also fetch data that are not
#       present in every container and saves the scraped data to a CSV file through pandas
#       data frame.
# By: Mesbah Uddin


# importing necessary libraries
import requests
from bs4 import BeautifulSoup
import time
import pandas as pd

# setting the target url under url variable
url = "https://www.yellowpages.com/detroit-mi/beauty?page="

# setting the user agent
headers = {
    "User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:77.0) Gecko/20100101 Firefox/77.0"}

# creating a blank list to append information that comes from the for loop.
salon_info = []

# to loop through multiple pages
for x in range(1, 4):

    # sending a request to the server to get the HTML of the given page and feeding this to the r variable.
    r = requests.get(url+str(x), headers=headers)

    # parsing HTML with the help of BeautifulSoup and feeding this to the soup variable.
    soup = BeautifulSoup(r.text, "html.parser")

    # to find out all the containers on the page
    containers = soup.findAll(class_="info")[:30]

    # setting a for loop to extract target elements from all containers
    for container in containers:

        # adding try and except block because some elements are missing in some containers
        try:
            name = container.find(class_="business-name").text
        except Exception as e:
            name = None

        try:
            phone = container.find(class_="phones phone primary").text
        except Exception as e:
            phone = None

        try:
            ratings = container.find(class_="count").text
        except Exception as e:
            ratings = None

        try:
            street_address = container.find(class_="street-address").text
        except Exception as e:
            street_address = None

        try:
            local_address = container.find(class_="locality").text
        except Exception as e:
            local_address = None

        # saving the scraped data into a dictionary as it is flexible to work with dictionaries
        info = {
            "Name": name,
            "Ratings": ratings,
            "Contact": phone,
            "Str. Address": street_address,
            "Locality": local_address,
        }

        # appending data to the empty list after every page is scraped
        salon_info.append(info)

    # waiting time before scraping next page
    time.sleep(3)

    # printing the number of items scraped to the console
    print("the number of items scraped: " + str(len(salon_info)))

# creating a data frame with pandas
df = pd.DataFrame(salon_info)

# printing the head of the file to the console to check if it works
print(df.head())

# exporting the data frame to a CSV file
df.to_csv("myfirst_scraper/salon_in_detroit.csv")
