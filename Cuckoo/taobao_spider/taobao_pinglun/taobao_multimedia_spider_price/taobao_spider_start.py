# coding=utf-8
# version: 1.1
# 脚本功能: 淘宝商品数据获取程序启动器
# 参数: taobaourl.txt (存放所需获取的淘宝商品链接,每行只能存放一个商品链接,例子如下)
# 例: https://item.taobao.com/item.htm?id=545146161124
# date : 2018-02-11
# Creator: lwq

import re
import time
import copy
from collections import Counter
from taobao_info_entrance import Product_Parameters
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


# 链接去重
def go_repeat():
    with open('taobaourl.txt', 'rb') as f:
        lines = f.readlines()
        new_lines = copy.deepcopy(lines)
    print '去重前--------------------------------------------'
    print len(lines)
    print '------------------------------------------------------'

    url_list = []
    for line in lines:
        id = url_process(line)
        url_list.append(id)

    c = Counter()
    for ch in url_list:
        c[ch] = c[ch] + 1

    max_list = []
    repeat_dict = {}
    for k, v in c.items():
        if v > 1:
            repeat_dict[k] = v
            max_list.append(k)

    length = len(max_list)

    print '共有%s个id重复, 如需查看重复ID请打开"重复商品ID.txt"' % length
    for repeat_id in repeat_dict:
        with open('重复商品ID.txt', 'a') as f:
            f.write(repeat_id + " ID出现次数: " + str(repeat_dict[repeat_id]) + '\n')

    i = 0
    # 用来存放重复的索引的列表
    repeat_index_list = []
    while i < length:
        key = max_list[i]
        value_num = repeat_dict[key]
        lines_length = len(lines)
        j = 0
        while j < lines_length:
            if key in lines[j]:
                if value_num > 1:
                    repeat_index_list.append(j)
                    value_num -= 1
            j += 1
        i += 1

    # 翻转列表,从后往前删
    new_repeat_index_list = list(reversed(repeat_index_list))
    for i in new_repeat_index_list:
        new_lines.pop(i)
    print '去重后--------------------------------------------'

    print len(new_lines)
    for j in new_lines:
        with open('淘宝商品.txt', 'a') as f:
            f.write(j)
    print '---------------------------------------------------'
    return new_lines


def url_process(url):
    res = re.compile(r'(\?|&)id=(\d+).*?', re.S)
    id = res.search(url).group(2)
    return ''.join(id)

if __name__ == '__main__':
    start = time.time()
    pp = Product_Parameters()

    start = time.time()
    new_lines = go_repeat()
    new_length = len(new_lines)
    i = 0
    while i < new_length:
        line = new_lines[i]
        id = url_process(line)
        # id = "546019442312"

        print "[INFO]:开始抓取...................................."
        with open("Schedule.txt", 'a') as f:
            f.write("[INFO]:开始抓取....%s - %s\n" % (id, time.ctime()))

        pp.property_count(id)
        with open("Schedule.txt", 'a') as f:
            f.write("[INFO]: %s 商品信息执行完成! - %s\n" % (id, time.ctime()))
        time.sleep(0.4)

        i += 1
        print "[INFO]:第%s件商品 已完成抓取!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!\n\n" % str(i)


    end = time.time()
    time_s = end-start
    print "[INFO]:所有抓取任务已完成！共计用时%s秒\n\n" % time_s

