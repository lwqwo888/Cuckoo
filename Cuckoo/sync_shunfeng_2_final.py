# !/usr/bin/env python
# -*- coding: utf-8 -*-
# version: 0.4
# 新版ERP
# 同步物流状态
# 1.新导入的运单号 2.签收 3.退货 4.拒签 5.签收转退货 6.订单状态缺货 7.订单状态取消
# 参数: normal(默认), all(更新所有), success(更新已签收),
# 脚本功能:
# 参数:-d db_name -u user -p password -r run_mode -t thread_count=10 [-s 625009994794] [-l 2017-01-01:2017-01-09]
# 1.主程序读取要同步的运单号信息
# 2.主程序分配多线程同时抓取物流状态信息
# 3.主程序同步更新到数据库

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

# from cat_date import send_date
# from config import DB_TYPE,DB_HOST,DB_NAME,DB_USER,DB_PWD,DB_PORT

LOCK_FILE_NAME = 'dec'
defaultencoding = 'utf-8'
if sys.getdefaultencoding() != defaultencoding:
    reload(sys)
    sys.setdefaultencoding(defaultencoding)


class Sync:
    def __init__(self, host, user, passwd, db_name, mode='normal', thread_count=10):
        self.user = user
        self.passwd = passwd
        self.db_name = db_name
        self.mode = mode
        self.queue = Queue.Queue()
        self.save = Queue.Queue()
        current_path = os.path.split(os.path.realpath(__file__))[0]
        self.__file_log = open('%s/log%s.txt' % (current_path, time.strftime('%Y_%m_%d')), 'a+')
        self.flag_end = False
        self.thread_count = thread_count
        self.total_count = 0
        # 创建了一个数据库连接对象
        self.connection = pymysql.connect(
            host=host,
            user=user,
            password=passwd,
            db=db_name,
            charset='utf8',
            cursorclass=pymysql.cursors.DictCursor
        )

        self.mutex = threading.Lock()
        self.save_mutex = threading.Lock()
        self.save_event = threading.Event(True)
        self.counts = {}

    def normal(self):
        """更新2个月内:除签收,退货,拒签的数据"""
        d = datetime.datetime.now()
        day60 = datetime.timedelta(days=60)
        day = d - day60
        start_time = datetime.datetime(day.year, day.month, day.day, 0, 0, 0)
        end_time = datetime.datetime(d.year, d.month, d.day, 0, 0, 0)
        cursor = self.connection.cursor()
        cursor.execute('SET NAMES utf8')
        sql = u"""SELECT id_order_shipping, o.id_order, o.id_shipping, status_label, track_number, fetch_count ,summary_status_label
                                  FROM erp_order as o LEFT JOIN  erp_order_shipping as os on o.id_order = os.id_order
                                  WHERE  o.id_shipping in(51) AND track_number IS NOT NULL AND track_number != '' """
        sql += u"""And is_settlemented = 0 AND o.id_order_status in (8,9,16,23)"""
        sql += u" AND o.date_delivery >= '" + start_time.strftime('%Y-%m-%d 00:00:00') + "' "
        sql += u""" ORDER BY fetch_count ASC, o.date_delivery DESC """
        print sql
        self.log(sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        for d in data:
            self.queue.put(d)
# 暂时不用
    def all(self):
        """更新2个月内:所有数据"""
        d = datetime.datetime.now()
        day60 = datetime.timedelta(days=90)
        day = d - day60
        start_time = datetime.datetime(day.year, day.month, day.day, 0, 0, 0)
        end_time = datetime.datetime(d.year, d.month, d.day, 0, 0, 0)
        cursor = self.connection.cursor()
        cursor.execute('SET NAMES utf8')
        sql = u"""SELECT id_order_shipping, id_order, id_shipping, status_label, track_number, fetch_count ,summary_status_label
              FROM erp_order_shipping WHERE id_shipping in(51) and is_settlemented=0 and track_number not like 'SZT%' and track_number IS NOT NULL AND track_number != ''"""
        sql += u" AND created_at >= '" + start_time.strftime('%Y-%m-%d 00:00:00') + "' "
        sql += u"""ORDER BY fetch_count ASC, created_at DESC"""

        self.log(sql)
        print sql
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        for d in data:
            self.queue.put(d)
# 暂时不用
    def empty(self):
        """更新2个月内:所有空状态数据"""
        cursor = self.connection.cursor()
        cursor.execute('SET NAMES utf8')
        sql = u"""SELECT id_order_shipping, id_order, id_shipping, status_label, track_number, fetch_count ,summary_status_label
              FROM erp_order_shipping
              WHERE  id_shipping in(51) and track_number not like 'SZT%' and track_number IS NOT NULL AND track_number != '' AND (status_label = '' OR status_label IS NULL )
              ORDER BY fetch_count ASC, created_at DESC"""

        self.log(sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        for d in data:
            self.queue.put(d)

    def success(self):
        """更新15天内:签收的数据"""
        d = datetime.datetime.now()
        day60 = datetime.timedelta(days=30)
        day = d - day60
        start_time = datetime.datetime(day.year, day.month, day.day, 0, 0, 0)

        cursor = self.connection.cursor()
        cursor.execute('SET NAMES utf8')
        sql = u"""SELECT a.id_order_shipping, a.id_order, a.id_shipping, a.status_label, a.track_number, a.fetch_count ,a.summary_status_label,b.id_increment
                      FROM erp_order_shipping a
                      INNER JOIN erp_order b on a.id_order=b.id_order
                      WHERE  a.id_shipping in (51) and a.track_number not like 'SZT%' and a.track_number IS NOT NULL and a.track_number != ''
                      and ( a.summary_status_label = '已签收' or a.summary_status_label = '拒收') a.is_settlemented = 0 """
        sql += u" AND a.created_at >= '" + start_time.strftime('%Y-%m-%d 00:00:00') + "' "
        sql += u"""ORDER BY a.fetch_count ASC, a.created_at DESC"""

        self.log(sql)

        print sql
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        for d in data:
            self.queue.put(d)

    def single(self, track_number):
        """更新单个运单号"""
        self.mode = 'single'
        d = datetime.datetime.now()
        day60 = datetime.timedelta(days=30)
        day = d - day60
        start_time = datetime.datetime(day.year, day.month, day.day, 0, 0, 0)

        cursor = self.connection.cursor()
        cursor.execute('SET NAMES utf8')
        sql = u"""SELECT a.id_order_shipping, a.id_order, a.id_shipping, a.status_label, a.track_number, a.fetch_count ,a.summary_status_label,b.id_increment
                  FROM erp_order_shipping a
                  INNER JOIN erp_order b on a.id_order=b.id_order
                  WHERE a.track_number = '%s' """ % track_number
        # sql += u" AND created_at >= '" + start_time.strftime('%Y-%m-%d 00:00:00') + "' "
        # sql += u""" ORDER BY fetch_count ASC, created_at DESC"""
        print sql
        self.log(sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        for d in data:
            self.queue.put(d)

    # pass
    def time_range(self, time_start, time_end):
        self.mode = 'time_range'
        # cursor用来执行命令的方法
        cursor = self.connection.cursor()
        # execute(self, query, args):执行单条sql语句, 接收的参数为sql语句本身和使用的参数列表, 返回值为受影响的行数
        cursor.execute('SET NAMES utf8')
        sql = u"""SELECT id_order_shipping, id_order, id_shipping, status_label, track_number, fetch_count ,summary_status_label
                          FROM erp_order_shipping
                          WHERE """
        sql += u" created_at >= '" + time_start + "' "
        sql += u" AND created_at <= '" + time_end + "' "

        self.log(sql)
        cursor.execute(sql)
        data = cursor.fetchall()
        cursor.close()
        for d in data:
            self.queue.put(d)

    def get_item(self):
        if not self.queue.empty():
            item = self.queue.get()
        else:
            item = None
        return item

    def log(self, msg):
        # 获取互斥锁????
        self.mutex.acquire()
        # 写入日志文件并换行
        self.__file_log.write(msg.encode('utf-8'))
        self.__file_log.write(u'\n'.encode('utf-8'))
        # 释放互斥锁????
        self.mutex.release()

    def save_queue(self, item):
        self.save.put(item)

    def get_save_item(self):
        if not self.save.empty():
            item = self.save.get()
        else:
            item = None
        return item

    def save_item(self, item):
        pass

    def increment(self):
        self.mutex.acquire()
        self.total_count += 1
        self.mutex.release()

    def start(self):
        if self.mode == 'single':
            pass
        elif self.mode == 'success':
            self.success()
        elif self.mode == 'all':
            self.all()
        elif self.mode == 'time_range':
            self.time_range(self.time_start, self.time_end)
        else:
            self.normal()
        start_time = time.time()
        total = self.queue.qsize()
        self.log(u"开始抓取:%s,共:%s,模式:%s" % (time.strftime("%Y-%m-%d %H:%M:%S"), total, self.mode))
        print(u"开始抓取:%s,共:%s,模式:%s" % (time.strftime("%Y-%m-%d %H:%M:%S"), total, self.mode))
        threads = []
        for idx in range(self.thread_count):
            thread = SyncStatusThread(self)
            thread.start()
            threads.append(thread)

        save_thread = SaveThread(self)
        save_thread.start()

        for t in threads:
            t.join()

        self.flag_end = True
        self.save_event.set()
        save_thread.join()
        # 所有都抓取完
        end_time = time.time()
        self.log(u"完成抓取:%s,共:%s,模式:%s,用时:%s秒" % (
            time.strftime("%Y-%m-%d %H:%M:%S"),
            total,
            self.mode,
            (end_time - start_time)))
        str_cocunt = u''
        for k, v in self.counts.iteritems():
            str_cocunt += u"状态:%s,数量:%s," % (k, v)
        self.log(u"抓取:%s" % str_cocunt[:-1])
        print(u"完成抓取:%s,共:%s,模式:%s,用时:%s秒" % (
            time.strftime("%Y-%m-%d %H:%M:%S"),
            total,
            self.mode,
            (end_time - start_time)))
        print(u"抓取:%s" % str_cocunt[:-1])


class SaveThread(threading.Thread):
    def __init__(self, sync):
        super(SaveThread, self).__init__()
        self.sync = sync

    def run(self):
        while True:
            try:
                item = self.sync.get_save_item()
                if not item:
                    if self.sync.flag_end:
                        break
                    else:
                        self.sync.save_event.clear()
                        self.sync.save_event.wait()
                        continue
                self.sync.save_item(item)
            except Exception as e:
                self.sync.log(str(e))
                self.sync.log(traceback.format_exc())
            finally:
                pass

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
	    bindIpObj.changeIp("") # ??????????????????????????????
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
                # 第一次使用正则匹配出所有被<scanstatusname>标签包裹的值
                getstat_init = re.findall(res_tab1, html, re.S | re.M)
                i = 0
                print len(getstat_init)
                # 列表的长度即为值的个数
                for x in range(len(getstat_init)):
                    # 第一次使用正则匹配出所有被<scanstatusname>标签包裹的对应下标的值
                    getstat = re.findall(res_tab1, html, re.S | re.M)[i].decode('gbk')

                    res_tab2 = r'<scandate>(.*?)</scandate>'
                    # 第二次使用正则匹配出被<scandate>标签包裹的对应下标的值
                    date_list1 = re.findall(res_tab2, html, re.S | re.M)[i].decode('gbk')

                    res_tab3 = r'<scandime>(.*?)</scandime>'
                    # 第三次使用正则匹配出被<scandate>标签包裹的对应下标的值
                    date_list2 = re.findall(res_tab3, html, re.S | re.M)[i].decode('gbk')
                    # 得到新的字符串
                    logistics_time = date_list1 + ' ' + date_list2
                    tran_status = send_date(getstat, logistics_time, track, summary_status, '(51)',
                                            '').acquire_date()
                    i = i+1

                    if tran_status:
                        for tran_status_item in tran_status:
                            # 移除字符串首尾空格
                            if tran_status_item['status_label'].strip() in getstat:
                                tran_ssynctatus_label = tran_status_item['status_label']
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


def main():
    try:
        # 函数getopt(args, shortopts短格式 (-),或者 longopts=[]长格式(--) )
        # 参数args一般是sys.argv[1:]
        opts, args = getopt.getopt(sys.argv[1:], 'hs:d:u:p:r:l:')
    except getopt.GetoptError as e:
        print(str(e))
        # traceback模块被用来跟踪异常返回信息,traceback.print_exc()打印到屏幕，便于调试.
        traceback.print_exc()
        sys.exit(1)

    thread_count = 40
    # 所有信息初始化为空字符串
    db_name = db_user = db_passwd = ''
    run_mode = 'normal'
    single = None
    time_start = None
    time_end = None
    for o, v in opts:
        if o in ('-h', '--help'):
            # show help
            pass
        if o in ('-d', '--database'):
            # dbname
            db_name = v
        if o in ('-u', '--user'):
            db_user = v
        if o in ('-p', '--password'):
            db_passwd = v
        if o in ('-r', '--run'):
            run_mode = v
        if o in ('-t', '--thread_count'):
            thread_count = int(v)
        if o in ('-s', '--single'):
            # 运单号
            single = v.strip()
        if o in ('-l'):
            run_mode = 'time_range'
            (time_start, time_end) = v.split(':')

    print(opts)
    lock_file = '.fetch_dec_' + run_mode
    if os.path.exists(lock_file):
        print('%s 模式已在运行中...' % lock_file)
        os.remove(lock_file)
        sys.exit(1)
    file_hide = file(lock_file, 'w')
    file_hide.write(lock_file)
    file_hide.close()
    sync = Sync(host='120.77.222.224', user=db_user, passwd=db_passwd, db_name=db_name,
                mode=run_mode, thread_count=thread_count)
    try:
        if single:
            # 给类方法传递运单号参数,然后运行抓取程序
            sync.single(single)
        # 如果运行模式为时间范围模式,同样运行抓取程序
        if run_mode == 'time_range':
            sync.time_start = time_start
            sync.time_end = time_end
        # 运行抓取程序*****************************************************************
        sync.start()
        # ***************************************************************************
    except Exception as e:
        sync.log(str(e))
        sync.log(traceback.print_exc())
    finally:
        os.path.exists()
        # 用于判断文件、文件夹等是否存在,返回布尔类型
        if os.path.exists(lock_file):
            # 删除指定路径的文件
            os.remove(lock_file)
        # 写入日志
        sync.log(u"结束")


if __name__ == '__main__':
    main()
