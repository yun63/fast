# coding=UTF-8

import threading


class Singleton(type):

    _instance_lock = threading.Lock()
    _instance = {}

    def __call__(cls, *args, **kwargs):
        if cls not in cls._instance:
            with Singleton._instance_lock:
                if cls not in cls._instance:
                    cls._instance[cls] = super(Singleton, cls).__call__(*args, **kwargs)
        return cls._instance[cls]



class SingletonTest(Singleton):

    __metaclass__ = Singleton

    def __init__(self):
        print('SingletonTest.init')

    def load(self):
        print('load')



if __name__ == '__main__':
    t = SingletonTest()
    t2 = SingletonTest()
    print(id(t), id(t2))
    t.load()
    t2.load()

