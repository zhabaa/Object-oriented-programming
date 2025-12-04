from interfaces.interface1 import Interface1

class Class1Release(Interface1):
    def __init__(self, value: int = 42):
        self._value = value

    def run(self) -> str:
        return f"Class1Release value={self._value}"
