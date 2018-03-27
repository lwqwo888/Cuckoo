#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : start.py
# @Author: handan
# @Date  : 2017/11/24
# @Desc  :

import os
import re
import time
import log


# 启动日志
log.start_log(file_path="task")
log.logging.info('[INFO Start Time Task.]')

PYTHONPATH = "python"
# 定时任务几点执行
RUN_TIME = 0
# 多少秒检查一次是否到指定的时间
SLEEP_TIME = 1800

def execCmd(cmd):
    r = os.popen(cmd)
    text = r.read()
    r.close()
    return text

while True:
    print 'okkkkkkkkkkkkk'
    sys_ps = execCmd('ps -ef | grep python')
    log.logging.info("[INFO] System Process: ")
    log.logging.info(sys_ps)
    current_time   = time.localtime(time.time())
    this_time_hour = current_time.tm_hour

    # 检查博加图思密达终极扛把子有没有执行
    times_final         = re.search(r'sync_taiguo2_final2\.py', sys_ps)
    # 检查香港CXC-》 X系列终极版有没有执行
    xiangg_cxc_final    = re.search(r'xianggang_cxc_final\.py', sys_ps)
    # 检查沙特终极版-》脚本战斗机有没有执行
    Arame_final         = re.search(r'Aramex_final\.py', sys_ps)
    # 检查印尼终极版-》脚本战斗机有没有执行
    yinni_final = re.search(r'sync_yinni_final\.py', sys_ps)

    # 检查times终极版-》脚本战斗机有没有执行
    time_final = re.search(r'taiguo_api2_final\.py', sys_ps)
    # 检查天马弼马温终极版脚本有没有执行
    sync_youz_final     = re.search(r'sync_youzheng_final\.py', sys_ps)

    if RUN_TIME <= this_time_hour <= (RUN_TIME + 1):

        if not times_final:
            log.logging.info('[INFO] Run start_web')
            os.popen("{0} sync_taiguo2_final2.py -d new_erp -u logistics -p ZmEzMThiY2U5NmZh -r normal &".format(PYTHONPATH))

        if not xiangg_cxc_final:
            log.logging.info('[INFO] Run start_web')
            os.popen("{0} xiangg_cxc_final.py -d new_erp -u logistics -p ZmEzMThiY2U5NmZh -r normal &".format(PYTHONPATH))

        if not Arame_final:
            log.logging.info('[INFO] Run start_web')
            os.popen("{0} Aramex_final.py -d new_erp -u logistics -p ZmEzMThiY2U5NmZh -r normal &".format(PYTHONPATH))

        if not sync_youz_final:
            log.logging.info('[INFO] Run start_web')
            os.popen("{0} sync_youzheng_final.py -d new_erp -u logistics -p ZmEzMThiY2U5NmZh -r normal &".format(PYTHONPATH))

        if not time_final:
            log.logging.info('[INFO] Run start_web')
            os.popen("{0} taiguo_api2_final.py -d new_erp -u logistics -p ZmEzMThiY2U5NmZh -r normal &".format(PYTHONPATH))

        if not yinni_final:
            log.logging.info('[INFO] Run start_web')
            os.popen("{0} sync_yinni_final.py -d new_erp -u logistics -p ZmEzMThiY2U5NmZh -r normal &".format(PYTHONPATH))


    log.logging.info('[INFO] SLEEP {0}'.format(SLEEP_TIME))
    time.sleep(SLEEP_TIME)

