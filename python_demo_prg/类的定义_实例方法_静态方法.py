class Person:
    age = 18 #类的属性
    def __init__(self, name):
        # 实例属性
        self.name = name
    def sayHi(self):  #实例方法
        print("hello, how are you " + self.name)
    def eat(self):
        print(self.name + "吃饭了")
    @staticmethod
    def staticmethod(something):
        print("我是类的静态方法" + something)   #演示类的静态方法
    @classmethod
    def classmethod(cls):
        print("我是类的类方法")   #演示类的静态方法
p = Person("张三")
p1 = Person("李四")
p.sayHi()
p1.sayHi()
p1.eat()
# 演示另外一种实例调用方法
Person.eat(p)
# 类属性是所有的实例对象共同所有的
print(p.age)
print(p1.age)
Person.staticmethod("bbb")
Person.classmethod()
p.staticmethod("aaa")

# 下面演示实例对象属性与方法的动态绑定
p1.area = "天津"   #给对象p1增加area属性
print(p1.area)
# print(p.area)  # 实例对象p并没有area属性
def showarea(area):
    print("这是一个显示地区的函数，地区为：" + area)
#给实例对象绑定方法
p1.show = showarea
p1.show(p1.area)



