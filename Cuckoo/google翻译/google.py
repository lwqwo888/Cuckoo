# coding=utf-8
import time
import requests
import urllib
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

import re
import execjs
import urllib, urllib2


class Py4Js():
    def __init__(self):
        self.ctx = execjs.compile("""
        function TL(a) {
        var k = "";
        var b = 406644;
        var b1 = 3293161072;

        var jd = ".";
        var $b = "+-a^+6";
        var Zb = "+-3^+b+-f";

        for (var e = [], f = 0, g = 0; g < a.length; g++) {
            var m = a.charCodeAt(g);
            128 > m ? e[f++] = m : (2048 > m ? e[f++] = m >> 6 | 192 : (55296 == (m & 64512) && g + 1 < a.length && 56320 == (a.charCodeAt(g + 1) & 64512) ? (m = 65536 + ((m & 1023) << 10) + (a.charCodeAt(++g) & 1023),
            e[f++] = m >> 18 | 240,
            e[f++] = m >> 12 & 63 | 128) : e[f++] = m >> 12 | 224,
            e[f++] = m >> 6 & 63 | 128),
            e[f++] = m & 63 | 128)
        }
        a = b;
        for (f = 0; f < e.length; f++) a += e[f],
        a = RL(a, $b);
        a = RL(a, Zb);
        a ^= b1 || 0;
        0 > a && (a = (a & 2147483647) + 2147483648);
        a %= 1E6;
        return a.toString() + jd + (a ^ b)
    };

    function RL(a, b) {
        var t = "a";
        var Yb = "+";
        for (var c = 0; c < b.length - 2; c += 3) {
            var d = b.charAt(c + 2),
            d = d >= t ? d.charCodeAt(0) - 87 : Number(d),
            d = b.charAt(c + 1) == Yb ? a >>> d: a << d;
            a = b.charAt(c) == Yb ? a + d & 4294967295 : a ^ d
        }
        return a
    }
    """)

    def getTk(self, text):
        return self.ctx.call("TL", text)


def open_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:23.0) Gecko/20100101 Firefox/23.0'}
    req = urllib2.Request(url=url, headers=headers)
    response = urllib2.urlopen(req)
    data = response.read().decode('utf-8')
    return data


def translate(content):
    js = Py4Js()
    tk = js.getTk(content)
    print tk

    content = urllib2.quote(content)
    url = "http://translate.google.cn/translate_a/single?client=t" \
          "&sl=auto&tl=zh-CN&hl=EN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca" \
          "&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1" \
          "&srcrom=0&ssel=0&tsel=0&kc=2&tk=%s&q=%s" % (tk, content)

    result = open_url(url)
    end = result.find("\",")
    if end > 4:
        texts = result[4:end]
    return texts


if __name__ == "__main__":
    text = "request() got an unexpected keyword argument 'hearders'"
    texts = text.split('。')
    results = ''
    for i in range(len(texts)):
        try:
            results = results + "" + translate(str(texts[i]))
        except Exception as e:
            print e
    print results





# str = "hello%20world"
# # d = {'q': str}
# # print urllib.urlencode(d)
# url = "https://translate.google.cn/translate_a/single?client=t&sl=auto&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1&ssel=0&tsel=0&kc=3&tk=280581.145730&q=%s" % str
# headers = {
#     "authority":"translate.google.cn",
#     "method":"GET",
#     "path":"/translate_a/single?client=t&sl=auto&tl=zh-CN&hl=zh-CN&dt=at&dt=bd&dt=ex&dt=ld&dt=md&dt=qca&dt=rw&dt=rm&dt=ss&dt=t&ie=UTF-8&oe=UTF-8&clearbtn=1&otf=1&pc=1&ssel=0&tsel=0&kc=3&tk=280581.145730&q=Kindle%20Oasis%20(New%E3%83%A2%E3%83%87%E3%83%AB)%208GB%E3%80%81Wi-Fi%E3%80%81%E3%82%AD%E3%83%A3%E3%83%B3%E3%83%9A%E3%83%BC%E3%83%B3%E6%83%85%E5%A0%B1%E3%81%A4%E3%81%8D%E3%83%A2%E3%83%87%E3%83%AB%E3%80%81%E9%9B%BB%E5%AD%90%E6%9B%B8%E7%B1%8D%E3%83%AA%E3%83%BC%E3%83%80%E3%83%BC",
#     "scheme":"https",
#     "accept":"*/*",
#     "accept-encoding":"gzip, deflate, br",
#     "accept-language":"zh-CN,zh;q=0.9",
#     "cookie":"_ga=GA1.3.1525713841.1519358248; _gid=GA1.3.1098659882.1519976827; NID=124=AgihF_xFzIAOebxdzo6Huu3WwzW1TDKzCQzs-cAaSiu8skUPbdvDAKnPmfxX8APcLJOGpVSO7-5IVAKt_u_yBKRWZUAboVDrKWsWzkkB_ixln1N1fKH6qOlQDsomhWWK; 1P_JAR=2018-3-3-2",
#     "referer":"https://translate.google.cn/",
#     "user-agent":"Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/63.0.3239.132 Safari/537.36",
#     "x-chrome-uma-enabled":"1",
#     "x-client-data":"CIW2yQEIo7bJAQjBtskBCPqcygEIqZ3KAQioo8oB",
# }
# res = requests.get(url, headers=headers).content
# print res
