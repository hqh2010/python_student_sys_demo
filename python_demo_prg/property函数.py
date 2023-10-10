class Student():
    def __init__(self):
        self.age = 0

    def getx(self):
        return self.age

    def setx(self, value):
        self.age = value

    def delx(self):
        del self.age

    x = property(getx, setx, delx, "I'm the 'x' property.")

stu = Student()
print(stu.age)
stu.x = 20
print(stu.age)

# https://www.runoob.com/python/python-func-property.html
# property 可以创建类的属性的别名，且可以很方便的创建一个只读属性
class Parrot(object):
    def __init__(self):
        self._voltage = 100000
    @property
    def voltage(self):
        """Get the current voltage."""
        return self._voltage

P1 = Parrot()
print(P1.voltage)
P1.voltage = 60  #P1._voltage是可以改的
print(P1.voltage)
