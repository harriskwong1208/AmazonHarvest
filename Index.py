from bs4 import BeautifulSoup as BS
import time 
import datetime
import smtplib
import requests
import csv
import pandas as pd

header = ['Title','Price','Date']

#Create or write to excel file with title and price data and headers
with open('AmazonHarvest.csv','w',newline='',encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(header)



def check_price():
    
    URL = 'https://www.amazon.com/Funny-Data-Systems-Business-Analyst/dp/B07FNW9FGJ/ref=sr_1_3?dchild=1&keywords=data%2Banalyst%2Btshirt&qid=1626655184&sr=8-3&customId=B0752XJYNL&th=1'

    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/78.0.3904.108 Safari/537.36", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

    page = requests.get(URL, headers=headers)

    soup1 = BS(page.content, "html.parser")
    soup2 = BS(soup1.prettify(),"html.parser")

    title = soup2.find(id="productTitle").get_text()
    title = title.strip()
    price = soup2.find_all("div", {"class": "a-section a-spacing-none aok-align-center aok-relative"})
    price = price[0].get_text()
    price = price.replace(" ","")
    price = price.replace("\n","")
    price = price.split("$")
    price = '$'+ price[1]
    price = price.strip()[1:]

    today = datetime.date.today()


    data = [title,price,today]

    #Appead to excel file 
    with open('AmazonHarvest.csv','a+',newline='',encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

# Grab data from amazon item every 5 seconds 1o times
counter = 1
while(counter <= 10):
    print(f'Obtaining Data, In Progress: {counter}/10......')
    counter = counter +1
    check_price()
    time.sleep(5)


df = pd.read_csv('AmazonHarvest.csv')
print(df)