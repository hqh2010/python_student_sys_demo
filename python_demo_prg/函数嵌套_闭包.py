import time

# 闭包是能够读取外部函数内部变量的函数
# 作用1：闭包是将外层函数内的局部变量和外层函数的外部连接起来的一座桥梁
# 作用2：拓宽外部函数的局部变量的作用域
def logger(msg):
    def time_master(func):
        def call_func():
            start = time.time()
            func()
            stop = time.time()
            print(f'{msg}一共耗费了{(stop-start):.2f}')
        return call_func
    return time_master

def funA():
    time.sleep(1)
    print('正在调用funA...')

def funB():
    time.sleep(2)
    print('正在调用funB...')

fun1 = logger(msg='A')(funA)
fun2 = logger(msg='B')(funB)
fun1()
fun2()

# lambda表达式
# lambda arg1, arg2, arg3, ... argN: expression

def squareX(x):
    return x * x
print(squareX(3))

print('使用lambda表达式求值')
squareY = lambda y:y*y
print(squareY(3))
print(squareY)

# lambda可以作为参数
