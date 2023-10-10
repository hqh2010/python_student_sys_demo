class Student:
    def __init__(self, name, age):
        self.name = name
        self.__age = age  #以两个下划线开始的属性为私有属性，在类的外部无法使用，但是类的方法中可以使用
    def showinfo(self):
        print("学生的姓名为：" + self.name + ",年龄：", self.__age)

stu1 = Student("张三", 35)
stu1.showinfo()
# print(stu1.__age) # __开头的实例属性在类的外部无法使用