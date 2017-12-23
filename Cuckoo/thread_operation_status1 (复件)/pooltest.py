# coding=utf-8
import requests
from multiprocessing.dummy import Pool
import gevent
from gevent import monkey
# gevent 让我们可以用同步的逻辑，来写异步的程序。
# monkey.patch_all() 在Python程序执行的时候，会动态的将底层的网络库（socket，select）打个补丁，变成异步的库。
# 让程序在执行网络操作的时候，按异步的方式去执行。
monkey.patch_all()
import sys
reload(sys)
sys.setdefaultencoding('utf-8')



file_object = open("ceshi.txt")
try:
    all_txt = file_object.read()
    print all_txt
finally:
    file_object.close()

def add(all_txt):
    with open("xieru.txt","a") as f:
        f.write(all_txt)

if __name__ == '__main__':
    # pool = Pool(5)
    # pool.map(add,all_txt)
    # pool.close()
    # pool.join()
    job_list = []
    for i in range(10):
        # 创建协程任务并执行
        job = gevent.spawn(add,all_txt)
        job_list.append(job)
    gevent.joinall(job_list)
