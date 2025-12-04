from abc import ABC, abstractmethod


class Interface1(ABC):
    @abstractmethod
    def run(self) -> str:
        pass
