from di.injector import Injector
from di.lifestyle import LifeStyle
from implementations import (
    Class1Debug,
    Class1Release,
    Class2Debug,
    Class2Release,
    Class3Debug,
    Class3Release,
)
from interfaces import Interface1, Interface2, Interface3

# ---- Конфигурации ----

def configure_a(injector: Injector) -> None:
    injector.register(Interface3, Class3Debug, 
                      life_circle=LifeStyle.PerRequest, params=(5,))
    
    injector.register(Interface2, Class2Debug, 
                      life_circle=LifeStyle.Scoped)

    injector.register(Interface1, Class1Debug, 
                      life_circle=LifeStyle.Singleton)


def configure_b(injector: Injector) -> None:
    injector.register(Interface3, Class3Release, 
                      life_circle=LifeStyle.Singleton)

    injector.register(Interface2, Class2Release, 
                      life_circle=LifeStyle.PerRequest)

    def factory_for_interface1() -> Interface1:
        return Class1Release(value=123)

    injector.register(Interface1, factory=factory_for_interface1)


if __name__ == "__main__":
    print("=== Демонстрация конфигурации A ===")

    inj = Injector()
    configure_a(inj)

    with inj.create_scope() as scope:
        a1 = scope.get_instance(Interface1)
        a2 = scope.get_instance(Interface1)

        print("Interface1 singleton: a1 is a2 ->", a1 is a2)
        print("a1.run() ->", a1.run())


    try:
        inj.get_instance(Interface2)

    except RuntimeError as e:
        print("Ожидаемая ошибка при запросе Scoped вне scope:", e)

    with inj.create_scope() as scope:
        s1 = scope.get_instance(Interface2)
        s2 = scope.get_instance(Interface2)

        print("Scoped: s1 is s2 ->", s1 is s2)

        dep3_1 = scope.get_instance(Interface3)
        dep3_2 = scope.get_instance(Interface3)

        print("PerRequest (inside scope): dep3_1 is dep3_2 ->", dep3_1 is dep3_2)
        print("s1.info() ->", s1.info())

    # ______________________________________

    print("\n=== Демонстрация конфигурации B ===")

    inj2 = Injector()
    configure_b(inj2)

    f1 = inj2.get_instance(Interface1)
    f2 = inj2.get_instance(Interface1)

    print("Interface1 via factory: f1 is f2 ->", f1 is f2)
    print("f1.run() ->", f1.run())

    i3_1 = inj2.get_instance(Interface3)
    i3_2 = inj2.get_instance(Interface3)

    print("Interface3 singleton: i3_1 is i3_2 ->", i3_1 is i3_2)

    i2_1 = inj2.get_instance(Interface2)
    i2_2 = inj2.get_instance(Interface2)

    print("Interface2 PerRequest: i2_1 is i2_2 ->", i2_1 is i2_2)
    print("i2_1.info() ->", i2_1.info())

    print("\n=== Конец демонстрации ===")
