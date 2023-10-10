import time
def timecost(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        res = func(*args, **kwargs)
        stop_time = time.time()
        print(f"{func.__name__} run time is {stop_time - start_time}")
        return res
    return wrapper

@timecost
def index():
    time.sleep(1)
    print('welcome to the index page')
    return 200
# 调用 index() 函数时，会自动将其转换成 timecost(index)() 这样的形式，将 index 函数作为参数传递给 timecost() 函数，
# 并将返回值再次作为函数调用。由于 timecost() 函数返回了一个闭包函数 wrapper()，所以最终的函数调用结果就是执行了闭包函数 wrapper()
ret = index()
# 打印得到的返回值
print(ret)

# 类装饰器就是使用类来实现的装饰器。它们通常通过在类中定义 __call__ 方法来实现。当我们使用 @ 语法应用装饰器时，
# Python 会调用装饰器类的 __init__ 方法创建一个实例，然后将被装饰的函数或类作为参数传递给 __init__ 方法。
# 当被装饰的函数或方法被调用时，Python 会调用装饰器实例的 __call__ 方法。

class TimeCostDecorator:
    def __init__(self, func):
        print("TimeCostDecorator __init__ called")
        self.func = func
    def __call__(self, *args, **kwargs):
        start_time = time.time()
        result = self.func(*args, **kwargs)
        end_time = time.time()
        print(f"Function {self.func.__name__} took {end_time - start_time} seconds to run.")
        return result

@TimeCostDecorator
def slow_function():
    time.sleep(2)
    return 300

ret = slow_function()   # 相当于TimeCostDecorator(slow_function)
print(ret)