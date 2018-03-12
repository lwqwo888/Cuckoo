# coding=utf-8
# 全和悅物流轨迹python对接方法
# 此demo为感谢全和悅技术人员Tiger的技术支持而制作

# url : 为物流轨迹请求地址
# params 参数的构建
#　　　　　1、params为请求参数,用三引号(''')包裹最稳妥,第一个三引号后必须紧跟参数内容(xml),不能使用空格或者换行,否则会导致参数错误.如果当前行使用了'''的话那么>后不能添加任何空格
#        2、<>yxxxy或<></>yxxxy :　xxx为标签包裹内容，y为位置，y位置可以使用空格或者换行以提高代码可读性，美观性．
#        3、<xxx><xxx/xxx> : xxx位置不建议使用任何为代码美观而更改的操作，比如添加空格或者换行．极大可能大致参数错误．(具体由标签是单标签<>还是双标签<></>决定，单标签<>：紧跟<后必须为原始标签内容不能添加任何东西，>前紧也不能添加任何除原始内容外的内容．双标签<></>：跟在<后必须为原始标签内容不能添加任何东西，/前不能添加任何内容，>前且紧贴着>的地方可以添加空格或者换行．)
#        4、<paramsJson>xxx</paramsJson> : xxx内容的格式为{"codes":["yyy","yyy","yyy",...]}     yyy为运单号码　可为多个　用""包裹　用,隔开
#        5、以上内容临时编写，如有不妥望见谅，遇构建参数问题无法解决时建议把xml写为一行再进行尝试，不使用任何空格换行以及缩进．
# 请求方式：POST(使用post方式将url和params传入即可)
# 2018-01-18
import re
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


url = "http://tms.alljoylogistics.com/default/svc/web-service"

params = '''<?xml version="1.0" encoding="UTF-8"?>
    <SOAP-ENV:Envelope xmlns:SOAP-ENV = "http://schemas.xmlsoap.org/soap/envelope/" xmlns:ns1="http://www.example.org/Ec/">
    <SOAP-ENV:Body>
    <ns1:callService>
    <paramsJson>{"codes":[%s]}</paramsJson>
    <appToken>40a4ebbcf22e6960e8670c9fe09a7625</appToken>
    <appKey>40a4ebbcf22e6960e8670c9fe09a76256f46a75a0a76cf7caf5e3d1c08b2af50</appKey>
    <service>getCargoTrack</service>
    </ns1:callService>
    </SOAP-ENV:Body>
    </SOAP-ENV:Envelope>
    ''' % result['track']

response = requests.post(url, data=params).text
print response
all_res = re.compile(r'"Detail":\[(.*?)\]', re.S)
all_data_list = all_res.findall(response)
all_data_list = ''.join(all_data_list)
all_status = re.compile(r'"Comment":"(.*?)"}', re.S)
all_status_list = all_status.findall(all_data_list)
all_time = re.compile(r'"Occur_date":"(.*?)"', re.S)
all_time_list = all_time.findall(all_data_list)

status_id = send_date(status, logistics_time, track, summary_status, '(250, 256)', '').acquire_date_id()

if all_time_list:
    tuerqi_quanheyue_list = [x for x in zip(all_time_list, all_status_list)]
    for logistics_time, status in tuerqi_quanheyue_list:
        tran_status_label = status
        # tran_status = send_date(status, logistics_time, track, summary_status, '(250)', '').acquire_date()
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
        # 以下2行测试使用******************************************************************
        print 'time:-------:', logistics_time
        print 'status:-------:', status

else:
    status = '未上线'
    logistics_time = ''
    # 以下2行测试使用******************************************************************
    print 'time:-------:', logistics_time
    print 'status:-------:', status