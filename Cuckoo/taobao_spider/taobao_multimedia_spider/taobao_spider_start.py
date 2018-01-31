# coding=utf-8
import os
import re
import time
import requests
from multiprocessing import Pool
from taobao_img_spider import Taobao_Img
from taobao_videos_spider import Taobao_Videos
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


if __name__ == '__main__':
    start = time.time()
    ti = Taobao_Img()
    tv = Taobao_Videos()
    with open('taobaourl.txt', 'rb') as f:
        lines = f.readlines()
    for line in lines:
        id = ti.url_process(line)
        ti.page_data(id)
        ti.turn_img(id)
        ti.color_img(id)
        ti.detail_img(id)
        print "%s商品所有图片抓取完成！！！！！！！！\n\n" % id
        tv.video(id)

    end = time.time()
    time_s = end-start
    print "所有抓取任务已完成！共计用时%s秒\n\n" % time_s
