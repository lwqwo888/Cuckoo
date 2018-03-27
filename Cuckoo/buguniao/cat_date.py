#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : cat_date.py
# @Author: handan
# @Date  : 2017/10/19
# @Desc  :

import pymysql
import time
import datetime
class send_date:
    def __init__(self,status,logistics_time,track_n,summary_status,shipping_id,tran_status_label,host='120.77.222.224',user='logistics',password='ZmEzMThiY2U5NmZh',db='new_erp'):
        self.connection = pymysql.connect(host=host,
                                 user=user,
                                 password=password,
                                 db=db,
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor
                                 )
        self.status         = status
        self.summary_status = summary_status
        self.tran_status_label = tran_status_label
        self.logistics_time    = logistics_time
        self.track_n        = track_n
        self.shipping_id = shipping_id


    def update_send(self):
        '''
        更新数据的sql
        :return:
        '''
        cur = self.connection.cursor()
        sql = u"update erp_order_shipping set status_label ='" + self.status + u"',updated_at = '"+time.strftime("%Y-%m-%d %H:%M:%S")+u"',date_signed ='" + self.logistics_time +u"',summary_status_label = '" + self.summary_status + "'"
        sql += u" where track_number='" + self.track_n + "'"
        cur.execute(sql)
        self.connection.commit()
        self.connection.close()

    def acquire_date(self):
        '''
        获取数据的sql
        :return:
        '''
        try:
            cur = self.connection.cursor()
            sql =u"select status_label from erp_logistics_label where id_shipping in "+self.shipping_id
            cur.execute(sql)
            print (sql)
            data = cur.fetchall()
            self.connection.commit()
            self.connection.close()
            return data

        except Exception as e:
            print (e)


    def selete_delete_date(self):
        '''
        选择我们需要的数据
        :return:
        '''
        d = datetime.datetime.now()
        day60 = datetime.timedelta(days=90)
        day = d - day60
        start_time = datetime.datetime(day.year, day.month, day.day, 0, 0, 0)
        try:
            cur = self.connection.cursor()
            sql = u"select  b.id_shipping,a.track_number,a.status_label,a.date_at from erp_cat_status a "
            sql +=u"INNER JOIN erp_order_shipping b on a.track_number=b.track_number where b.created_at>= '"\
                  + start_time.strftime('%Y-%m-%d 00:00:00') + "'"
            #sql +=u"INNER JOIN erp_order_shipping b on a.track_number=b.track_number limit 2"
            #sql +="where b.created_at>= '" + start_time.strftime('%Y-%m-%d 00:00:00') + "' "
            cur.execute(sql)
            print sql
            data = cur.fetchall()
            self.connection.commit()
            self.connection.close()
            return data
        except Exception , e:
            print e

    def acquire_date_id(self):
        '''
        获取shipping数据的sql
        :return:
        '''
        try:
            cur = self.connection.cursor()
            sql =u"select id_shipping, summary_status_label from erp_order_shipping where track_number='"+self.track_n+"'"
            cur.execute(sql)
            print (sql)
            data = cur.fetchall()
            return data
        except Exception as e:
            print (e)


    def insert_date(self):
        '''
        插入数据的sql
        :return:
        '''
        try:
            cur = self.connection.cursor()
            sql = u"replace into erp_logistics_track(id_shipping,track_number,status_label,date,tran_status_label) VALUES "
            sql += u"("+self.shipping_id+",'" + self.track_n + "','" + self.status + "','" + self.logistics_time + "','" + self.tran_status_label + "')"
            cur.execute(sql)
            print (sql)
            self.connection.commit()
            self.connection.close()
        except Exception as e:
            print (e)

    def insert_date_cat(self):
        '''
        插入数据的sql
        :return:
        '''
        try:
            cur = self.connection.cursor()
            sql = u"replace into erp_cat_status(track_number,status_label,date_at) VALUES "
            sql += u"('" + self.track_n + "','" + self.status + "','" + self.logistics_time + "')"
            print sql
            cur.execute(sql)
            self.connection.commit()
            self.connection.close()
        except Exception , e:
            print e

    def insert_not_exit(self):
        
        '''
        插入数据的sql
        :return:
        '''
        try:
            cur = self.connection.cursor()
            sql = u"update erp_order_shipping set status_label ='" + self.status + u"',updated_at = '" + time.strftime("%Y-%m-%d %H:%M:%S") + u"',date_signed ='" + self.logistics_time + u"',summary_status_label = '" + self.summary_status + "'"
            sql += u" where track_number='" + self.track_n + "'"
            cur.execute(sql)
            self.connection.commit()
            self.connection.close()
        except Exception as e:
            print (e)
