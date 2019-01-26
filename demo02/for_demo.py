#!/usr/bin/env python
# -*- coding: UTF-8 -*-

s = "my python"
for a in s:
    print a,
else:
    print

fruits = ['banana', 'apple', 'mango']
for index in range(len(fruits)):
    print '当前水果 :', fruits[index]

print "Good bye!"

fruits = ['banana', 'apple', 'mango']
for fruit in fruits:  # 第二个实例
    print '当前水果 :', fruit

print range(5)
print "Good bye!"

for num in range(10, 20):  # 迭代 10 到 20 之间的数字
    for i in range(2, num):  # 根据因子迭代
        if num % i == 0:  # 确定第一个因子
            j = num / i  # 计算第二个因子
            print '%d 等于 %d * %d' % (num, i, j)
            break  # 跳出当前循环
    else:  # 循环的 else 部分
        print num, '是一个质数'

sequence = [12, 34, 34, 23, 45, 76, 89]
for i, j in enumerate(sequence):
    print i, j

print "My name is %s and weight is %d kg!" % ('Zara', 21)
