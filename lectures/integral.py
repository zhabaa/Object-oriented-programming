from abc import ABC, abstractmethod
from typing import Callable
import math
import numpy as np

class Calcer(ABC):
    # def __init__(self, a: float, b: float):
    #     self.a = a
    #     self.b = b

    @abstractmethod
    def calc(self, f: Callable[[float], float], a: float, b: float) -> float:
        pass


class ZeroCalcer(Calcer):
    def calc(self, f: Callable[[float], float], a: float, b: float) -> float:
        return 0.0


class OneCalcer(Calcer):
    def calc(self, f: Callable[[float], float], a: float, b: float) -> float:
        return 1.0


class RectangleCalcer(Calcer):
    def __init__(self, n_points: int):
        self.n_points = n_points
    
    def calc(self, f: Callable, a, b):
        return 2.
        
# f: Callable[[float, float], float]
# Первый вргкмент - переменные, приминаемые функцией
# Второй - возвращаемое значение

calcer0 = ZeroCalcer()
calcer1 = OneCalcer()
print(calcer0.calc(lambda x: x**5, a=0, b=1))
print(calcer1.calc(lambda x: math.sin(x), a=0, b=1))
