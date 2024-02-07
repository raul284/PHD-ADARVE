from dataclasses import dataclass

@dataclass
class Vector2D:
    x: float
    y: float

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __repr__(self) -> None:
        return f'Vector2D({self.x}, {self.y})'

    def __str__(self) -> None:
        return f'Vector2D({self.x}, {self.y})'