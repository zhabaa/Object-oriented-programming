import math
import pytest
from lab1 import Angle


class TestAngle:
    """Тесты для класса Angle"""
    
    def test_init_valid_radians(self):
        """Тест инициализации с валидными радианами"""
        angle = Angle(1.5)
        assert angle._rad == 1.5
        
        angle = Angle(0)
        assert angle._rad == 0
        
        angle = Angle(-math.pi)
        assert angle._rad == -math.pi
    
    def test_init_invalid_type(self):
        """Тест инициализации с неверным типом"""
        with pytest.raises(TypeError, match="Radians must be a number"):
            Angle("invalid") #type: ignore
        
        with pytest.raises(TypeError, match="Radians must be a number"):
            Angle(None) #type: ignore
    
    def test_init_nan_inf(self):
        """Тест инициализации с NaN и Inf"""
        with pytest.raises(ValueError, match="Radians cannot be nan or inf"):
            Angle(float('nan'))
        
        with pytest.raises(ValueError, match="Radians cannot be nan or inf"):
            Angle(float('inf'))
    
    def test_from_degrees(self):
        """Тест создания из градусов"""
        angle = Angle.from_degrees(180)
        assert math.isclose(angle._rad, math.pi)
        
        angle = Angle.from_degrees(90)
        assert math.isclose(angle._rad, math.pi / 2)
        
        angle = Angle.from_degrees(0)
        assert angle._rad == 0
    
    def test_from_degrees_invalid(self):
        """Тест создания из невалидных градусов"""
        with pytest.raises(TypeError, match="Degrees must be a number"):
            Angle.from_degrees("invalid") #type: ignore
    
    def test_radians_property(self):
        """Тест свойства radians"""
        angle = Angle(2 * math.pi + 1)  # больше 2π
        assert math.isclose(angle.radians, 1.0)  # нормализовано
        
        angle = Angle(-1)
        assert math.isclose(angle.radians, 2 * math.pi - 1)
    
    def test_radians_setter(self):
        """Тест сеттера radians"""
        angle = Angle(0)
        angle.radians = math.pi
        assert math.isclose(angle._rad, math.pi)
        
        # Тест нормализации при получении
        angle.radians = 3 * math.pi
        assert math.isclose(angle.radians, math.pi)
    
    def test_radians_setter_invalid(self):
        """Тест сеттера radians с невалидными значениями"""
        angle = Angle(0)
        
        with pytest.raises(TypeError):
            angle.radians = "invalid" #type: ignore
        
        with pytest.raises(ValueError):
            angle.radians = float('nan')
    
    def test_degrees_property(self):
        """Тест свойства degrees"""
        angle = Angle(math.pi)
        assert math.isclose(angle.degrees, 180.0)
        
        angle = Angle(2 * math.pi)
        assert math.isclose(angle.degrees, 0.0)
        
        angle = Angle(-math.pi / 2)
        assert math.isclose(angle.degrees, 270.0)
    
    def test_degrees_setter(self):
        """Тест сеттера degrees"""
        angle = Angle(0)
        angle.degrees = 180
        assert math.isclose(angle._rad, math.pi)
        
        angle.degrees = 90
        assert math.isclose(angle._rad, math.pi / 2)
        
        angle.degrees = 450
        assert math.isclose(angle.degrees, 90.0)
    
    def test_degrees_setter_invalid(self):
        """Тест сеттера degrees с невалидными значениями"""
        angle = Angle(0)
        
        with pytest.raises(TypeError):
            angle.degrees = "invalid" #type: ignore
        
        with pytest.raises(ValueError):
            angle.degrees = float('inf')
    
    def test_repr(self):
        """Тест __repr__"""
        angle = Angle(1.5)
        assert repr(angle) == "Angle(radians=1.5)"
    
    def test_str(self):
        """Тест __str__"""
        angle = Angle(math.pi)
        assert str(angle) == "180.00°"
        
        angle = Angle(math.pi / 2)
        assert str(angle) == "90.00°"
    
    def test_float_conversion(self):
        """Тест преобразования в float"""
        angle = Angle(1.5)
        assert float(angle) == 1.5
    
    def test_int_conversion(self):
        """Тест преобразования в int"""
        angle = Angle(1.7)
        assert int(angle) == 1
        
        angle = Angle(2.3)
        assert int(angle) == 2
    
    def test_equality(self):
        """Тест сравнения на равенство"""
        angle1 = Angle(math.pi)
        angle2 = Angle(math.pi)
        angle3 = Angle(math.pi / 2)
        
        assert angle1 == angle2
        assert angle1 != angle3
        assert angle1 == math.pi
        assert angle1 != "string"
        
        # Тест с нормализацией
        angle4 = Angle(3 * math.pi)

        assert angle2.radians == angle4.radians  # π == 3π после нормализации (норм-ия только с геттером)
    
    def test_comparison(self):
        """Тест операторов сравнения"""
        angle1 = Angle(math.pi / 2)
        angle2 = Angle(math.pi)
        
        assert angle1 < angle2
        assert angle1 <= angle2
        assert angle2 > angle1
        assert angle2 >= angle1
        
        # С числами
        assert angle1 < math.pi
        assert angle1 <= math.pi
        assert angle2 > math.pi / 2
        assert angle2 >= math.pi / 2
    
    def test_addition(self):
        """Тест сложения"""
        angle1 = Angle(math.pi / 2)
        angle2 = Angle(math.pi / 2)
        
        result = angle1 + angle2
        assert math.isclose(result._rad, math.pi)
        
        # С числами
        result = angle1 + math.pi / 2
        assert math.isclose(result._rad, math.pi)
        
        # Правостороннее сложение
        result = math.pi / 2 + angle1
        assert math.isclose(result._rad, math.pi)
    
    def test_subtraction(self):
        """Тест вычитания"""
        angle1 = Angle(math.pi)
        angle2 = Angle(math.pi / 2)
        
        result = angle1 - angle2
        assert math.isclose(result._rad, math.pi / 2)
        
        # С числами
        result = angle1 - math.pi / 2
        assert math.isclose(result._rad, math.pi / 2)
        
        # Правостороннее вычитание
        result = 2 * math.pi - angle1
        assert math.isclose(result._rad, math.pi)
    
    def test_multiplication(self):
        """Тест умножения"""
        angle = Angle(math.pi / 2)
        
        result = angle * 2
        assert math.isclose(result._rad, math.pi)
        
        # Правостороннее умножение
        result = 2 * angle
        assert math.isclose(result._rad, math.pi)
    
    def test_division(self):
        """Тест деления"""
        angle = Angle(math.pi)
        
        result = angle / 2
        assert math.isclose(result._rad, math.pi / 2)
        
        # Деление на ноль
        with pytest.raises(ZeroDivisionError):
            angle / 0 # type: ignore
    
    def test_edge_cases(self):
        """Тест граничных случаев"""
        # Очень большие значения
        angle = Angle(1000 * math.pi)
        assert 0 <= angle.radians < 2 * math.pi
        assert 0 <= angle.degrees < 360
        
        # Очень маленькие (отрицательные) значения
        angle = Angle(-1000 * math.pi)
        assert 0 <= angle.radians < 2 * math.pi
        assert 0 <= angle.degrees < 360
        
        # Ноль
        angle = Angle(0)
        assert angle.radians == 0
        assert angle.degrees == 0


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
