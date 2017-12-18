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
import sys
import getopt
import traceback
import os
import Queue
import time
import pymysql
import threading
import datetime
import requests
import hashlib
import base64
import re
import ChangeIp

class Sync(object):
    # init初始化了数据库连接信息，模式，线程数量
    # queue和save为两个队列
    def __init__(self,host,user,passwd,db_name,mode='nomal',thread_count=10):
        self.user = user
        self.passwd = passwd
        self.db_name = db_name
        self.mode = mode
        self.queue = Queue.Queue()
        self.save = Queue.Queue()
        # os.path.relpath(path[, start])  # 从start开始计算相对路径
        # os.path.split()：将文件名和路径分割开,返回一个元组
        # 最后获得当前文件的路径
        current_path = os.path.split(os.path.relpath(__file__))[0]
        self.__file_log = open('%s/log%s.txt'%(current_path,time.strftime('%Y_%m_%d')),"a+")
        self.flag_end = False
        self.thread_count = thread_count
        self.total_count = 0 # 总数量？？？
        # 创建连接
        self.connection = pymysql.connect(
            host=host,
            user=user,
            passwd=passwd,
            db=db_name,
            charset="utf-8",
            # 游标设置为字典类型
            cursorclass=pymysql.cursors.DictCursor
        )
        # 创建线程锁
        self.mutex = threading.Lock()
        self.save_mutex = threading.Lock()
        self.save_event = threading.Event(True)
        self.counts = {}

    def normal(self):
        """更新2个月内:除签收,退货,拒签的数据"""
        # 获取当前时间,然后减60天，得出两个月前的时间作为开始时间
        # 当前时间为结束时间
        d = datetime.datetime.now()
        day60 = datetime.timedelta(days=60)
        day = d - day60
        start_time = datetime.datetime(day.year, day.month, day.day, 0, 0, 0)
        end_time = datetime.datetime(d.year, d.month, d.day, 0, 0, 0)
        # 调用Connection对象的cursor()方法
        cursor = self.connection.cursor()
        cursor.execute('SET NAMES utf8')# ？？？？？？？？
        sql = u"""SELECT id_order_shipping, o.id_order, o.id_shipping, status_label, track_number, fetch_count ,summary_status_label
                    FROM erp_order as o LEFT JOIN erp_order_shipping as os on o.id_order = os.id_order
                    WHERE o.id_shipping in(51) AND track_number IS NOT NULL AND track_number != '' """
        sql += u"""And is_settlemented = 0 AND o.id_order_status in (8,9,16,23)"""
        sql += u" AND o.date_delivery >= '" + start_time.strftime('%Y-%m-%d 00:00:00') + "' "
        sql += u""" ORDER BY fetch_count ASC, o.date_delivery DESC """
        print(sql)
        self.log(sql)
        # 执行sql语句，返回值为受影响的行数
        cursor.execute(sql)
        # 获取查询结果
        data = cursor.fetchall()
        # 打印查询的结果
        print data
        # 关闭Cursor对象
        cursor.close()
        # 把查询结果逐条放入老队列
        for d in data:
            self.queue.put(d)

    def success(self):
        """更新15天内:签收的数据"""
        d = datetime.datetime.now()
        day30 = datetime.timedelta(days=30)
        day = d - day30
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
        # d = datetime.datetime.now()
        # day30 = datetime.timedelta(days=30)
        # day = d - day30
        # start_time = datetime.datetime(day.year, day.month, day.day, 0, 0, 0)

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

    # 获取队列中数据并返回
    def get_item(self):
        if not self.queue.empty():
            item = self.queue.get()
        else:
            item = None
        return item

    def log(self,msg):
        # 上锁
        self.mutex.acquire()
        self.__file_log.write(msg.encode("utf-8"))
        self.__file_log.write(u'\n'.encode('utf-8'))
        # 解锁
        self.mutex.release()

    # 存入新队列
    def save_queue(self, item):
        self.save.put(item)

    # 获取新队列中数据并返回
    def get_save_item(self):
        if not self.save.empty():
            item = self.save.get()
        else:
            item = None
        return item

    def save_item(self):
        pass

    # 增加总数量（至于是什么总数量现在我也不知道）***************************************************
    def increment(self):
        self.mutex.acquire()
        self.total_count += 1
        self.mutex.release()

    # 根据选项启动对应的模式
    def start(self):
        if self.mode == 'single':
            pass
        elif self.mode == 'sccess':
            self.success()
        elif self.mode == 'all':
            self.all()
        elif self.mode == 'time_range':
            self.time_range(self.time_start, self.time_end)
        else:
            self.normal()
        start_time = time.time()
        # 队列中的数量
        total = self.queue.qsize()
        self.log(u"开始抓取：%s，共：%s个，模式：%s")%(time.strftime("%Y-%m-%d %H:%M:%S"), total,self.mode)
        print((u"开始抓取：%s，共：%s个，模式：%s")%(time.strftime("%Y-%m-%d %H:%M:%S"), total,self.mode))
        threads = []
        for idx in range(self.thread_count):
            # 把Sync传给了SyncStatusThread类？
            thread = SyncStatusThread(self)
            # 类对象.start()？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？？
            thread.start()
            threads.append(thread)


