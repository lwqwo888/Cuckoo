# coding=utf-8
# 此接口url地址为http/post类型地址
# xml信息
# 服务名:RouteService 语言为中文简体
# Head接入编码:BSPdevelop
# Body:请求报文
# passwd:密钥
# xml报文+密钥后进行md5和base64后即为校验码
# 构建post数据,内容为xml报文和校验码
# 发送post请求

import hashlib
import base64
import requests

def md5(str):
    m = hashlib.md5(str).digest()
    print m
    return m

url = "http://bsp-ois.sit.sf-express.com:9080/bsp-ois/sfexpressService"

string_message = """
    <Request service="RouteService" lang="zh-CN">
        <Head>BSPdevelop</Head>
            <Body>
                <RouteRequest
                tracking_type="1"
                method_type="1"
                tracking_number="172249304966"/>
            </Body>
    </Request>
"""

passwd  = "j8DzkIFgmlomPt0aLuwU"

combine = string_message+passwd

result  = base64.b64encode(md5(combine))
print result
params = {
    "xml": string_message,
    "verifyCode": result
}
res = requests.post(url,data=params)

print res.text