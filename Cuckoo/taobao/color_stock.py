# coding=utf-8
# 根据商品ID获取商品参数
import re
import time
import json
import jsonpath
import requests
from lxml import etree
from size_color_skuid_formal import skuid_num
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


def main(size_color):
    t = time.time()
    times = (int(round(t * 1000)))
    dict = skuid_num()
    print type(dict)
    id = '557200845972'
    print size_color
    skuId = dict[size_color]
    url = '''https://mdskip.taobao.com/core/initItemDetail.htm?cartEnable=true&queryMemberRight=true&tmallBuySupport=true&tryBeforeBuy=false&isSecKill=false&cachedTimestamp=%s&isAreaSell=false&isForbidBuyItem=false&service3C=false&isPurchaseMallPage=false&itemId=%s&isUseInventoryCenter=false&addressLevel=2&offlineShop=false&isRegionLevel=false&household=false&showShopProm=false&isApparel=true&sellerPreview=false&callback=setMdskip&timestamp=%s&isg=null&isg2=AtjYd2VcNuKz1Bl5_wUsFM5yqQaqaT1Pr_CqmBLKjZPGrXiXutEM2-7NkdNm'''%(str(times-315000), id, str(times))
    print url
    # url = 'https://detail.tmall.com/item.htm?spm=a230r.1.14.154.29b70e2cmQb92Y&id=563134951881&ns=1&abbucket=15'
    headers = {
        # "authority": "mdskip.taobao.com",
        # "method": "GET",
        # "path": "/core/initItemDetail.htm?cartEnable=true&queryMemberRight=true&tmallBuySupport=true&tryBeforeBuy=false&isSecKill=false&cachedTimestamp=1515846164558&isAreaSell=false&isForbidBuyItem=false&service3C=false&isPurchaseMallPage=false&itemId=557200845972&isUseInventoryCenter=false&addressLevel=2&offlineShop=false&isRegionLevel=false&household=false&showShopProm=false&isApparel=true&sellerPreview=false&callback=setMdskip&timestamp=1515847105682&isg=null&isg2=AtjYd2VcNuKz1Bl5_wUsFM5yqQaqaT1Pr_CqmBLKjZPGrXiXutEM2-7NkdNm",
        # "scheme": "https",
        # "accept": "*/*",
        # "accept-encoding": "gzip, deflate, br",
        # "accept-language": "zh-CN,zh;q=0.9",
        "cookie": "miid=1416914392893341000; hng=CN%7Czh-CN%7CCNY%7C156; thw=cn; tracknick=%5Cu6211%5Cu6210%5Cu4F60%5Cu5669%5Cu68A6; _cc_=Vq8l%2BKCLiw%3D%3D; tg=0; l=ArS04f0dgYQRMtMqetwpb6bSBHkmodh3; x=e%3D1%26p%3D*%26s%3D0%26c%3D0%26f%3D0%26g%3D0%26t%3D0%26__ll%3D-1; cna=5w2/EagEn1sCAbcnVm41KZrQ; t=41a78c0d4f8236cec127e49a3a1d7668; _m_h5_tk=22cd676b46cffe81b7111f72345a4001_1515316266867; _m_h5_tk_enc=594d3f94ed8fe96523affc4889339ae4; enc=LUFqvB76IYLq0NOBSAnqkWEGqx3%2BVDxCaFTpeHTRbd0shSzi6kJ4TKcjRtCKKhB5vGwnjUQpJXJWux06z0QC5w%3D%3D; cookie2=13A91D312332FF9E6F9441B09BD42AEF; v=0; _tb_token_=f385ee7fb8e5b; mt=ci%3D-1_1; isg=BEpKIf4uJNw9j6sTmsbzTbXNmzAsk8-R8Wr4btSFcR3_h-1BvMnkp5C_k_Nbd0Yt",
        "referer": "https://detail.tmall.com/item.htm?spm=a230r.1.14.1.29b70e2cmQb92Y&id=%s&ns=1&abbucket=13"%id,
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/62.0.3202.94 Safari/537.36",
    }
    html = requests.get(url, headers=headers).text
    print html
    res = re.compile(r'setMdskip\n\((.*?)\)', re.S)
    str_list = res.findall(html)
    # 指定商品库存
    for i in str_list:
        json_str1 = json.loads(i)
        print json_str1
        json_res = jsonpath.jsonpath(json_str1, expr='$..inventoryDO.skuQuantity.%s.quantity'%skuId)
        # 库存
        print json_res

    # for i in str_list:
    #     json_str1 = json.loads(i)
    #     print json_str1
    #     json_res = jsonpath.jsonpath(json_str1, expr='$..itemPriceResultDO.priceInfo.%s.suggestivePromotionList..price'%skuId)
    #     # 指定商品价格
    #     print json_res
    # 指定店铺详细
    'https://hdc1.alicdn.com/asyn.htm?pageId=1303352866&userId=645039969'
if __name__ == '__main__':
    size = raw_input('请输入您要查看的尺码:')
    color = raw_input('请输入您要查看的颜色:')
    size_color = size + color
    # print size_color
    main(size_color)