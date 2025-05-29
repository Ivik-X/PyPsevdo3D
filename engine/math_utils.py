"""Математические утилиты"""
import math

class Vector2:
    """Двумерный вектор"""
    def __init__(self, x=0, y=0):
        self.x = x
        self.y = y

    def __add__(self, other):
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar):
        return Vector2(self.x * scalar, self.y * scalar)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def normalize(self):
        length = self.length()
        if length > 0:
            return Vector2(self.x / length, self.y / length)
        return Vector2(0, 0)

    def to_tuple(self):
        return (self.x, self.y)

def clamp(value, min_val, max_val):
    """Ограничивает значение между минимумом и максимумом"""
    return max(min_val, min(max_val, value))

def lerp(a, b, t):
    """Линейная интерполяция между a и b"""
    return a + (b - a) * t
