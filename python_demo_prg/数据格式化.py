# python格式化字符
name = '张三'
age = 20
print('我叫%s，今年%d岁'%(name, age))
print('我叫{0}，今年{1}岁'.format(name, age))
print(f'我叫{name}，今年{age}岁')
# 在f字符串中打印{}
print(f'我叫{{{name}}}，今年{age}岁')
print("%5d"%60)
print("%.3f" % 3.1415926)  #3.142
print("%10.3f" % 3.1415926)  #3.142

# python在if块中定义的变量出了if块还是可用的