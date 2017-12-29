# coding=utf-8
import requests
import json
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


# url = 'http://www.sz56t.com:8082/selectTrack.htm?documentCode=1171226121221604271'
url = 'http://113.105.65.70:8032/query.aspx'
params = {
    '__VIEWSTATE': '/wEPDwUKMTg2MTYyMDc5M2RkjCDPEC/ksTqq44KYqvtadq7XLC4=',
    '__EVENTVALIDATION': '/wEWAwKi0rjlDwKvgcuQCQKM54rGBuq0mYrzxG6dbfcTTEtuhzTz4r+/',
    'TrackNum': '1171226121221604271',
    'Button1': '追踪',
}
json_data = requests.post(url, data=params).text
xpath = "//form[@id='form1']/center/div/table[last()]/tbody/tr[last()]/td[last()]/div[last()]"
xpath = "//form[@id='form1']/center/div/table[last()]/tbody/tr[last()]/td[last()]/div"
print json_data