import math
from typing import Self

class Point2D:
    # Валидация для лабы
    def __init__(self, x, y):
        self.x = x
        self.y = y


class Vector2D:
    def __init__(self, x: int, y: int) -> None:
        self.x = x
        self.y = y

    @classmethod
    def form_points(cls, start: Point2D, end: Point2D) -> Self:
        return Vector2D(
            end.x - start.x,
            end.y - start.y
        )

    # Для пользователя
    def __str__(self):
        return f"(x = {self.x}; y = {self.y})"

    # Для программиста
    def __repr__(self):
        return f"<{type(self).__name__} x = {self.x}; y = {self.y}>"

    # Переопределение метода ==
    def __eq__(self, other):
        
        if not isinstance(other, type(self)):
            raise ValueError(
                f"Cannot compare {type(self).__name__} with {type(other).__name__}!"
                )           
        
        return self.x == other.x and self.y == other.y
    
    def __add__(self, other: Self):
        return Vector2D(
            self.x + other.x, self.y + other.y
            )

    def __sub__(self, other):
        return Vector2D(
            self.x - other.x, self.y - other.y
        )

    def __mul__(self, value):
        return Vector2D(
            self.x * value,
            self.y * value
        )
    
    def __rmul__(self, other):
        if not isinstance(other, int | float):
            return Vector2D(
                self.x * other,
                self.y * other
            )
        
        return ValueError("Unsopported type")

    def __iadd__(self, other):
        self.x += other.x
        self.y += other.y
        
        return self

    def __matmul__(self, other):
        return other.x * self.x + other.y * self.y
    
    def __iter__(self):
        pass

    def __next__(self):
        pass
    
    def __getitem__(self, index):
        pass
    
    def __setitem__(self):
        pass
    
    def __abs__(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def __len__(self):
        return 2
    


v1 = Vector2D(x=2, y=3)
v2 = Vector2D(x=2, y=3)
p1 = Vector2D.form_points()
print(v1, v2)

print(v1 @ v2)
print(abs(v1))
# for i in v1:
#     print(i)


