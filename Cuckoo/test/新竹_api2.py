# coding=utf-8
# 此接口url地址为http/post类型地址
# xml信息请求报文
# 服务名:RouteService 语言为中文简体
# Head接入编码:BSPdevelop
# Body:请求内容
# passwd:密钥
# xml报文+密钥后进行md5和base64后即为校验码
# 构建post数据,内容为xml报文和校验码
# 发送post请求

import hashlib
import base64
import requests
import json
import datetime
import re
import Queue
# DES加密CBC模式
from pyDes import des,CBC,PAD_PKCS5
# AES加密CBC模式
# from cryptokit import AESCrypto
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

track_number = ''

# AESCrypto.cbc_encrypt()
xml_str = '''<?xml version="1.0" encoding="utf-8"?><qrylist><order orderid="6703093320"></order></qrylist>'''
# Des_Key = "BHC#@*UM" # Key
now = datetime.datetime.now()
delta = datetime.timedelta(days=40)
n_days = now + delta
gold_key = n_days.strftime('%Y%m%d')
print 'money',gold_key

IV = "VKXHKJVG" # 自定IV向量

str = xml_str + str(gold_key) + IV
str = str.encode('utf-8')
pad = 8-(len(str) % 8)
repeat = pad * chr(pad)
print type(repeat)
print 'repeat',repeat.encode('utf-8')
str = xml_str + repeat
print 'str',str
print 'pad',pad

def DesEncrypt(str):
    k = des("DESCRYPT", CBC, IV)
    EncryptStr = k.encrypt(str)
    return base64.b64encode(EncryptStr) #转base64编码返回

key_str = DesEncrypt(str)
print key_str

url = """https://www.hct.com.tw/phone/searchGoods_Main.aspx?no=""" + key_str +"""&v=7856A92C813BFEE003AAEB434545ACC3"""
print 666
res = requests.post(url).content.encode('utf-8')
print res
print type(res)
# pattern = re.compile(r'"status":"(.*?)"', re.S)
# status = pattern.findall(res)
# print status
# if status == []:
#     getstat = '未找到'
#
# else:
#     getstat = status
for i in res:

    with open("新竹信息1.txt","a") as f:
        f.write(i+'\n')
