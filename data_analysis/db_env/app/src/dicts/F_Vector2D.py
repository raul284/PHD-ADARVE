from dataclasses import dataclass

@dataclass
class Vector2D:
    _x: float
    _y: float

    def __init__(self, x, y):
        self._x = x
        self._y = y

    def __repr__(self) -> None:
        return f'Vector2D({self._x}, {self._y})'

    def __str__(self) -> None:
        return f'Vector2D({self._x}, {self._y})'