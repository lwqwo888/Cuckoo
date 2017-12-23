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
import re
import Queue
# DES加密CBC模式
from pyDes import des,CBC,PAD_PKCS5
# AES加密CBC模式
# from cryptokit import AESCrypto
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def md5(str):
    # digest()作为二进制数据字符串值
    m = hashlib.md5(str).hexdigest()
        # digest()
    print m
    return m
data_queue = Queue.Queue()
track_number = ''

# AESCrypto.cbc_encrypt()
key_str = ''
Des_Key = "BHC#@*UM" # Key
Des_IV = " VKXHKJVG" # 自定IV向量
def DesEncrypt(str):
    k = des(Des_Key, CBC, Des_IV, pad=None, padmode=PAD_PKCS5)
    EncryptStr = k.encrypt(str)
    return base64.b64encode(EncryptStr) #转base64编码返回
key_str = DesEncrypt(str)

url = """https://www.hct.com.tw/phone/searchGoods_Main.aspx?no=""" + key_str +"""&v=7856A92C813BFEE003AAEB434545ACC3"""
params = {
    "awb": str
}

print 666
res = requests.post(url,data=params).content.decode('unicode-escape')
print res
print type(res)
pattern = re.compile(r'"status":"(.*?)"', re.S)
status = pattern.findall(res)
print status
if status == []:
    getstat = '未找到'

else:
    getstat = status
for i in getstat:

    with open("J&T信息1.txt","a") as f:
        f.write(i+'\n')
