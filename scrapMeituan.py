#!/usr/bin/python
#encoding : utf-8

import requests
from bs4 import BeautifulSoup
import csv
import time
import logging
import random
import re
import sys

reload(sys)
sys.setdefaultencoding('utf8')

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("_scrapy_")
headers = {
    'Host':'www.meituan.com',
    'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    'Accept': '*/*',
    'Accept-Language': 'zh-CN,zh;q=0.8,en;q=0.6,zh-TW;q=0.4',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Cookie':'rvct=1; _lxsdk_cuid=15f80d94afbc8-0109ec1774b8de-31657c00-fa000-15f80d94afbc8; uuid=0dfcb1dc644fb96a5496.1509695244.0.0.0; oc=To5Wko0nIcX0g1fdK8Js-bosrOmLpMwKDmfM2bYdnz0QaDUpeyefb8_K7uTAblmmbOOUrVEXNGK3Z3ALFhD0-z7GxyvztIwlJejQXJ7efFQS8z6cCPhTfWxUMVnabd-lof7ZVgF_vwhz7IhZ0QXnWQz4CnLVkTHPMmjJmZuISRM; __mta=211195178.1509695280184.1509968906983.1509968924202.8; IJSESSIONID=pmvoyog5njj01kgq1oijwr98y; iuuid=28CFD38A886F728F71DE326B34F61F6B38581E19D0D6632D511906E8FB1F6A81; webp=1; idau=1; ci3=1; latlng=39.90403,116.407526,1509969037925; _hc.v=75d58719-71bd-096e-2de5-b35b166322a5.1509969068; ci=1; cityname="%E5%8C%97%E4%BA%AC"; _lxsdk_s=15f912823a8-d87-419-c65%7C%7C34; i_extend=C_b3GimthomepagesearchH__a100001__b1; __utma=74597006.1394191629.1509969021.1509969021.1509969021.1; __utmb=74597006.18.9.1509969074783; __utmc=74597006; __utmz=74597006.1509969021.1.1.utmcsr=(direct)|utmccn=(direct)|utmcmd=(none)'}

count = 0

def extractData(content):
    logger.info("Scrap " + str(count) + " pages!")
    print content

def getData(url):
    global count
    logger.info(" Request "+ url)
    r = requests.get(url, headers=headers)
    logger.info(" Begin to extract data")
    count = count + 1
    extractData(r.text)

def start():
    url = "http://www.meituan.com/ptapi/poi/getcomment?id=274627&pageSize=10&sortType=1&offset="
    for i in xrange(0,10001):
        logger.info(" Start to process page "+str(i))
        req_url =url + str(i*10)
        getData(req_url)
        time.sleep(random.randint(5,10))

if __name__ == "__main__":
    start()
