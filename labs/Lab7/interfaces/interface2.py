from abc import ABC, abstractmethod


class Interface2(ABC):
    @abstractmethod
    def info(self) -> str:
        pass
