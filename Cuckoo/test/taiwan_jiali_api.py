# coding=utf8
import re
import requests
import datetime
import sys
from lxml import etree
reload(sys)
sys.setdefaultencoding('utf-8')

url = "http://stg.timesoms.com/api/orders/40002000074"
headers = {
    'Authorization': "Bearer sbv99QoVncfr4twUlpByLwGLNKMMfLlSKtU0DIZYGFl85o5SlWeMvsShlIvl"
}

res = requests.get(url, headers=headers).content
print res
res = re.compile(r'', re.S)