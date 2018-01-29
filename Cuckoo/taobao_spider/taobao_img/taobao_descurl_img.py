# coding=utf-8
import os
import re
import time
import gzip
import random
import urllib
import urllib2
import requests
import StringIO
from lxml import etree
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


class Taobao_Img(object):
    def __init__(self):
        self.proxy = {"http": ""}
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
            'user-agent': "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
        }
    def property_count(self, id):
        url = 'https://detail.tmall.com/item.htm?&id=%s' % id

        html = requests.get(url, headers=self.headers, proxies=self.proxy).text
        res = etree.HTML(html)
        ron = res.xpath('''//*[@id="J_UlThumb"]//a/img/@src|//*[@id="J_UlThumb"]//a/img/@data-src''')
        cover_img_list = []
        for err_url in ron:
            index_num = self.find_last(err_url, "_")
            cover_img_list.append(err_url[:index_num])
        for true_url in cover_img_list:
            print '************', true_url
            with open("img_url.txt", 'a') as f:
                f.write("http:" + true_url + '\n')
                print "http:" + true_url
        cover_img_list_length = len(cover_img_list)
        self.download_img(cover_img_list_length, cover_img_list, id, "展示图")

        desc_url_obj = re.compile(r'''descUrl.*?('//(.*?)'|"//(.*?)")''', re.S)
        desc_url_list = desc_url_obj.findall(html)
        desc_url = 'http:' + desc_url_list[0][0].replace('"', '').replace("'", '')
        print desc_url
        print '++++++++++++++++', self.proxy
        res = requests.get(desc_url, headers=self.headers, proxies=self.proxy).content
        print res
        img_url_obj = re.compile(r'(//img.*?\.(jpg|png|SS2))', re.S)
        img_url_list = img_url_obj.findall(res)
        length = len(img_url_list)
        print '去重前url数量', length
        temporary_img_url_list = []
        for i in img_url_list:
            temporary_img_url_list.append(i[0])
        news_img_url_list = list(set(temporary_img_url_list))
        news_img_url_list.sort(key=temporary_img_url_list.index)
        new_length = len(news_img_url_list)
        print '去重后url数量', new_length
        for j in news_img_url_list:
            with open("img_url.txt", 'a') as f:
                f.write("http:" + j + '\n')
                print "http:" + j
        self.download_img(new_length, news_img_url_list, id, "细节图")
        # with open('img_url.txt', 'rb') as f:
        #     lines = f.readlines()
            # print '///////////////////////',len(lines)
    def download_img(self, list_length, list, id, name):
        k = 0
        # new_length = 1
        while k < list_length:
            img_url = list[k]
            img_url = "http:" + img_url
            # img_url = lines[k].replace('\n', '')
            data = requests.get(img_url, headers=self.headers, proxies=self.proxy).content
            path = "img/%s" % id
            if (not (os.path.exists(path))):
                os.mkdir(path)

            format = img_url[-4:]
            # print format
            img_name = id + name + str(k+1)
            with open("img/" + id + "/" + img_name + format, 'wb') as f:
                # print '******************',res
                f.write(data)

            print '第%s个url: %s' % (k+1, img_url)
            time.sleep(1)

            k += 1

    def find_last(self, string, str):
        last_position = -1
        while True:
            # 在string字符串的last_position+1下标后面找不到str会返回-1
            position = string.find(str, last_position + 1)
            # print position
            if position == -1:
                return last_position
            last_position = position

    def url_process(self, url):
        res = re.compile(r'(\?|&)id=(\d+).*?', re.S)
        id = res.search(url).group(2)
        # print id
        return ''.join(id)

    def set_proxy(self):
        """
        设置代理
        """
        # 获取xicidaili的高匿代理
        proxy_info_list = []  # 抓取到的ip列表
        for page in range(1, 2):  # 暂时只抓第一页
            request = urllib2.Request('http://www.xicidaili.com/nn/%d' % page)
            request.add_header('Accept-Encoding', 'gzip, deflate')
            request.add_header('Accept', 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8')
            request.add_header('Accept-Language', 'zh-CN,zh;q=0.8,en;q=0.6')
            request.add_header('User-Agent', 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36')
            response = urllib2.urlopen(request, timeout=5)

            headers = response.info()
            content_type = headers.get('Content-Type')
            if content_type:
                charset = re.findall(r"charset=([\w-]+);?", content_type)[0]
            else:
                charset = 'utf-8'
            if headers.get('Content-Encoding') == 'gzip':
                gz = gzip.GzipFile(fileobj=StringIO.StringIO(response.read()))
                content = gz.read().decode(charset)
                gz.close()
            else:
                content = response.read().decode(charset)
            response.close()
            print u'获取第 %d 页' % page
            ip_page = re.findall(r'<td>(\d.*?)</td>', content)
            proxy_info_list.extend(ip_page)
            time.sleep(random.choice(range(1, 3)))

        # 打印抓取的内容
        print u'代理IP地址\t端口\t存活时间\t验证时间'
        for i in range(0, len(proxy_info_list), 4):
            print u'%s\t%s\t%s\t%s' % (proxy_info_list[i], proxy_info_list[i + 1], proxy_info_list[i + 2], proxy_info_list[i + 3])

        all_proxy_list = []  # 待验证的代理列表
        # proxy_list = []  # 可用的代理列表
        for i in range(0, len(proxy_info_list), 4):
            proxy_host = proxy_info_list[i] + ':' + proxy_info_list[i + 1]
            all_proxy_list.append(proxy_host)

        # 开始验证

        # 单线程方式
        for i in range(len(all_proxy_list)):
            proxy_host = self.test(all_proxy_list[i])
            if proxy_host:
                break
        else:
            # TODO 进入下一页
            print u'没有可用的代理'
            return None

        # 多线程方式
        # threads = []
        # # for i in range(len(all_proxy_list)):
        # for i in range(5):
        #     thread = threading.Thread(target=test, args=[all_proxy_list[i]])
        #     threads.append(thread)
        #     time.sleep(random.uniform(0, 1))
        #     thread.start()
        #
        # # 等待所有线程结束
        # for t in threading.enumerate():
        #     if t is threading.currentThread():
        #         continue
        #     t.join()
        #
        # if not proxy_list:
        #     print u'没有可用的代理'
        #     # TODO 进入下一页
        #     sys.exit(0)
        print u'使用代理： %s' % proxy_host
        return proxy_host

    def test(self, proxy_host):
        """
        验证代理IP有效性的方法
        :param proxy_host:
        :return:
        """
        try:
            request = urllib2.Request('http://cn.bing.com/')  # 用于验证代理是否有效
            request.add_header(
                'User-Agent',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/59.0.3071.86 Safari/537.36')
            urllib2.install_opener(urllib2.build_opener(urllib2.ProxyHandler({'http': proxy_host})))
            http_code = urllib2.urlopen(request, timeout=5).getcode()
            if http_code == 200:
                return proxy_host
        except Exception as e:
            print e
            return None


if __name__ == '__main__':
    ti = Taobao_Img()
    with open('taobaourl.txt', 'rb') as f:
        lines = f.readlines()
    for line in lines:
        id = ti.url_process(line)
        ti.property_count(id)
    # url = "https://detail.tmall.com/item.htm?id=557200845972"
    # url = "https://item.taobao.com/item.htm?spm=a219r.lmn002.14.174.6f516358W81jq9&id=562441235623&ns=1&abbucket=16"
    # url = 'https://item.taobao.com/item.htm?spm=a219r.lm874.14.31.5dc9e78e7Fcl7j&id=557200845972&ns=1&abbucket=16#detail'

