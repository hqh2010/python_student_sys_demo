# 演示类的继承
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
    def info(self):
        print("姓名:{0},年龄:{1}".format(self.name, self.age))

class Student(Person):  #python还支持多继承
    def __init__(self, name, age, stu_no):
        super().__init__(name,age)
        self.stu_no = stu_no
    '''
    重写父类的方法
    '''
    def info(self):
        super().info();
        print(self.stu_no)
class Teacher(Person):
    def __init__(self,name,age, teachofyear):
        super().__init__(name,age)
        self.teachofyear = teachofyear

stu = Student('张三', 20, '10010')
tea = Teacher('李老师', 40, 10)
stu.info()
tea.info()

# 演示python的多态
class Animal(object):
    def eat(self):
        print('动物会吃')
class Dog(Animal):
    def eat(self):
        print("狗吃骨头...")
class Cat(Animal):
    def eat(self):
        print("猫吃鱼刺...")
class Human:
    def eat(self):
        print("人吃五谷杂粮...")

def func(obj):
    obj.eat()
func(Dog())
func(Cat())

func(Human())