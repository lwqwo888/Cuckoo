import Queue
import base64
import datetime
import getopt
import hashlib
import os
import random
import re
import sys
import threading
import time
import traceback
import requests
import json
import ChangeIp
import pymysql
# 线程状态
class SyncStatusThread(threading.Thread):
    def __init__(self, sync):
        super(SyncStatusThread, self).__init__()
        self.sync = sync

    def run(self):

        while True:
            try:
                item = self.sync.get_item()
                if not item:
                    self.sync.log(u"TH:%s,完成:%s" % (
                        threading.currentThread().getName(),
                        time.strftime("%Y-%m-%d %H:%M:%S")))
                    break
                self.sync.log(u"START:TH:%s,开始:%s,运单号:%s" % (
                    threading.currentThread().getName(),
                    time.strftime("%Y-%m-%d %H:%M:%S"),
                    item['track_number']))

                result = self.fetch_dec(item)

                self.sync.increment()
                self.sync.save_queue(result)
                self.sync.save_event.set()

                self.sync.log(u"DONE:TH:%s,完成:%s,运单号:%s,状态:%s,状态时间:%s" % (
                    threading.currentThread().getName(),
                    time.strftime("%Y-%m-%d %H:%M:%S"),
                    item['track_number'],
                    result['status'],
                    result['time']))
            except Exception as e:
                self.sync.log(u'EX-SYNC:' + str(e))
                self.sync.log(traceback.format_exc())
            finally:
                pass
    def fetch_dec(self, item):
        """DEC抓取"""
        summary_status = ''
        getstat = ''
        logistics_time = ''
        track = item['track_number']

        result = {'track': item['track_number'],
                  'fetch_count': item['fetch_count'],
                  'id_order_shipping': item['id_order_shipping'],
                  'id_order': item['id_order'],
                  'id_shipping': item['id_shipping'],
                  'old_status': item['status_label'],
                  'old_summary_status': item['summary_status_label'],
                  'summary_status': '',
                  'getstat': '',
                  'time': '',
                  'loc': ''}
        status = result['old_status']
        summary_status = result['old_summary_status']
        try:
            bindIpObj = ChangeIp.bindIp()
            bindIpObj.randomIp()
            print '当前IP：%s  总IP：%s' % (str(bindIpObj.getIp()), str(bindIpObj.getIpsCount()))
            bindIpObj.changeIp(bindIpObj.getIp())
            url = "http://218.16.117.83:8033/APIQuery.aspx?TrackNum=" + item['track_number']
            res = requests.get(url)
            html = res.content
	    bindIpObj.changeIp("")
            status_id = send_date(getstat, logistics_time, track, ' ', '(51)', '').acquire_date_id()
            res_tab = r'<ishaspod>(.*?)</ishaspod>'
            stat = re.findall(res_tab, html, re.S | re.M)[0]
            if not stat:
                getstat = '未上线'
                logistics_time = ''
                tran_status_label = '未上线'
                send_date(getstat, logistics_time, track, ' ', str(status_id[0]['id_shipping']),tran_status_label).insert_date()

            else:
                res_tab1 = r'<scanstatusname>(.*?)</scanstatusname>'
                getstat_init = re.findall(res_tab1, html, re.S | re.M)
                i = 0
                print len(getstat_init)
                for x in range(len(getstat_init)):
                    getstat = re.findall(res_tab1, html, re.S | re.M)[i].decode('gbk')
                    res_tab2 = r'<scandate>(.*?)</scandate>'
                    date_list1 = re.findall(res_tab2, html, re.S | re.M)[i].decode('gbk')
                    res_tab3 = r'<scandime>(.*?)</scandime>'
                    date_list2 = re.findall(res_tab3, html, re.S | re.M)[i].decode('gbk')
                    logistics_time = date_list1 + ' ' + date_list2
                    tran_status = send_date(getstat, logistics_time, track, summary_status, '(51)',
                                            '').acquire_date()
                    i = i+1
                    if tran_status:
                        for tran_status_item in tran_status:
                            if tran_status_item['status_label'].strip() in getstat:
                                tran_status_label = tran_status_item['status_label']
                                break
                            else:
                                tran_status_label = getstat
                        send_date(getstat, logistics_time, track, ' ', str(status_id[0]['id_shipping']),tran_status_label).insert_date()
            result['status'] = getstat
            result['time'] = logistics_time
            print '%s --- %s --- %s' % (
            result['track'], result['status'], result['time'])
            return result
        except Exception, e:
            print e
            return "程序错误"
