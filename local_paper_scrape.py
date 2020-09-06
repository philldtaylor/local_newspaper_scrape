#!/usr/bin/python3

#first of all we need to grab the web page using requests
import requests
from bs4 import BeautifulSoup
from datetime import date
import pandas as pd
import smtplib, ssl
import re
import smtplib

today = date.today().strftime('%d-%m-%Y')
headlines = []
URLlist = []
uriRegex = re.compile(r'\/.*\/')
newsRegex = re.compile(r'[a-zA-Z0-9]*')

def scrapesite(baseurl):
    r = requests.get(baseurl)
    c = r.content
    soup = BeautifulSoup(c,'html.parser')
    all = soup.find_all('div',{'class':'nq-article-card-content'})
    count = len(all) - 1
    for n in range(0,count):
        strjustnews = ''
        try:
            fullstr = str(all[n].find_all('a')[1])
            hr = fullstr.split(' ')
            href = hr[2]
            uri = href.split('"')[1]
            uri_anchor_removed = uriRegex.findall(uri)
            fullURL = baseurl + uri_anchor_removed[0]
            URLlist.append(str(fullURL))
        except Exception as e:
            print(e)
            URLlist.append('Sorry, URL unavailable for this story')

        try:
            news = all[n].find_all('a')[0].text
            justnews = newsRegex.findall(news)
            for i in justnews:
                strjustnews = strjustnews + ' ' +  i
            headlines.append(strjustnews)
        except Exception as e:
            print(e)
            headlines.append("This headline has gone missing!")
        d = {'Headline':headlines,'URL':URLlist}
        df = pd.DataFrame(data = d)
        df.to_csv('/home/phill/Documents/python_projects/BN_headlines.csv')

def senditout(recipient1,recipient2,recipient3): #function to send email
    with open('/home/phill/Documents/python_projects/BN_headlines.csv', 'r') as rf:
        msg = rf.read()
    conn = smtplib.SMTP('smtp.gmail.com',587)
    conn.ehlo()
    conn.starttls()
    conn.login("OttoKretschmer666@gmail.com","Submarine1")
    conn.sendmail('OttoKretschmer666@gmail.com','OttoKretschmer666@gmail.com', 'Subject: Automatic news from your local rag \n \n \n' + msg, mail_options=('SMTPUTF8'))
    conn.sendmail('OttoKretschmer666@gmail.com',recipient1, 'Subject: Automatic news from your local rag \n \n \n' + msg, mail_options=('SMTPUTF8'))
    #conn.sendmail('OttoKretschmer666@gmail.com',recipient2, 'Subject: Automatic news from your local rag \n \n \n' + msg, mail_options=('SMTPUTF8'))
    #conn.sendmail('OttoKretschmer666@gmail.com',recipient3, 'Subject: Automatic news from your local rag \n \n \n' + msg, mail_options=('SMTPUTF8'))
    conn.quit()

scrapesite('https://www.theboltonnews.co.uk/')
senditout('phillit@hotmail.co.uk','l.partington2012@googlemail.com','ilovebrickwork@gmail.com')
