class D:
    def __init__(self, name, func):
        self.name = name
        self.func = func
    def __del__(self):
        self.func(self)

def outer():
    x = 0
    # y=None 不能写成y
    def inner(y=None):
        nonlocal x
        if y:
            x = y
        else:
            return x
    return inner

f = outer()
e = D("小甲鱼", f)
print(e.name)
del e
# 销毁e
# print(e)
g = f()
print(g.name)

# 演示类的私有属性
class Person:
    def __init__(self, name, age):
        self.name = name
        self.__age= age

p = Person('小明', 18)
print(p.name)
print(getattr(p, "name"))
# 直接访问会报错
# print(p.__age)
print(p.__dict__)
print(p._Person__age)
print(getattr(p, "_Person__age"))