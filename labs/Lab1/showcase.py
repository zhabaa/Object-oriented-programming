from math import pi
from lab1 import Angle, AngleRange

print("---- Создание углов ----")
a1 = Angle(pi/2)
a2 = Angle.from_degrees(90)
print(a1, a2, "→ оба должны быть π/2")  

print("\n---- Получение и присваивание ----")
print(a1.radians, "→ π/2")
print(a1.degrees, "→ 90")
a1.radians = pi
print(a1.radians, a1.degrees, "→ π, 180")
a1.degrees = 45
print(a1.radians, a1.degrees, "→ π/4, 45")

print("\n---- Преобразования ----")
a = Angle(pi/2)
print(float(a), int(a), str(a), repr(a), "→ float, int, str, repr")


print("\n---- Арифметика ----")
a = Angle(pi/2)
b = Angle(pi/4)
print(a + b, "→ 3π/4")
print(a - b, "→ π/4")
print(a + pi/4, "→ 3π/4")
print(pi/4 + a, "→ 3π/4")
print(a - pi/4, "→ π/4")
print(pi/2 - a, "→ 0")
print(a * 2, "→ π")
print(2 * a, "→ π")
print(a / 2, "→ π/4")


print("\n---- Создание диапазонов ----")
r1 = AngleRange(0, pi/2)
r2 = AngleRange(pi/2, pi)
r3 = AngleRange(3*pi/2, pi/2)
r4 = AngleRange(0, pi*2)
print(r1)
print(r2)
print(r3)

print("\n---- Получение длины диапазона ----")
print(abs(r1), "→ должно быть π/2")
print(abs(r3), "→ должно быть π (от 3π/2 до π/2 через 2π)")

print("\n---- Проверка вхождения углов ----")
a = Angle(pi/4)
b = Angle(3*pi/2)
print(a in r1, "→ True (π/4 ∈ [0, π/2])")
print(b in r4, "→ True (3π/2 ∈ [0, 2π])")
print(b in r3, "→ False (3π/2 ∉ [3π/2, π/2)")

print("\n---- Проверка вхождения диапазонов ----")
r4 = AngleRange(0, pi)
r5 = AngleRange(pi/4, pi/2)
r6 = AngleRange(pi/2, 3*pi/2)
print(r5 in r4, "→ True ([π/4, π/2] внутри [0, π])")
print(r6 in r4, "→ False ([π/2, 3π/2] частично выходит за границы)")
print(r3 in r4, "→ False (wrap-around не внутри обычного диапазона)")
print(r4 in r3, "→ False (обычный диапазон не входит в wrap-around, длина меньше)")

print("\n---- Проверка включающих и исключающих границ ----")
r7 = AngleRange(0, pi, start_included=False, end_included=False)
print(Angle(0) in r7, "→ False (начало исключено)")
print(Angle(pi) in r7, "→ False (конец исключён)")
print(AngleRange(pi/4, pi/2) in r7, "→ True (середина включена)")

print("\n---- Сумма диапазонов ----")
r11 = AngleRange(0, pi/2)
r12 = AngleRange(pi/4, pi)
sum_result = r11 + r12
print(sum_result)
print("→ должно получиться один объединённый диапазон [0, π]")

r13 = AngleRange(3*pi/2, 2*pi)
r14 = AngleRange(0, pi/4)
sum_wrap = r13 + r14
print(sum_wrap)

print("\n---- Разность диапазонов ----")
r15 = AngleRange(0, pi)
r16 = AngleRange(pi/4, 3*pi/4)
diff_result = r15 - r16
print(diff_result)
print("→ должно остаться два диапазона: [0, π/4] и [3π/4, π]")

r17 = AngleRange(3*pi/2, pi/2)
r18 = AngleRange(0, pi/4)
diff_wrap = r17 - r18
print(diff_wrap)
print("→ диапазон wrap-around минус маленький — должен остаться разорванный участок")

print("\n---- Форматирование ----")

a = Angle(pi)

print(f"rad = {a:rad}\tdeg = {a:deg}")


ar = AngleRange(0, pi, start_included=True, end_included=False)
print(f"ar rad = {ar:rad}\tar deg = {ar:deg}")
