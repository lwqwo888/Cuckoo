#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : cat_date.py
# @Author: handan
# @Date  : 2017/10/19
# @Desc  :

import pymysql
import time
from pymysql.cursors import DictCursor
from DBUtils.PooledDB import PooledDB
from config import DB_TYPE,DB_HOST,DB_NAME,DB_USER,DB_PWD,DB_PORT,DB_charset

class send_date:
    def __init__(self,status,logistics_time,track_n,summary_status,shipping_id,tran_status_label):

        self.status            = status
        self.tran_status_label = tran_status_label
        self.summary_status    = summary_status
        self.logistics_time    = logistics_time
        self.track_n           = track_n
        self.shipping_id       = shipping_id
        self._conn = send_date.__getConn()
        self._cursor = self._conn.cursor()

    """ 
        MYSQL数据库对象，负责产生数据库连接 , 此类中的连接采用连接池实现获取连接对象：conn = Mysql.getConn() 
                释放连接对象;conn.close()或del conn 
        """
    # 连接池对象
    __pool = None

    # def __init__(self):
    #     # 数据库构造函数，从连接池中取出连接，并生成操作游标
    #     self._conn = send_date.__getConn()
    #     self._cursor = self._conn.cursor()

    @staticmethod
    def __getConn():
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
        """

        if send_date.__pool is None:
            __pool = PooledDB(creator=pymysql, mincached=1, maxcached=20,
                              host='120.77.222.224', port=3306, user='logistics', passwd='ZmEzMThiY2U5NmZh',
                              db='new_erp', use_unicode=False, charset='utf8', cursorclass=DictCursor)
        return __pool.connection()

    def update_send(self):
        '''
        更新数据的sql
        :return:
        '''
        sql = u"update erp_order_shipping set status_label ='" + self.status + u"',updated_at = '"+time.strftime("%Y-%m-%d %H:%M:%S")+u"',date_signed ='" + self.logistics_time +u"',summary_status_label = '" + self.summary_status + "'"
        sql += u" where track_number='" + self.track_n + "'"
        self._cursor.execute(sql)

    def acquire_date(self):
        '''
        获取数据的sql
        :return:
        '''
        try:

            sql =u"select status_label,summary_status_label from erp_logistics_label as a left join erp_summary_status_label as b on a.summary_status_label_id = b.id where id_shipping in"+self.shipping_id
            self._cursor.execute(sql)
            data = self._cursor.fetchall()
            return data

        except Exception , e:
            print e



    def acquire_date_id(self):
        '''
        获取shipping数据的sql
        :return:
        '''
        try:
            sql =u"select id_shipping, summary_status_label from erp_order_shipping where track_number='"+self.track_n+"'"
            self._cursor.execute(sql)
            data = self._cursor.fetchall()
            return data
        except Exception , e:
            print e


    def insert_date(self):
        '''
        插入数据的sql
        :return:
        '''
        try:
            sql = u"replace into erp_logistics_track(id_shipping,track_number,status_label,date,tran_status_label) VALUES "
            sql += u"("+self.shipping_id+",'" + self.track_n + "','" + self.status + "','" + self.logistics_time + "','" + self.tran_status_label + "')"
            self._cursor.execute(sql)
        except Exception , e:
            print e


    def insert_not_exit(self):
        
        '''
        插入数据的sql
        :return:
        '''
        try:
            sql = u"update erp_order_shipping set status_label ='" + self.status + u"',updated_at = '" + time.strftime("%Y-%m-%d %H:%M:%S") + u"',date_signed ='" + self.logistics_time + u"',summary_status_label = '" + self.summary_status + "'"
            sql += u" where track_number='" + self.track_n + "'"
            self._cursor.execute(sql)
        except Exception , e:
            print e
