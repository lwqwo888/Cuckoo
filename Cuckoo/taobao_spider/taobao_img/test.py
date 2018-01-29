# coding=utf-8
import re
import requests
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def property_count(id):
    url = 'https://detail.tmall.com/item.htm?&amp;id=%s' % id
    headers = {
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
    html = requests.get(url, headers=headers).text
    # print html

    # img_url_obj = re.compile(r'//img.*?\.jpg', re.S)
    # img_url_obj = re.compile(r'//img\S*?\.(png|jpg)$/', re.S)

    img_url_obj = re.compile(r'(//img.*?\.(png|jpg|SS2))', re.S)
    img_url_list = img_url_obj.findall(html)
    print len(img_url_list)
    for i in img_url_list:
        # if ',' in i:
        #     img_url_list.remove(i)
        # else:
        #     print i
        print i[0]
    print len(img_url_list)


def url_process(url):
    res = re.compile(r'(\?|&)id=(\d+).*?', re.S)
    id = res.search(url).group(2)
    # print id
    return ''.join(id)


if __name__ == '__main__':

    url = 'https://item.taobao.com/item.htm?spm=a219r.lm874.14.31.5dc9e78e7Fcl7j&amp;id=557200845972&ns=1&abbucket=16#detail'
    # id = url_process(url)
    id = '557200845972'
    property_count(id)