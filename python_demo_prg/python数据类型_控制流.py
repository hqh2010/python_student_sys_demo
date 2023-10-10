# python基本数据类型
a = 11
a1 = 0b1011  # 0b开头的表示二进制数
b = 'hello'
b1 = "world"
# 三引号可以表示可换行的字符串
b2 = """
可以换行的字符串
python
"""
print(b2)
b3 = r"hello\nworld"  # r表示原字符串，相当于给所有的特殊字符自动加了转义
print(b3)
b4 = u"This is a Unicode string."  # u表示unicode字符串
print(b4)
c = 1.73
c1 = 3.14e2  # 科学计数法表示浮点数
d = False
e = 3 - 91j
e1 = complex(3, -91)  # python支持复数类型
print(type(a), type(b), type(b1), type(c), type(d), type(e), "浮点数的id:", id(c))  # 演示python基本数据类型

# python运算符
print(2 ** 4)  # 演示乘方运算符 幂运算符优先级是最高的
print(11 // 3)  # //表示整除
print(11 % 3)  # //表示取模
print(type(e1));
print(c1)  # 默认情况下一个物理行写一条语句，如果写多行，请使用;分隔
s = 'This is a string. \
This continues the string.'
print(s)
# 逻辑运算符
f1 = 3
print(not f1)

# 控制流 if for while
i = 0
while i <= 5:
    print(i)
    i = i + 1
str = input("请输入一个整数：")
if int(str) == 1:  # if 后面的冒号不能少
    print("您输入的是1")
else:
    print("您输入的不是1")
for j in range(1, 5):
    if j == 3:
        break
    print(j)
