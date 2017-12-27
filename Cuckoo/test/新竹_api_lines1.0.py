# coding=utf-8
import base64
import requests
import datetime
from bs4 import BeautifulSoup
from pyDes import des,CBC,PAD_PKCS5
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# track_number = '6702527985'# 6702527985   6703093320
track_number = track_number

now = datetime.datetime.now()
delta = datetime.timedelta(days=40)
n_days = now + delta
gold_key = n_days.strftime('%Y%m%d')
print 'gold_key',gold_key

IV = "VKXHKJVG" # 自定IV向量

def DesEncrypt(str,IV):
    k = des(gold_key, CBC, IV=IV, padmode=PAD_PKCS5)
    EncryptStr = k.encrypt(str)
    return base64.b64encode(EncryptStr) #转base64编码返回

key_str = DesEncrypt(track_number,IV)

url = """https://www.hct.com.tw/phone/searchGoods_Main.aspx?no=""" + key_str +"""&v=7856A92C813BFEE003AAEB434545ACC3"""
html = requests.post(url).content

soup = BeautifulSoup(html, "lxml")
bs4_res = soup.find_all("tr")[2:]

if len(bs4_res) == 0:
    getstat = '未找到'
    gettime = '未找到'
    # 以下2行测试使用******************************************************************
    with open("新竹信息1.txt", "a") as f:
        f.write(getstat + '\n' + gettime + '\n')
else:
    for i in bs4_res:
        getstat = i.get_text().strip().replace('\r', '').replace('\n', '').replace('\t', '').replace('/', '-')[:16]
        getstat += ':00'
        gettime = i.get_text().strip().replace('\r', '').replace('\n', '').replace('\t', '')[16:]
        # 以下2行测试使用******************************************************************
        with open("新竹信息1.txt","a") as f:
            f.write(getstat + '\n' + gettime + '\n')