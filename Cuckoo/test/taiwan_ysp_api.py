# coding=utf-8
import re
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

<<<<<<< HEAD
url = 'http://220.132.209.89/API/esp.php?A=esp&C=esp1234&S=39526424124874'
=======
url = 'http://220.132.209.89/API/esp.php?A=esp&C=esp1234&S=59471624124874'
>>>>>>> b38c728aaae98a3d51c84dbedb98d7d8761193ca
res = requests.get(url).text
print res
time_list = []
time_info = re.compile(r'"states_t":\[(.*?)\]', re.S)
status_info = re.compile(r'"states_s":\[(.*?)\]', re.S)
all_time = time_info.findall(res)
# status_id = send_date(status, logistics_time, track, '', '(258,262)','').acquire_date_id()

if all_time:
    all_status = status_info.findall(res)
    time_str = ''.join(all_time).split(',')
    status_list = ''.join(all_status).split(',')

    for i in time_str:
        list = i.replace('"', '').split(' ')
        date = list[0][:4] + '-' + list[0][4:6] + '-' + list[0][6:8]
        time = list[1][:2] + ':' + list[1][2:4] + ':' + list[1][4:6]
        time_list.append(date + ' ' + time)

    taiwanysp_list = [x for x in zip(time_list, status_list)]
    for logistics_time, status in taiwanysp_list:
        status = status.decode("unicode-escape")
        tran_status_label = status
        # print logistics_time
        # print status
        # tran_status = send_date(status, logistics_time, track, summary_status, '(258,262)', '').acquire_date()
        # print tran_status
        # if tran_status:
        #     for tran_status_item in tran_status:
        #         if tran_status_item['status_label'].strip() in status:
        #             tran_status_label = tran_status_item['status_label']
        #             print tran_status_label
        #             break
        #         else:
        #             tran_status_label = status
        # send_date(status, logistics_time, track, ' ', str(status_id[0]['id_shipping']),tran_status_label).insert_date()
        # 以下1行测试使用******************************************************************
        print 'time:---------------: ', logistics_time + '\n' + 'status:---------------: ', status + '\n' + 'tran:---------------: ', tran_status_label + '\n'

        with open('台湾ysp信息.txt', 'a') as f:
            f.write(logistics_time + '\n' + status + '\n')

else:
    status = '未上线'
    logistics_time = ''
    tran_status_label = status
    # send_date(status, logistics_time, track, ' ', str(status_id[0]['id_shipping']), tran_status_label).insert_date()
    # 以下1行测试使用******************************************************************
    print 'time:---------------: ', logistics_time + '\n' + 'status:---------------: ', status + '\n' + 'tran:---------------: ', tran_status_label + '\n'
