#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : cat_data_base.py
# @Author: handan
# @Date  : 2017/12/20
# @Desc  :
import pymysql
from pymysql.cursors import DictCursor
from DBUtils.PooledDB import PooledDB


from config import  DB_HOST_FINAL2, DB_NAME_FINAL2, DB_USER_FINAL2, DB_PWD_FINAL2


class Db_base(object):
    # def __init__(self, host=DB_HOST,user=DB_USER,password=DB_PWD,db=DB_NAME):
    #     self.connection = pymysql.connect(host=host,
    #                                       user=user,
    #                                       password=password,
    #                                       db=db,
    #                                       charset=DB_charset,
    #                                       cursorclass=pymysql.cursors.DictCursor
    #                                       )

    def __init__(self):
        self._conn = Db_base.__getConn()
        # print self._conn
        self._cursor = self._conn.cursor()
        # print self._cursor
        # self._commit = self._conn.commit()

    # 连接池对象
    __pool = None

    # def __init__(self):
    # 数据库构造函数，从连接池中取出连接，并生成操作游标
    #     self._conn = send_date.__getConn()
    #     self._cursor = self._conn.cursor()

    @staticmethod
    def __getConn():
        """
        @summary: 静态方法，从连接池中取出连接
        @return MySQLdb.connection
        """

        if Db_base.__pool is None:
            __pool = PooledDB(creator=pymysql, mincached=1, maxcached=100,
                              host=DB_HOST_FINAL2, port=3306, user=DB_USER_FINAL2, passwd=DB_PWD_FINAL2,
                              db=DB_NAME_FINAL2, use_unicode=False, charset='utf8', cursorclass=DictCursor)
        return __pool.connection()

    def execute(self, sql):
        """
        执行sql
        :param sql:
        :return:
        """
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(sql)
            self.connection.commit()
        except Exception as e:
            self.connection.rollback()


    def close(self):
        self.connection.close()

