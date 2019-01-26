#!/usr/bin/python
# -*- coding: UTF-8 -*-
from collections import Iterable

print(1, list(range(0, 100, 2)))
print 2, range(0, 100)
print 3, range(100)
print(4, list(range(0, 100, 2))[0:25])  # 切片
print(5, list(range(0, 100, 2))[:])  # 甚至什么都不写，只写[:]就可以原样复制一个list：
print(6, tuple(list(range(0, 100, 2)))[:3])  # tuple也是一种list，唯一区别是tuple不可变。因此，tuple也可以用切片操作，只是操作的结果仍是tuple：

print '字符串\'xxx\'也可以看成是一种list，每个元素就是一个字符。因此，字符串也可以用切片操作，只是操作结果仍是字符串：'
print 'ABCDEFG'[:3]
print 'ABCDEFG'[::2]
print
for i, value in enumerate(['A', 'B', 'C']):
    print(i, value)
print
for x, y in [(1, 1), (2, 4), (3, 9)]:
    print(x, y)
print
print isinstance('abc', Iterable)
print
for i, value in enumerate(['A', 'B', 'C']):  # 获取下标的方式
    print(i, value)

print '写列表生成式时，把要生成的元素x * x放到前面，后面跟for循环，就可以把list创建出来，十分有用，多写几次，很快就可以熟悉这种语法。'
print [x * x for x in range(1, 11)]  # 但是循环太繁琐，而列表生成式则可以用一行语句代替循环生成上面的list：

print 'for循环后面还可以加上if判断，这样我们就可以筛选出仅偶数的平方：'
print [x * x for x in range(1, 11) if x % 2 == 0]

print '还可以使用两层循环，可以生成全排列：'
print [m + n for m in 'ABC' for n in 'XYZ']
var1 = [m + n for m in 'ABC' for n in 'XYZ']
print var1[-2:-1]

L1 = ['Hello', 'World', 18, 'Apple', None]
L2 = []
for l in L1:
    if isinstance(l,str):
        L2.append(l)
print L2

print
g = (x * x for x in range(10))
for n in g:
    print(n)
print

def f(x):
    return x * x

r = map(f, [1, 2, 3, 4, 5, 6, 7, 8, 9])
print r

print list(map(str, [1, 2, 3, 4, 5, 6, 7, 8, 9]))

print ''' filter 的用法 '''
def not_empty(s):
    return s and s.strip()

print list(filter(not_empty, ['A', '', 'B', None, 'C', '  ']))

def is_odd(n):
    return n % 2 == 1

list(filter(is_odd, [1, 2, 4, 5, 6, 9, 10, 15]))

def lazy_sum(*args):
    def sum():
        ax = 0
        for n in args:
            ax = ax + n
        return ax
    return sum

a = lazy_sum(1,2,3)
print a()
