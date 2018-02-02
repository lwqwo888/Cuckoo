# coding=utf-8
import os
import re
import time
import requests
from collections import Counter
from multiprocessing import Pool
from taobao_img_spider import Taobao_Img
from taobao_videos_spider import Taobao_Videos
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def go_heavy():
    with open('taobaourl.txt', 'rb') as f:
        lines = f.readlines()
        new_lines = lines
    print '删除前--------------------------------------------'
    print lines
    print len(lines)
    print '------------------------------------------------------'

    url_list = []
    for line in lines:
        dir_name_list = line.split("*")
        category_name = dir_name_list[1]
        dir_name = dir_name_list[2]
        # print category_name
        # print dir_name
        id = url_process(line)
        url_list.append(id)

    c = Counter()
    for ch in url_list:
        c[ch] = c[ch] + 1
    count_list = list(c.values())
    print count_list
    # max_value = max(count_list)
    # print max_value
    max_list = []
    repeat_dict = {}
    for k, v in c.items():
        if v > 1:
            repeat_dict[k] = v
            max_list.append(k)
    # max_list = sorted(max_list)
    length = len(max_list)
    print max_list
    print repeat_dict
    print '共有%s个id重复,分别是:' % length
    i = 0
    index_list = []
    # length = 6
    while i < length:
        key = max_list[i]
        value_num = repeat_dict[key]
        lines_length = len(lines)
        print '----------', lines_length
        j = 0
        while j < lines_length:
            print '**************',lines[j]
            if key in lines[j]:
                if value_num > 1:
                    index_list.append(j)
                    # new_lines.pop(j)
                    # del new_lines[j]
                    value_num -= 1
                    # repeat_dict[key] = value_num
            j += 1
        i += 1

    print index_list
    b = list(reversed(index_list))
    for i in b:
        new_lines.pop(i)
    print '删除后--------------------------------------------'
    print new_lines
    print len(new_lines)
    print '---------------------------------------------------'
    print lines
    print len(lines)
    # url_list_length = len(url_list)
    # print "去重前url数量:%s" % url_list_length
    # news_img_url_list = list(set(url_list))
    # news_img_url_list.sort()
    # new_length = len(news_img_url_list)
    # print '去重后url数量:', new_length
    # return news_img_url_list, category_name, dir_name

def url_process(url):
    res = re.compile(r'(\?|&)id=(\d+).*?', re.S)
    id = res.search(url).group(2)
    # print id
    return ''.join(id)

if __name__ == '__main__':
    start = time.time()
    ti = Taobao_Img()
    tv = Taobao_Videos()
    start = time.time()
    news_img_url_list = go_heavy()

    # category_name = go_heavy()[1]
    # dir_name = go_heavy()[2]
    # new_length = len(news_img_url_list)
    # i = 0
    # while i < new_length:
    #     id = news_img_url_list[i]
    #     # id = "546019442312"
    #     # ti.page_data(id)
    #     # ti.turn_img(id, category_name, dir_name)
    #     # ti.color_img(id, category_name, dir_name)
    #     # ti.detail_img(id, category_name, dir_name)
    #     print "%s商品所有图片抓取完成！！！！！！！！\n" % id
    #     # tv.video(id, category_name, dir_name)
    #     i += 1
    #     print "第%s件商品 已完成抓取!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n" % str(i)


    end = time.time()
    time_s = end-start
    print "所有抓取任务已完成！共计用时%s秒\n\n" % time_s




    # for line in lines:
    #     id = ti.url_process(line)
    #     ti.page_data(id)
    #     ti.turn_img(id)
    #     ti.color_img(id)
    #     ti.detail_img(id)
    #     print "%s商品所有图片抓取完成！！！！！！！！\n\n" % id
    #     tv.video(id)
