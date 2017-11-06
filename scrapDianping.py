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
    'Host':'www.dianping.com',
    'User-Agent':"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36",
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8,application/json, text/javascript',
    'Accept-Language': 'en-US,en;q=0.5',
    'Accept-Encoding': 'gzip, deflate',
    'Connection': 'keep-alive',
    'Cookie':'_lxsdk_cuid=15f1984610fc8-002538764b6b48-31657c00-fa000-15f19846110c8; _lxsdk=15f1984610fc8-002538764b6b48-31657c00-fa000-15f19846110c8; _hc.v=4e063b1a-a80a-5c8e-b97d-0b59ffdf732c.1507961627; JSESSIONID=00A5DF9DD06496B52211790E507B15F5; aburl=1; cy=2; cye=beijing; _lxsdk_s=15f254be7ab-959-0c8-c89%7C%7C36'}
#    'Cookie': 'PHOENIX_ID=0a650c81-154a0633f47-a97843; _hc.v="\"e27e18eb-3a3d-4b40-b06a-cbe624c96048.1462979739\""; s_ViewType=10; JSESSIONID=877B00919AD417544F72F5A9953E54B4; aburl=1; cy=2; cye=beijing'}

#headers = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36','upgrade-insecure-requests':'1','Cookie': 'PHOENIX_ID=0a650c81-154a0633f47-a97843; _hc.v="\"e27e18eb-3a3d-4b40-b06a-cbe624c96048.1462979739\""; s_ViewType=10; JSESSIONID=877B00919AD417544F72F5A9953E54B4; aburl=1; cy=2; cye=beijing'}


def getUserInfo(user_id):
    url = "http://dianping.com/member/jsonp/userCarte?rand=464.98264045866455&memberId="+user_id+"&callback=dianping"
    r = requests.get(url, headers=headers)
    r =requests.get(url, headers=headers)

    data = r.text
    re_words=re.compile(r'msg\":\"([\s\S]*)\"\}\);')
    m = re_words.search(data)
    html = m.group(1)
    html = html.replace("\\\"", "\"")
    soup = BeautifulSoup(html,"lxml")
    eara = soup.select("html > body > div.account_infor > div.account_person > p.eara > span")
    user_gender_area =  ""
    for item in eara:
        if item.string != None:
            if user_gender_area == "":
                user_gender_area = item.string
            else:
                user_gender_area += "," + item.string
    #user_gender_area = ",".join(item.string for item in eara) if len(eara) > 0 else ""
    #gender = eara[0].string if len(eara) >=2 else  ""
    #area = eara[1].string if len(eara) >=2 else  ""
    #return gender, area
    return user_gender_area

def extractData(content):
    soup = BeautifulSoup(content, "lxml")
    comment_list = soup.find("div", "comment-list")
    if comment_list is  None:
        logger.error(content)
        return
    ultag = comment_list.contents
    for li in ultag[1].contents:
        if li.name == "li":
            name = li.select("div > p.name")[0].string
            user_id = li.select("div.pic > a.J_card")[0]['user-id']
            time.sleep(1)
            user_gender_area = getUserInfo(user_id)
            contribution = li.select("div > p.contribution > span")[0]['title']
            content = li.select("div.content")[0]
            user_info = content.select("div.user-info")[0]
            rank = user_info.select("span")[0]['title']
            price_tag = user_info.select("span.comm-per")
            price_per = ""
            if len(price_tag) > 0:
                price_per = price_tag[0].string

            comment_tags=""
            comment_rst = user_info.select("div.comment-rst > span.rst")
            for span in comment_rst:
                comment_tags+=span.text + ","
            comment_txt = content.select("div.comment-txt > div.J_brief-cont")[0].text

            misc_info = content.select("div.misc-info")[0]
            post_time = misc_info.select("span.time")[0].string
            misc_name = misc_info.select("h2.misc-name")[0].string
            col_right = misc_info.select("span.col-right")[0]
            heart_count = col_right.select("span.countWrapper > a")[0]['data-count']
            re_count = col_right.select("span > a[total]")[0]['total']
            data = user_id + "|" + name + "|" + user_gender_area + "|"  + contribution + "|" +  rank + "|" + price_per + "|" + comment_tags + "|" + comment_txt.strip() + "|" + heart_count + "|" + re_count + "|" + post_time + "|" + misc_name
            print data.encode('utf-8')

def getData(url):
    #headers = {'user-agent': 'Mozilla/5.0 (iPad; U; CPU OS 3_2_1 like Mac OS X; en-us) AppleWebKit/531.21.10 (KHTML, like Gecko) Mobile/7B405'}
    #proxies = { "http": "http://123.125.5.100:3128"} 
    #proxies = { "http": "http://59.41.204.246:5328"} 
    #proxies = { "http": "http://115.29.170.58:8118"} 
    logger.info(" Request "+ url)
    r = requests.get(url, headers=headers)
    #cookies = r.cookies
    #for k,v in cookies.items():
    #    print k, v
    #r = requests.get(url, headers=headers, proxies=proxies)
    logger.info(" Begin to extract data")
    extractData(r.text)

def start():
    url = "http://www.dianping.com/shop/1916992/review_all?pageno="
    for i in xrange(56,158):
        logger.info(" Start to process page "+str(i))
        req_url =url + str(i)
        getData(req_url)
        time.sleep(random.randint(10,20))


if __name__ == "__main__":
    start()
