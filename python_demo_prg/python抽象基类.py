from abc import ABC, abstractmethod

class Animal(ABC):
    @abstractmethod
    def eat(self):
        pass

    @abstractmethod
    def voice(self):
        pass

class Dog(Animal):
    pass


if __name__ == "__main__":
    # dog 没有实现抽象方法 所以实例化的时候会报错
    d = Dog()
    print('a dog comes...')
