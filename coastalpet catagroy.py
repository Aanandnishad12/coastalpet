"""Ms. Harshal Lad"""
from bs4 import BeautifulSoup 
import re
import time
import requests
import sys
import time
import json
import csv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
import time
import mysql.connector
import sys


mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  password="Anishad@123",
  database = "abc"
)

mycursor = mydb.cursor()
mycursor.execute("""CREATE TABLE if not exists `coastalpet_categories` (
  `id` int(11) NOT NULL AUTO_INCREMENT,
  `category` varchar(250) NOT NULL,
  `sub_category` varchar(250) NOT NULL,
  `sub_sub_category` varchar(250) NOT NULL,
  `sub_sub_sub_category` varchar(250) NOT NULL,
  `page_url` varchar(250) NOT NULL,
  `processed` int(11) NOT NULL DEFAULT '0',
  KEY `id` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=1 DEFAULT CHARSET=latin1""")

headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}   
def anand():
    def get_category(link):
        global headers
        response = requests.get(link, headers = headers)
        #print(response.status_code)
        #print(response.text)
        html = response.text
        soup = BeautifulSoup(html)
        # print(soup)
        return soup

    def data(cat1,cat2,link1_val):
        #print(cat1,cat2,link1_val)
        link1='https://coastalpet.com'+str(link1_val)
        #print(link1)
        soup2=get_category(link1)
        tag =soup2.findAll('ul',attrs = {'class':'product-category__sidebar-list'})
        for tagval in tag:
         
            link2_val=tagval.findAll('a')
            for val in link2_val:
             
                cat3=val.text.lstrip().rstrip()
                #print(cat3)
                link2=val.get('href')
                #print(link2)
            # print(cat3,link2)     
                soup3=get_category(link2)
                tag3 =soup3.findAll('ul',attrs = {'class':'product-category__sidebar-list'})
                for tagval3 in tag3:
                 
                    link3_val=tagval3.findAll('a')
                    for val3 in link3_val:
                        
                        cat4=val3.text.lstrip().rstrip()
                #        print(cat4)
                        link3=val3.get('href')
                        link3='https://coastalpet.com'+str(link3)
                #       print(link3)
                        try:
                            mycursor = mydb.cursor()
                            mycursor.execute("select id from coastalpet_categories where `page_url`=%s ",(link3,))
                            result = mycursor.fetchall()
                        #   print(result)
                            if result ==[]:
                             
                                mycursor = mydb.cursor()
                                val=list(zip((cat1,),(cat2,),(cat3,),(cat4,),(link3,)))
                        #      print(val)
                                sql = """insert into coastalpet_categories(`category`, `sub_category`, `sub_sub_category`,`sub_sub_sub_category`,`page_url`) values (%s,%s,%s,%s,%s)""" 
                                
                                mycursor.executemany(sql,val) 
                                mydb.commit()

                        except Exception as e:
                            print (e)           
    url='https://www.coastalpet.com/'
    soup =get_category(url)
    ul_tag2 =soup.findAll('li',attrs = {'class':'site-navigation__sub-item'})
    for li in ul_tag2:
       
        a_tag=li.findAll('a',attrs = {'class':'site-navigation__cta site-navigation__cta--top'})
        for val in a_tag:
          
            link1val=val.get('href')
            cat2=val.text.lstrip().rstrip()
            # print(cat2)
            if 'dogs' in link1val:
                cat1='Dogs'
            # print(cat1)
                data(cat1,cat2,link1val)
            elif 'cats' in link1val:
                cat1='Cats'
                #print(cat1)
                data(cat1,cat2,link1val)
def mail_send(s):
    fromaddr = "anandn@fcsus.com"
    toaddr = "nishadaman4438@gmail.com"
    msg = MIMEMultipart()
    # storing the senders email address  
    msg['From'] = fromaddr
    # storing the receivers email address 
    msg['To'] = toaddr
    # storing the subject 
    msg['Subject'] = "costalpet catagory status "
    # string to store the body of the mail
    body = s
    msg.attach(MIMEText(body, 'plain'))
    # open the file to be sent 
    s = smtplib.SMTP('smtp.office365.com', 587)
    s.starttls()  
    # Authentication(password)
    s.login(fromaddr, 'Aman@123')
    text = msg.as_string()
    s.sendmail(fromaddr, toaddr, text)
    s.quit()
def main():
    try:
        anand()
        s = "Script Executed Successfully"
        mail_send(s)
        print(s)
    except:
        s = "Script Executed Unsuccessfully"
        print(s)

if __name__ == "__main__":
    main()
            
        
   