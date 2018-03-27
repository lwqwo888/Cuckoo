# coding=utf-8
import requests
import json
import re
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SyncStatusThread(object):
    def __init__(self):
        self.status = '未找到'
    def main(self):
        url = "http://jk.jet.co.id:22261/jant_szcuckoo_web/szcuckoo/trackingAction!tracking.action"

        params = {
            "awb": 'JK0000011444'
        }
        params = json.dumps(params,ensure_ascii=False)
        json_object = json.loads(params)
        res = requests.post(url, data=params).content.decode('unicode-escape')
        all_status = re.compile(r'"status":"(.*?)"', re.S)
        all_time = re.compile(r'"date_time":"(.*?)"', re.S)
        status_list = all_status.findall(res)
        datetime_list = all_time.findall(res)

        if datetime_list:
            J_and_T_list = [i for i in zip(status_list, datetime_list)]
            for self.status, j in J_and_T_list:
                str_time = j.split(' ')
                time_list = str_time[0].split('-')[::-1]
                month_num = self.month_func(time_list[1])
                logistics_time = time_list[0] + '-' + month_num + '-' + time_list[2] + ' ' + str_time[1]
                tran_status_label = self.control(self.str_process(self.status))
                # 以下1行测试使用******************************************************************
                print logistics_time + '\n' + self.status + '\n' + tran_status_label + '\n'
                # print logistics_time
                # print status
        else:
            status = '未找到'
            logistics_time = ''
            tran_status_label = status
            # 以下1行测试使用******************************************************************
            print logistics_time + '\n' + status + '\n' + tran_status_label + '\n'
            # print logistics_time
            # print status

    def month_func(self, mth):
        swtich = {
            'JAN': '01',
            'FEB': '02',
            'MAR': '03',
            'APR': '04',
            'MAY': '05',
            'JUN': '06',
            'JUL': '07',
            'AUG': '08',
            'SEP': '09',
            'OCT': '10',
            'NOV': '11',
            'DEC': '12',
        }
        return swtich.get(mth, '00')


    def control(self, yn_str):
        # 订单处理中
        if self.str_process('Manifes') in yn_str:
            zh_str = 'Manifes'
        # 发件 'Paket akan dikirimkan ke & 网点名称':
        elif self.str_process('Paket akan dikirimkan ke') in yn_str:
            zh_str = 'Paket akan dikirimkan ke + 网点名称'
        # 收件 'Paket telah diterima oleh & 网点名称'
        elif self.str_process('Paket telah diterima oleh') in yn_str:
            zh_str = 'Paket telah diterima oleh + 网点名称'
        # 到件 'Paket telah sampai di & 网点名称'
        elif self.str_process('Paket telah sampai di') in yn_str:
            zh_str = 'Paket telah sampai di + 网点名称'
        # 派件
        elif self.str_process('Paket akan dikirim ke alamat penerima') in yn_str:
            zh_str = 'Paket akan dikirim ke alamat penerima'
        # 签收
        elif self.str_process('Paket telah diterima') in yn_str:
            zh_str = 'Paket telah diterima'
        # 疑难件
        elif self.str_process('Paket disimpan di gudang J&T') in yn_str:
            zh_str = 'Paket disimpan di gudang J&T'
        # 快件已被退回
        elif self.str_process('Package returned to seller') in yn_str:
            zh_str = 'Package returned to seller'
        # 装袋
        elif self.str_process('Pack') in yn_str:
            zh_str = 'Pack'
        # 拆袋
        elif self.str_process('Unpack') in yn_str:
            zh_str = 'Unpack'
        # 快件将被退回
        elif self.str_process('Paket akan diretur') in yn_str:
            zh_str = 'Paket akan diretur'
        # 问题件
        elif self.str_process('Paket Gagal dikirim') in yn_str:
            zh_str = 'Paket Gagal dikirim'
        # 问题件
        elif self.str_process('Pickup Failed') in yn_str:
            zh_str = 'Pickup Failed'
        # 快件处理中
        elif self.str_process('Paket Gagal dipickup') in yn_str:
            zh_str = 'Paket Gagal dipickup'
        # # 运单无效
        # elif str_process('Expired AWB') in yn_str:
        #     zh_str = '运单无效'
        # 其他官方未给出的状态
        else:
            zh_str = self.status
        return zh_str

    def str_process(self, str):
        new_str = str.replace(' ', '').lower()
        return new_str

if __name__ == '__main__':
    s = SyncStatusThread()
    s.main()

