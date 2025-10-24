from lab1 import Angle, AngleRange
import math


def test_angle_range_class():
    print("\n" + "=" * 50)
    print("ТЕСТИРОВАНИЕ КЛАССА ANGLE RANGE")
    print("=" * 50)

    print("\n1. Создание промежутков:")

    range1 = AngleRange(0, math.pi / 2)  # из чисел
    range2 = AngleRange(Angle.from_degrees(90), Angle.from_degrees(180))  # из углов
    range3 = AngleRange(math.pi, 0, start_included=False, end_included=False)  # с исключениями

    print(f"range1 = {range1}")
    print(f"range2 = {range2}")
    print(f"range3 = {range3}")
    print(f"repr(range1) = {repr(range1)}")

    print("\n2. Длина промежутков:")
    ranges = [
        AngleRange(0, math.pi / 2),
        AngleRange(math.pi / 2, math.pi),
        AngleRange(math.pi, 0),  # охватывает переход через 2π
        AngleRange.from_degrees(270, 90)
    ]

    for i, r in enumerate(ranges, start=1):
        print(f"Промежуток {i}: {r}, длина = {abs(r).degrees:.2f}°")

    print("\n3. Проверка принадлежности углов промежутку:")
    test_range = AngleRange.from_degrees(45, 135)
    test_angles = [0, 45, 90, 135, 180, 270]

    print(f"Промежуток: {test_range}")
    for deg in test_angles:
        angle = Angle.from_degrees(deg)
        result = "∈" if angle in test_range else "∉"
        print(f"Угол {deg:3}° {result} промежутку")

    print("\n4. Проверка принадлежности промежутков:")
    main_range = AngleRange.from_degrees(30, 150)
    sub_ranges = [
        AngleRange.from_degrees(40, 50),  # полностью внутри
        AngleRange.from_degrees(20, 40),  # частично снаружи
        AngleRange.from_degrees(140, 160),  # частично снаружи
        AngleRange.from_degrees(30, 150)  # точно такой же
    ]

    print(f"Главный промежуток: {main_range}")
    for sub_range in sub_ranges:
        result = "⊂" if sub_range in main_range else "⊄"
        print(f"Промежуток {sub_range} {result} главному")

    print("\n5. Сравнение промежутков:")
    print('====================================')
    range_a = AngleRange.from_degrees(0, 90)
    range_b = AngleRange.from_degrees(0, 90)
    range_c = AngleRange.from_degrees(0, 90, end_included=False)

    print(f"range_a = {range_a}")
    print(f"range_b = {range_b}")
    print(f"range_c = {range_c}")
    print(f"range_a == range_b: {range_a == range_b}")
    print(f"range_a == range_c: {range_a == range_c}")

    print("\n6. Операции с промежутками:")
    range_x = AngleRange.from_degrees(0, 90)
    range_y = AngleRange.from_degrees(60, 120)

    print(f"range_x = {range_x}")
    print(f"range_y = {range_y}")

    union_result = range_x + range_y
    print(f"range_x + range_y = {union_result}")

    diff_result = range_x - range_y
    print(f"range_x - range_y = {diff_result}")

test_angle_range_class()
