# coding=utf-8
import json
import jsonpath
from suds.client import Client
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


url = 'http://www.pfcexpress.com/webservice/APIWebService.asmx?wsdl'
client = Client(url)
Orderid = result['track']
secretkey = '434a2ed2-8056-4579-9a47-cfaa48676ffb80000'
res = client.service.getOrder_Track(Orderid, secretkey)
# status_id = send_date(status, logistics_time, track, '', '(228)','').acquire_date_id()

# json字符串转换为python字典对象
all_info_dict = json.loads(res)
if all_info_dict:
    all_status = jsonpath.jsonpath(all_info_dict, expr='$..DetailDesc')
    all_time = jsonpath.jsonpath(all_info_dict, expr='$..OccurTime')
    Pakistan_list = [x for x in zip(all_time, all_status)]
    for time, status in Pakistan_list:
        logistics_time = time + ':00'
        tran_status_label = status
        # print logistics_time
        # print status
        # tran_status = send_date(status, logistics_time, track, summary_status, '(228)', '').acquire_date()
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

        with open('巴基斯坦信息.txt', 'a') as f:
            f.write(logistics_time + '\n' + status + '\n')

else:
    status = '未上线'
    logistics_time = '未上线'
    tran_status_label = status
    # send_date(status, logistics_time, track, ' ', str(status_id[0]['id_shipping']), tran_status_label).insert_date()
    # 以下1行测试使用******************************************************************
    print 'time:---------------: ', logistics_time + '\n' + 'status:---------------: ', status + '\n' + 'tran:---------------: ', tran_status_label + '\n'




























    # url = 'http://www.pfcexpress.com/Manage/WebManage/Inquire.aspx?txtID=No'
# params = {
#     "__VIEWSTATE": "/wEPDwUJNzA0MDM4NDQxD2QWAgIDD2QWBAIDDxYCHglpbm5lcmh0bWwFDVJTNzMzNTMwOTk0TkxkAgcPFgIeC18hSXRlbUNvdW50AgEWAmYPZBYMAgEPDxYCHgRUZXh0BQ1SUzczMzUzMDk5NE5MZGQCCA8PFgIfAgUQUjg4NzcxMTYxMjI3MDAwNGRkAgkPFQEAZAIKDw8WAh8CBQzmn6Xor6LkuI3liLBkZAILDxUBFmh0dHA6Ly93d3cucG9zdG5sLnBvc3RkAgwPFgIfAQICFgRmD2QWAmYPFQIz5Lqk6L+Q5Y+R5b6A55uu55qE5ZywKFNoaXBtZW50IHNlbnQgdG8gZGVzdGluYXRpb24pEzIwMTYvMTIvMjcgMjM6MTY6NTlkAgEPZBYCZg8VAiDmlLblj5bljIXoo7koU2hpcG1lbnQgcGlja2VkIHVwKRMyMDE2LzEyLzI3IDE1OjI2OjQwZGQ=",
#     "__EVENTVALIDATION": "/wEdAA1B/5EuABonXzGsobt5My8qzNCzw1gwjBlA50UnPUJCAJRAu/OD0Jy+o9gY8Vm8qx7ViiV4CmJW9sxEFEDUThETy05SHEBC01jgZA725qKZPsCrd+BYicQK4OUbLVBXV5UYYKj3GiIxqu6Gw0I+iwhw99ENsFVYZPTPTIq/n6JyYYyYeXB3gxaFALTQhsqvhd5WTqkeGILv73Oswc4eEHjk5UjbSplqEJ8RoaweO464dTKGuStP+zoHUp3spTVeUI5LnROtGoq+aA3oU+wDQg07",
#     "txtNo": "RS733530994NL",
#     # "BtnConfirm": "包裹查询",
# }
# print requests.post(url, data=params).text