class SaveThread(object,threading.Thread):
    # 为什么不直接用继承Sync?????????????????????????????????????
    def __init__(self, sync):
        super(SaveThread, self).__init__()
        self.sync = sync

    def run(self):
        while True:
            try:
                # item为新队列中的数据
                item = self.sync.get_save_item()
                # 如果不为空
                if not item:
                    # flag_end为布尔类型，初始化的时候为False
                    if self.sync.flag_end:
                        break
                    else:
                        self.sync.save_event.clear()
                        self.sync.save_event.wait()
                        continue
                self.sync.save_item(item)
            except Exception as e:
                self.sync.log(str(e))
                # traceback模块被用来跟踪异常返回字符串信息
                self.sync.log(traceback.format_exc())
            finally:
                pass

# 执行线程
class SyncStatusThread(object,threading.Thread):
    def __init__(self, sync):
        super(SyncStatusThread, self).__init__()
        self.sync = sync

    def run(self):
        while True:
            try:
                # 获取老队列中的数据
                item = self.sync.get_item()
                if not item:
                    # 完成的线程和完成时间存入日志,并跳出循环
                    self.sync.log(u"TH：%s,完成：%s" %(
                        threading.currentThread().getName(),
                        time.strftime("%Y-%m-%d %H:%M:%S")
                    ))
                    break
                self.sync.log(u'START:TH:%s,开始：%s，运单号：%s' %(
                    threading.currentThread().getName(),
                    time.strftime("%Y-%m-%d %H:%M:%S"),
                    item['track_number']
                ))
                # result是根据数据库的运单通过接口查出来的最新物流状态!!!!!!!!
                result = self.fetch_dec(item)
                # 增加总数量
                self.sync.increment()
                # 放入新队列(把什么放进去了？？？？？？？？？？？？？？？？？？？？)
                self.sync.save_queue(result)
                self.sync.save_event.set()

                self.sync.log(u"DONE:TH:%s,完成：%s，运单号：%s, 状态：%s，状态时间：%s")%(
                    threading.currentThread().getName(),
                    time.strftime("%Y-%m-%d %H:%M:%S"),
                    item['track_number'],
                    result['status'],
                    result['time']
                )
            except Exception as e:
                self.sync.log(u'EX-SYNC:' + str(e))
                self.sync.log(traceback.format_exc())
            finally:
                pass

    # 抓取接口数据
    def fetch_dec(self, item):
        # 概要——状态？？？
        summary_status = ''
        getstat = ''
        # 物流时间
        logistics_time = ''
        track = item['track_number']
        # 字典键值为对应数据库的字段
        result = {
            'track': item['track_number'],
            'fetch_count': item['fetch_count'],
            'id_order_shipping': item['id_order_shipping'],
            'id_order': item['id_order'],
            'id_shipping': item['id_shipping'],
            'old_status': item['status_label'],
            'old_summary_status': item['summary_status_label'],
            'summary_status': '',
            'getstat': '',
            'time': '',
            'loc': ''
        }
        status = result['old_status']
        summary_status = result['old_summary_status']
        try:
            bindIpObj = ChangeIp.bindIp()
            bindIpObj.randomIp()
            print '当前IP：%s  总IP：%s' % (str(bindIpObj.getIp()), str(bindIpObj.getIpsCount()))
            bindIpObj.changeIp(bindIpObj.getIp())
            url = "http://bsp-ois.sit.sf-express.com:9080/bsp-ois/sfexpressService"
            string_message = """
                <Request service="RouteService" lang="zh-CN">
                    <Head>BSPdevelop</Head>
                        <Body>
                            <RouteRequest
                            tracking_type="1"
                            method_type="1"
                            tracking_number=""" + track + """/>
                        </Body>
                </Request>
            """

            passwd = "j8DzkIFgmlomPt0aLuwU"

            combine = string_message + passwd
            m = hashlib.md5(combine).digest()
            result = base64.b64encode(m)
            print result
            params = {
                "xml": string_message,
                "verifyCode": result
            }
            res = requests.post(url,data=params).content
            bindIpObj.changeIp("")
            status_id = send_date(getstat, logistics_time, track, ' ', '(51)').acquicre_date_id()
            pattern = re.compile(r'<Route remark="(.*?)"', re.S)
            n = pattern.findall(res)
            # n为物流轨迹信息，t为对应物流信息的时间点
            if n == []:
                getstat = '未上线'
                logistics_time = ''
                tran_status_label = '未上线'
                send_date(getstat, logistics_time, track, ' ', str(status_id[0]['id_shipping']),tran_status_label).insert_date()
            else:
                pattern = re.compile(r'accept_time="(.*?)"', re.S)
                t = pattern.findall(res)
                sf_list = [i for i in zip(n, t)]
                print sf_list
                for i, j in sf_list:
                    getstat = i
                    logistics_time = j
                tran_status = send_date(getstat, logistics_time, track, summary_status, '(51)','').acquire_date()
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
        opts,args = getopt.getopt(sys.argv[1:],"hs:d:u:p:r:l:")
    except getopt.GetoptError as e:
        print(str(e))
        # traceback模块被用来跟踪异常返回信息,traceback.print_exc()打印到屏幕
        traceback.print_exc()
        sys.exit(1)
    # 默认不指定线程数量情况下为40条线程
    thread_count = 40
    # 所有信息初始化为空字符串
    db_name = db_user = db_passwd = ''
    run_mode = 'normal'
    single = None
    time_start = None
    time_end = None
    for o,v in opts:
        if o in ('-h','--help'):
            pass
        if o in ('-d','--database'):
            db_name = v
        if o in ('-r', '--run'):
            run_mode = v
        if o in ('-t', '--thread_count'):
            thread_count = int(v)
        if o in ('-s', '--single'):
            # 单个运单号
            single = v.strip()
        if o in ('-l'):
            run_mode = 'time_range'
            (time_start, time_end) = v.split(':')

    print(opts)
    lock_file = '.fetch_dec' + run_mode
    # 用于判断文件等是否存在,返回布尔类型
    # 如果文件存在则删除文件,并以写模式创建新的文件
    if os.path.exists(lock_file):
        print("%s 模式已在运行中..." % lock_file)
        os.remove(lock_file)
        sys.exit(1)
    with open(lock_file,'w') as f:
        f.write(lock_file)
    # 创建对象,并传入数据库连接信息和运行模式以及线程数
    sync = Sync(host='120.77.222.224', user=db_user, passwd=db_passwd, db_name=db_name,
                mode=run_mode, thread_count=thread_count)
    try:
        if single:
            # 给类方法传递运单个运单号参数,然后运行抓取程序
            sync.single(single)
        # 如果运行模式为时间范围模式就以时间范围模式运行抓取程序
        if run_mode == 'time_range':
            sync.time_start = time_start
            sync.time_end = time_end
# 运行抓取程序*****************************************************************
        sync.start()
# ***************************************************************************
    except Exception as e:
        # 如果启动失败则记录失败日志并输出在屏幕上
        sync.log(str(e))
        sync.log(traceback.print_exc())
    finally:
        # 无论成功失败，都将执行完finally后执行return（如果有return的话）
        os.path.exists()
        if os.path.exists(lock_file):
            os.remove(lock_file)
        sync.log(u"结束")



if __name__ == '__main__':
    main()