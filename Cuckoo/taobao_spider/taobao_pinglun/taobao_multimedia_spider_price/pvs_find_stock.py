# coding=utf-8
# 通过pvs直接找库存
# 优点：速度稍快
# 缺点：无货商品库存没有体现，需手动置0或置为＂无货＂
import re
import time
import json
import random
import jsonpath
import requests
import linecache
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Skuid_Color(object):
    def __init__(self):
        self.srequests = requests.Session()
        # 代理服务器
        proxyHost = ""
        proxyPort = ""

        # 代理隧道验证信息
        proxyUser = ""
        proxyPass = ""

        proxyMeta = "http://%(user)s:%(pass)s@%(host)s:%(port)s" % {
            "host": proxyHost,
            "port": proxyPort,
            "user": proxyUser,
            "pass": proxyPass,
        }
        proxyMeta = ''
        self.proxy = {
            "http": proxyMeta,
            "https": proxyMeta,
        }
        self.num = 1
        self.count = 0
        self.sec = 0
        self.old_sec = 0

    def change_ua(self):
        tunnel = random.randint(1, 1036)
        user_agent = linecache.getline('1000ua-pc.log', tunnel)
        user_agent = user_agent.strip().replace('\n', '').replace('\r', '')

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
            "referer": "https://item.taobao.com/item.htm?spm=a219r.lmn002.14.174.6f516358W81jq9&id=561495525977&ns=1&abbucket=16",
            'user-agent': user_agent,
        }

    def skuid_num(self, id, pvs_list):
        html = ""
        self.resp_code = ""
        # originalPrice为价格 sellerId可加可不加
        url = "https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId=%s&sellerId=2847682332&modules=dynStock,soldQuantity,originalPrice&callback=onSibRequestSuccess" % id
        self.change_ua()

        time.sleep(0.3)
        try:
            response = self.srequests.get(url, headers=self.headers)
            self.resp_code = response.status_code
            if self.resp_code == 200:
                html = response.text

        except Exception as e:
            print '数据请求失败...正在重试......', e
            with open('request.log', 'a') as f:
                f.write('%s [代理]请求失败(%s) %s - %s\n' % (url, self.resp_code, id, time.ctime()))
            # # global NETWORK_STATUS
            NETWORK_STATUS = False  # 请求超时改变状态

            if NETWORK_STATUS == False:
                #     '请求超时'
                for i in range(1, 11):
                    time.sleep(0.3)
                    print '请求失败，第%s次重复请求' % i
                    if i == 5:
                        print "[INFO]: 代理睡眠中......"
                        time.sleep(10)
                    if i == 7:
                        print "[INFO]: 代理睡眠中......"
                        time.sleep(30)
                    if i == 9:
                        print "[INFO]: 代理睡眠中......"
                        time.sleep(60)
                    self.change_ua()

                    try:
                        response = self.srequest.get(url, headers=self.headers)
                        self.resp_code = response.status_code
                        if self.resp_code == 200:
                            html = response.text
                            with open('request.log', 'a') as f:
                                f.write('%s 重新请求成功%s - %s\n' % (url, id, time.ctime()))
                            print ('[INFO]:重发请求成功!!!!!!!!!!')
                            break
                    except:
                        with open('request.log', 'a') as f:
                            f.write('%s 重新请求失败, %s  继续重试...%s - %s\n' % (url, self.resp_code, id, time.ctime()))
                        print ('[INFO]:重发请求失败!!!!!!!!!!')
                        print '第%s次重复请求失败%s! 继续重试...' % (i, self.resp_code)
                        continue

                if self.resp_code == 200:
                    with open('request.log', 'a') as f:
                        f.write('%s 最终请求成功!!!!!%s - %s\n' % (url, id, time.ctime()))
                    print ('[INFO]:最终请求成功!!!!!!!!!!')
                else:
                    with open('request.log', 'a') as f:
                        f.write('%s 最终请求失败%s ! ! ! ! !%s - %s\n' % (url, self.resp_code, id, time.ctime()))
                    print ('[INFO]:最终请求失败%s!!!!!!!!!!') % self.resp_code

        sell_list = []
        html_obj = re.compile(r'onSibRequestSuccess\((.*?)\);', re.S)
        json_data = html_obj.findall(html)
        json_obj = json.loads(json_data[0])
        json_res = jsonpath.jsonpath(json_obj, expr="$..dynStock")
        str_res = json.dumps(json_res[0])

        tb_s_res = re.compile(r'"confirmGoodsCount":(\d+),', re.S)
        tm_s_res = re.compile(r'"soldTotalCount":(\d+)}', re.S)
        tb_sell_obj = tb_s_res.findall(html)
        tm_sell_obj = tm_s_res.findall(html)

        sell_list.append(tb_sell_obj[0])
        sell_list.append(tm_sell_obj[0])

        stock_list = []
        price_list = []
        for pvs in pvs_list:

            res = re.compile(r'%s.*?"sellableQuantity":(.*?),' % pvs, re.S)
            p_res = re.compile(r'%s.*?"price":"(.*?)"' % pvs, re.S)

            single_stock = res.findall(str_res)
            price_obj = p_res.findall(html)

            if single_stock:
                stock_list.append(''.join(single_stock))
            else:
                stock_list.append(0)
            price_list.append(''.join(price_obj))

        return stock_list, price_list, sell_list

if __name__ == '__main__':
    sc = Skuid_Color()
    sc.skuid_num(1, [2])