# coding=utf-8
# 根据商品ID获取商品参数
import re
import time
import requests
from lxml import etree
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

t = time.time()
times = (int(round(t * 1000)))
id = '560217830586'
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
