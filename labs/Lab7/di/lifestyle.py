from enum import Enum

class LifeStyle(Enum):
    PerRequest = "PerRequest"
    Scoped = "Scoped"
    Singleton = "Singleton"
