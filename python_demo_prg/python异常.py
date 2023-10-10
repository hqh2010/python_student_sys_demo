try:
    result = 20/int(input("请输入一个整数："))
    print(result)
except ValueError:
    print("必须输入整数")
except ArithmeticError as e:
    print(e)
else:
    print("没有异常")
finally:
    print("执行finally 分支")
