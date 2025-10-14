import math
from typing import Self, Union


class Angle:
    def __init__(self, rad: int | float) -> None:
        self.rad = rad

    #region properties
    @classmethod
    def from_degrees(cls, deg: int | float) -> Self:
        return cls(math.radians(deg))

    @property
    def radians(self) -> int | float:
        return self._normalize_rad(self.rad)

    @radians.setter
    def radians(self, new_rad: int | float) -> None:
        if not isinstance(new_rad, int | float): # type: ignore # new_rad: int | float => isinstance
            raise TypeError("Radians must be a number")

        if math.isnan(new_rad) or math.isinf(new_rad):
            raise ValueError("Radians cannot be nan or inf")

        self.rad = self._normalize_rad(new_rad)

    @property
    def degrees(self) -> int | float:
        return self._normalize_deg(math.degrees(self.rad))

    @degrees.setter
    def degrees(self, new_deg: int | float) -> None:
        if not isinstance(new_deg, int | float): # type: ignore # new_deg: int | float => isinstance
            raise TypeError("Degrees must be a number")

        if math.isnan(new_deg) or math.isinf(new_deg):
            raise ValueError("Degrees cannot be nan or inf")

        self.rad = math.radians(self._normalize_deg(new_deg))
        
    # endregion

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

    def __eq__(self, other: object) -> bool:
        if isinstance(other, type(self)):
            return math.isclose(self.rad, other.rad)

        return False

    def __lt__(self, other: Self) -> bool:
        if isinstance(other, type(self)):
            return self.rad < other.rad

        elif isinstance(other, int | float):
            return self.rad < (other % (2 * math.pi))

        return NotImplemented

    def __le__(self, other: Self) -> bool:
        if isinstance(other, type(self)):
            return self.rad <= other.rad

        elif isinstance(other, int | float):
            return self.rad <= (other % (2 * math.pi))

        return NotImplemented

    def __add__(self, other: Union[int, float, Self]) -> Self:
        if isinstance(other, type(self)):
            return type(self)(self.rad + other.rad)

        elif isinstance(other, int | float):
            return type(self)(self.rad + other)
    
        raise NotImplementedError

    def __radd__(self, other: int | float) -> Self:
        return self.__add__(other)

    def __sub__(self, other: Self | int | float) -> Self:
        if isinstance(other, type(self)):
            return type(self)(self.rad - other.rad)

        elif isinstance(other, int | float):
            return type(self)(self.rad - other)

        return NotImplemented

    def __rsub__(self, other: int | float) -> Self:
        if isinstance(other, int | float): # type: ignore # other: int | float => isinstance
            return type(self)(other - self.rad)

        return NotImplemented

    def __mul__(self, value: int | float) -> Self:
        if isinstance(value, int | float): # type: ignore # value: int | float => isinstance
            return type(self)(self.rad * value)

        return NotImplemented

    def __rmul__(self, value: int | float) -> Self:
        return self.__mul__(value)

    def __truediv__(self, value: int | float) -> Self:
        if not value:
            raise ZeroDivisionError

        if isinstance(value, int | float): # type: ignore # value: int | float => isinstance
            return type(self)(self.rad / value)

        return NotImplemented

    # endregion


class AngleRange:
    def __init__(
        self,
        start: Union[Angle, int, float],
        end: Union[Angle, int, float],
        start_included: bool = True,
        end_included: bool = True,
    ):
        self._start = self._ensure_angle(start)
        self._end = self._ensure_angle(end)
        self._start_included = start_included
        self._end_included = end_included

    # region properties
    @property
    def start(self) -> Angle:
        return self._start

    @start.setter
    def start(self, value: Union[Angle, int, float]) -> None:
        self._start = self._ensure_angle(value)

    @property
    def end(self) -> Angle:
        return self._end

    @end.setter
    def end(self, value: Union[Angle, int, float]) -> None:
        self._end = self._ensure_angle(value)

    @property
    def start_included(self) -> bool:
        return self._start_included

    @start_included.setter
    def start_included(self, value: bool) -> None:
        self._start_included = value

    @property
    def end_included(self) -> bool:
        return self._end_included

    @end_included.setter
    def end_included(self, value: bool) -> None:
        self._end_included = value
    # endregion

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
        return (math.isclose(self._end.rad, other._start.rad) or
                math.isclose(other._end.rad, self._start.rad))

    def _contains_angle(self, angle: Angle) -> bool:
        rad = angle.rad
        
        in_range = self._start.rad <= rad <= self._end.rad
        
        if not self._start_included and math.isclose(rad, self._start.rad):
            return False

        if not self._end_included and math.isclose(rad, self._end.rad):
            return False
        
        return in_range

    def _contains_range(self, other: Self) -> bool:
        return self._contains_angle(other._start) and self._contains_angle(other._end)

    # region dunder methods
    def __eq__(self, other: object) -> bool:
        if not isinstance(other, AngleRange):
            return NotImplemented
        
        return (math.isclose(self._start.rad, other._start.rad) and
                math.isclose(self._end.rad, other._end.rad) and
                self._start_included == other._start_included and
                self._end_included == other._end_included)

    def __contains__(self, other: Union[Self, Angle, int, float]) -> bool:
        if isinstance(other, Angle):
            return self._contains_angle(other)

        elif isinstance(other, (int, float)):
            return self._contains_angle(Angle(other))

        elif isinstance(other, type(self)):
            return self._contains_range(other)

        return False

    def __add__(self, other: Self) -> list[Self]:
        if not isinstance(other, type(self)):
            return NotImplemented

        if self._overlaps(other) or self._adjacent(other):
            new_start = min(self._start, other._start, key=lambda x: x.rad)
            new_end = max(self._end, other._end, key=lambda x: x.rad)
            
            new_start_inc = (
                self._start_included if new_start.rad == self._start.rad 
                else other._start_included
            )

            new_end_inc = (
                self._end_included if new_end.rad == self._end.rad 
                else other._end_included
            )

            return [type(self)(new_start, new_end, new_start_inc, new_end_inc)]

        else:
            return sorted([self, other], key=lambda x: x._start.rad)

    def __sub__(self, other: Self) -> list[Self]:
        if not isinstance(other, type(self)):
            return NotImplemented

        result: list[Self] = list()

        if not self._overlaps(other):
            return [self]

        if self._start.rad < other._start.rad:
            start_inc = self._start_included and not other._start_included
            result.append(
                type(self)(
                    self._start, other._start, self._start_included, start_inc
                )
            )

        if other._end.rad < self._end.rad:
            end_inc = self._end_included and not other._end_included
            result.append(
                type(self)(other._end, self._end, end_inc, self._end_included)
            )

        return result

    def __str__(self) -> str:
        start_bracket = "[" if self._start_included else "("
        end_bracket = "]" if self._end_included else ")"
        return f"{start_bracket}{self._start.rad:.2f}; {self._end.rad:.2f}{end_bracket}"

    def __repr__(self) -> str:
        start_bracket = "[" if self._start_included else "("
        end_bracket = "]" if self._end_included else ")"
        return f"AngleRange({start_bracket}{self._start.rad:.2f}; {self._end.rad:.2f}{end_bracket})"

    def __abs__(self) -> Angle:
        return Angle(self._end.rad - self._start.rad)

    # endregion
