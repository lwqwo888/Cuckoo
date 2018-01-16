# coding=utf-8
# 根据商品ID获取商品参数
import re
import time
import urllib
import requests
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

t = time.time()
times = (int(round(t * 1000)))
id = '560217830586'
skuId = '3664600867959'
# 添加到购物车api
# url = 'https://cart.taobao.com/add_cart_item.htm?item_id=557200845972'


# url = urllib.unquote('7e056b706dfe4&')
# print urllib.quote('{"deliveryCityCode":440300,"campaignId":0,"from_etao":"","umpkey":"","items":[{"itemId":"560217830586","skuId":"3664600867959","iChannel":"","quantity":1,"serviceInfo":"","extraAttribute":{}}]}')
add_str = urllib.urlencode({'add':'{"deliveryCityCode":440300,"campaignId":0,"from_etao":"","umpkey":"","items":[{"itemId":"560217830586","skuId":"3664600867959","iChannel":"","quantity":1,"serviceInfo":"","extraAttribute":{}}]}'})
print add_str
# sellerId:卖家ID
# categoryId:类别ID
params = {
    "_tb_token_": "30783b151de8b",
    "tsid": "41a78c0d4f8236cec127e49a3a1d7668",
    "itemId": id,
    "sellerId": "3432882180",
    "categoryId": "50011744",
    "root_refer": "",
    "_ksTS": "1515951261320_1665",
    "callback": "jsonp1666",

}
# print params
params_str = urllib.urlencode(params) + '&' + add_str
print params_str
url = '''https://fbuy.tmall.com/cart/addCartItems.do?''' + params_str
# url = '''https://fbuy.tmall.com/cart/addCartItems.do?_tb_token_=7e056b706dfe4&add=%7B%22deliveryCityCode%22%3A440300%2C%22campaignId%22%3A0%2C%22from_etao%22%3A%22%22%2C%22umpkey%22%3A%22%22%2C%22items%22%3A%5B%7B%22itemId%22%3A%22560217830586%22%2C%22skuId%22%3A%223664600867959%22%2C%22iChannel%22%3A%22%22%2C%22quantity%22%3A1%2C%22serviceInfo%22%3A%22%22%2C%22extraAttribute%22%3A%7B%7D%7D%5D%7D&tsid=4d814acaeff7745d2b1df5c531cb7227&itemId=560217830586&sellerId=3432882180&categoryId=50011744&root_refer=&item_url_refer=&_ksTS=1515999130398_1272&callback=jsonp1273'''
print url
headers = {
    # "authority": "mdskip.taobao.com",
    "method": "GET",
    # "path": "/core/initItemDetail.htm?cartEnable=true&queryMemberRight=true&tmallBuySupport=true&tryBeforeBuy=false&isSecKill=false&cachedTimestamp=1515846164558&isAreaSell=false&isForbidBuyItem=false&service3C=false&isPurchaseMallPage=false&itemId=557200845972&isUseInventoryCenter=false&addressLevel=2&offlineShop=false&isRegionLevel=false&household=false&showShopProm=false&isApparel=true&sellerPreview=false&callback=setMdskip&timestamp=1515847105682&isg=null&isg2=AtjYd2VcNuKz1Bl5_wUsFM5yqQaqaT1Pr_CqmBLKjZPGrXiXutEM2-7NkdNm",
    # "scheme": "https",
    # "accept": "*/*",
    # "accept-encoding": "gzip, deflate, br",
    # "accept-language": "zh-CN,zh;q=0.9",
    'Connection': 'keep-alive',
    "cookie": "cna=5w2/EagEn1sCAbcnVm41KZrQ; x=__ll%3D-1%26_ato%3D0; hng=CN%7Czh-CN%7CCNY%7C156; uc1=cookie14=UoTdfkKtks6l8w%3D%3D&lng=zh_CN&cookie16=UtASsssmPlP%2Ff1IHDsDaPRu%2BPw%3D%3D&existShop=true&cookie21=URm48syIYn73&tag=8&cookie15=W5iHLLyFOGW7aA%3D%3D&pas=0; uc3=sg2=WqIrBf2WEDhnXgIg9lOgUXQnkoTeDo019W%2BL27EjCfQ%3D&nk2=rUs9FkCy6Zs6Ew%3D%3D&id2=VWeZAHoeqUWF&vt3=F8dBzLgrpMV1BvHSmJg%3D&lg2=VFC%2FuZ9ayeYq2g%3D%3D; tracknick=%5Cu6211%5Cu6210%5Cu4F60%5Cu5669%5Cu68A6; _l_g_=Ug%3D%3D; unb=688489285; lgc=%5Cu6211%5Cu6210%5Cu4F60%5Cu5669%5Cu68A6; cookie1=W8sivp9OeD7CvuVdh6i1LLRCZWfw5Of6GKWiySUCS9Q%3D; login=true; cookie17=VWeZAHoeqUWF; cookie2=38518becf2aaeff0e67d62c772aaf1da; _nk_=%5Cu6211%5Cu6210%5Cu4F60%5Cu5669%5Cu68A6; uss=V33DdgQCI1MgOSGAMSNlX2eByPhz9fYofocO29hW%2FrleKN2N%2FIEXsK64cQ%3D%3D; sg=%E6%A2%A657; t=41a78c0d4f8236cec127e49a3a1d7668; _tb_token_=30783b151de8b; otherx=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0; whl=-1%260%260%260; isg=Ai8v8rAvqf2eaq7cDFBD2S0vvkP5fILyLP09vUG8yx6lkE-SSaQTRi1CZrZV",
    "referer": "https://detail.tmall.com/item.htm?spm=a230r.1.14.1.29b70e2cmQb92Y&id=%s&ns=1&abbucket=13"%id,
    "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
}
requests_session = requests.Session()
html = requests_session.get(url, headers=headers).text
print html
