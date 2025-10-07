from typing import Iterable, Iterator, TypeVar

T = TypeVar('T')

names = ['Владимир', 'Никита', 'Полина', 'Герман',
         'Никита', 'Владислав', 'Виктор', 'Максим',
         'Александр', 'Виктория', 'Александр',
         'Иван', 'Александра', 'Маргарита']


def filter_data(data: Iterable[T], value: T) -> Iterator[T]:
    for item in data:
        if item == value:
            yield item


# for name in filter_data(names, 'Александр'):
#     print(name)


class Vector3d(Iterable[float]):
    def __init__(self, x: float, y: float, z: float) -> None:
        self.x = x
        self.y = y
        self.z = z

    def __iter__(self) -> Iterator[float]:
        yield self.x
        yield self.y
        yield self.z


vector = Vector3d(10, 10, 20)

for x in filter_data(vector, 10):
    print(x)


def get_data():
    yield 1
    yield 2
    yield 3

a = get_data()

for i in a:
    print(i)
