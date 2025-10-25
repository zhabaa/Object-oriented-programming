import math
import pytest
from lab1 import AngleRange, Angle


class TestAngleRange:
    """Тесты для класса AngleRange"""

    def test_init_with_angles(self):
        """Тест инициализации с объектами Angle"""
        start = Angle(0)
        end = Angle(math.pi)
        range_obj = AngleRange(start, end)

        assert range_obj.start == start
        assert range_obj.end == end
        assert range_obj.start_included
        assert range_obj.end_included

    def test_init_with_numbers(self):
        """Тест инициализации с числами"""
        range_obj = AngleRange(0, math.pi)
        assert range_obj.start.radians == 0
        assert range_obj.end.radians == math.pi

    def test_init_swap_start_end(self):
        """Тест автоматической замены start и end при необходимости"""
        range_obj = AngleRange(math.pi, 0)
        assert range_obj.start.radians == 0
        assert range_obj.end.radians == math.pi

        # Проверка замены флагов включения
        range_obj = AngleRange(math.pi, 0, False, True)
        assert range_obj.start_included  # было end_included
        assert not range_obj.end_included  # было start_included

    def test_from_degrees(self):
        """Тест создания из градусов"""
        range_obj = AngleRange.from_degrees(0, 180)
        assert math.isclose(range_obj.start.degrees, 0)
        assert math.isclose(range_obj.end.degrees, 180)

    def test_from_degrees_invalid(self):
        """Тест создания из невалидных градусов"""
        with pytest.raises(TypeError):
            AngleRange.from_degrees("invalid", 180) #type: ignore

        with pytest.raises(ValueError):
            AngleRange.from_degrees(float("nan"), 180)

    def test_contains_angle(self):
        """Тест проверки принадлежности угла"""
        range_obj = AngleRange(0, math.pi)

        # Углы внутри диапазона
        assert Angle(1.0) in range_obj
        assert 1.0 in range_obj
        assert math.pi / 2 in range_obj

        # Граничные углы
        assert 0 in range_obj
        assert math.pi in range_obj

        # Углы вне диапазона
        assert -0.1 not in range_obj
        assert math.pi + 0.1 not in range_obj

    def test_contains_range(self):
        """Тест проверки принадлежности диапазона"""
        range1 = AngleRange(0, 2 * math.pi)
        range2 = AngleRange(math.pi / 2, math.pi)

        assert range2 in range1
        assert range1 not in range2

    def test_contains_excluded_bounds(self):
        """Тест граничных условий с исключенными границами"""
        range_obj = AngleRange(0, math.pi, False, False)

        assert 0 not in range_obj
        assert math.pi not in range_obj
        assert math.pi / 2 in range_obj

    def test_eq(self):
        """Тест сравнения на равенство"""
        range1 = AngleRange(0, math.pi, True, False)
        range2 = AngleRange(0, math.pi, True, False)
        range3 = AngleRange(0, math.pi, False, True)

        assert range1 == range2
        assert range1 != range3

    def test_abs(self):
        """Тест вычисления длины диапазона"""
        range_obj = AngleRange(0, math.pi)
        assert abs(range_obj) == Angle(math.pi)

        range_obj = AngleRange(math.pi / 2, 3 * math.pi / 2)
        assert abs(range_obj) == Angle(math.pi)

    def test_repr(self):
        """Тест строкового представления"""
        range_obj = AngleRange(0, math.pi)
        repr_str = repr(range_obj)
        assert "AngleRange" in repr_str
        assert "0.0000" in repr_str
        assert "3.1416" in repr_str

    def test_str(self):
        """Тест преобразования в строку"""
        range_obj = AngleRange.from_degrees(
            0, 180, start_included=True, end_included=False
        )
        str_repr = str(range_obj)
        assert "[0.00;" in str_repr
        assert "180.00)" in str_repr

    def test_format(self):
        """Правильный тест форматирования"""
        range_obj = AngleRange.from_degrees(0, 180, True, False)

        rad_format = format(range_obj, "rad")
        deg_format = format(range_obj, "deg")

        # Проверяем ожидаемый формат
        assert rad_format.startswith("[")  # start_included = True
        assert rad_format.endswith(")")  # end_included = False
        assert ";" in rad_format  # разделитель

        assert deg_format.startswith("[")  # start_included = True
        assert deg_format.endswith(")")  # end_included = False
        assert ";" in deg_format  # разделитель

    def test_add_overlapping(self):
        """Тест сложения перекрывающихся диапазонов"""
        range1 = AngleRange(0, math.pi)
        range2 = AngleRange(math.pi / 2, 3 * math.pi / 2)

        result = range1 + range2
        assert len(result) == 1
        assert result[0].start.radians == 0
        assert result[0].end.radians == 3 * math.pi / 2

    def test_add_adjacent(self):
        """Тест сложения смежных диапазонов"""
        range1 = AngleRange(0, math.pi / 2)
        range2 = AngleRange(math.pi / 2, math.pi)

        result = range1 + range2
        assert len(result) == 1
        assert result[0].start.radians == 0
        assert result[0].end.radians == math.pi

    def test_add_separate(self):
        """Тест сложения разделенных диапазонов"""
        range1 = AngleRange(0, math.pi / 4)
        range2 = AngleRange(math.pi / 2, math.pi)

        result = range1 + range2
        assert len(result) == 2
        assert result[0].start.radians == 0
        assert result[1].start.radians == math.pi / 2

    def test_sub_overlapping(self):
        """Тест вычитания перекрывающихся диапазонов"""
        range1 = AngleRange(0, math.pi)
        range2 = AngleRange(math.pi / 4, math.pi / 2)

        result = range1 - range2
        assert len(result) == 2
        assert result[0].end.radians == math.pi / 4
        assert result[1].start.radians == math.pi / 2

    def test_sub_contained(self):
        """Тест вычитания когда один диапазон содержится в другом"""
        range1 = AngleRange(0, 2 * math.pi)
        range2 = AngleRange(math.pi / 2, math.pi)

        result = range1 - range2
        assert len(result) == 2

    def test_sub_no_overlap(self):
        """Тест вычитания без перекрытия"""
        range1 = AngleRange(0, math.pi / 2)
        range2 = AngleRange(math.pi, 3 * math.pi / 2)

        result = range1 - range2
        assert len(result) == 1
        assert result[0] == range1

    def test_edge_cases(self):
        """Тест граничных случаев"""
        # Полный круг
        full_circle = AngleRange(0, 2 * math.pi)
        assert Angle(math.pi) in full_circle
        assert Angle(3 * math.pi) not in full_circle  # Не нормализованный
        assert Angle(3 * math.pi).radians in full_circle  # Нормализованный

        # Нулевая длина
        zero_range = AngleRange(math.pi, math.pi)
        assert math.pi in zero_range
        assert math.pi + 0.1 not in zero_range

    def test_properties(self):
        """Тест свойств доступа"""
        range_obj = AngleRange(0, math.pi, False, True)

        assert isinstance(range_obj.start, Angle)
        assert isinstance(range_obj.end, Angle)
        assert not range_obj.start_included
        assert range_obj.end_included


if __name__ == "__main__":
    # run_tests()
    # pytest.test_anglerange.py -v
    pytest.main([__file__, "-v", "--tb=no"])
