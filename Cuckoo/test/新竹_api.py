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

import requests
import hashlib
import datetime
import time
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

def md5(str):
    # digest()作为二进制数据字符串值
    m = hashlib.md5(str).hexdigest()
        # digest()
    print m
    return m



# a,b,c = time.strftime('%H%M%S',time.localtime(time.time()))
# time1_str = datetime.datetime.strftime('%Y-%m-%d %H:%M:%S')
day = datetime.datetime.now()
time_str = time.strftime("%S%H%M", time.localtime())
print time_str


# track_number = ''
# url = "https://www.hct.com.tw/phone/HCTInvQueryHis.aspx"
# str = '' + 'H@t' + track_number + '!'
# params = {
#     "awb": str
# }
#
# print 666
# res = requests.post(url,data=params).content.decode('unicode-escape')
# print res
# print type(res)
# pattern = re.compile(r'"status":"(.*?)"', re.S)
# status = pattern.findall(res)
# print status
# if status == []:
#     getstat = '未找到'
#
# else:
#     getstat = status
# for i in getstat:
#
#     with open("J&T信息1.txt","a") as f:
#         f.write(i+'\n')
