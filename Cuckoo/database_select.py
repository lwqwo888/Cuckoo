#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : cat_date.py
# @Author: lwq
# @Date  : 2018/02/07
# @Desc  :192.168.105.162 old_erp old_erp123!@#

import pymysql
import sys
reload(sys)
sys.setdefaultencoding('utf-8')


class send_date:
    def __init__(self, host='120.77.222.224',user='logistics',password='ZmEzMThiY2U5NmZh',db='new_erp'):
    # def __init__(self, host='192.168.105.162', user='old_erp', password='old_erp123!@#', db='new_erp'):

        self.connection = pymysql.connect(host=host,
                                 user=user,
                                 password=password,
                                 db=db,
                                 charset='utf8',
                                 cursorclass=pymysql.cursors.DictCursor
                                 )

    def acquire_date(self):
        '''
        获取数据的sql
        :return:
        '''
        list = ["620132730391",
                "620126279496",
                "620126285280",
                "620126277446",
                "620126493191",
                "620124981334",
                "620124974193",
                "620124971344",
                "620124902270",
                "620124981966",
                "620124973212",
                "620124943672",
                "620124972992",
                "620124943942",
                "620124783970",
                "620124977196",
                "620124861285",
                "620124861263",
                "620124861061",
                "620124851396",
                "620124940924",
                "620124972255",
                "620124943874",
                "620124969550",
                "620124944186",
                "620124789976",
                "620121646160",
                "620124940272",
                "620124940235",
                "620124940224",
                "620124850395",
                "620124940171",
                "620124954472",
                "620121645653",
                "620124983722",
                "620124983700",
                "620124983452",
                "620124983362",
                "620121645473",
                "620124983055",
                "620121631666",
                "620124982945",
                "620124974950",
                "620124982912",
                "620124449842",
                "620124435350",
                "620124974834",
                "620124880773",
                "620121697043",
                "620121697574",
                "620121644955",
                "620121644933",
                "620124974441",
                "620121698373",
                "620121698474",
                "620124435721",
                "620121644753",
                "620121696356",
                "620124755502",
                "620119023196",
                "620124760213",
                "620119023163",
                "620124760171",
                "620118986346",
                "620119023104",
                "620124776182",
                "620119023062",
                "620124944004",
                "620119037554",
                "620124744671",
                "620124814452",
                "620119042131",
                "620124430385",
                "620119021146",
                "620118715512", ]
        for track_number in list:
            try:
                cur = self.connection.cursor()
                sql =u"""select status_label,date from erp_logistics_track where track_number='""" + track_number + "'" + " order by date DESC;"
                cur.execute(sql)
                # print (sql)
                data = cur.fetchall()
                self.connection.commit()
                # print track_number, data
                if data:
                    print track_number, data
                    for i in data:
                        # print i['status_label'], i['date']
                        str = "%s %s %s" % (track_number, i['date'], i['status_label'],)
                        with open("Track_Information.txt", "a") as f:
                            f.write(str + '\n')
                    with open("Track_Information.txt", "a") as f:
                        f.write('\n')
                else:
                    with open("Track_Information.txt", "a") as f:
                        # print ("******************************")
                        str1 = "%s                     <数据库中未查找到此运单信息>\n\n" % track_number
                        f.write(str1)
                        # print track_number, data

            except Exception as e:
                print (e)

        self.connection.close()
        print '已完成!!!!!!!!!!!!!!!!!!!!!!!!!!!!!'

if __name__ == '__main__':

    sd = send_date()
    sd.acquire_date()