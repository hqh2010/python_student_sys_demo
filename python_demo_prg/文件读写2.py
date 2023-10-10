file = open('a.txt', 'r', encoding='utf-8')
result = file.read()
file.seek(0)  #读完之后要重新定位，因为read已经到文件尾了
result1 = file.readline() #读取一行
result2 = file.readline()
file.close()
print(result)
print(result1)
print(result2)

# with 自动关闭文件 不用调用close
with open('a.txt','r',encoding='utf-8') as file1:
    print(file1.read())

# 演示上下文管理的类，用于说明with自动翻译资源的原理
class MyContentMgr:
    def __enter__(self):
        print("__enter__方法被调用了")
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        print("__exit__方法被调用了")
    def show(self):
        print("show方法被调用了")

with MyContentMgr() as file2:
    file2.show()

import os
print(os.getcwd())
print(os.listdir('''../python_project'''))
print(os.path.abspath('''../python_project'''))
print(os.path.join('D:\\Python', '文件读写.py'))
print(os.path.splitext('文件读写.py'))  #拆分文件名和后缀