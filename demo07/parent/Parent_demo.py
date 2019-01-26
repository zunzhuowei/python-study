#!/usr/bin/python
# -*- coding: UTF-8 -*-

class Parent:
    parentAttr = 100

    def __init__(self):
        print "调用父类构造方法"

    def parentMethod(self):
        print "调用父类方法"

    def setAttr(self, attr):
        self.parentAttr = attr

    def getAttr(self):
        return self.parentAttr


class Child(Parent):  # 定义子类

    def __init__(self):
        print "调用子类构造方法"

    def childMethod(self):
        print '调用子类方法 child method'


c = Child()  # 实例化子类
c.childMethod()  # 调用子类的方法
c.parentMethod()  # 调用父类方法
c.setAttr(200)  # 再次调用父类的方法
print c.getAttr()  # 再次调用父类的方法