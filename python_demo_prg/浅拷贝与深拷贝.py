class CPU:
    pass
class DISK:
    pass
class Computer:
    def __init__(self, cpu, disk):
        self.cpu = cpu
        self.disk = disk
cpu1 = CPU()
cpu2 = cpu1
# 演示浅拷贝 cpu1和cpu2实际指向的是同一个对象
print(cpu1, id(cpu1))
print(cpu2, id(cpu2))

disk = DISK()
computer = Computer(cpu1,disk)
# 浅拷贝 子对象的地址没有变化
import copy
computer2 = copy.copy(computer)
print(computer, computer.cpu, computer.disk)
print(computer2, computer2.cpu, computer2.disk)
# 深拷贝 会递归拷贝目标对象的子对象
computer3 = copy.deepcopy(computer)
print(computer3, computer3.cpu, computer3.disk)

# 导入模块的方式
# import 模块名称 as 别名
# from 模块名称 import 函数/变量/类
import math
print(id(math))
print(type(math))
print(math)

print(math.pi)
print('-------------------------------')
print(dir(math))
