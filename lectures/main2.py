from abc import ABC, abstractmethod
import math
from dataclasses import dataclass


@dataclass(frozen=True)
class Point:
    x: int
    y: int


class Figure(ABC):
    @property
    @abstractmethod
    def area(self) -> float:
        pass

    @property
    @abstractmethod
    def perimeter(self) -> float:
        pass


class Circle(Figure):
    def __init__(self, radius: float, center: Point) -> None:
        self.radius = radius
        self.center = center

    @property
    def area(self) -> float:
        return math.pi * self.radius * self.radius

    @property
    def perimeter(self) -> float:
        return 2 * math.pi * self.radius


class Rectangle(Figure):
    def __init__(self, top_left: Point, widht: float, height: float) -> None:
        self.top_left = top_left
        self.width = widht
        self.height = height

    @property
    def area(self) -> float:
        return self.width * self.height

    @property
    def perimeter(self) -> float:
        return 2 * (self.width + self.height)

# figure = Figure()
circle = Circle(10, Point(10, 20))
rectangle = Rectangle(Point(10, 20), 30, 30)

figures: list[Figure] = [circle, rectangle]

for figure in figures:
    print(figure.area)
