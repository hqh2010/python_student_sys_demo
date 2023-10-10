from threading import RLock
single_lock = RLock()

def Singleton(cls):
    instance = {}
    def _singleton_wrapper(*args, **kargs):
        with single_lock:
            if cls not in instance:
                instance[cls] = cls(*args, **kargs)
        return instance[cls]
    return _singleton_wrapper
@Singleton
class SingletonTest():
    def __init__(self, name):
        self.name = name

s1 = SingletonTest('zhangsan')
s2 = SingletonTest('lisi')
print(id(s1))
print(id(s2))