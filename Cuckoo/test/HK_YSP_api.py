# coding=utf8
import re
import requests
import sys
reload(sys)
sys.setdefaultencoding('utf-8')

class SyncStatusThread(object):
    def acquire_date(self):
        '''
        获取数据
        :return:789624665516
                789641730707
        '''
        # url = 'http://119.23.28.96/cgi-bin/GInfo.dll?EmsApiTrack&cno=' + track_number
        url = 'http://119.23.28.96/cgi-bin/GInfo.dll?EmsApiTrack&cno=789714899316'
        html = requests.get(url).content.decode('gbk').encode('utf-8')
        print html
        all_status = re.compile(r'<INFO>(.*?)</INFO>', re.S)
        all_time = re.compile(r'<DATETIME>(.*?)</DATETIME>', re.S)
        status_list = all_status.findall(html)
        time_list = all_time.findall(html)

        if time_list:
            ysp_list = [i for i in zip(time_list, status_list)]
            for i, j in ysp_list:
                res = re.compile(r'^(\d+)$', re.S)
                id = res.findall(j)
                if id:
                    status = "已签收"
                else:
                    status = j
                if len(i) > 10:
                    logistics_time = i + ':00'
                else:
                    logistics_time = i + ' 00:00:00'
                ran_status_label = self.control(self.str_process(status))
                # 以下2行测试使用******************************************************************
                with open("HK_YSP信息1.txt", "a") as f:
                    f.write(logistics_time + '\n' + status + '\n' )
        else:
            status = '未找到'
            logistics_time = ''
            ran_status_label = status
            # 以下2行测试使用******************************************************************
            with open("HK_YSP信息1.txt", "a") as f:
                f.write(logistics_time + '\n' + status + '\n' + ran_status_label + '\n')

    def control(self, original_str):
        print 'original_str : ', original_str
        # 派件
        if '正在派送途中' in original_str:
            ran_status = '正在派送途中'
        elif ('快件在'in original_str) and ('已装车' in original_str) and ('准备发往' in original_str):
            ran_status = '正在派送途中'
        elif ('快件在' in original_str) and ('装车' in original_str) and ('已发往' in original_str):
            ran_status = '正在派送途中'
        # 签收
        elif '快件到达' in original_str:
            ran_status = '快件到达'
        # 快件派送不成功
        elif '快件派送不成功' in original_str:
            ran_status = '快件派送不成功'
        # 其他状态
        else:
            ran_status = original_str
        return ran_status

    def str_process(self,old_str):
        new_str = old_str.strip().replace('\r', '').replace('\n', '').replace('\t', '').replace(' ', '').lower()
        return new_str

if __name__ == '__main__':
    s = SyncStatusThread()
    s.acquire_date()