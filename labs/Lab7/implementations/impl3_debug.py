from interfaces.interface3 import Interface3

class Class3Debug(Interface3):
    def __init__(self, base: int = 1):
        self._base = base

    def compute(self) -> int:
        return self._base * 100
