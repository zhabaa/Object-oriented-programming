from interfaces.interface1 import Interface1
from interfaces.interface2 import Interface2

class Class1Debug(Interface1):
    def __init__(self, dep2: Interface2):
        # демонстрируем внедрение зависимости Interface2
        self._dep2 = dep2

    def run(self) -> str:
        return f"Class1Debug -> {self._dep2.info()}"
