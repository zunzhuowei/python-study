#!/usr/bin/python
# -*- coding: UTF-8 -*-

def read(file_name, access_mode="wb", buffering=0):
    fo = open(file_name, access_mode)
    print "文件名: ", fo.name
    print "是否已关闭 : ", fo.closed
    print "访问模式 : ", fo.mode
    print "末尾是否强制加空格 : ", fo.softspace
    fo.close()


def write(file_name, access_mode="wb", buffering=0):
    fo = open(file_name, access_mode)
    fo.write("中国人民八一建军节人\n民快乐，123")
    fo.close()

def read2(file_name, access_mode="r+", buffering=0):
    # 打开一个文件
    fo = open(file_name, access_mode)
    str = fo.readline()
    print "读取的字符串是 : ", str
    # 关闭打开的文件
    fo.close()
