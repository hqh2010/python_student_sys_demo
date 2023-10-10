num=int(input('请输入一个十进制数：'))
print(num, '对应的十进制数为:', bin(num))
print(f'{num}对应的八进制数为:{oct(num)}')
print('{0}对应的八进制数为:{1}'.format(num, hex(num)))
money=8
print('当前的余额为:\033[0:35m', money,'元\033[m')

# 收集参数 可变参数 参数要带*
def myfunc(*args):
    print("有{}个参数".format(len(args)))
    print('第二个参数是：{0}'.format(args[1]))
    print(args)
    print(type(args))

myfunc('参数1','参数二')

# 利用元组，函数可以返回多个参数
def myfunc1():
    return 1,2,3
print(type(myfunc1()))
x,y,z = myfunc1()
print(x,y,z)

# 关键字参数 带2个*的参数 打包成字典
def myfunc2(**kwargs):
    print(type(kwargs))
    print(kwargs)
myfunc2(key1=1, key2='b')

#元组的解包

def myfunc3(a,b,c,d):
    print(a,b,c,d)
args1 = (1,2,3,4) # 定义一个元组
myfunc3(*args1)  #元组解包
kwargs1 = {'a':1, 'b':2, 'c':3, 'd':4}
myfunc3(**kwargs1) #字典解包

# 函数嵌套
def funA():
    x = 520
    def funB():
        # nonlocal x
        x = 880
        print('In funB, x=', x)
    funB()
    print('In funA, x=', x)
funA()  # 如何调用funB呢？？？？


def funC():
    x = 520
    def funD():
        # nonlocal x
        # x = 880
        print('In funB, x=', x)
    return funD
print('==================================')
funC()()
# 通过funD 拓宽了x的作用域
funny = funC()
funny()