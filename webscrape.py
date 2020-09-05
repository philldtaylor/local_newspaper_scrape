#!/usr/bin/python3

#first of all we need to grab the web page using requests
import requests
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd
import smtplib, ssl
import re

today = date.today().strftime('%d-%m-%Y')
baseurl = 'https://www.theboltonnews.co.uk/'
headlines = []
URLlist = []
uriRegex = re.compile(r'\/.*\/')
newsRegex = re.compile(r'[a-zA-Z0-9]*')
#def scrapesite():
r = requests.get(baseurl)
c = r.content
soup = BeautifulSoup(c,'html.parser')
all = soup.find_all('div',{'class':'nq-article-card-content'})
print(all)
count = len(all) - 1
print(count)

for n in range(0,count):
    strjustnews = ''
    try:
        fullstr = str(all[n].find_all('a')[1])
        hr = fullstr.split(' ')
        href = hr[2]
        uri = href.split('"')[1]
        uri_anchor_removed = uriRegex.findall(uri)
        #print(uri_anchor_removed[0])
        fullURL = baseurl + uri_anchor_removed[0]
        #print(fullURL)
        URLlist.append(str(fullURL))
    except Exception as e:
        print(e)
        URLlist.append('Sorry, URL unavailable for this story')

    try:
        #headlines.append(str(all[n].find_all('a')[0].text))
        news = all[n].find_all('a')[0].text
        #print(news)
        justnews = newsRegex.findall(news)
        #print(justnews)
        for i in justnews:
            strjustnews = strjustnews + ' ' +  i
        headlines.append(strjustnews)
    except Exception as e:
        print(e)
        headlines.append("This headline has gone missing!")

d = {'Headline':headlines,'URL':URLlist}
#d = {'URL':URLlist}
df = pd.DataFrame(data = d)
#print(df)
df.to_csv('/home/phill/Documents/python_projects/BN_headlines_' + today + '.csv')
with open('/home/phill/Documents/python_projects/BN_headlines_' + today + '.csv', 'r') as rf:
    msg = rf.read()
#msg = str(df)
import smtplib
conn = smtplib.SMTP('smtp.gmail.com',587)
conn.ehlo()
conn.starttls()
conn.login("OttoKretschmer666@gmail.com","Submarine1")
conn.sendmail('OttoKretschmer666@gmail.com','OttoKretschmer666@gmail.com', 'Subject: Automatic news from your local rag \n \n \n' + msg, mail_options=('SMTPUTF8'))
conn.sendmail('OttoKretschmer666@gmail.com','phillit@hotmail.co.uk', 'Subject: Automatic news from your local rag \n \n \n' + msg, mail_options=('SMTPUTF8'))
conn.sendmail('OttoKretschmer666@gmail.com','l.partington2012@googlemail.com', 'Subject: Automatic news from your local rag \n \n \n' + msg, mail_options=('SMTPUTF8'))
#conn.sendmail('OttoKretschmer666@gmail.com','phillit@hotmail.co.uk',msg, mail_options=('SMTPUTF8'))
#conn.sendmail('OttoKretschmer666@gmail.com','OttoKretschmer666@gmail.com', 'Subject: Automatic news from the local rag')
conn.quit()
