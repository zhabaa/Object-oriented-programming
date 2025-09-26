import math
from typing import Self


class Angle:
    def __init__(self, rad: int | float) -> None:
        self.rad = rad

    @classmethod
    def form_degees(cls, deg: int | float) -> Self:
        return cls(math.radians(deg))

    @property
    def radians(self) -> int | float:
        return self._normalize_rad(self.rad)

    @radians.setter
    def radians(self, new_rad: int | float) -> None:
        if not isinstance(new_rad, int | float):
            raise TypeError("Radians must be a number")

        if math.isnan(new_rad) or math.isinf(new_rad):
            raise ValueError("Radians cannot be nan or inf")

        self.rad = self._normalize_rad(new_rad)

    @property
    def degrees(self) -> int | float:
        return self._normalize_deg(math.degrees(self.rad))

    @degrees.setter
    def degrees(self, new_deg: int | float) -> None:
        if not isinstance(new_deg, int | float):
            raise TypeError("Degrees must be a number")

        if math.isnan(new_deg) or math.isinf(new_deg):
            raise ValueError("Degrees cannot be nan or inf")

        self.rad = math.radians(self._normalize_deg(new_deg))

    @staticmethod
    def _normalize_deg(degrees: int | float) -> int | float:
        return degrees % 360

    @staticmethod
    def _normalize_rad(radians: int | float) -> int | float:
        return radians % (2 * math.pi)

    # region dunder methods

    def __repr__(self) -> str:
        return f"{type(self).__name__}(radians = {self.rad})"

    def __int__(self) -> int:
        return int(self.radians)

    def __str__(self) -> str:
        return f"{self.rad:.4f}"

    def __float__(self) -> float:
        return self.rad

    def __eq__(self, other: Self) -> bool:
        if isinstance(other, Self):
            return abs(self.rad - other.rad) < 1e-10

        return False

    def __lt__(self, other: Self) -> bool:
        if isinstance(other, Self):
            return self.rad < other.rad

        elif isinstance(other, int | float):
            return self.rad < (other % (2 * math.pi))

        return NotImplemented

    def __le__(self, other: Self) -> bool:
        if isinstance(other, Self):
            return self.rad <= other.rad

        elif isinstance(other, int | float):
            return self.rad <= (other % (2 * self.PI))

        return NotImplemented

    def __add__(self, other: Self | int | float) -> Self:
        if isinstance(other, Self):
            return Angle(self.rad + other.rad)

        elif isinstance(other, int | float):
            return Angle(self.rad + other)

        return NotImplemented

    def __radd__(self, other: int | float) -> Self:
        return self.__add__(other)

    def __sub__(self, other: Self | int | float) -> Self:
        if isinstance(other, Self):
            return Angle(self.rad - other.rad)

        elif isinstance(other, int | float):
            return Angle(self.rad - other)

        return NotImplemented

    def __rsub__(self, other: int | float) -> Self:
        if isinstance(other, int | float):
            return Angle(other - self.rad)

        return NotImplemented

    def __mul__(self, value: int | float) -> Self:
        if isinstance(value, int | float):
            return Angle(self.rad * value)

        return NotImplemented

    def __rmul__(self, value: int | float) -> Self:
        return self.__mul__(value)

    def __truediv__(self, value: int | float) -> Self:
        if not value:
            raise ZeroDivisionError

        if isinstance(value, int | float):
            return Angle(self.rad / value)

        return NotImplemented

    # endregion


class AngleRange:
    def __init__(
        self,
        start: Angle | int | float,
        end: Angle | int | float,
        start_included: bool = False,
        end_included: bool = False,
    ):
        self.start: Angle | int | float = Angle(start) if isinstance(start, int | float) else start
        self.end: Angle | int | float = Angle(end) if isinstance(end, int | float) else end
        self.start_included = start_included
        self.end_included = end_included

        self._normalize()

    def _normalize(self) -> None:
        if self.start.rad > self.end.rad:
            self.end.rad = Angle(self.end.rad + 2 * math.pi)

    def _overlaps(self, other: Self) -> bool:
        return (
            self.start in other
            or self.end in other
            or other.start in self
            or other.end in self
        )

    def _adjacent(self, other: Self) -> bool:
        return (
            abs(self.end.rad - other.start.rad) < 1e-10
            or abs(other.end.rad - self.start.rad) < 1e-10
        )
        
    # region dunder methods

    def __eq__(self, other: Self) -> bool:
        if not isinstance(other, Self):
            return NotImplemented

        return (
            self.start.rad == other.start.rad
            and self.end.rad == other.end.rad
            and self.start_included == other.start_included
            and self.end_included == other.end_included
        )

    def __str__(self) -> str:
        start_brackets = "[" if self.start_included else "("
        end_brackets = "]" if self.end_included else ")"
        return f"{start_brackets}{self.start.rad}; {self.end.rad}{end_brackets}"

    def __repr__(self) -> str:
        start_brackets = "[" if self.start_included else "("
        end_brackets = "]" if self.end_included else ")"
        return f"{type(self).__name__}(range={start_brackets}{self.start.rad}; {self.end.rad}{end_brackets})"

    def __abs__(self) -> Angle:
        return Angle(self.end.rad - self.start.rad)

    def __contains__(self, other: Self | Angle) -> bool:
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

    def __add__(self, other: Self) -> Self:
        if not isinstance(other, Self):
            return NotImplemented

        if self._overlaps(other) or self._adjacent(other):
            new_start = min(self.start, other.start)
            new_end = max(self.end, other.end)
            
            new_start_inc = {
                self.start: self.start_included, 
                other.start: other.start_included
            }.get(new_start, True)

            new_end_inc = {
                self.end: self.end_included,
                other.end: other.end_included  
            }.get(new_end, True)

            return AngleRange(new_start, new_end, new_start_inc, new_end_inc)
        else:
            return sorted([self, other], key=lambda x: x.start.radians)

    def __sub__(self, other: Self) -> Self:
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
    
    # endregion
