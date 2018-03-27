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
        proxyHost = "n10.t.16yun.cn"
        proxyPort = "6442"

        # 代理隧道验证信息
        proxyUser = "16SBYYUY"
        proxyPass = "658666"

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
            "authority": "detailskip.taobao.com",
            "method": "GET",
            "path": "/service/getData/1/p1/item/detail/sib.htm?itemId=553028074550&sellerId=2847682332&modules=dynStock,qrcode,viewer,price,duty,xmpPromotion,delivery,activity,fqg,zjys,couponActivity,soldQuantity,originalPrice,tradeContract&callback=onSibRequestSuccess",
            "scheme": "https",
            "accept": "*/*",
            "accept-encoding": "gzip, deflate, br",
            "accept-language": "zh-CN,zh;q=0.9",
            "cookie": "thw=cn; cna=zlgpE1AGhCYCAQ4VLvIgUO4/; t=650e40dd9362554c7eeffbc8ae7d9919; enc=KXvpo3HkybgzyFZzoxEm5cZ%2F0XVreF%2BBYpafvXbyyA%2Bj2YBdJBG8WOgzpg2TUSS1VosnSzr1zprKt2gA1%2FRwgA%3D%3D; hng=CN%7Czh-CN%7CCNY%7C156; mt=ci%3D-1_1; _m_h5_tk=c80b4de930310614d5df33ff8dc019dd_1521613558097; _m_h5_tk_enc=fb88fb1c564e2c0ed4804d2a4be63abd; miid=723482872197753828; v=0; cookie2=1ca58d9d9dcb8c686d2bae2d4158ccfb; _tb_token_=e538e6e33de75; isg=BN3d7ztvW8UqiT_4uKJjezr17LkXUnoXkfi35J-iMjRjVv2IZ0ohHKunhErQlikE",
            "referer": "https://item.taobao.com/item.htm?spm=a230r.1.14.164.56357042O1I5sx&id=553028074550&ns=1&abbucket=14",
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/65.0.3325.146 Safari/537.36",
        }

    def skuid_num(self, id, pvs_list):
        html = ""
        self.resp_code = ""
        # originalPrice为价格
        url = 'https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId=%s&modules=dynStock,originalPrice,soldQuantity&callback=onSibRequestSuccess'%id
        # url = "https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId=%s&modules=dynStock,qrcode,viewer,price,duty,xmpPromotion,delivery,activity,zjys,couponActivity,soldQuantity,originalPrice,tradeContract&callback=onSibRequestSuccess"%id
        url = "https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId=%s&sellerId=2847682332&modules=dynStock,soldQuantity,originalPrice&callback=onSibRequestSuccess" % id
        # url = "https://detailskip.taobao.com/service/getData/1/p1/item/detail/sib.htm?itemId=525081717701&sellerId=2847682332&modules=dynStock,soldQuantity,originalPrice&callback=onSibRequestSuccess"
        print url
        self.change_ua()

        time.sleep(0.3)
        try:
            response = self.srequests.get(url, headers=self.headers, proxies=self.proxy)
            self.resp_code = response.status_code
            if self.resp_code == 200:
                html = response.text
                print html

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
                        response = self.srequest.get(url, headers=self.headers, proxies=self.proxy)
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
        print '**********', tb_sell_obj
        sell_list.append(tb_sell_obj[0])
        sell_list.append(tm_sell_obj[0])

        stock_list = []
        price_list = []
        for pvs in pvs_list:

            res = re.compile(r'%s.*?"sellableQuantity":(.*?),' % pvs, re.S)
            p_res = re.compile(r'%s.*?"price":"(.*?)"' % pvs, re.S)

            single_stock = res.findall(str_res)
            price_obj = p_res.findall(html)

            # print ''.join(sell_obj)
            if single_stock:
                stock_list.append(''.join(single_stock))

            else:
                stock_list.append(0)
            price_list.append(''.join(price_obj))


        return stock_list, price_list, sell_list

if __name__ == '__main__':
    sc = Skuid_Color()
    sc.skuid_num(1, [2])