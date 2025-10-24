import math
from typing import Self, Union


class Angle:
    def __init__(self, rad: int | float) -> None:
        if not isinstance(rad, (int, float)):
            raise TypeError("Radians must be a number")

        if math.isnan(rad) or math.isinf(rad):
            raise ValueError("Radians cannot be nan or inf")

        self._rad = rad

    @classmethod
    def from_degrees(cls, deg: int | float) -> Self:
        if not isinstance(deg, (int, float)):
            raise TypeError("Degrees must be a number")

        return cls(math.radians(deg))

    # region properties

    @property
    def radians(self) -> float:
        return self._rad % (2 * math.pi)

    @radians.setter
    def radians(self, new_rad: int | float) -> None:
        if not isinstance(new_rad, (int, float)):
            raise TypeError("Radians must be a number")

        if math.isnan(new_rad) or math.isinf(new_rad):
            raise ValueError("Radians cannot be nan or inf")

        self._rad = new_rad

    @property
    def degrees(self) -> float:
        return (math.degrees(self._rad)) % 360

    @degrees.setter
    def degrees(self, new_deg: int | float) -> None:
        if not isinstance(new_deg, (int, float)):
            raise TypeError("Degrees must be a number")

        if math.isnan(new_deg) or math.isinf(new_deg):
            raise ValueError("Degrees cannot be nan or inf")

        self._rad = math.radians(new_deg)

    # endregion

    # region dunder methods

    def __repr__(self) -> str:
        return f"{type(self).__name__}(radians={self._rad})"

    def __str__(self) -> str:
        return f"{self.degrees:.2f}°"

    def __float__(self) -> float:
        return float(self._rad)

    def __int__(self) -> int:
        return int(self._rad)

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return math.isclose(self._rad, other._rad)

        if isinstance(other, (int, float)):
            return math.isclose(self._rad, float(other))

        return NotImplemented

    def __lt__(self, other: Union[int, float, Self]) -> bool:
        if isinstance(other, type(self)):
            return self._rad < other._rad

        if isinstance(other, (int, float)):
            return self._rad < other

        return NotImplemented

    def __le__(self, other: Union[int, float, Self]) -> bool:
        if isinstance(other, type(self)):
            return self._rad <= other._rad

        if isinstance(other, (int, float)):
            return self._rad <= other

        return NotImplemented

    def __add__(self, other: Union[int, float, Self]) -> Self:
        if isinstance(other, type(self)):
            return type(self)(self._rad + other._rad)

        if isinstance(other, (int, float)):
            return type(self)(self._rad + other)

        return NotImplemented

    def __radd__(self, other: Union[int, float]) -> Self:
        return self.__add__(other)

    def __sub__(self, other: int | float) -> Self:
        if isinstance(other, type(self)):
            return type(self)(self._rad - other._rad)

        if isinstance(other, (int, float)):
            return type(self)(self._rad - other)

        return NotImplemented

    def __rsub__(self, other: Union[int, float]) -> Self:
        if isinstance(other, (int, float)):
            return type(self)(other - self._rad)

        return NotImplemented

    def __mul__(self, value: Union[int, float]) -> Self:
        if isinstance(value, (int, float)):
            return type(self)(self._rad * value)

        return NotImplemented

    def __rmul__(self, value: Union[int, float]) -> Self:
        return self.__mul__(value)

    def __truediv__(self, value: Union[int, float]) -> Self:
        if not isinstance(value, (int, float)):
            return NotImplemented

        if value == 0:
            raise ZeroDivisionError("Division by zero")

        return type(self)(self._rad / value)

    # endregion


