from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re
from stockapi.models import Ticker, OHLCV, STOCKINFO, Info
import pandas as pd
import math


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


def info(ticker):
    success = False
    data_list=[]
    date = datetime.now().strftime('%Y%m%d')
    f = open(date+"_daily_info_log.txt", 'w')
    user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
    for i in range(len(ticker)) :
        url = 'http://companyinfo.stock.naver.com/v1/company/c1010001.aspx?cn=&cmp_cd='+ ticker[i].code
        code = ticker[i].code
        name = ticker[i].name
        r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
        soup = BeautifulSoup(r.text, 'html.parser')
        tmp = soup.findAll('td',{'class':'cmp-table-cell td0101'})
        if len(tmp) != 0:
            tmp=tmp[0].findAll('dt',{'class':'line-left'})[1].text.replace(' ','').split(':')
            market_type = tmp[0]
            industry = tmp[1]
            url = 'http://finance.naver.com/item/coinfo.nhn?code='+ ticker[i].code
            r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
            soup = BeautifulSoup(r.text, 'html.parser')
            todayinfo = soup.findAll('dl',{'class':'blind'})
            stockinfo = pd.read_html(url, thousands='')
            price = todayinfo[0].findAll('dd')[3].text.split(' ')[1].replace(',','')
            if len(stockinfo[1]) == 5:
                face_val = stockinfo[1].iloc[3,1].replace(' ','').replace(',','').replace('원','').split('l')[0]
                stock_nums = stockinfo[1].iloc[2,1].replace(',','')#상장주식수
                foreign_limit = stockinfo[2].iloc[0,1].replace(',','')
                foreign_possession = stockinfo[2].iloc[1,1].replace(',','')
                foreign_ratio = stockinfo[2].iloc[2,1].replace('%','')
                #per, eps
                per_td = soup.findAll('table',{'class':'per_table'})
                td = per_td[0].findAll('em')
                per_table = []
                for t in td:
                    a = t.text
                    per_table.append(a)
                if per_table[0] == "N/A":
                    per = 0
                else:
                    per = per_table[0].replace(',','')
                if per_table[1] == "N/A":
                    eps = 0
                else:
                    eps = per_table[1].replace(',','')
                if per_table[8] == "N/A":
                    yield_ret = 0
                else:
                    yield_ret = per_table[8]
                if per_table[7] == "N/A":
                    bps = 0
                else:
                    bps = per_table[7].replace(',','')
                if bps == 0:
                    pbr = 0
                else:
                    pbr= round(int(price)/int(bps),2)
                print(code,stockinfo[5].iloc[0,1])
                try:
                    math.isnan(float(stockinfo[5].iloc[0,1].replace('배','').replace(',','')))
                    industry_per = float(stockinfo[5].iloc[0,1].replace('배','').replace(',',''))
                except AttributeError:
                    industry_per = 0
                print(code,industry_per)
                market_cap = int(price)*int(stock_nums) #시가총액
            elif len(stockinfo[1]) == 4:
                face_val = 0
                stock_nums = stockinfo[1].iloc[2,1].replace(',','')#상장주식수
                foreign_limit = stockinfo[2].iloc[0,1].replace(',','')
                foreign_possession = stockinfo[2].iloc[1,1].replace(',','')
                foreign_ratio = stockinfo[2].iloc[2,1].replace('%','')
                #per, eps
                per_td = soup.findAll('table',{'class':'per_table'})
                td = per_td[0].findAll('em')
                per_table = []
                for t in td:
                    a = t.text
                    per_table.append(a)
                per = per_table[0]
                eps = per_table[1].replace(',','')
                if per_table[8] == "N/A":
                    yield_ret = 0
                else:
                    yield_ret = per_table[8]
                if per_table[7] == "N/A":
                    bps = 0
                else:
                    bps = per_table[7].replace(',','')
                if bps == 0:
                    pbr = 0
                else:
                    pbr= round(int(price)/int(bps),2)
                try:
                    math.isnan(float(stockinfo[5].iloc[0,1].replace('배','').replace(',','')))
                    industry_per = float(stockinfo[5].iloc[0,1].replace('배','').replace(',',''))
                except AttributeError:
                    industry_per = 0
                print(code,industry_per)
                market_cap = int(price)*int(stock_nums)
            else:
                face_val = 0
                stock_nums = stockinfo[1].iloc[1,1].replace(',','')#상장주식수
                foreign_limit = 0
                foreign_possession = 0
                foreign_ratio = 0
                per = 0
                eps = 0
                pbr = 0
                bps = 0
                industry_per = 0
                yield_ret = 0
                market_cap = int(price)*int(stock_nums)
            tmp_json=Info(date=date,code=code,name=name,market_type=market_type,industry=industry,
                      price=price,face_val=face_val,stock_nums=stock_nums,market_cap=market_cap,foreign_limit=foreign_limit,
                      foreign_possession=foreign_possession, foreign_ratio=foreign_ratio,per=per,eps=eps,
                      bps=bps,pbr=pbr,industry_per=industry_per,yield_ret=yield_ret)
            data_list.append(tmp_json)
            log = {'date':date,'code':code,'name':name,'market_type':market_type,'industry':industry,'price':price,'face_val':face_val,'stock_nums':stock_nums,
                'market_cap':market_cap,'foreign_limit':foreign_limit,'foreign_possession':foreign_possession, 'foreign_ratio':foreign_ratio,
                'per':per,'eps':eps,'bps':bps,'pbr':pbr,'industry_per':industry_per,'yield_ret':yield_ret}
            f.write(str(log)+'\n')
        else:
            url = 'http://finance.naver.com/item/coinfo.nhn?code='+ ticker[i].code
            r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
            soup = BeautifulSoup(r.text, 'html.parser')
            market_type = "KOSPI"
            industry = "ETF"
            soup = BeautifulSoup(r.text, 'html.parser')
            todayinfo = soup.findAll('dl',{'class':'blind'})
            price = todayinfo[0].findAll('dd')[3].text.split(' ')[1].replace(',','')
            stockinfo = pd.read_html(url, thousands='')
            stock_nums = stockinfo[1].iloc[1,1].replace(',','')#상장주식수
            face_val = 0
            market_cap = int(price)*int(stock_nums) #시가총액
            foreign_limit = 0
            foreign_possession = 0
            foreign_ratio = 0
            per = 0
            eps = 0
            pbr = 0
            bps = 0
            industry_per = 0
            yield_ret = 0
            tmp_json=Info(date=date,code=code,name=name,market_type=market_type,industry=industry,
                      price=price,face_val=face_val,stock_nums=stock_nums,market_cap=market_cap,foreign_limit=foreign_limit,
                      foreign_possession=foreign_possession, foreign_ratio=foreign_ratio,per=per,eps=eps,
                      bps=bps,pbr=pbr,industry_per=industry_per,yield_ret=yield_ret)
            data_list.append(tmp_json)
            log = {'date':date,'code':code,'name':name,'market_type':market_type,'industry':industry,'price':price,'face_val':face_val,'stock_nums':stock_nums,
                'market_cap':market_cap,'foreign_limit':foreign_limit,'foreign_possession':foreign_possession,'foreign_ratio':foreign_ratio,
                'per':per,'eps':eps,'bps':bps,'pbr':pbr,'industry_per':industry_per,'yield_ret':yield_ret}
            f.write(str(log)+"\n")
    f.close()
    success=True
    Info.objects.bulk_create(data_list)
    return success

@task(name="info-get-01")
def info_1():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//5
    ticker_list = ticker[:ticker_cut]
    info(ticker_list)

@task(name="info-get-02")
def info_2():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//5
    ticker_list = ticker[ticker_cut:2*ticker_cut]
    info(ticker_list)

@task(name="info-get-03")
def info_3():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//5
    ticker_list = ticker[2*ticker_cut:3*ticker_cut]
    info(ticker_list)

@task(name="info-get-04")
def info_4():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//5
    ticker_list = ticker[3*ticker_cut:4*ticker_cut]
    info(ticker_list)

@task(name="info-get-05")
def info_5():
    today = datetime.now().strftime('%Y%m%d')
    ticker = Ticker.objects.filter(date=today).order_by('id')
    ticker_count = ticker.count()
    ticker_cut = ticker_count//5
    ticker_list = ticker[4*ticker_cut:]
    info(ticker_list)
