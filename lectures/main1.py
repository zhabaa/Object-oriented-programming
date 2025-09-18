from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Point:
    x: int
    y: int
    description: Optional[str] = field(
        default=None,
        repr=False,
        compare=False,
        init=False
    )

    def __postinit__(self):
        if self.x < 0:
            raise ValueError("x < 0")
        

p = Point(1, 1)
p1 = Point(1, 1)
p1.description = 'Max'
print(p, p1)
print(p == p1)
