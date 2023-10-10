#!/usr/bin/python

# 自定义一个函数
def sayHello(x):
    print("hello:" + x)

sayHello("liming")

def printMax(a, b):
 if a > b:
    print(a, 'is maximum')
 else:
    print(b, 'is maximum')
printMax(8, 7)

# global 关键字用来在函数中声明全局变量
def func_test():
    global x
    print("x =", x)
    x = 2
    print("change x to ", x)
x = 50
func_test()
print("after call func_test x = ", x)
# 带默认参数的函数
def say(message, times=1):
    print(message*times)
say("hello", 3)

# 如果你的某个函数有许多参数，而你只想指定其中的一部分，那么你可以通过命名来为这些参
# 数赋值——这被称作关键参数

def func_test2(a, b=5, c=10):
    print("a = ", a,",b = ", b, ", c = ",c)
func_test2(c=50, a = 40)
func_test2(25, c =24)

# 函数下面的字符串为文档字符串，可以显示函数的类的帮助信息 __doc__
# __doc__ 注释要放在函数定义的下面，不然无法显示
def printMax1(x, y):
    '''Prints the maximum of two numbers.
    The two values must be integers.'''
    x = int(x) # convert to integers, if possible
    y = int(y)
    if x > y:
        print(x, 'is maximum')
    else:
        print(y, 'is maximum')
printMax1(5, 9)
print(printMax1.__name__)
print(printMax1.__doc__)

from decimal import Decimal
# python浮点数的计算不准确 需要使用Decimal模块
nums=[1.1,1.2,0.3,0.4]
result = sum(nums)
print("result is :", result)

result1= sum([Decimal(str(i)) for i in nums])
print("result1 is :", result1)
help(printMax1)

# 函数类型注释
def test(s:list[int], c:dict[str,int], b:int = 3):
    pass
print(test.__annotations__)