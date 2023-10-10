# python中的包
# 包是一个分层次的目录结构，它将一组功能相近的模块组织在一个目录
# 作用：
# 代码规范
# 避免模块名称冲突
#
# 包与目录的区别
# 包含__init__.py文件的目录称为包
# 目录通常不包含__init__.py文件
#
# 包的导入
# import 包名.模块名

# import 模块名称 as 别名
# from 模块名称 import 函数/变量/类

# import mypackage.module_a
# print(mypackage.module_a.a)
import mypackage.module_a as m_a
print(m_a.a)