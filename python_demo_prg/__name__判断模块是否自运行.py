#!/usr/bin/python
# 通过模块的__name__来判断模块是自运行还是被其它模块调用
print(f"模块被运行了{__name__}")
if __name__ == '__main__':
 print('This program is being run by itself')
else:
 print('I am being imported from another module')