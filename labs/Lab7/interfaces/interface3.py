from abc import ABC, abstractmethod

class Interface3(ABC):
    @abstractmethod
    def compute(self) -> int:
        pass
