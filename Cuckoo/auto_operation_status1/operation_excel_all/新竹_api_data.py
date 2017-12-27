# coding=utf-8
from operation_excel import OperationExcel
from config import FILE_NAME, col_number, FILE_Path, SHEET_ID
from send_excel import send
import base64
import requests
import datetime
from bs4 import BeautifulSoup
from pyDes import des,CBC,PAD_PKCS5
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class Date(OperationExcel):

    def __init__(self,file):
        self.file = file
        super(Date, self).__init__()
        # self.file_name = file_name
        # super(Date, self).__init__()

    # def A(self):
    #     print 'wwwwwwww'
    def acquire_date(self,track_number):
        '''
        获取数据
        :return:
        '''
        # track_number = '6702527985'# 6702527985   6703093320
        # 金钥
        now = datetime.datetime.now()
        delta = datetime.timedelta(days=40)
        n_days = now + delta
        gold_key = n_days.strftime('%Y%m%d')
        # print 'gold_key',gold_key

        # 自定IV向量
        IV = "VKXHKJVG"

        def DesEncrypt(str,IV):
            k = des(gold_key, CBC, IV=IV, padmode=PAD_PKCS5)
            EncryptStr = k.encrypt(str)
            return base64.b64encode(EncryptStr) #转base64编码返回

        key_str = DesEncrypt(track_number,IV)
        # print key_str

        url = """https://www.hct.com.tw/phone/searchGoods_Main.aspx?no=""" + key_str +"""&v=7856A92C813BFEE003AAEB434545ACC3"""
        # print url
        res = requests.post(url).content  # .encode('utf-8')

        soup = BeautifulSoup(res, "lxml")

        res_html = soup.find_all("tr")

        if len(res_html) == 0:
            getstat = '未找到'
            gettime = '未找到'
        else:
            sta_ti = res_html[-1].get_text().strip().replace('\r','').replace('\n','').replace('\t','').replace(' ','')
            getstat = sta_ti[0:10]
            gettime = sta_ti[15:]

        with open("新竹信息1.txt","a") as f:
            f.write(getstat +'\n'+ gettime + '\n')

# 这里传入一个Excel
# 返回值为指定列号的列数据,ssss是没用数据,无影响
lists = Date('ssss').get_col_all_data(col_number)

file = Date('sss').A()
length = len(lists)
list_data = []

i = 1
for list in lists:
    print "第%s个单号,共%s个: %s," % (i, length, list)
    # 拿出列中的订单号发送请求返回运单号和状态,并追加到列表
    list_data.append(Date('sss').acquire_date(list))
    i = i + 1
    if i > len(lists):
        break
        # print i
# 把数据和文件名发送走
send(list_data, FILE_NAME)