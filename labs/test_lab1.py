import math
from lab1 import Angle, AngleRange


def simple_test():
    """Простой тест основных функций"""
    print("=== Simple Tests ===")

    angle1 = Angle(math.pi)
    angle2 = Angle.from_degrees(90)
    print(f"Angle 1: {angle1}")
    print(f"Angle 2: {angle2}")

    sum_angle = angle1 + angle2
    print(f"Sum: {sum_angle}")

    range1 = AngleRange(0, math.pi)
    range2 = AngleRange(math.pi / 2, 3 * math.pi / 2)
    print(f"Range 1: {range1}")
    print(f"Range 2: {range2}")

    print(f"Angle 2 in Range 1: {angle2 in range1}")

    union = range1 + range2
    print(f"Union: {union}")

    subtraction = range1 - range2
    print(f"Subtraction: {subtraction}")
    
    print("Done!")


if __name__ == "__main__":
    simple_test()
