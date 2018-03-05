#!/usr/bin/env python
# -*- coding:utf-8 -*-
# __author__ = 'guojie'

import os
import time

workpath = 'data'


def root_path(path):
    if not os.path.exists(path):
        os.makedirs(path)
    return path


def time_file():
    # 返回正常时间
    now = time.strftime("%Y_%m_%d", time.localtime())
    return now


def file_name():
    name = time.strftime("%H_%M_%S", time.localtime())
    return name


def DataStoreFile(path, file_body, pcname):
    """

    :param path: sysinfo
    :param file_body: json
    :param pcname: dict_name
    :return:创建文件，写入json数据
    """
    now = time_file()
    # 时分秒-dictname.json
    name = file_name() + '_' + pcname + '.json'
    # 如果不存在，创建data/年月日/sysinfo
    rootpath = root_path(workpath + '/' + now + '/' + path)
    with open(rootpath + '/' + name, 'a') as f:
        f.write(file_body)
    return


if __name__ == '__main__':
    DataStoreFile('sysinfo', '123', 'guojie.jsac')
