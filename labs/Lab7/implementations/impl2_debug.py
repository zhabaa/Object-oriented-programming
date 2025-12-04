from interfaces.interface2 import Interface2
from interfaces.interface3 import Interface3

class Class2Debug(Interface2):
    def __init__(self, dep3: Interface3):
        self._dep3 = dep3

    def info(self) -> str:
        return f"Class2Debug -> compute={self._dep3.compute()}"
