############ ********* Jumia Web Scraping **************###################
# importing libraries
from bs4 import BeautifulSoup
import requests
import time 
import datetime
import csv

import smtplib # for sending emails 


#connect to jumia
URL='https://www.jumia.ma/t-shirt-noir-otaku-attack-on-titan-100-coton-generic-mpg1347506.html'

# go to httpbin.org/get to get your user-agent that we put in headers 
headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0', "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
page=requests.get(URL, headers=headers)

soup1=BeautifulSoup(page.content, 'html.parser')
soup2=BeautifulSoup(soup1.prettify(), 'html.parser')#just to make it formated
# to get the title of the item
title = soup1.find("h1", {"class": "-fs20 -pts -pbxs"}).get_text()

# to get the price of the item
# note that the price in jumia can be given in two formats 
#   as a range '10 Dhs - 25 Dhs' or a fixed price '15 Dhs'
price = soup1.find("span", {"class": "-b -ltr -tal -fs24 -prxs"}).get_text()
prices=[price.split(' ')[0], price.split(' ')[3] if len(price.split(' '))> 2 else None]
# max price among min dh - max dh format used by jumia
    
# putting the data in a csv file

#date of today
today = datetime.date.today()
header=['Item','Price','Max Price','Date']
data= [title]+prices+[today]

with open('jumiaScraping.csv', 'w', newline='', encoding='UTF8') as file:
    writer=csv.writer(file)
    writer.writerow(header)
    writer.writerow(data)

#Now we are appending data to the csv

with open('jumiaScraping.csv', 'a+', newline='', encoding='UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(data)


# we can put all of the above in a function

def priceCheck():
    URL='https://www.jumia.ma/t-shirt-noir-otaku-attack-on-titan-100-coton-generic-mpg1347506.html' 
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:109.0) Gecko/20100101 Firefox/119.0', "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}
    
    page=requests.get(URL, headers=headers) 
    soup1=BeautifulSoup(page.content, 'html.parser')
    soup2=BeautifulSoup(soup1.prettify(), 'html.parser')
    
    title = soup2.find("h1", {"class": "-fs20 -pts -pbxs"}).get_text()
    
    price = soup2.find("span", {"class": "-b -ltr -tal -fs24 -prxs"}).get_text()
    prices=[price.split(' ')[0], price.split(' ')[3] if len(price.split(' '))> 2 else None]

    today = datetime.date.today()
    
    header=['Item','Price','Max Price','Date']
    data= [title]+prices+[today]
    
    with open('jumiaScraping.csv', 'w', newline='', encoding='UTF8') as file:
        writer=csv.writer(file)
        writer.writerow(header)
        writer.writerow(data)
    file.close()
    
    with open('jumiaScraping.csv', 'a+', newline='', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

# we can programmm this function to be executed once every day (for example)
while(True):
    priceCheck()
    time.sleep(86400)# we have 86400 s in a day (60*60*24)
    
# now if we want for example to watch that article in jumia for a price drop, and send an email


def send_email():
    server = smtplib.SMTP_SSL('smtp.gmail.com',465)
    server.ehlo()
    #server.starttls()
    server.ehlo()
    server.login('belfaidabrahim@gmail.com','************')
    
    subject = "Price drop! Now is your chance to buy!"
    body = """Xerxes, This is the moment we have been waiting for. Now is your chance to 
    pick up the shirt of your dreams. Don't mess it up! 
    Link here: https://www.jumia.ma/t-shirt-noir-otaku-attack-on-titan-100-coton-generic-mpg1347506.html
    """
   
    msg = f"Subject: {subject}\n\n{body}"
    
    server.sendmail(
        'belfaidabrahim@gmail.com',
        msg
     
    )

if prices[0]<80:
    send_email()

























