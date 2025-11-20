class Singleton1:
    _instance = None
    
    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls, *args, **kwargs) # Send __new__ to Object
        
        return cls._instance

obj1 = Singleton1()
obj2 = Singleton1()

print(obj1, obj2, obj1 is obj2, sep='\n')

# just one class may exist like a singleton


class SingletonMeta(type):
    _instances = None
    
    def __call__(cls, *args, **kwargs):
        if SingletonMeta._instances is None:
            SingletonMeta._instances = super(SingletonMeta, cls).__call__(*args, **kwargs)
        
        return SingletonMeta._instances


class MySingleton(metaclass=SingletonMeta):
    ...


obj3 = MySingleton()
obj4 = MySingleton()

print(obj3, obj4, obj3 is obj4, sep='\n')


def singleton(cls):
    _instance = None
    
    def _singleton(*args, **kwargs):
        nonlocal _instance

        if _instance is None:
            _instance = cls(*args, **kwargs)
        
        return _instance
    
    return _singleton

@singleton
class SingletonWithDecorator:
    ...


obj5 = SingletonWithDecorator()
obj6 = SingletonWithDecorator()

print(obj5, obj6, obj5 is obj6, sep='\n')

