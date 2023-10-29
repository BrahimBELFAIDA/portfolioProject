# in this project,i am  scraping data from the website scrapethissite.com
from bs4 import BeautifulSoup
import requests
import pandas as pd
def page_scrape(url):
    page=requests.get(url)
    soup=BeautifulSoup(page.text,'html')

    #the actual  raw data
    raw_data=soup.find_all('tr')
    # cleaning it and putting it in a matrix
    for line in raw_data[1:]:# get rid of that first tr that contains th (headers) and no td
        row_data=[data.text.strip() for data in line.find_all('td')]
        data_table.append(row_data)


url_='https://www.scrapethissite.com/pages/forms/?page_num='
data_table=[['Team name','Year','Wins','Losses','OT Losses','Win %','Goals For','Goals Against', '+/-']]
for i in range(1,24): # the web site contains 24 page
    link=url_+str(i)
    page_scrape(link)
#using pandas
df=pd.DataFrame(columns=data_table[0])
#putting the data in the data frame 

for row in data_table[1:]:
    lenght=len(df)
    df.loc[lenght]=row
#Exporting the data into a csv file 
df.to_csv(r'C:\Users\belfa\OneDrive\Documents\Data Analyst bootcamp\Python\Web scraping\Hockey_teams.csv', index=False)