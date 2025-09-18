from lab1 import Angle, AngleRange
import math

def demonstrate_functionality():
    print("Демонстрация Angle")
    
    angle1 = Angle(math.pi/4)  # 45
    angle2 = Angle.form_degees(60)  # 60
    
    print(f"angle1 (45°): {angle1}, градусы: {angle1.degrees:.1f}°")
    print(f"angle2 (60°): {angle2}, градусы: {angle2.degrees:.1f}°")
    
    sum_angle = angle1 + angle2  # 45 + 60 = 105
    print(f"Сумма: {sum_angle}, градусы: {sum_angle.degrees:.1f}°")
    
    big_angle = Angle(5 * math.pi)
    print(f"5π нормализовано: {big_angle}, градусы: {big_angle.degrees:.1f}°")
    
    print("\nДемонстрация AngleRange")
    
    range1 = AngleRange(0, math.pi/2, True, False)  # [0, 90)
    range2 = AngleRange(math.pi/4, math.pi, True, True)  # [45, 180]
    
    print(f"range1: {range1}")
    print(f"range2: {range2}")
    print(f"Длина range1: {abs(range1).degrees:.1f}°")
    
    test_angle = Angle(math.pi/3)  # 60
    print(f"Угол 60° в range1: {test_angle in range1}")
    print(f"range2 в range1: {range2 in range1}")
    
    union = range1 + range2
    
    if isinstance(union, AngleRange):
        print(f"Сумма: {union}")
    else:
        print(f"Сумма: список из {len(union)} диапазонов")


if __name__ == "__main__":
    demonstrate_functionality()
