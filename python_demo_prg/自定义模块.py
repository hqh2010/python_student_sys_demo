#!/usr/bin/python
# Filename: using_sys.py
import sys
print('The command line arguments are:')
for i in sys.argv:
 print(i)
print('\n\nThe PYTHONPATH is', sys.path, '\n')

# mymodule 为自定义模块
import mymodule
mymodule.sayhi()
print("mymodule version=", mymodule.version)
# 当你为dir()提供一个模块名的时候，它返回模块定义的名称列表。如果不提供参数，它返回当
# 前模块中定义的名称列表
# print(dir(sys))
print(dir())
print(__package__)