class AngleRange:
    def __init__(
        self,
        start: Union[int, float, Angle],
        end: Union[int, float, Angle],
        start_included: bool = True,
        end_included: bool = True,
    ):
        self._start: Angle = start if isinstance(start, Angle) else Angle(start)
        self._end: Angle = end if isinstance(end, Angle) else Angle(end)

        self._start_included = bool(start_included)
        self._end_included = bool(end_included)

        if self._start._rad > self._end._rad:
            self._start, self._end = self._end, self._start
            self._start_included, self._end_included = (
                self._end_included,
                self._start_included,
            )

    @classmethod
    def from_degrees(
        cls,
        start_deg: int | float,
        end_deg: int | float,
        start_included: bool = True,
        end_included: bool = True,
    ) -> Self:
        if not isinstance(start_deg, (int, float)):
            raise TypeError("Start degrees must be a number")
        
        if not isinstance(end_deg, (int, float)):
            raise TypeError("End degrees must be a number")

        if math.isnan(start_deg) or math.isinf(start_deg):
            raise ValueError("Start degrees cannot be nan or inf")
        
        if math.isnan(end_deg) or math.isinf(end_deg):
            raise ValueError("End degrees cannot be nan or inf")

        start_angle = Angle.from_degrees(start_deg)
        end_angle = Angle.from_degrees(end_deg)
        
        return cls(start_angle, end_angle, start_included, end_included)

    # region help functions

    def _ensure_angle(self, value: Union[Angle, int, float]) -> Angle:
        if isinstance(value, (int, float)):
            return Angle(value)

        elif isinstance(value, Angle): # type: ignore #type(self) -> typeError
            return value

        raise TypeError(f"Expected: Angle | int | float; got {type(value)}")

    def _overlaps(self, other: Self) -> bool:
        return (self._contains_angle(other._start) or 
                self._contains_angle(other._end) or
                other._contains_angle(self._start) or
                other._contains_angle(self._end))

    def _adjacent(self, other: Self) -> bool:
        return (math.isclose(self._end._rad, other._start._rad) or
                math.isclose(other._end._rad, self._start._rad))

    def _contains_angle(self, angle: Angle) -> bool:
        rad = angle._rad
        
        in_range = self._start._rad <= rad <= self._end._rad
        
        if not self._start_included and math.isclose(rad, self._start._rad):
            return False

        if not self._end_included and math.isclose(rad, self._end._rad):
            return False
        
        return in_range

    def _contains_range(self, other: Self) -> bool:
        return self._contains_angle(other._start) and self._contains_angle(other._end)

    # endregion

    # region properties

    @property
    def start(self) -> Angle:
        return self._start

    @property
    def end(self) -> Angle:
        return self._end

    @property
    def start_included(self) -> bool:
        return self._start_included

    @property
    def end_included(self) -> bool:
        return self._end_included

    # endregion

    # region dunder

    def __contains__(self, other: Union[Self, Angle, int, float]) -> bool:
        if isinstance(other, Angle):
            return self._contains_angle(other)

        elif isinstance(other, (int, float)):
            return self._contains_angle(Angle(other))

        elif isinstance(other, type(self)):
            return self._contains_range(other)

        return False

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, type(self)):
            return NotImplemented

        return (
            math.isclose(self._start._rad, other._start._rad)
            and math.isclose(self._end._rad, other._end._rad)
            and self._start_included == other._start_included
            and self._end_included == other._end_included
        )

    def __abs__(self) -> Angle:
        return Angle((self.end.radians - self.start.radians) % (2 * math.pi))

    def __repr__(self) -> str:
        start_br = "[" if self._start_included else "("
        end_br = "]" if self._end_included else ")"

        return (
            f"{type(self).__name__}("
            f"{start_br}{self._start.radians:.4f}; {self._end.radians:.4f}{end_br})"
        )

    def __str__(self) -> str:
        start_br = "[" if self._start_included else "("
        end_br = "]" if self._end_included else ")"

        return f"{start_br}{self._start.degrees:.2f}; {self._end.degrees:.2f}{end_br}"

    def __add__(self, other: Self) -> list["AngleRange"]:
        if not isinstance(other, AngleRange):
            return NotImplemented

        if self._overlaps(other) or self._adjacent(other):
            new_start = min(self._start, other._start, key=lambda a: a._rad)
            new_end = max(self._end, other._end, key=lambda a: a._rad)

            new_start_inc = (
                self._start_included
                if new_start is self._start
                else other._start_included
            )

            new_end_inc = (
                self._end_included if new_end is self._end else other._end_included
            )

            return [AngleRange(new_start, new_end, new_start_inc, new_end_inc)]

        return sorted([self, other], key=lambda r: r._start._rad)

    def __sub__(self, other: Self) -> list["AngleRange"]:
        if not isinstance(other, AngleRange):
            return NotImplemented

        if not self._overlaps(other):
            return [self]

        result: list["AngleRange"] = []

        s1, e1 = self._start._rad, self._end._rad
        s2, e2 = other._start._rad, other._end._rad

        if s1 < s2:
            result.append(
                AngleRange(
                    self._start,
                    other._start,
                    self._start_included,
                    not other._start_included,
                )
            )

        if e2 < e1:
            result.append(
                AngleRange(
                    other._end,
                    self._end,
                    not other._end_included,
                    self._end_included,
                )
            )

        return result

    # endregion
