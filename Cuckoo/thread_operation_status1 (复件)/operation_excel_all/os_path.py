#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @File  : os_path.py
# @Author: handan
# @Date  : 2017/9/19
# @Desc  :

import os
import re

def get_this_path(file):
    pass

def create_folder(folder_path,path_excel):
    '''
    创建文件夹
    :param folder_path:文件夹的路径
    :return:
    '''
    # 先判断文件夹是否存在
    status = is_has_folder(folder_path)

    print(status)
    if not status:
        os.makedirs(folder_path)
    else:
        if is_has_file(path_excel):
            os.unlink(path_excel)
        os.removedirs(folder_path)
        os.makedirs(folder_path)

def is_has_folder(folder_path):
    '''
    判断一个路径是不是存在一个文件夹
    :param folder_path:
    :return: True代表有这个文件夹 False代表没有
    '''
    if isinstance(folder_path, str):
        # 判断文件是否存在
        if os.path.exists(folder_path):
            if os.path.isfile(folder_path):
                print('1121122222')
                # 说明是文件不是文件夹
                return False
            else:
                # 不是文件说明是文件夹
                return True
        else:
            return False
    else:
        return False


def is_has_file(folder_path):
    '''
    判断一个路径是不是存在一个文件夹
    :param folder_path:
    :return: True代表有这个文件夹 False代表没有
    '''
    if isinstance(folder_path, str):
        # 判断文件是否存在
        if os.path.exists(folder_path):
            if os.path.isfile(folder_path):
                print('1121122222')
                # 说明是文件不是文件夹
                return True
            else:
                # 不是文件说明是文件夹
                return False
        else:
            return False
    else:
        return False