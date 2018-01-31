from __future__ import absolute_import, unicode_literals
from celery.decorators import task
from datetime import datetime
from bs4 import BeautifulSoup
import requests
import re
from stockapi.models import Ticker, OHLCV, STOCKINFO, Info
import pandas as pd



class crawler(object):
    def __init__(self):
        self. market_dic = {'P':'KOSPI', 'Q':'KOSDAQ'}
        self.date = datetime.now().strftime('%Y%m%d')
        self.url = 'http://finance.daum.net/quote/volume.daum?stype={}&page={}'
    def ticker(self):
        data_list = []
        page = 1
        while 1:
            url = self.url.format('P',str(page))
            user_agent = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/55.0.2883.95 Safari/537.36'}
            r = requests.get(url, headers= user_agent, auth=('user', 'pass'))
            soup = BeautifulSoup(r.text, 'html.parser')
            table = soup.findAll('tr',{'onmouseout':'highlight(this,false)'})
            length = len(table)
            if length==0:
                page=1
                while 1:
                    url = self.url.format('Q',str(page))
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
                        market_type = self.market_dic['Q']
                        ticker_inst = Ticker(date=self.date,
                                            name=name,
                                            code=code,
                                            market_type=market_type)
                        data_list.append(ticker_inst)
                    page = page + 1
            for i in range(len(table)):
                code = table[i].find('a').attrs['href'][-6:]
                name = table[i].text.split("\n")[2]
                market_type = self.market_dic['P']
                ticker_inst = Ticker(date=self.date,
                                    name=name,
                                    code=code,
                                    market_type=market_type)
                data_list.append(ticker_inst)
            page = page + 1

from datetime import datetime, timedelta

class Management(object):
    def __init__(self):
        self.today = datetime.now()
        # self.oneday_ago = self.today-timedelta(days=1)
        # self.oneday_ago = self.oneday_ago.strftime('%Y%m%d')
        self.ticker = Ticker.objects.filter(date=self.today)
        self.ordered_info_list = Info.objects.filter(date=self.today).order_by('-market_cap')

    def sizeMangement(self):
        kospi_rank = 1
        kosdaq_rank = 1
        for self.ordered_info in self.ordered_info_list:
            print(self.ordered_info)
            market = self.ticker.filter(code=self.ordered_info.code)[0].market_type
            if market=='KOSPI' : #코스피
                #시가총액 순위
                self.ordered_info.market_cap_rank = kospi_rank
                #코스피 사이즈 매기기
                if(kospi_rank<=100):
                    self.ordered_info.size_type = 'L'
                elif(kospi_rank<=300):
                    self.ordered_info.size_type = 'M'
                else:
                    self.ordered_info.size_type = 'S'
                self.ordered_info.save()
                kospi_rank += 1
                print(kospi_rank)
            else: #코스닥
                self.ordered_info.market_cap_rank = kosdaq_rank
                if (kosdaq_rank<=100):
                    self.ordered_info.size_type = 'L'
                elif (kosdaq_rank<=400):
                    self.ordered_info.size_type = 'M'
                else:
                    self.ordered_info.size_type = 'S'
                self.ordered_info.save()
                kosdaq_rank += 1
                print(kosdaq_rank)
        return True
