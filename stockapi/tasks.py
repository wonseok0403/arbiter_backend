from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re
from stockapi.models import Ticker, OHLCV, STOCKINFO
import pandas as pd


@task(name="stock-ticker")
def ticker():
    data_list = []
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
                    Ticker.objects.bulk_create(data_list)
                    success = True
                    return success
                for i in range(len(table)):
                    code = table[i].find('a').attrs['href'][-6:]
                    name = table[i].text.split("\n")[2]
                    market_type = market_dic['Q']
                    ticker_inst = Ticker(date=date,
                                        name=name,
                                        code=code,
                                        market_type=market_type)
                    data_list.append(ticker_inst)
                page = page + 1
        for i in range(len(table)):
            code = table[i].find('a').attrs['href'][-6:]
            name = table[i].text.split("\n")[2]
            market_type = market_dic['P']
            ticker_inst = Ticker(date=date,
                                name=name,
                                code=code,
                                market_type=market_type)
            data_list.append(ticker_inst)
        page = page + 1


def ohlcv(ticker):
    success = False
    data_list = []
    date_time = datetime.now().strftime('%Y%m%d')
    for i in range(len(ticker)):
        url = 'http://finance.naver.com/item/sise.nhn?code=' + ticker[i].code
        code = ticker[i].code
        user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
        r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
        soup = BeautifulSoup(r.text, 'html.parser')
        name = soup.findAll('dt')[1].text
        df = pd.read_html(url, thousands='')
        market = ticker[i].market_type
        name = name
        code = code
        date = date_time
        open_price = df[1].iloc[3,3].replace(",","")  #시가
        close_price = df[1].iloc[0,1].replace(",","") #현재가,종가
        high_price = df[1].iloc[4,3].replace(",","")  #고가
        low_price = df[1].iloc[5,3].replace(",","") #저가
        volume = df[1].iloc[3,1].replace(",","")

        ohlcv_inst = OHLCV(date=date, name=name, code=code, market_type=market,
                            open_price=open_price, close_price=close_price,
                            high_price=high_price, low_price=low_price,
                            volume=volume)

        data_list.append(ohlcv_inst)
    OHLCV.objects.bulk_create(data_list)
    success=True
    return success, "Data request complete"


@task(name="kospistock-info")
def kospistockinfo():
    success = False
    data_list = []
    date_time = datetime.now().strftime('%Y%m%d%H%M')
    page = 0
    market_dic = {'P':'KOSPI', 'Q':'KOSDAQ'}
    while 1:
        page = page + 1
        url = 'http://finance.daum.net/quote/volume.daum?stype=P&page={}'.format(str(page))
        market_dic = {'P':'KOSPI', 'Q':'KOSDAQ'}
        user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
        r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.findAll('tr',{'onmouseout':'highlight(this,false)'})
        length = len(table)
        if length==0:
            break
        for i in range(len(table)):
            code = table[i].find('a').attrs['href'][-6:]
            name = table[i].text.split("\n")[2]
            price = table[i].text.split("\n")[3].replace(',','')
            volume = table[i].text.split("\n")[6].replace(',','')
            market_type = market_dic['P']
            stockinst = STOCKINFO(date=date_time,name=name,code=code,
                                    price=price, volume=volume, market_type=market_type)
            data_list.append(stockinst)
    STOCKINFO.objects.bulk_create(data_list)
    success=True
    return success, "Data request complete"



@task(name="kosdaqstock-info")
def kosdaqstockinfo():
    # start = time.time()
    success = False
    data_list = []
    date_time = datetime.now().strftime('%Y%m%d%H%M')
    page = 0
    market_dic = {'P':'KOSPI', 'Q':'KOSDAQ'}
    while 1:
        page = page + 1
        url = 'http://finance.daum.net/quote/volume.daum?stype=Q&page={}'.format(str(page))
        market_dic = {'P':'KOSPI', 'Q':'KOSDAQ'}
        user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
        r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
        soup = BeautifulSoup(r.text, 'html.parser')
        table = soup.findAll('tr',{'onmouseout':'highlight(this,false)'})
        length = len(table)
        if length==0:
            break
        for i in range(len(table)):
            code = table[i].find('a').attrs['href'][-6:]
            name = table[i].text.split("\n")[2]
            price = table[i].text.split("\n")[3].replace(',','')
            volume = table[i].text.split("\n")[6].replace(',','')
            market_type = market_dic['Q']
            stockinst = STOCKINFO(date=date_time,name=name,code=code,
                                    price=price, volume=volume, market_type=market_type)
            data_list.append(stockinst)
    STOCKINFO.objects.bulk_create(data_list)
    success=True
    return success, "Data request complete"


@task(name="ohlcv-get-01")
def ohlcv_1():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[:ticker_cut]
    ohlcv(ticker_list)

@task(name="ohlcv-get-02")
def ohlcv_2():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[ticker_cut:2*ticker_cut]
    ohlcv(ticker_list)

@task(name="ohlcv-get-03")
def ohlcv_3():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[2*ticker_cut:3*ticker_cut]
    ohlcv(ticker_list)

@task(name="ohlcv-get-04")
def ohlcv_4():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[3*ticker_cut:4*ticker_cut]
    ohlcv(ticker_list)

@task(name="ohlcv-get-05")
def ohlcv_5():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[4*ticker_cut:5*ticker_cut]
    ohlcv(ticker_list)

@task(name="ohlcv-get-06")
def ohlcv_6():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[5*ticker_cut:6*ticker_cut]
    ohlcv(ticker_list)

@task(name="ohlcv-get-07")
def ohlcv_7():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[6*ticker_cut:7*ticker_cut]
    ohlcv(ticker_list)

@task(name="ohlcv-get-08")
def ohlcv_8():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[7*ticker_cut:8*ticker_cut]
    ohlcv(ticker_list)

@task(name="ohlcv-get-09")
def ohlcv_9():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[8*ticker_cut:9*ticker_cut]
    ohlcv(ticker_list)

@task(name="ohlcv-get-10")
def ohlcv_10():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//10
    ticker_list = ticker[9*ticker_cut:]
    ohlcv(ticker_list)



# @task(name="kospi-ticker")
# def kospiticker():
#     # for market in market_list:
#     success = False
#     industry = {}
#     data_list=[]
#     date = datetime.now().strftime('%Y%m%d')
#     url = 'http://finance.daum.net/quote/all.daum?type=U&stype=P'
#     user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
#     r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
#     soup = BeautifulSoup(r.text, 'html.parser')
#     h4 = soup.findAll('h4', {'class':'fl_le'})
#     table = soup.findAll('table',{'class':'gTable clr'})
#
#     for i in range(len(h4)):
#         sec = h4[i].text
#         sec = re.sub('[0-9]','',sec)
#         sec = re.sub('[-.%|]','',sec)
#         industry[i] = sec
#
#     for i in range(len(industry)):
#         td = table[i].findAll('td', {'class':'txt'})
#         sector = industry[i]
#         for t in td:
#             ticker_inst = {}
#             name = t.text
#             a_tag = t.findAll('a')
#             link = a_tag[0].attrs['href']
#             code = link[-6:]
#
#             ticker_inst = Ticker(date=date,
#                                 name=name,
#                                 code=code,
#                                 sector=sector,
#                                 market_type='KOSPI')
#             data_list.append(ticker_inst)
#     Ticker.objects.bulk_create(data_list)
#     success = True
#     return success
