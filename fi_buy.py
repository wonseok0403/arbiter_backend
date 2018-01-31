
# coding: utf-8

# In[2]:

from datetime import datetime, timedelta
from bs4 import BeautifulSoup
from datetime import datetime
import time
import requests
import re
import pandas as pd
import math
import time


# In[3]:

today = datetime.now()
one_years_ago = today-timedelta(days=366)
one_years_ago = one_years_ago.strftime('%Y%m%d')
one_years_ago


# In[12]:

def ticker():
    stock = []
    page = 1
    market_dic = {'P':'KOSPI', 'Q':'KOSDAQ'}
    date = datetime.now().strftime('%Y%m%d')
    while 1:
        url = 'http://finance.daum.net/quote/volume.daum?stype=P&page={}'.format(str(page))
        market_dic = {'P':'KOSPI', 'Q':'KOSDAQ'}
        user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
        r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.findAll('tr',{'onmouseout':'highlight(this,false)'})
        length = len(table)
        if length==0:
            page=1
            while 1:
                url = 'http://finance.daum.net/quote/volume.daum?stype=Q&page={}'.format(str(page))
                r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
                soup = BeautifulSoup(r.text, 'html.parser')
                table = soup.findAll('tr',{'onmouseout':'highlight(this,false)'})
                if len(table)==0:
                    return stock
                for i in range(len(table)):
                    code = table[i].find('a').attrs['href'][-6:]
                    name = table[i].text.split("\n")[2]
                    market_type = market_dic['Q']
                    stockinst = {'date':date, 'name':name, 'code':code, 'market_type':market_type}
                    stock.append(stockinst)
                page = page + 1
        for i in range(len(table)):
            code = table[i].find('a').attrs['href'][-6:]
            name = table[i].text.split("\n")[2]
            market_type = market_dic['P']
            stockinst = {'date':date, 'name':name, 'code':code, 'market_type':market_type}
            stock.append(stockinst)
        page = page + 1
    
stock = ticker()


# In[21]:

def buysellrecent():
    data_list=[]
    start = time.time()
    for i in range(100):
        url = 'http://finance.naver.com/item/frgn.nhn?code='+ stock[i]['code']
        print(url)
        user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
        r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
        soup = BeautifulSoup(r.text, 'html.parser')
        tmp = soup.findAll('table',{'class':'type2'})
        table = soup.findAll('tr',{'onmouseout':'mouseOut(this)'})
        date=table[1].find('span',{'class':'tah p10 gray03'}).text.replace('.','')
        code=stock[i]['code']
        name=stock[i]['name']
        institustion = table[0].findAll('td')[5].text
        if type(institustion) == int:
            institustion = institustion
        else:
            institustion = institustion.replace(',','')
        foriegn = table[0].findAll('td')[6].text
        if type(foriegn) == int:
            foriegn = foriegn
        else:
            foriegn = foriegn.replace(',','')
        tmp_data = {'date':date, 'code':code, 'name':name, 'institution':institustion, 'foreign':foriegn}
        data_list.append(tmp_data)
    end = time.time()
    return end-start, data_list

buyselltoday()


# In[36]:

def buyselltotal():
    today = datetime.now()
    one_years_ago = today-timedelta(days=365)
    one_years_ago = one_years_ago.strftime('%Y%m%d')
    one_years_ago
    data_list = []
    page = 1
    while 1:
        url = 'http://finance.naver.com/item/frgn.nhn?code=058820&page='+ str(page)
        print(url)
        user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
        r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
        soup = BeautifulSoup(r.text, 'html.parser')
        tmp = soup.findAll('table',{'class':'type2'})
        table = soup.findAll('tr',{'onmouseout':'mouseOut(this)'})
        for i in range(len(table)):
            date=table[i].find('span',{'class':'tah p10 gray03'}).text.replace('.','')
            if date <= one_years_ago:
                return data_list
            institustion = table[i].findAll('td')[5].text
            if type(institustion) == int:
                institustion = institustion
            else:
                institustion = institustion.replace(',','')
            foriegn = table[0].findAll('td')[6].text
            if type(foriegn) == int:
                foriegn = foriegn
            else:
                foriegn = foriegn.replace(',','')
            tmp = {'date':date, 'code':'058820', 'institustion':institustion, 'foriegn':foriegn}
            data_list.append(tmp)
        page = page+1


# In[37]:

buysell()
