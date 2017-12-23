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
        # 如果队列不为空
        if not self.queue.empty():
            # 获取队列
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
        # 将一个值放入队列中
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