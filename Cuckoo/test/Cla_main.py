#!/usr/bin/env python

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
        # 如果运行模式为随机时间,同样运行抓取程序
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
        # 用于判断变量、文件等是否存在,返回布尔类型
        if os.path.exists(lock_file):
            # 删除指定路径的文件
            os.remove(lock_file)
        # 写入日志
        sync.log(u"结束")


if __name__ == '__main__':
    main()