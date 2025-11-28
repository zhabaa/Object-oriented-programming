from abc import ABC, abstractmethod

from lab7 import (
    ConsoleLogger,
    FileLogger,
    IDatabase,
    IEmailService,
    ILogger,
    Injector,
    LifeStyle,
    MockEmailService,
    PostgresDatabase,
    RealEmailService,
    SQLiteDatabase,
)


def demo():
    print("\n========= CONFIG 1 (ConsoleLogger + SQLite + MockEmail) =========")

    inj = Injector()

    # logger singleton
    inj.register(
        ILogger,
        implementation=ConsoleLogger,
        lifestyle=LifeStyle.SINGLETON,
        prefix="DEMO",
    )

    # sqlite per-request
    inj.register(
        IDatabase,
        implementation=SQLiteDatabase,
        lifestyle=LifeStyle.PER_REQUEST,
        connection_string="sqlite://local",
    )

    # mock email scoped
    inj.register(
        IEmailService, implementation=MockEmailService, lifestyle=LifeStyle.SCOPED
    )

    db1 = inj.get_instance(IDatabase)
    db2 = inj.get_instance(IDatabase)

    print("db1 is db2:", db1 is db2)  # False

    logger1 = inj.get_instance(ILogger)
    logger2 = inj.get_instance(ILogger)

    print("logger1 is logger2:", logger1 is logger2)  # True

    print("\n-- Scoped block --")

    with inj as scope:
        email1 = scope.get_instance(IEmailService)
        email2 = scope.get_instance(IEmailService)
        print("email1 is email2:", email1 is email2)  # True

    print("-- After scope --")

    with inj as scope2:
        email3 = scope2.get_instance(IEmailService)
        print("email1 is email3:", email1 is email3)  # False

    print("\n========= CONFIG 2 (FileLogger + Postgres + RealEmail) =========")

    inj2 = Injector()

    # File logger factory example
    inj2.register(
        ILogger,
        factory=lambda: FileLogger("log_demo.txt"),
        lifestyle=LifeStyle.SINGLETON,
    )

    inj2.register(
        IDatabase,
        implementation=PostgresDatabase,
        lifestyle=LifeStyle.SCOPED,
        host="localhost",
        port=5432,
    )

    inj2.register(
        IEmailService,
        implementation=RealEmailService,
        lifestyle=LifeStyle.PER_REQUEST,
        smtp_server="smtp.example.com",
    )

    with inj2 as scope:
        dbA = scope.get_instance(IDatabase)
        dbB = scope.get_instance(IDatabase)
        print("dbA is dbB:", dbA is dbB)  # True

        emailA = scope.get_instance(IEmailService)
        emailB = scope.get_instance(IEmailService)
        print("emailA is emailB:", emailA is emailB)  # False

        dbA.connect()
        dbA.execute("SELECT 1")
        emailA.send("user@mail.com", "Hello!")

    print("\n========= FACTORY-ONLY INTERFACE =========")

    class Dummy(ABC):
        @abstractmethod
        def run(self):
            pass

    class DummyClass(Dummy):
        def run(self):
            print("Dummy object created via factory")

    inj3 = Injector()
    inj3.register(Dummy, factory=lambda: DummyClass())

    obj = inj3.get_instance(Dummy)
    obj.run()

    class IDummy11(ABC):
        pass

    class Dummy1(IDummy1):
        def __init__(self, name: str = "Dummy1"):
            self.name = name
            print(f"Создан {self.name}")

    class Dummy2(IDummy2):
        def __init__(self, subclass: IDummy1):  # Зависит от Dummy1!
            self.sub = subclass
            print(f"Создан Dummy2 с зависимостью {self.sub.name}")

    i1 = Injector()
    # Регистрируем зависимости
    i1.register(Dummy1, IDummy1, LifeStyle.SINGLETON)  # Сначала регистрируем зависимость
    i1.register(Dummy2, IDummy2, LifeStyle.SINGLETON)  # Потом то, что от нее зависит

    # Инжектор сам разрешит зависимости при создании
    d2 = i1.get_instance(Dummy2)  # ✅ Сработает!
    # Инжектор автоматически создаст Dummy1 и передаст его в Dummy2


# endregion


# run demo
demo()
