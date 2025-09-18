import math


class Angle:
    """Класс для хранения углов"""

    PI = math.pi

    def __init__(self, rad):
        self.rad = rad

    # @classmethod
    # def from_radians(cls, rad):
    #     return cls(rad)

    @classmethod
    def form_degees(cls, deg):
        return cls(math.radians(deg))

    @property
    def radians(self):
        return self._normalize_rad(self.rad)

    @radians.setter
    def radians(self, new_rad):
        if not isinstance(new_rad, (int, float)):
            raise TypeError("Radians must be a number")

        if math.isnan(new_rad) or math.isinf(new_rad):
            raise ValueError("Radians cannot be nan or inf")

        # Нормализация [0, 2pi)
        self.rad = self._normalize_rad(new_rad)

    @property
    def degrees(self):
        return self._normalize_deg(math.degrees(self.rad))

    @degrees.setter
    def degrees(self, new_deg):
        if not isinstance(new_deg, (int, float)):
            raise TypeError("Degrees must be a number")

        if math.isnan(new_deg) or math.isinf(new_deg):
            raise ValueError("Degrees cannot be nan or inf")

        # Нормализация в диапазон [0, 360)
        self.rad = math.radians(self._normalize_deg(new_deg))

    @staticmethod
    def _normalize_deg(degrees):
        return degrees % 360

    @staticmethod
    def _normalize_rad(radians):
        return radians % (2 * math.pi)

    def __repr__(self):
        return f"{type(self).__name__}(radians = {self.rad})"

    def __int__(self):
        return int(self.radians)

    def __str__(self):
        return f"{self.rad:.4f}"

    def __float__(self):
        return self.rad

    def __eq__(self, other):
        if isinstance(other, Angle):
            return abs(self.rad - other.rad) < 1e-10

        return False

    def __lt__(self, other):
        if isinstance(other, Angle):
            return self.rad < other.rad

        elif isinstance(other, (int, float)):
            return self.rad < (other % (2 * math.pi))

        return NotImplemented

    def __le__(self, other):
        if isinstance(other, Angle):
            return self.rad <= other.rad

        elif isinstance(other, (int, float)):
            return self.rad <= (other % (2 * self.PI))

        return NotImplemented

    def __add__(self, other):
        if isinstance(other, Angle):
            return Angle(self.rad + other.rad)

        elif isinstance(other, (int, float)):
            return Angle(self.rad + other)

        return NotImplemented

    def __radd__(self, other):
        return self.__add__(other)

    def __sub__(self, other):
        if isinstance(other, Angle):
            return Angle(self.rad - other.rad)

        elif isinstance(other, (int, float)):
            return Angle(self.rad - other)

        return NotImplemented

    def __rsub__(self, other):
        if isinstance(other, (int, float)):
            return Angle(other - self.rad)

        return NotImplemented

    def __mul__(self, value):
        if isinstance(value, (int, float)):
            return Angle(self.rad * value)

        return NotImplemented

    def __rmul__(self, value):
        return self.__mul__(value)

    def __truediv__(self, value):
        if not value:
            raise ZeroDivisionError

        if isinstance(value, (int, float)):
            return Angle(self.rad / value)

        return NotImplemented


class AngleRange:
    def __init__(self, start, end, start_included=False, end_included=False):
        self.start: Angle = Angle(start) if isinstance(start, (int, float)) else start
        self.end: Angle = Angle(end) if isinstance(end, (int, float)) else end
        self.start_included = start_included
        self.end_included = end_included

        self._normalize()

    def _normalize(self):
        if self.start.rad > self.end.rad:
            self.end.rad = Angle(self.end.rad + 2 * math.pi)

    def _overlaps(self, other):
        return (
            self.start in other
            or self.end in other
            or other.start in self
            or other.end in self
        )

    def _adjacent(self, other: "AngleRange"):
        return (
            abs(self.end.rad - other.start.rad) < 1e-10
            or abs(other.end.rad - self.start.rad) < 1e-10
        )

    def __eq__(self, other: "AngleRange"):
        if not isinstance(other, self):
            return NotImplemented

        return (
            self.start.rad == other.start.rad
            and self.end.rad == other.end.rad
            and self.start_included == other.start_included
            and self.end_included == other.end_included
        )

    def __str__(self):
        start_brackets = "[" if self.start_included else "("
        end_brackets = "]" if self.end_included else ")"
        return f"{start_brackets}{self.start.rad}; {self.end.rad}{end_brackets}"

    def __repr__(self):
        start_brackets = "[" if self.start_included else "("
        end_brackets = "]" if self.end_included else ")"
        return f"{type(self).__name__}(range={start_brackets}{self.start.rad}; {self.end.rad}{end_brackets})"

    def __abs__(self):
        return Angle(self.end.rad - self.start.rad)  # или просто self.end - self.start

    def __contains__(self, other):
        if isinstance(other, Angle):
            rad = other.rad % (2 * math.pi)

            in_range = self.start.rad <= rad <= self.end.rad

            if not self.start_included and abs(rad - self.start.rad) < 1e-10:
                return False

            if not self.end_included and abs(rad - self.end.rad) < 1e-10:
                return False

            return in_range

        elif isinstance(other, AngleRange):
            return other.start.rad in self and other.end.rad in self

        return False

    def __add__(self, other):
        if not isinstance(other, AngleRange):
            return NotImplemented

        if self._overlaps(other) or self._adjacent(other):
            new_start = min(self.start, other.start)
            new_end = max(self.end, other.end)
            new_start_inc = (
                self.start_included
                if self.start == new_start
                else other.start_included
                if other.start == new_start
                else True
            )
            new_end_inc = (
                self.end_included
                if self.end == new_end
                else other.end_included
                if other.end == new_end
                else True
            )

            return AngleRange(new_start, new_end, new_start_inc, new_end_inc)
        else:
            return sorted([self, other], key=lambda x: x.start.radians)

    def __sub__(self, other):
        if not isinstance(other, AngleRange):
            return NotImplemented

        result = []

        if not self._overlaps(other):
            return [self]

        if self.start.rad < other.start.rad:
            start_inc = self.start_included and not other.start_included
            result.append(
                AngleRange(
                    self.start.rad, other.start.rad, self.start_included, start_inc
                )
            )

        if other.end.rad < self.end.rad:
            end_inc = self.end_included and not other.end_included
            result.append(
                AngleRange(other.end.rad, self.end.rad, end_inc, self.end_included)
            )

        return result
