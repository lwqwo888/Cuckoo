# coding=utf-8
# 免责声明: 此代码是为快捷查询由刘文强编写的
import re
import json
import time
import random
import datetime
import requests
import linecache
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class ttt(object):
    def __init__(self):
        self.srequest = requests.Session() # 自动处理cookie

    def change_ua(self):
        tunnel = random.randint(1, 1036)
        print tunnel
        user_agent = linecache.getline('1000ua-pc.log', tunnel)
        user_agent = user_agent.strip().replace('\n', '').replace('\r', '')
        print user_agent
        self.headers = {
            'authority': 'detail.tmall.com',
            'method': 'GET',
            'scheme': "https",
            'accept': "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
            'accept-encoding': "gzip, deflate, br",
            'accept-language': "zh-CN,zh;q=0.9",
            'cache-control': "max-age=0",
            'cookie': "cna=XTyQEoI1uE4CAXBfh3IMFSpJ; cq=ccp%3D1; t=4d814acaeff7745d2b1df5c531cb7227; _tb_token_=3eb56ee77e988; cookie2=17B3F5F8A0D9CB4142FFBB0733EC948B; pnm_cku822=098%23E1hvApvUvbpvjQCkvvvvvjiPPL5wljtVP25hgjivPmPy1jYRRsdvzjiRR2z91jQPvpvhvvvvvvhCvvOvUvvvphvEvpCWh8%2Flvvw0zj7OD40OwoAQD7zheutYvtxr1RoKHkx%2F1RBlYb8rwZBleExreE9aWXxr1noK5FtffwLyaB4AVAdyaNoxdX3z8ikxfwoOddyCvm9vvvvvphvvvvvv96Cvpv9hvvm2phCvhRvvvUnvphvppvvv96CvpCCvkphvC99vvOC0B4yCvv9vvUvQud1yMsyCvvpvvvvviQhvCvvv9UU%3D; isg=ArOzZnnX7QJos6HBeuocdKfGQrcdQCLrPU38GWVQTFIJZNMG7bjX-hH2aqJx",
            'upgrade-insecure-requests': "1",
            # 'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
            'user-agent': user_agent,
        }


    def req(self):
        self.change_ua()
        url = 'http://taobao.com'
        self.srequest = requests.Session()
        resp = self.srequest.get(url)
        print resp
        r = self.srequest.get("http://httpbin.org/cookies")
        print r.text


if __name__ == '__main__':
    t = ttt()
    t.req()

